# 📚 KMLA 생기부 조회 시스템 프로토타입

민족사관고등학교 학교생활기록부 조회 웹 애플리케이션

## 📁 파일 구조

```
생기부-시스템/
├── index.html                     # 메인 웹앱
├── data/                          # 구글 시트용 CSV 파일
│   ├── 학생_기본정보.csv
│   ├── 성적_등급과목.csv
│   └── 성적_성취도과목.csv
└── markdown/                      # 세특/진로/자율/행동 마크다운
    ├── 권정민_세특_국어.md
    ├── 권정민_세특_영어.md
    ├── 권정민_세특_수학.md
    ├── 권정민_세특_과학.md
    ├── 권정민_세특_사회.md
    ├── 권정민_세특_정보.md
    ├── 권정민_세특_교양.md
    ├── 권정민_진로활동.md
    ├── 권정민_자율활동.md
    └── 권정민_행동특성.md
```

## 🚀 설정 방법

### 1단계: 구글 시트 만들기

1. **새 구글 시트 생성**: https://sheets.new

2. **3개의 시트 탭 만들기:**
   - `학생_기본정보`
   - `성적_등급과목`
   - `성적_성취도과목`

3. **CSV 데이터 복사:**
   - `data/` 폴더의 각 CSV 파일을 열어서
   - 해당하는 구글 시트 탭에 붙여넣기

4. **웹에 게시:**
   - 파일 > 공유 > 웹에 게시
   - "전체 문서" 선택
   - "게시" 클릭

5. **시트 ID 복사:**
   - 브라우저 주소창에서 `/d/` 와 `/edit` 사이의 문자열
   - 예: `https://docs.google.com/spreadsheets/d/[이부분이_SHEET_ID]/edit`

### 2단계: GitHub 저장소 만들기

1. **GitHub에 새 저장소 생성**
   - Repository name: `kmla-saenggibu-data`
   - Public으로 설정

2. **파일 업로드:**
   ```bash
   cd ~/Desktop/생기부-시스템
   git init
   git add markdown/ index.html
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/kmla-saenggibu-data.git
   git push -u origin main
   ```

3. **GitHub Pages 활성화:**
   - Settings > Pages
   - Source: Deploy from a branch
   - Branch: main / (root)
   - Save

### 3단계: index.html 설정 수정

`index.html` 파일을 열어서 다음 부분을 수정:

```javascript
// 14-15번째 줄 근처
const SHEET_ID = 'YOUR_SHEET_ID_HERE';  // 1단계에서 복사한 구글 시트 ID
const GITHUB_BASE = 'https://raw.githubusercontent.com/YOUR_USERNAME/kmla-saenggibu-data/main/markdown/';
```

### 4단계: 테스트

1. **로컬 테스트:**
   - `index.html` 파일을 더블클릭하여 브라우저에서 열기
   - 또는 Live Server 사용

2. **온라인 테스트:**
   - `https://YOUR_USERNAME.github.io/kmla-saenggibu-data/`

## ✨ 주요 기능

### 📊 대시보드
- 전체 평균 등급 표시
- 성취도 과목 수 표시
- 주요 세특 평가 표현 하이라이트

### 📈 성적 분석
- 학년/학기별 필터링
- 등급과목 / 성취도과목 통합 조회
- 원점수, 평균, 등급/성취도 표시

### 📚 세특 (마크다운)
- 과목별 탭 (국어, 영어, 수학, 과학, 사회, 정보, 교양)
- 학년/학기별 아코디언 형식
- 중요 키워드 하이라이트
- 부드러운 펼치기/접기 애니메이션

### 🎯 진로활동 / 자율활동 / 행동특성
- 마크다운 렌더링
- 연도별 구조화된 표시

## 🔄 나머지 12명 학생 추가 방법

### CSV 파일 업데이트:
```csv
# 학생_기본정보.csv에 추가
김민수,3,2,2,이공계열,https://example.com/profile2.jpg
이지혜,3,2,3,인문사회계열,https://example.com/profile3.jpg
...

# 성적_등급과목.csv에 추가
김민수,1학년,1학기,국어,3,88,85.0,4
...

# 성적_성취도과목.csv에 추가
김민수,1학년,1학기,프로그래밍기초,2,90,82.0,A
...
```

### 마크다운 파일 추가:
```bash
markdown/
├── 김민수_세특_국어.md
├── 김민수_세특_영어.md
...
├── 이지혜_세특_국어.md
...
```

## 🎨 디자인 특징

- ✅ 민사고 블루 계열 (#1e3a8a → #3b82f6)
- ✅ 그라데이션 & 글래스모피즘 효과
- ✅ 반응형 디자인 (모바일/태블릿/데스크톱)
- ✅ 부드러운 아코디언 애니메이션
- ✅ 마크다운 내 **강조** 표현 자동 빨간색 하이라이트

## 📝 마크다운 작성 팁

### 강조할 내용은 **볼드** 처리:
```markdown
학생이 **예리한 질문을 던지는 모습**이 인상적이었음.
```
→ 웹앱에서 빨간색으로 표시됨

### 메타데이터 추가 (highlights):
```markdown
<!-- highlights: "예리한 질문", "깊은 사고", "탁월한 분석력" -->
```
→ 대시보드 "주요 세특 평가 표현"에 활용 가능

## 🔧 문제 해결

### "데이터를 불러올 수 없습니다" 오류
- 구글 시트 "웹에 게시" 확인
- SHEET_ID가 정확한지 확인
- 시트 탭 이름이 정확한지 확인

### 마크다운이 안 보임
- GITHUB_BASE URL이 정확한지 확인
- 파일명이 `{학생명}_세특_{과목}.md` 형식인지 확인
- GitHub 저장소가 Public인지 확인

### CORS 오류
- 로컬에서 `file://` 프로토콜로 열면 발생 가능
- Live Server 사용하거나 GitHub Pages에 배포

## 📞 다음 단계

1. ✅ 프로토타입 테스트
2. ⬜ 나머지 12명 데이터 추가
3. ⬜ PDF → Markdown 변환 (Claude vs Solar 비교)
4. ⬜ 추가 기능 개발 (검색, 필터, 인쇄 등)

---

**제작:** KMLA 생기부 조회 시스템
**버전:** 1.0 (프로토타입)
