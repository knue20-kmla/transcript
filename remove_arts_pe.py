#!/usr/bin/env python3
"""
음악, 미술, 체육 과목 제거

성적 데이터에서 음악, 미술, 체육 과목을 모두 제거합니다.
"""

import json

def remove_arts_pe():
    with open('data/students.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    exclude_subjects = ['음악', '미술', '체육']

    for student in data['students']:
        print(f"\n✅ {student['이름']} 학생 처리 중...")

        grades = student.get('성적', [])
        original_count = len(grades)

        # 음악, 미술, 체육 제외
        filtered_grades = []
        removed_count = 0

        for grade in grades:
            과목 = grade.get('과목', '')

            if 과목 in exclude_subjects:
                print(f"  ❌ 제거: {과목} ({grade.get('학년')} {grade.get('학기')})")
                removed_count += 1
            else:
                filtered_grades.append(grade)

        student['성적'] = filtered_grades

        print(f"  📊 {original_count}개 → {len(filtered_grades)}개 (제거: {removed_count}개)")

    # 저장
    with open('data/students.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("\n✅ 완료! 음악, 미술, 체육 과목이 제거되었습니다.")

if __name__ == '__main__':
    remove_arts_pe()
