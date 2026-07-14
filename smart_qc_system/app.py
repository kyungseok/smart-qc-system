import streamlit as st
import sys
import os
from datetime import datetime
import subprocess
import socket
import time

# --- 0. 모듈 경로 설정 및 로거 연결 ---
sys.path.append(r"C:\smart_qc_system")
from utils import logger 

# --- 세션 상태 초기화 ---
if "logs" not in st.session_state:
    st.session_state.logs = []
if "page" not in st.session_state:
    st.session_state.page = "main"

def add_log(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_text = f"[{timestamp}] {message}"
    st.session_state.logs.append(log_text)
    if hasattr(logger, 'log_info'):
        logger.log_info(message)
    # 로그가 15개 이상 넘어가면 최신 위주로 관리
    if len(st.session_state.logs) > 15:
        st.session_state.logs.pop(0)

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

def start_app(app_type):
    state_key = f"{app_type}_url"
    if state_key not in st.session_state:
        port = get_free_port()
        app_path = rf"C:\smart_qc_system\core\{app_type}.py"
        
        add_log(f"서버 시작 중... [{app_type}]")
        cmd = [sys.executable, "-m", "streamlit", "run", app_path, "--server.port", str(port)]
        subprocess.Popen(cmd)
        
        time.sleep(3) 
        st.session_state[state_key] = f"http://localhost:{port}"
        
        add_log(f"성공: {app_type} 앱이 실행되었습니다.")
        add_log(f"-> Local URL: {st.session_state[state_key]}")
        add_log(f"-> 포트 번호: {port}")
    else:
        add_log(f"알림: {app_type} 앱은 이미 실행 중입니다.")
        
    return st.session_state[state_key]

# 폴더 열기 함수
def open_folder(path):
    if os.path.exists(path):
        os.startfile(path)
        add_log(f"폴더 열기: {path}")
    else:
        st.error(f"경로를 찾을 수 없습니다: {path}")
        add_log(f"오류: 경로를 찾을 수 없습니다 ({path})")

# 페이지 설정
st.set_page_config(page_title="Smart QC Inspection System", layout="wide")

# CSS 스타일링
st.markdown("""
    <style>
    .main-header { font-size: 32px; font-weight: bold; color: #1f77b4; }
    /* 모든 버튼 크기 통일 */
    .stButton>button, .stLinkButton>a { 
        width: 100%; height: 80px; font-weight: bold; font-size: 16px; 
        display: flex; align-items: center; justify-content: center; 
        border-radius: 10px; border: 1px solid #ccc;
    }
    .stButton>button:hover, .stLinkButton>a:hover { border-color: #1f77b4; color: #1f77b4; }
    </style>
""", unsafe_allow_html=True)

# --- 메인 페이지 로직 ---
if st.session_state.page == "main":
    with st.container():
        col_l, col_r = st.columns([3, 1])
        with col_l:
            st.markdown('<p class="main-header">📹 Smart QC Inspection System</p>', unsafe_allow_html=True)
            st.write("검사 정보를 입력하고 공정별 데이터를 캡처하여 성적서를 생성합니다.")
        with col_r:
            st.info("👤 사용자: Manager\n\n🟢 상태: 정상 작동")

    st.divider()
    st.subheader("📝 주요 기능")

    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("📥 Standard 제품 성적서 작성"):
            start_app("standard")
            st.rerun()
    with c2:
        if st.button("🧢 Capsule 제품 성적서 작성"):
            start_app("capsule")
            st.rerun()
    with c3:
        if st.button("🔄 Flux 제품 성적서 작성"):
            start_app("flux")
            st.rerun()

    c4, c5, c6 = st.columns(3)
    with c4:
        if st.button("📷 라벨 포장 성적서 작성"):
            start_app("label")
            st.rerun()
    with c5:
        if st.button("💾 데이터 병합 및 메일 보고"):
            start_app("merge_and_send")
            st.rerun()
    with c6:
        if st.button("📄 성적서 PDF 출력"):
            start_app("pdf_report")
            st.rerun()

    # --- 작업 폴더 바로가기 ---
    st.divider()
    st.subheader("📂 작업 폴더 바로가기")
    col_path1, col_path2, col_path3, col_path4 = st.columns(4)
    with col_path1:
        if st.button("📁 엑셀 성적서 폴더"):
            open_folder(r"C:\smart_qc_system\data\reports\output")
    with col_path2:
        if st.button("📁 PDF 성적서 폴더"):
            open_folder(r"C:\smart_qc_system\data\reports\pdf")
    with col_path3:
        if st.button("📁 라벨 PDF 폴더"):
            open_folder(r"C:\smart_qc_system\data\reports\pdf_cam")
    with col_path4:
        st.link_button("🌐 구글 공유 폴더", "https://drive.google.com/drive/folders/10yI79ChsJ3R3GLpeGjLxBYlev6-nk7BG")

    st.divider()
    st.subheader("📜 시스템 로그")
    with st.container(height=150):
        for log in reversed(st.session_state.logs):
            st.text(log)

    st.divider()
    st.subheader("🔗 실행 중인 어플리케이션 접속")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.session_state.get("standard_url"):
            st.link_button("🚀 [Standard] 바로가기", st.session_state.standard_url)
        if st.session_state.get("capsule_url"):
            st.link_button("🚀 [Capsule] 바로가기", st.session_state.capsule_url)
    with col2:
        if st.session_state.get("flux_url"):
            st.link_button("🚀 [Flux] 바로가기", st.session_state.flux_url)
        if st.session_state.get("label_url"):
            st.link_button("🚀 [라벨포장] 바로가기", st.session_state.label_url)
    with col3:
        if st.session_state.get("merge_and_send_url"):
            st.link_button("🚀 [데이터병합] 바로가기", st.session_state.merge_and_send_url)
        if st.session_state.get("pdf_report_url"):
            st.link_button("🚀 [PDF보고서] 바로가기", st.session_state.pdf_report_url)