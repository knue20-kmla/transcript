# 관리자 시스템 사용 가이드

## 📚 개요

KMLA Transcript 시스템의 관리자 대시보드를 통해 학생 생기부 PDF를 업로드하고 자동으로 시스템에 추가할 수 있습니다.

## 🚀 시작하기

### 1. 백엔드 서버 실행

```bash
cd /Users/apple/Desktop/생기부-시스템
python3 backend_server.py
```

서버가 `http://localhost:5001`에서 실행됩니다.

### 2. 관리자 로그인

브라우저에서 `login.html` 파일을 엽니다:
- **아이디**: `admin`
- **비밀번호**: `kmla2025`

### 3. PDF 업로드

1. 관리자 대시보드에서 PDF 파일을 드래그 앤 드롭하거나 "파일 선택" 버튼 클릭
2. 시스템이 자동으로:
   - Solar Pro API로 PDF 파싱
   - JSON 데이터 생성
   - 마크다운 파일 생성
   - Git에 커밋 및 푸시

## 📋 시스템 구성

### 파일 구조

```
생기부-시스템/
├── login.html              # 관리자 로그인 페이지
├── admin_dashboard.html    # 관리자 대시보드
├── backend_server.py       # Flask 백엔드 서버
├── upload_student.py       # PDF 파싱 로직
├── generate_markdown.py    # 마크다운 생성 로직
├── data/
│   └── students.json       # 학생 데이터
├── markdown/               # 생성된 마크다운 파일
└── pdfs/                   # 업로드된 PDF 파일
```

### API 엔드포인트

- `POST /upload` - PDF 파일 업로드 및 처리
- `GET /students` - 학생 목록 조회
- `GET /health` - 서버 상태 확인

## 🔧 환경 설정

### 필수 환경 변수

```bash
export UPSTAGE_API_KEY='your-upstage-api-key'
```

### Python 패키지

```bash
pip3 install flask flask-cors requests
```

## 📝 처리 흐름

1. **PDF 업로드**: 관리자가 생기부 PDF 업로드
2. **텍스트 추출**: Upstage Document Parse API로 PDF → 텍스트
3. **데이터 파싱**: Solar Pro API로 텍스트 → 구조화된 JSON
4. **데이터 저장**: students.json에 학생 데이터 추가
5. **마크다운 생성**: 과목군별 마크다운 파일 자동 생성
6. **Git 커밋**: 변경사항 자동 커밋 및 푸시
7. **완료**: 메인 시스템에서 즉시 확인 가능

## 🎯 주요 기능

### 자동 처리
- ✅ PDF → JSON 변환
- ✅ 과목군 자동 분류 (국어, 영어, 수학, 과학, 사회, 정보, 제2외국어, 교양)
- ✅ 마크다운 파일 자동 생성
- ✅ Git 자동 커밋/푸시
- ✅ 중복 학생 자동 덮어쓰기

### 데이터 구조
- 성적 (학년, 학기, 과목, 등급, 성취도, 세특)
- 세특종합분석 (과목군별 핵심역량, 주요평가, 발전가능성)
- Highlights (주요 세특 평가 표현)
- 진로활동, 동아리활동, 자율활동, 행동특성

## 🔒 보안

- 세션 기반 로그인 (sessionStorage)
- CORS 설정으로 외부 접근 제한
- 프로덕션 환경에서는 서버 기반 인증 구현 권장

## 🐛 문제 해결

### 서버 연결 실패
- 백엔드 서버가 실행 중인지 확인
- `http://localhost:5001/health`로 서버 상태 확인

### API 키 오류
- `UPSTAGE_API_KEY` 환경변수 확인
- API 키 유효성 확인

### Git 푸시 실패
- Git 인증 정보 확인
- 원격 저장소 접근 권한 확인

## 📞 문의

시스템 관련 문의는 개발팀에 연락하세요.
