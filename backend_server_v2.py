#!/usr/bin/env python3
"""
관리자 대시보드 백엔드 서버 (간소화 버전)
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import json
import subprocess

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

UPLOAD_FOLDER = 'pdfs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/test', methods=['GET'])
def test():
    """테스트 엔드포인트"""
    return jsonify({'status': 'ok', 'message': '백엔드 서버 정상 작동 중'})

@app.route('/students', methods=['GET'])
def get_students():
    """학생 목록 조회"""
    try:
        with open('data/students.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

        # upload_student.py 실행
        print("🔄 upload_student.py 실행 중...")
        result = subprocess.run(
            ['python3', 'upload_student.py', pdf_path],
            capture_output=True,
            text=True,
            check=True
        )

        print("✅ 파싱 완료")
        print(result.stdout)

        # 학생 이름 추출 (간단하게 파일명에서)
        student_name = file.filename.replace('.pdf', '')

        # 마크다운 생성
        print("🔄 마크다운 파일 생성 중...")
        subprocess.run(['python3', 'generate_markdown.py'], check=True)
        print("✅ 마크다운 파일 생성 완료")

        # Git 커밋
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

    except subprocess.CalledProcessError as e:
        print(f"❌ 프로세스 오류: {e.stderr}")
        return jsonify({'error': f'처리 중 오류: {e.stderr}'}), 500
    except Exception as e:
        print(f"❌ 오류 발생: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("🚀 관리자 대시보드 백엔드 서버 시작")
    print("=" * 50)
    print("📍 URL: http://localhost:5001")
    print("🧪 테스트: GET /test")
    print("📤 업로드: POST /upload")
    print("👥 학생 목록: GET /students")
    print("=" * 50)

    app.run(debug=True, host='0.0.0.0', port=5001)
