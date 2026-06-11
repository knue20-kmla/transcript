# 📚 KMLA 생기부 조회 시스템

민족사관고등학교 학교생활기록부 조회 웹 애플리케이션 (JSON 기반)

## 🌟 주요 특징

- ✅ **JSON 기반 데이터 관리** - 구글 시트 불필요
- ✅ **마크다운 세특** - GitHub에서 직접 관리
- ✅ **민사고 블루 디자인** - 세련된 UI/UX
- ✅ **반응형** - 모바일/태블릿/데스크톱 지원
- ✅ **확장 가능** - 13명 → 100명도 문제없음

## 📁 파일 구조

```
transcript/
├── index.html                     # 메인 웹앱
├── data/
│   └── students.json              # 학생 데이터 (기본정보 + 성적 + 하이라이트)
└── markdown/                      # 세특/진로/자율/행동 마크다운
    ├── 권정민_세특_국어.md
    ├── 권정민_세특_영어.md
    └── ...
```

## 🚀 사용 방법

### 웹사이트 접속
```
https://knue20-kmla.github.io/transcript/
```

그냥 접속하면 됩니다! 별도 설정 불필요.

## 📝 학생 추가하는 법

### 1단계: students.json에 학생 추가

`data/students.json` 파일을 열어서 `students` 배열에 추가:

```json
{
  "students": [
    {
      "이름": "권정민",
      "학년": "3",
      ...
    },
    {
      "이름": "김민수",  // 새 학생 추가
      "학년": "3",
      "반": "2",
      "번호": "2",
      "계열": "이공계열",
      "프로필이미지URL": "https://...",
      "성적": [
        {"학년": "1학년", "학기": "1학기", "과목": "국어", ...},
        ...
      ],
      "highlights": [
        {"text": "뛰어난 논리적 사고", "subject": "수학"},
        ...
      ]
    }
  ]
}
```

### 2단계: 마크다운 파일 추가

`markdown/` 폴더에 파일 생성:
```
김민수_세특_국어.md
김민수_세특_영어.md
김민수_진로활동.md
...
```

### 3단계: Git 푸시

```bash
cd ~/Desktop/생기부-시스템
git add .
git commit -m "김민수 학생 데이터 추가"
git push
```

**끝!** 1-2분 후 웹사이트에 자동 반영됩니다.

## 🤖 자동화 계획

### PDF → JSON 자동 변환

**Claude Sonnet vs Solar 3 Pro 비교 예정:**

1. 생기부 PDF 1개로 두 AI 테스트
2. 품질/속도/비용 비교
3. 최종 방식 결정
4. 13명 일괄 변환

**변환 프로세스:**
```
생기부 PDF → AI 파싱 → students.json + 마크다운 자동 생성
```

## 📊 데이터 구조

### students.json 필드

```typescript
{
  이름: string,
  학년: string,
  반: string,
  번호: string,
  계열: string,
  프로필이미지URL: string,
  성적: [
    {
      학년: string,
      학기: string,
      과목: string,
      학점: number,
      원점수: number,
      평균: number,
      등급: number | null,
      성취도: string | null
    }
  ],
  highlights: [
    {
      text: string,  // "한차원 더 깊은 사고"
      subject: string  // "국어"
    }
  ]
}
```

## 🎨 UI 기능

### 대시보드
- 전체 평균 등급
- 성취도 과목 수
- ⭐ 주요 세특 평가 표현 (highlights에서 자동 표시)

### 성적 분석
- 학년/학기별 필터
- 등급과목 + 성취도과목 통합 조회

### 세특 (마크다운)
- 과목별 탭 (국어, 영어, 수학, 과학, 사회, 정보, 교양)
- 학년/학기별 아코디언
- 마크다운 렌더링 (굵은 글씨 빨간색 강조)

### 진로/자율/행동
- 마크다운 파일 자동 로드

## 🔧 개발 정보

**기술 스택:**
- React 18 (CDN)
- Marked.js (마크다운)
- Tailwind CSS
- GitHub Pages

**브라우저 지원:**
- Chrome, Safari, Firefox, Edge (최신 버전)

## 📈 확장성

- **현재:** 1명 (권정민)
- **목표:** 13명
- **최대:** 제한 없음 (JSON 파일 크기 100MB 이하면 OK)

**예상 용량:**
- 13명 × 30KB = ~400KB (매우 작음)
- GitHub Pages 용량 제한: 1GB

## 🐛 문제 해결

### "데이터를 불러올 수 없습니다"
- GitHub Pages 배포 상태 확인
- URL이 올바른지 확인: `https://knue20-kmla.github.io/transcript/`

### 마크다운이 안 보임
- 파일명 형식 확인: `{이름}_세특_{과목}.md`
- GitHub 저장소가 Public인지 확인

### 학생이 드롭다운에 안 나옴
- `students.json`의 `students` 배열에 추가했는지 확인
- JSON 문법 오류 확인 (쉼표, 중괄호 등)

## 📞 다음 단계

- [x] 프로토타입 완성
- [x] JSON 기반 전환
- [x] GitHub Pages 배포
- [ ] PDF → JSON 자동 변환 (AI 비교 테스트)
- [ ] 나머지 12명 데이터 추가
- [ ] 추가 기능 (검색, 인쇄, 엑셀 내보내기 등)

---

**제작:** KMLA 생기부 조회 시스템  
**버전:** 2.0 (JSON 기반)  
**저장소:** https://github.com/knue20-kmla/transcript
