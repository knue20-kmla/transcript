# 📚 생기부 자동 업로드 시스템

## 🎯 개요

생기부 PDF를 업로드하면 Claude API가 자동으로 파싱하여 `students.json`에 추가하는 시스템입니다.

---

## 🚀 빠른 시작

### 1. Python 설치 확인

```bash
python3 --version
```

Python 3.7 이상 필요

---

### 2. 필수 패키지 설치

```bash
pip3 install anthropic
```

---

### 3. Claude API 키 설정

#### 방법 A: 환경변수 (추천)

```bash
export ANTHROPIC_API_KEY='sk-ant-api03-...'
```

영구 설정 (macOS/Linux):
```bash
echo 'export ANTHROPIC_API_KEY="sk-ant-api03-..."' >> ~/.zshrc
source ~/.zshrc
```

#### 방법 B: 스크립트 수정

`upload_student.py` 파일 상단에 직접 입력:
```python
ANTHROPIC_API_KEY = "sk-ant-api03-..."
```

---

## 📖 사용법

### 기본 사용

```bash
cd ~/Desktop/생기부-시스템
python3 upload_student.py 홍길동_생기부.pdf
```

### 실행 흐름

```
1. PDF 파일 읽기
   ↓
2. Claude API로 분석 (30초-1분)
   ↓
3. JSON 변환
   ↓
4. students.json 업데이트
   ↓
5. Git 커밋 여부 선택
   ↓
6. 완료!
```

---

## ✅ 체크리스트

**업로드 전:**
- [ ] Python 3.7+ 설치됨
- [ ] `anthropic` 패키지 설치됨
- [ ] Claude API 키 설정됨
- [ ] 생기부 PDF 준비됨

**업로드 후:**
- [ ] `data/students.json` 확인
- [ ] 웹사이트에서 데이터 확인
- [ ] Git 커밋 & 푸시

---

## 🔍 출력 JSON 형식

스크립트는 다음 형식으로 변환합니다:

```json
{
  "이름": "홍길동",
  "학년": "3",
  "반": "1",
  "번호": "5",
  "계열": "자연계열",
  "프로필이미지URL": "",
  "성적": [...],
  "highlights": [...],
  "세특종합분석": {...},
  "진로활동": {...},
  "동아리활동": [...],
  "자율활동": [...],
  "행동특성": [...]
}
```

---

## ⚠️ 주의사항

### 1. 중복 확인
같은 이름의 학생이 이미 있으면 덮어쓰기 여부를 묻습니다.

### 2. API 비용
- Claude 3.5 Sonnet: $3 / 1M input tokens
- 생기부 1개: 약 $0.10-0.30
- 10명 = 약 $3

### 3. 변환 정확도
- 첫 실행 후 `students.json` 확인 필수
- 오류 발견 시 수동 수정 필요

---

## 🐛 문제 해결

### 오류: "ANTHROPIC_API_KEY가 설정되지 않았습니다"

**해결:**
```bash
export ANTHROPIC_API_KEY='your-api-key-here'
```

### 오류: "anthropic 모듈을 찾을 수 없습니다"

**해결:**
```bash
pip3 install anthropic
```

### 오류: "파일을 찾을 수 없습니다"

**해결:**
```bash
# 절대 경로 사용
python3 upload_student.py ~/Downloads/생기부.pdf
```

### JSON 형식이 이상함

**해결:**
1. `data/students.json` 열기
2. 해당 학생 데이터 수동 수정
3. 저장 후 Git 커밋

---

## 💡 팁

### 1. 여러 학생 한번에 업로드

```bash
for pdf in *.pdf; do
  python3 upload_student.py "$pdf"
done
```

### 2. 백업 생성

```bash
cp data/students.json data/students.backup.json
```

### 3. 로그 저장

```bash
python3 upload_student.py 생기부.pdf > upload.log 2>&1
```

---

## 📞 문의

문제가 발생하면:
1. `upload.log` 확인
2. GitHub Issues에 문의
3. 수동으로 JSON 편집

---

## 🔄 향후 계획

- [ ] 웹 UI 추가 (Vercel)
- [ ] 로그인 시스템
- [ ] 실시간 업로드
- [ ] 자동 배포

---

**마지막 업데이트:** 2025년 6월
