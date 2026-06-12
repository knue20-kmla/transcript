# 📚 생기부 자동 업로드 시스템 (Solara 3 Pro)

## 🎯 개요

생기부 PDF를 업로드하면 Solara 3 Pro API가 자동으로 파싱하여 `students.json`에 추가하는 시스템입니다.

**특징:**
- ✅ 한글 문서에 특화된 Solara 3 Pro 사용
- ✅ 높은 정확도의 한글 텍스트 인식
- ✅ 자동 JSON 변환
- ✅ 웹 관리자 화면 (드래그 앤 드롭)
- ✅ Git 자동 커밋

---

## 🚀 빠른 시작 (웹 관리자 - 추천!)

### 1. 패키지 설치
```bash
pip3 install streamlit pandas requests
```

### 2. API 키 설정
```bash
export UPSTAGE_API_KEY='up_...'

# 영구 설정
echo 'export UPSTAGE_API_KEY="up_..."' >> ~/.zshrc
source ~/.zshrc
```

### 3. 관리자 화면 실행
```bash
cd ~/Desktop/생기부-시스템
streamlit run admin.py
```

### 4. 브라우저 열기
자동으로 열리거나 직접 접속:
```
http://localhost:8501
```

### 5. PDF 업로드
1. 📤 업로드 탭 선택
2. PDF 파일 **드래그 앤 드롭** 또는 찾아보기
3. 🚀 업로드 시작 클릭
4. 완료!

---

## 💻 CLI 사용 (고급)

커맨드라인에서 직접 실행하려면:

```bash
cd ~/Desktop/생기부-시스템
python3 upload_student.py 생기부.pdf
```

### 실행 흐름

```
1. PDF 파일 읽기
   ↓
2. Solara 3 Pro API로 분석 (30초-1분)
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
- [ ] `requests` 패키지 설치됨
- [ ] Upstage API 키 설정됨
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
Solara 3 Pro API 비용은 Upstage 공식 가격 정책을 참고하세요.
- 생기부 1개: 약 $0.10-0.30 (예상)
- 매우 경제적!

### 3. 변환 정확도
- 첫 실행 후 `students.json` 확인 필수
- 오류 발견 시 수동 수정 필요
- Solara 3 Pro는 한글 문서에 최적화되어 있어 높은 정확도 제공

---

## 🐛 문제 해결

### 오류: "UPSTAGE_API_KEY가 설정되지 않았습니다"

**해결:**
```bash
export UPSTAGE_API_KEY='up_...'
```

### 오류: "requests 모듈을 찾을 수 없습니다"

**해결:**
```bash
pip3 install requests
```

### 오류: "파일을 찾을 수 없습니다"

**해결:**
```bash
# 절대 경로 사용
python3 upload_student.py ~/Downloads/생기부.pdf
```

### API 오류 (400, 401, 500 등)

**해결:**
1. API 키 확인: `echo $UPSTAGE_API_KEY`
2. API 키가 올바른지 확인
3. Upstage 콘솔에서 사용량 확인

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

## 💰 비용

Solara 3 Pro API 비용은 Upstage 공식 가격 정책을 참고하세요.

**예상:**
- 생기부 1개: 약 $0.10-0.30
- 매우 경제적!

---

## 📞 문의

문제가 발생하면:
1. `upload.log` 확인
2. API 키 재확인
3. GitHub Issues에 문의
4. 수동으로 JSON 편집

---

## 🔄 향후 계획

- [ ] 웹 UI 추가 (Vercel)
- [ ] 로그인 시스템
- [ ] 실시간 업로드
- [ ] 자동 배포

---

**마지막 업데이트:** 2025년 6월
