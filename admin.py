#!/usr/bin/env python3
"""
생기부 관리자 화면 (Streamlit)

실행 방법:
    streamlit run admin.py

포트:
    http://localhost:8501
"""

import streamlit as st
import os
import sys
import subprocess
from pathlib import Path

# 페이지 설정
st.set_page_config(
    page_title="생기부 관리자",
    page_icon="📚",
    layout="wide"
)

# 타이틀
st.title("📚 생기부 자동 업로드 시스템")
st.markdown("---")

# 사이드바
with st.sidebar:
    st.header("⚙️ 설정")

    # API 키 확인
    api_key = os.environ.get("UPSTAGE_API_KEY")
    if api_key:
        st.success("✅ API 키 설정됨")
    else:
        st.error("❌ UPSTAGE_API_KEY 환경변수 필요")
        st.code("export UPSTAGE_API_KEY='your-key'")

    st.markdown("---")

    # 통계
    st.header("📊 통계")
    import json
    try:
        with open("data/students.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            student_count = len(data.get("students", []))
            st.metric("등록된 학생", f"{student_count}명")
    except:
        st.metric("등록된 학생", "0명")

# 메인 화면
tab1, tab2, tab3 = st.tabs(["📤 업로드", "👥 학생 목록", "📖 사용법"])

with tab1:
    st.header("📤 생기부 PDF 업로드")

    col1, col2 = st.columns([2, 1])

    with col1:
        # 파일 업로드
        uploaded_file = st.file_uploader(
            "생기부 PDF 파일을 드래그하거나 선택하세요",
            type=['pdf'],
            help="생기부 PDF 파일을 업로드하면 자동으로 파싱됩니다"
        )

        if uploaded_file:
            st.success(f"✅ 파일 선택됨: {uploaded_file.name}")

            # 미리보기 정보
            file_size = len(uploaded_file.getvalue()) / 1024  # KB
            st.info(f"📊 파일 크기: {file_size:.1f} KB")

            # 업로드 버튼
            if st.button("🚀 업로드 시작", type="primary", use_container_width=True):
                # 임시 파일 저장
                temp_path = Path("temp") / uploaded_file.name
                temp_path.parent.mkdir(exist_ok=True)

                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

                # 프로그레스 표시
                with st.spinner("📄 PDF 파싱 중... (30초-1분 소요)"):
                    try:
                        # upload_student.py 실행
                        result = subprocess.run(
                            [sys.executable, "upload_student.py", str(temp_path)],
                            capture_output=True,
                            text=True,
                            timeout=180  # 3분 타임아웃
                        )

                        if result.returncode == 0:
                            st.success("🎉 업로드 성공!")

                            # 출력 로그 표시
                            with st.expander("📋 상세 로그"):
                                st.code(result.stdout)

                            # Git 커밋 옵션
                            st.markdown("---")
                            if st.button("📝 Git 커밋 & 푸시", use_container_width=True):
                                with st.spinner("Git 푸시 중..."):
                                    commit_result = subprocess.run(
                                        ["git", "add", "data/students.json"],
                                        cwd=".",
                                        capture_output=True
                                    )
                                    subprocess.run(
                                        ["git", "commit", "-m", f"✨ {uploaded_file.name} 자동 업로드"],
                                        cwd=".",
                                        capture_output=True
                                    )
                                    push_result = subprocess.run(
                                        ["git", "push"],
                                        cwd=".",
                                        capture_output=True
                                    )

                                    if push_result.returncode == 0:
                                        st.success("✅ Git 푸시 완료!")
                                    else:
                                        st.error(f"❌ Git 푸시 실패: {push_result.stderr.decode()}")

                            # 새로고침 버튼
                            st.markdown("---")
                            if st.button("🔄 페이지 새로고침"):
                                st.rerun()
                        else:
                            st.error("❌ 업로드 실패")
                            st.code(result.stderr)

                    except subprocess.TimeoutExpired:
                        st.error("⏱️ 타임아웃: 처리 시간이 너무 오래 걸립니다")
                    except Exception as e:
                        st.error(f"❌ 오류 발생: {e}")
                    finally:
                        # 임시 파일 삭제
                        if temp_path.exists():
                            temp_path.unlink()

    with col2:
        st.info("""
        **📌 업로드 단계**

        1. PDF 파일 선택
        2. 업로드 시작 클릭
        3. 자동 파싱 대기
        4. Git 커밋 (선택)
        5. 완료!

        **⏱️ 예상 시간**
        - 파싱: 30초-1분
        - 커밋: 5초
        """)

with tab2:
    st.header("👥 등록된 학생 목록")

    try:
        with open("data/students.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            students = data.get("students", [])

            if students:
                # 테이블 형태로 표시
                import pandas as pd

                df = pd.DataFrame([
                    {
                        "이름": s.get("이름", ""),
                        "학년": s.get("학년", ""),
                        "반": s.get("반", ""),
                        "번호": s.get("번호", ""),
                        "계열": s.get("계열", "")
                    }
                    for s in students
                ])

                st.dataframe(df, use_container_width=True, hide_index=True)

                st.metric("총 학생 수", f"{len(students)}명")
            else:
                st.info("등록된 학생이 없습니다.")

    except FileNotFoundError:
        st.error("students.json 파일을 찾을 수 없습니다.")
    except Exception as e:
        st.error(f"오류: {e}")

with tab3:
    st.header("📖 사용 방법")

    st.markdown("""
    ## 🚀 빠른 시작

    ### 1. 환경 설정
    ```bash
    # Streamlit 설치
    pip3 install streamlit pandas

    # API 키 설정
    export UPSTAGE_API_KEY='your-api-key'
    ```

    ### 2. 실행
    ```bash
    cd ~/Desktop/생기부-시스템
    streamlit run admin.py
    ```

    ### 3. 브라우저 열기
    자동으로 브라우저가 열립니다:
    ```
    http://localhost:8501
    ```

    ---

    ## 📤 PDF 업로드

    1. **업로드 탭** 선택
    2. PDF 파일을 **드래그 앤 드롭** 또는 **찾아보기**
    3. **업로드 시작** 버튼 클릭
    4. 자동 파싱 완료 대기 (30초-1분)
    5. (선택) **Git 커밋 & 푸시** 버튼 클릭

    ---

    ## 🔧 문제 해결

    ### API 키 오류
    ```bash
    export UPSTAGE_API_KEY='up_...'
    ```

    ### Streamlit 설치 오류
    ```bash
    pip3 install --upgrade streamlit
    ```

    ### 포트 충돌
    ```bash
    streamlit run admin.py --server.port 8502
    ```

    ---

    ## 💡 팁

    - 여러 파일을 연속으로 업로드 가능
    - 업로드 후 학생 목록 탭에서 확인
    - Git 커밋은 선택사항 (나중에 수동 가능)
    """)

    st.markdown("---")
    st.success("✨ 생기부 자동 업로드 시스템 v1.0")
