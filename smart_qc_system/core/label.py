import streamlit as st
import datetime
import os
import io
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

# --- Page Settings & Responsive Design ---
st.set_page_config(page_title="Smart CAM Inspection System", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #F4F6F9; }
    h1 { color: #2C3E50; font-family: 'sans-serif'; font-size: 24px; }
    .stButton>button { width: 100%; font-weight: bold; height: 45px; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

st.title("📹 Smart CAM Inspection System")
st.write("품목 정보를 입력하고 제품과 라벨을 순차적으로 촬영한 후 PDF 성적서를 생성합니다.")

# Initialize Session State
if "prod_img_data" not in st.session_state: st.session_state.prod_img_data = None
if "label_img_data" not in st.session_state: st.session_state.label_img_data = None
if "cam_step" not in st.session_state: st.session_state.cam_step = 1

# --- Layout ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Inspection Information")
    date_val = st.date_input("Inspection Date", datetime.date.today())
    inspector_val = st.selectbox("Inspector", ["Lee Wan-hee", "Cho Kyung-seok", "Kim Min-woo", "Lee Hong-gyu"], index=1)
    pn_val = st.text_input("P/N (Product Name)", placeholder="Enter product name")
    lot_val = st.text_input("LOT No.", placeholder="Enter LOT number")
    manufacturer_val = st.text_input("Manufacturer", value="ABSFIL")
    client_val = st.text_input("Client", placeholder="Enter client name")
    
    st.markdown("---")
    st.subheader("💾 Export Report")
    
    formatted_date = date_val.strftime("%Y%m%d")
    clean_pn = pn_val if pn_val else "Unknown"
    clean_lot = lot_val if lot_val else "Unknown"
    pdf_filename = f"{formatted_date}_{clean_pn}_{clean_lot}_Inspection.pdf"

    def generate_pdf_bytes():
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=letter)
        c.setFont("Helvetica-Bold", 18)
        c.drawString(55, 733, "SMART CAM INSPECTION REPORT")
        # 이미지 데이터 보존 및 캔버스 그리기 로직
        if st.session_state.prod_img_data:
            st.session_state.prod_img_data.save("temp_p.jpg")
            c.drawImage("temp_p.jpg", 40, 295, width=250, height=175)
        if st.session_state.label_img_data:
            st.session_state.label_img_data.save("temp_l.jpg")
            c.drawImage("temp_l.jpg", 320, 295, width=250, height=175)
        c.save()
        if os.path.exists("temp_p.jpg"): os.remove("temp_p.jpg")
        if os.path.exists("temp_l.jpg"): os.remove("temp_l.jpg")
        buffer.seek(0)
        return buffer.getvalue()

    if st.session_state.prod_img_data and st.session_state.label_img_data:
        st.download_button("📥 Download PDF Report", data=generate_pdf_bytes(), file_name=pdf_filename, mime="application/pdf", type="primary")
    else:
        st.warning("⚠️ 촬영 완료 후 PDF 다운로드가 활성화됩니다.")

with col2:
    if st.session_state.cam_step == 1:
        st.subheader("📸 Step 1: Capture Product")
        cam_prod = st.camera_input("Take Product Photo", key="cam_prod_key")
        if cam_prod:
            st.session_state.prod_img_data = Image.open(cam_prod)
            if st.button("Proceed to Step 2 ➡️"):
                st.session_state.cam_step = 2
                st.rerun()
    elif st.session_state.cam_step == 2:
        st.subheader("📸 Step 2: Capture Label")
        cam_label = st.camera_input("Take Label Photo", key="cam_label_key")
        if cam_label:
            st.session_state.label_img_data = Image.open(cam_label)
            if st.button("Finish & Lock Photos 🔒"):
                st.session_state.cam_step = 3
                st.rerun()
    elif st.session_state.cam_step == 3:
        st.subheader("✅ Captures Completed")
        if st.button("🔄 Reset Photos"):
            st.session_state.prod_img_data = None
            st.session_state.label_img_data = None
            st.session_state.cam_step = 1
            st.rerun()