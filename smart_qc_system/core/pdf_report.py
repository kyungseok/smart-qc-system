import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# 1. 한글 폰트 설정
FONT_PATH = r"C:\Windows\Fonts\malgun.ttf"
pdfmetrics.registerFont(TTFont('MalgunGothic', FONT_PATH))

# 2. 저장 경로 설정
PDF_SAVE_DIR = r"C:\smart_qc_system\data\reports\pdf"
if not os.path.exists(PDF_SAVE_DIR):
    os.makedirs(PDF_SAVE_DIR)

def create_formatted_pdf(row, output_path):
    doc = SimpleDocTemplate(output_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    
    style_title = ParagraphStyle('title', fontName='MalgunGothic', fontSize=20, alignment=1)
    
    # 제목
    elements.append(Paragraph("최 종 검 사 성 적 서", style_title))
    elements.append(Spacer(1, 20))
    
    # 상단 정보 테이블
    info_data = [
        ["문서 번호", str(row.get('문서번호', '')), "LOT No.", str(row.get('LOT No.', '')), "고객사", str(row.get('고객사', ''))],
        ["품명", str(row.get('P/N (품명)', '')), "검사일자", str(row.get('검사일자', '')), "검사자", str(row.get('검사자', ''))]
    ]
    t_info = Table(info_data, colWidths=[70, 140, 60, 100, 60, 80])
    t_info.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONT', (0,0), (-1,-1), 'MalgunGothic', 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (0,1), colors.whitesmoke),
        ('BACKGROUND', (2,0), (2,1), colors.whitesmoke),
        ('BACKGROUND', (4,0), (4,1), colors.whitesmoke),
    ]))
    elements.append(t_info)
    elements.append(Spacer(1, 20))
    
    # 치수 검사 결과 테이블
    elements.append(Paragraph("1. 치수 검사 결과 (N=5)", ParagraphStyle('normal', fontName='MalgunGothic', fontSize=12)))
    dim_data = [["항목", "규격 및 공차", "N1", "N2", "N3", "N4", "N5", "결과"]]
    
    # 데이터 처리 (nan 값 공백으로 치환)
    def clean(val): return str(val) if pd.notnull(val) else ""
    
    dim_data.append(["길이", clean(row.get('[치수] 길이 치수 기준', '')), clean(row.get('[치수] 길이 치수 N1', '')), clean(row.get('[치수] 길이 치수 N2', '')), clean(row.get('[치수] 길이 치수 N3', '')), clean(row.get('[치수] 길이 치수 N4', '')), clean(row.get('[치수] 길이 치수 N5', '')), "OK"])
    
    t_dim = Table(dim_data, colWidths=[60, 120, 50, 50, 50, 50, 50, 60])
    t_dim.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONT', (0,0), (-1,-1), 'MalgunGothic', 9),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ]))
    elements.append(t_dim)
    
    doc.build(elements)

# 3. Streamlit UI
st.title("📄 최종 검사 성적서 출력 시스템")
file_path = r"C:\smart_qc_system\data\reports\output\출하검사 기록관리 대장.xlsx"

if os.path.exists(file_path):
    df = pd.read_excel(file_path)
    selected_idx = st.selectbox("검사 기록 선택", df.index, format_func=lambda i: f"{df.loc[i, '문서번호']}")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("PDF 생성"):
            out_filename = os.path.join(PDF_SAVE_DIR, f"성적서_{df.loc[selected_idx, '문서번호']}.pdf")
            create_formatted_pdf(df.loc[selected_idx], out_filename)
            st.success(f"생성 완료!")
    with col2:
        if st.button("저장 폴더 열기"):
            os.startfile(PDF_SAVE_DIR)
else:
    st.error("데이터 파일을 찾을 수 없습니다.")