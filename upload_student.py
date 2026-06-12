#!/usr/bin/env python3
"""
생기부 PDF를 students.json에 자동 추가하는 스크립트 (Solara 3 Pro API 버전)

사용법:
    python upload_student.py <생기부.pdf>

예시:
    python upload_student.py 홍길동_생기부.pdf
"""

import requests
import json
import sys
import os
import base64
from pathlib import Path

# Solara API 설정
SOLARA_API_URL = "https://api.upstage.ai/v1/solar/chat/completions"
SOLARA_API_KEY = os.environ.get("UPSTAGE_API_KEY")

if not SOLARA_API_KEY:
    print("❌ 오류: UPSTAGE_API_KEY 환경변수가 설정되지 않았습니다.")
    print("\n설정 방법:")
    print("  export UPSTAGE_API_KEY='your-api-key-here'")
    sys.exit(1)

# JSON 변환 프롬프트
CONVERSION_PROMPT = """
생기부 PDF를 분석하여 다음 JSON 형식으로 정확하게 변환해주세요.

**중요:**
- 모든 필드를 빠짐없이 채워주세요
- 성적은 학년/학기별로 정확히 분류
- 세특은 과목별로 상세히 추출
- 진로활동, 동아리, 자율활동, 행동특성도 포함

**JSON 형식:**
```json
{
  "이름": "학생이름",
  "학년": "3",
  "반": "2",
  "번호": "1",
  "계열": "인문사회계열",
  "프로필이미지URL": "",
  "성적": [
    {
      "학년": "1학년",
      "학기": "1학기",
      "과목": "국어",
      "학점": 3,
      "원점수": 90,
      "평균": 85.1,
      "등급": 4,
      "성취도": null
    }
  ],
  "highlights": [
    {
      "text": "주요 평가 표현",
      "subject": "과목명"
    }
  ],
  "세특종합분석": {
    "국어": {
      "핵심역량": ["텍스트 분석력", "비판적 사고"],
      "주요평가": [
        "평가 내용 1",
        "평가 내용 2"
      ],
      "발전가능성": "발전 가능성 설명"
    }
  },
  "진로활동": {
    "진로와직업": [
      {
        "학년": "1학년",
        "학기": "1학기",
        "내용": "진로와 직업 세특 내용"
      }
    ],
    "창체진로": [
      {
        "학년": "1학년",
        "학기": "전체",
        "내용": "창체 진로활동 내용"
      }
    ]
  },
  "동아리활동": [
    {
      "학년": "1학년",
      "학기": "전체",
      "동아리명": "동아리 이름",
      "시간": "50시간",
      "내용": "동아리 활동 내용"
    }
  ],
  "자율활동": [
    {
      "학년": "1학년",
      "내용": "자율활동 특기사항"
    }
  ],
  "행동특성": [
    {
      "학년": "1학년",
      "내용": "행동특성 및 종합의견"
    }
  ]
}
```

**주의사항:**
1. 성적에서 등급과목은 "등급" 필드에 숫자, 성취도과목은 "성취도" 필드에 A/B/C
2. 세특종합분석은 과목군별로 핵심역량, 주요평가, 발전가능성 포함
3. highlights는 교사의 강한 긍정 평가 표현 5-10개 추출
4. 모든 텍스트는 원문 그대로 유지

**응답은 JSON만 출력하고 다른 설명은 생략하세요.**
"""

def read_pdf_as_base64(pdf_path):
    """PDF 파일을 base64로 인코딩"""
    with open(pdf_path, 'rb') as f:
        return base64.standard_b64encode(f.read()).decode('utf-8')

def parse_pdf_with_solara(pdf_path):
    """Solara 3 Pro API로 PDF 파싱"""
    print(f"📄 PDF 읽는 중: {pdf_path}")

    pdf_data = read_pdf_as_base64(pdf_path)

    print("🤖 Solara 3 Pro API 호출 중... (30초-1분 소요)")

    headers = {
        "Authorization": f"Bearer {SOLARA_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "solar-pro",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "document": {
                            "url": f"data:application/pdf;base64,{pdf_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": CONVERSION_PROMPT
                    }
                ]
            }
        ],
        "max_tokens": 16000,
        "temperature": 0.1
    }

    response = requests.post(SOLARA_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"❌ API 오류: {response.status_code}")
        print(response.text)
        sys.exit(1)

    result = response.json()
    content = result['choices'][0]['message']['content']

    # ```json ... ``` 형태로 온 경우 추출
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]

    return json.loads(content.strip())

def update_students_json(new_student):
    """students.json에 학생 추가"""
    json_path = Path(__file__).parent / "data" / "students.json"

    # 기존 JSON 읽기
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 중복 체크
    existing_names = [s['이름'] for s in data['students']]
    if new_student['이름'] in existing_names:
        print(f"⚠️  경고: '{new_student['이름']}' 학생이 이미 존재합니다.")
        response = input("덮어쓰시겠습니까? (y/n): ")
        if response.lower() != 'y':
            print("❌ 취소되었습니다.")
            sys.exit(0)

        # 기존 학생 제거
        data['students'] = [s for s in data['students'] if s['이름'] != new_student['이름']]

    # 새 학생 추가
    data['students'].append(new_student)

    # JSON 저장 (예쁘게 포맷)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"✅ students.json 업데이트 완료!")
    return json_path

def main():
    if len(sys.argv) < 2:
        print("❌ 사용법: python upload_student.py <생기부.pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    if not os.path.exists(pdf_path):
        print(f"❌ 파일을 찾을 수 없습니다: {pdf_path}")
        sys.exit(1)

    print("=" * 50)
    print("🎓 생기부 자동 업로드 시스템")
    print("=" * 50)

    try:
        # 1. PDF 파싱
        student_data = parse_pdf_with_solara(pdf_path)
        print(f"✅ 파싱 완료: {student_data['이름']} 학생")

        # 2. JSON 업데이트
        json_path = update_students_json(student_data)

        # 3. Git 커밋 (선택사항)
        print("\n📝 Git 커밋을 진행하시겠습니까?")
        print("  - y: 자동 커밋 & 푸시")
        print("  - n: 수동으로 나중에 커밋")

        response = input("선택 (y/n): ")

        if response.lower() == 'y':
            student_name = student_data['이름']
            os.system(f'cd {json_path.parent.parent} && git add data/students.json')
            os.system(f'cd {json_path.parent.parent} && git commit -m "✨ {student_name} 학생 생기부 추가"')
            os.system(f'cd {json_path.parent.parent} && git push')
            print("✅ Git 푸시 완료!")
        else:
            print("ℹ️  나중에 수동으로 커밋하세요:")
            print("    git add data/students.json")
            print(f"    git commit -m '✨ {student_data['이름']} 학생 생기부 추가'")
            print("    git push")

        print("\n" + "=" * 50)
        print("🎉 완료!")
        print("=" * 50)

    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
