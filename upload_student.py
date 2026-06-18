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
from pathlib import Path

# Upstage API 설정
DOCUMENT_PARSE_URL = "https://api.upstage.ai/v1/document-ai/document-parse"
SOLARA_API_URL = "https://api.upstage.ai/v1/solar/chat/completions"
UPSTAGE_API_KEY = os.environ.get("UPSTAGE_API_KEY")

if not UPSTAGE_API_KEY:
    print("❌ 오류: UPSTAGE_API_KEY 환경변수가 설정되지 않았습니다.")
    print("\n설정 방법:")
    print("  export UPSTAGE_API_KEY='your-api-key-here'")
    sys.exit(1)

# JSON 변환 프롬프트
CONVERSION_PROMPT = """
생기부 PDF를 분석하여 다음 JSON 형식으로 정확하게 변환해주세요.

**🚨 매우 중요 - 반드시 지켜주세요:**
1. 각 과목의 성적 데이터에는 **반드시 "세특" 필드**를 포함해야 합니다
2. "세특" 필드에는 해당 과목의 **"세부능력 및 특기사항"을 전체** 복사
3. 세부능력 및 특기사항은 **단 한 글자도 빠뜨리지 말고** 전체를 완벽하게 복사해주세요
4. 행동특성 및 종합의견도 **전체 내용을 모두** 포함해주세요
5. 절대로 요약하거나 생략하지 마세요 - 원문 그대로 전부 추출
6. "..." 같은 생략 표시를 사용하지 마세요

**필수: 성적 데이터 형식**
성적 배열의 각 항목은 반드시 다음 필드를 모두 포함:
- 학년, 학기, 과목, 학점, 원점수, 평균, 등급, 성취도, **세특**

예시:
{
  "학년": "1학년",
  "학기": "1학기",
  "과목": "국어",
  "학점": 3,
  "원점수": 88,
  "평균": 85.1,
  "등급": 4,
  "성취도": null,
  "세특": "(1학기)국어: 김수영 시인의 풀에 대해서 발표하였음. 보편 해석이 설명해주지 못하는 바람보다 더 빨리 눕는 것의 의미... [전체 내용]"
}

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
      "성취도": null,
      "세특": "국어 세부능력 및 특기사항 전체 내용을 여기에 완전히 복사"
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
    },
    "영어": {
      "핵심역량": ["독해력", "의사소통"],
      "주요평가": [
        "평가 내용 1",
        "평가 내용 2"
      ],
      "발전가능성": "발전 가능성 설명"
    },
    "수학": {
      "핵심역량": ["수학적 사고", "문제해결"],
      "주요평가": [
        "평가 내용 1",
        "평가 내용 2"
      ],
      "발전가능성": "발전 가능성 설명"
    },
    "과학": {
      "핵심역량": ["과학적 탐구", "실험 설계"],
      "주요평가": [
        "평가 내용 1",
        "평가 내용 2"
      ],
      "발전가능성": "발전 가능성 설명"
    },
    "사회": {
      "핵심역량": ["비판적 사고", "자료 분석"],
      "주요평가": [
        "평가 내용 1",
        "평가 내용 2"
      ],
      "발전가능성": "발전 가능성 설명"
    },
    "정보": {
      "핵심역량": ["프로그래밍", "논리적 사고"],
      "주요평가": [
        "평가 내용 1",
        "평가 내용 2"
      ],
      "발전가능성": "발전 가능성 설명"
    },
    "제2외국어": {
      "핵심역량": ["언어 학습", "문화 이해"],
      "주요평가": [
        "평가 내용 1",
        "평가 내용 2"
      ],
      "발전가능성": "발전 가능성 설명"
    },
    "교양": {
      "핵심역량": ["융합적 사고", "진로 탐색"],
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
    import base64
    with open(pdf_path, 'rb') as f:
        return base64.standard_b64encode(f.read()).decode('utf-8')

def extract_text_from_pdf(pdf_path):
    """Document Parse API로 PDF에서 텍스트 추출"""
    print(f"📄 PDF 텍스트 추출 중...")

    headers = {
        "Authorization": f"Bearer {UPSTAGE_API_KEY}"
    }

    with open(pdf_path, 'rb') as f:
        files = {"document": f}
        data = {"ocr": "force"}  # OCR 강제 적용

        response = requests.post(
            DOCUMENT_PARSE_URL,
            headers=headers,
            files=files,
            data=data
        )

    if response.status_code != 200:
        print(f"❌ Document Parse API 오류: {response.status_code}")
        print(response.text)
        sys.exit(1)

    result = response.json()

    # HTML에서 텍스트 추출
    extracted_text = ""

    if "content" in result and "html" in result["content"]:
        # HTML 태그 제거하고 텍스트만 추출
        import re
        html_content = result["content"]["html"]
        # HTML 태그 제거
        extracted_text = re.sub(r'<[^>]+>', '\n', html_content)
        # 연속된 줄바꿈을 하나로
        extracted_text = re.sub(r'\n+', '\n', extracted_text)
        # 앞뒤 공백 제거
        extracted_text = extracted_text.strip()

    if not extracted_text or len(extracted_text) < 100:
        print("❌ 텍스트를 충분히 추출할 수 없습니다.")
        print(f"추출된 텍스트 길이: {len(extracted_text)}")
        print("HTML 내용 샘플:")
        if "content" in result and "html" in result["content"]:
            print(result["content"]["html"][:500])
        sys.exit(1)

    print(f"✅ 텍스트 추출 완료 ({len(extracted_text)} 글자)")
    return extracted_text

def parse_pdf_with_solara(pdf_path):
    """Solara 3 Pro API로 PDF 파싱 (2단계)"""
    print(f"📄 PDF 읽는 중: {pdf_path}")

    # 1단계: PDF → 텍스트
    extracted_text = extract_text_from_pdf(pdf_path)

    # 2단계: 텍스트 → JSON
    print("🤖 Solara 3 Pro API 호출 중... (30초-1분 소요)")

    headers = {
        "Authorization": f"Bearer {UPSTAGE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "solar-pro",
        "messages": [
            {
                "role": "user",
                "content": f"{CONVERSION_PROMPT}\n\n===== 생기부 텍스트 =====\n{extracted_text}"
            }
        ],
        "max_tokens": 30000,  # 적절한 크기로 조정
        "temperature": 0.1
    }

    response = requests.post(SOLARA_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"❌ Solar API 오류: {response.status_code}")
        print(response.text)
        sys.exit(1)

    result = response.json()
    content = result['choices'][0]['message']['content']

    # ```json ... ``` 형태로 온 경우 추출
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]

    try:
        return json.loads(content.strip())
    except json.JSONDecodeError as e:
        print(f"❌ JSON 파싱 오류: {e}")
        print(f"📄 응답 내용 (처음 500자):\n{content[:500]}...")
        print(f"📄 응답 내용 (마지막 500자):\n...{content[-500:]}")

        # JSON 수정 시도
        try:
            import re
            # trailing commas 제거
            fixed_content = re.sub(r',(\s*[}\]])', r'\1', content)
            print("🔧 JSON 수정 시도 중...")
            return json.loads(fixed_content)
        except Exception as fix_error:
            print(f"❌ JSON 수정 실패: {fix_error}")
            raise Exception(f"Solar API 응답을 JSON으로 파싱할 수 없습니다. 원본 오류: {str(e)}")

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
