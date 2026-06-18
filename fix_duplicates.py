#!/usr/bin/env python3
"""
김윤지 학생 데이터 중복 제거 및 세특 병합

중복된 과목을 제거하고, 세특이 있는 버전을 유지합니다.
"""

import json

def fix_duplicates():
    with open('data/students.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for student in data['students']:
        if student['이름'] != '김윤지':
            continue

        print(f"✅ {student['이름']} 학생 데이터 정리 중...")

        grades = student.get('성적', [])

        # 중복 제거 로직
        seen = {}
        unique_grades = []

        for grade in grades:
            학년 = grade.get('학년')
            학기 = grade.get('학기')
            과목 = grade.get('과목')
            세특 = grade.get('세특', '')

            # 키 생성 (학년-학기-과목)
            key = f"{학년}_{학기}_{과목}"

            # 이미 있는 과목인지 확인
            if key in seen:
                # 세특이 있는 버전을 우선
                if 세특 and not seen[key].get('세특'):
                    # 기존 항목을 새 항목으로 교체
                    idx = seen[key]['_idx']
                    unique_grades[idx] = grade
                    seen[key] = grade
                    seen[key]['_idx'] = idx
                    print(f"  🔄 {과목} ({학년} {학기}): 세특 있는 버전으로 교체")
                else:
                    print(f"  ⏭️  {과목} ({학년} {학기}): 중복 항목 건너뛰기")
            else:
                # 새 항목 추가
                grade['_idx'] = len(unique_grades)
                seen[key] = grade
                unique_grades.append(grade)
                status = "✅ 세특 있음" if 세특 else "⚠️  세특 없음"
                print(f"  ➕ {과목} ({학년} {학기}): {status}")

        # _idx 필드 제거
        for grade in unique_grades:
            if '_idx' in grade:
                del grade['_idx']

        print(f"\n📊 결과: {len(grades)}개 → {len(unique_grades)}개")
        student['성적'] = unique_grades

    # 저장
    with open('data/students.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n✅ 완료! students.json 업데이트됨")

if __name__ == '__main__':
    fix_duplicates()
