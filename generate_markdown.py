#!/usr/bin/env python3
"""
모든 학생 세특 마크다운 파일 생성

성적 데이터에서 과목별로 세특을 추출하여 마크다운 파일 생성
"""

import json
import os
from pathlib import Path

def generate_markdown_for_student(student):
    """특정 학생의 마크다운 생성"""

    student_name = student['이름']
    print(f"✅ {student_name} 학생 마크다운 생성 중...\n")

    # markdown 디렉토리 생성
    Path('markdown').mkdir(exist_ok=True)

    # 1. 세특 마크다운 생성
    generate_seteuk_markdown(student, student_name)

    # 2. 진로활동 마크다운 생성
    generate_career_markdown(student, student_name)

    # 3. 자율활동 마크다운 생성
    generate_autonomy_markdown(student, student_name)

    # 4. 행동특성 마크다운 생성
    generate_behavior_markdown(student, student_name)

def generate_seteuk_markdown(student, student_name):
    """세특 마크다운 생성"""

    # 과목군별 분류 (로마자 포함 강화)
    subject_groups = {
        '국어': ['국어', '현대문학 감상', '고전문학 감상', '한국 문학과 세계 문학', '생각하는 삶', '언어와 매체'],
        '영어': ['영어', '영국 문학 I', '영국 문학 II', '영국 문학Ⅰ', '영국 문학Ⅱ', '영국 문학 I', '영국 문학 II',
                '세계 문학 I', '세계 문학 II', '세계 문학Ⅰ', '세계 문학Ⅱ',
                '미국 문학 I', '미국 문학 II', '미국 문학Ⅰ', '미국 문학Ⅱ', 'American Literature I', 'American Literature II'],
        '수학': ['수학', '수학I', '수학II', '수학Ⅰ', '수학Ⅱ', '수학 I', '수학 II',
                'AP 통계학', 'AP Statistics', '수학적 사고와 통계'],
        '과학': ['통합과학', '과학탐구실험', 'Biology I', 'Biology II', 'AP 생물학I', 'AP 생물학II',
                '생명과학Ⅰ', '생명과학Ⅱ', '생명과학 I', '생명과학 II', '화학I', '화학II', '화학 I', '화학 II',
                '물리학Ⅰ', '물리학Ⅱ', '물리학 I', '물리학 II', '지구과학Ⅰ', '지구과학Ⅱ'],
        '사회': ['통합사회', '정치와 법', '한국사', '사회·문화', '국제 관계와 국제기구',
                'AP 심리학', 'AP Psychology', '비교정치', '정치학개론',
                'AP 미시경제', 'AP 거시경제', 'AP Microeconomics', 'AP Macroeconomics',
                '철학 I', '철학 II', '철학Ⅰ', '철학Ⅱ', '경제', 'AP 미국사 I', 'AP 미국사 II', 'AP US History',
                '윤리학', '윤리학 I', '윤리학 II', '윤리학Ⅰ', '윤리학Ⅱ'],
        '정보': ['프로그래밍기초', '컴퓨터 시스템 일반', '정보'],
        '제2외국어': ['스페인어 I', '스페인어 II', '스페인어Ⅰ', '스페인어Ⅱ', '스페인어II',
                    '스페인어 독해와 작문 I', '스페인어 독해와 작문 II',
                    '프랑스어 I', '프랑스어 II', '프랑스어Ⅰ', '프랑스어Ⅱ',
                    '중국어 I', '중국어 II', '중국어Ⅰ', '중국어Ⅱ', '중국어II',
                    '중국어 독해와 작문 I', '중국어 독해와 작문 II', '중국어 독해와 작문Ⅰ', '중국어 독해와 작문Ⅱ',
                    '일본어 I', '일본어 II', '일본어Ⅰ', '일본어Ⅱ',
                    '한문', '한문Ⅰ', '한문Ⅱ', '한문 I', '한문 II'],
        '교양': ['진로와 직업', '융합독서', '융합 상상력', '융합프로젝트']
    }

    # 과목군별로 세특 수집
    subject_data = {group: [] for group in subject_groups.keys()}

    for grade in student.get('성적', []):
        과목 = grade.get('과목', '')
        세특 = grade.get('세특', '').strip()
        학년 = grade.get('학년', '')
        학기 = grade.get('학기', '')

        if not 세특:
            continue

        # 과목이 어느 그룹에 속하는지 찾기
        for group, subjects in subject_groups.items():
            if 과목 in subjects:
                subject_data[group].append({
                    '학년': 학년,
                    '학기': 학기,
                    '과목': 과목,
                    '세특': 세특
                })
                break

    # 과목군별로 마크다운 파일 생성
    for group, items in subject_data.items():
        if not items:
            continue

        # 학년, 학기 순으로 정렬
        items.sort(key=lambda x: (x['학년'], x['학기']))

        # 마크다운 생성
        md_content = f"# {group}\n\n"

        for item in items:
            md_content += f"## {item['학년']} {item['학기']} - {item['과목']}\n\n"
            md_content += f"{item['세특']}\n\n"

        # 파일 저장
        filename = f"markdown/{student_name}_세특_{group}.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)

        print(f"✅ {group}: {len(items)}개 세특 → {filename}")

    print()

