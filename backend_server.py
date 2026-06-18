#!/usr/bin/env python3
"""
관리자 대시보드 백엔드 서버

PDF 업로드 → Solar Pro API 파싱 → JSON/마크다운 생성 → Git 커밋
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import subprocess
import json

# 환경변수 체크 우회
if 'UPSTAGE_API_KEY' not in os.environ:
    os.environ['UPSTAGE_API_KEY'] = 'dummy'  # 임시

# 기존 upload_student.py 로직 재사용
sys.path.insert(0, os.path.dirname(__file__))
from upload_student import parse_pdf_with_solara, update_students_json

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # 모든 origin 허용

UPLOAD_FOLDER = 'pdfs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    """PDF 업로드 및 처리"""

    if 'pdf' not in request.files:
        return jsonify({'error': '파일이 없습니다'}), 400

    file = request.files['pdf']

    if file.filename == '':
        return jsonify({'error': '파일명이 없습니다'}), 400

    if not file.filename.endswith('.pdf'):
        return jsonify({'error': 'PDF 파일만 업로드 가능합니다'}), 400

    try:
        # PDF 저장
        pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(pdf_path)

        print(f"✅ PDF 저장: {pdf_path}")

        # Solar Pro API로 파싱
        print("🔄 Solar Pro API 파싱 중...")
        student_data = parse_pdf_with_solara(pdf_path)

        student_name = student_data.get('이름', '알 수 없음')
        print(f"✅ 파싱 완료: {student_name}")

        # JSON 업데이트
        update_students_json(student_data)
        print("✅ students.json 업데이트 완료")

        # 마크다운 파일 생성 (generate_markdown.py 실행)
        print("🔄 마크다운 파일 생성 중...")
        subprocess.run(['python3', 'generate_markdown.py'], check=True)
        print("✅ 마크다운 파일 생성 완료")

        # Git 커밋 (자동)
        print("🔄 Git 커밋 중...")
        subprocess.run(['git', 'add', 'data/students.json', 'markdown/'], check=True)
        subprocess.run(['git', 'commit', '-m', f'📤 {student_name} 학생 추가 (관리자 업로드)'], check=True)
        subprocess.run(['git', 'push'], check=True)

        print("✅ Git 푸시 완료")

        return jsonify({
            'success': True,
            'student_name': student_name,
            'message': f'{student_name} 학생이 성공적으로 추가되었습니다.'
        })

    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/students', methods=['GET'])
def get_students():
    """학생 목록 조회"""
    try:
        import json
        with open('data/students.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 50)
    print("🚀 관리자 대시보드 백엔드 서버 시작")
    print("=" * 50)
    print("📍 URL: http://localhost:5001")
    print("📤 업로드 엔드포인트: POST /upload")
    print("👥 학생 목록: GET /students")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5001)
