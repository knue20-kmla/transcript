#!/usr/bin/env python3
"""
PDF 파싱 테스트 (저장 없이 결과만 출력)
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

CONVERSION_PROMPT = """
생기부 PDF를 분석하여 다음 JSON 형식으로 정확하게 변환해주세요.

**🚨 매우 중요 - 반드시 지켜주세요:**
1. 각 과목의 성적 데이터에는 **반드시 "세특" 필드**를 포함해야 합니다
2. "세특" 필드에는 해당 과목의 **"세부능력 및 특기사항"을 전체** 복사
3. 세부능력 및 특기사항은 **단 한 글자도 빠뜨리지 말고** 전체를 완벽하게 복사해주세요
4. **특히 로마자 숫자(Ⅰ, Ⅱ, Ⅲ)가 포함된 과목명을 정확하게 추출하세요**
5. 과목명 예시: 수학, 수학I, 수학II, 수학Ⅰ, 수학Ⅱ - 원본 PDF의 표기를 그대로 따라주세요

**필수: 성적 데이터 형식**
성적 배열의 각 항목은 반드시 다음 필드를 모두 포함:
- 학년, 학기, 과목, 학점, 원점수, 평균, 등급, 성취도, **세특**

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
      "세특": "국어 세부능력 및 특기사항 전체 내용"
    }
  ]
}
```

**응답은 JSON만 출력하고 다른 설명은 생략하세요.**
"""

def extract_text_from_pdf(pdf_path):
    """Document Parse API로 PDF에서 텍스트 추출"""
    print(f"📄 PDF 텍스트 추출 중...")

    headers = {
        "Authorization": f"Bearer {UPSTAGE_API_KEY}"
    }

    with open(pdf_path, 'rb') as f:
        files = {"document": f}
        data = {"ocr": "force"}

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

    extracted_text = ""
    if "content" in result and "html" in result["content"]:
        import re
        html_content = result["content"]["html"]
        extracted_text = re.sub(r'<[^>]+>', '\n', html_content)
        extracted_text = re.sub(r'\n+', '\n', extracted_text)
        extracted_text = extracted_text.strip()

    print(f"✅ 텍스트 추출 완료 ({len(extracted_text)} 글자)")
    return extracted_text

def parse_pdf(pdf_path):
    """PDF 파싱"""
    extracted_text = extract_text_from_pdf(pdf_path)

    print("🤖 Solara API 호출 중...")

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
        "max_tokens": 30000,
        "temperature": 0.1
    }

    response = requests.post(SOLARA_API_URL, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"❌ Solar API 오류: {response.status_code}")
        sys.exit(1)

    result = response.json()
    content = result['choices'][0]['message']['content']

    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]

    return json.loads(content.strip())

if __name__ == "__main__":
    pdf_path = "pdfs/유나.pdf"

    print("=" * 50)
    print("🧪 PDF 파싱 테스트")
    print("=" * 50)

    student_data = parse_pdf(pdf_path)

    print(f"\n✅ 파싱 완료: {student_data['이름']} 학생")
    print("\n📚 추출된 수학 과목:")

    for grade in student_data.get('성적', []):
        if '수학' in grade.get('과목', ''):
            print(f"  - {grade['학년']} {grade['학기']}: {grade['과목']}")

    # 전체 결과를 파일로 저장
    with open('/tmp/parsed_result.json', 'w', encoding='utf-8') as f:
        json.dump(student_data, f, ensure_ascii=False, indent=2)

    print(f"\n💾 전체 결과: /tmp/parsed_result.json")