def generate_career_markdown(student, student_name):
    """진로활동 마크다운 생성"""
    md_content = ""  # H1 제목 제거

    진로활동 = student.get('진로활동', {})

    # 진로와직업
    진로와직업 = 진로활동.get('진로와직업', [])
    if 진로와직업:
        md_content += "## 진로와 직업\n\n"
        for item in 진로와직업:
            학년 = item.get('학년', '')
            학기 = item.get('학기', '')
            내용 = item.get('내용', '')
            if 내용:
                md_content += f"### {학년} {학기}\n\n{내용}\n\n"

    # 창체진로
    창체진로 = 진로활동.get('창체진로', [])
    if 창체진로:
        md_content += "## 창의적 체험활동 - 진로활동\n\n"
        for item in 창체진로:
            학년 = item.get('학년', '')
            내용 = item.get('내용', '')
            if 내용:
                md_content += f"### {학년}\n\n{내용}\n\n"

    if len(md_content) > 10:  # 내용이 있으면
        filename = f"markdown/{student_name}_진로활동.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"✅ 진로활동 → {filename}")

def generate_autonomy_markdown(student, student_name):
    """자율활동 마크다운 생성"""
    md_content = ""  # H1 제목 제거

    자율활동 = student.get('자율활동', [])

    if 자율활동:
        md_content += "## 창의적 체험활동 - 자율활동\n\n"
        for item in 자율활동:
            학년 = item.get('학년', '')
            내용 = item.get('내용', '')
            if 내용:
                md_content += f"### {학년}\n\n{내용}\n\n"

    if len(md_content) > 10:  # 내용이 있으면
        filename = f"markdown/{student_name}_자율활동.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"✅ 자율활동 → {filename}")

def generate_behavior_markdown(student, student_name):
    """행동특성 마크다운 생성"""
    md_content = ""  # H1 제목 제거

    행동특성 = student.get('행동특성', [])

    if 행동특성:
        for item in 행동특성:
            학년 = item.get('학년', '')
            내용 = item.get('내용', '')
            if 내용:
                md_content += f"## {학년}\n\n{내용}\n\n"

    if len(md_content) > 10:  # 내용이 있으면
        filename = f"markdown/{student_name}_행동특성.md"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(md_content)
        print(f"✅ 행동특성 → {filename}")

def generate_markdown():
    """모든 학생의 마크다운 생성"""
    with open('data/students.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    students = data.get('students', [])

    if not students:
        print("❌ 학생 데이터가 없습니다.")
        return

    print(f"📚 총 {len(students)}명의 학생 마크다운 생성\n")
    print("=" * 50)

    for student in students:
        generate_markdown_for_student(student)
        print("=" * 50)

    print(f"\n🎉 완료! markdown/ 디렉토리에 파일 생성됨")

if __name__ == '__main__':
    generate_markdown()
