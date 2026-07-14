# C:\smart_qc_system\utils\file_manager.py
import os
import json
import pandas as pd
from utils.logger import log_info, log_error

def ensure_directory(path):
    """필요한 디렉토리가 없으면 생성합니다."""
    if not os.path.exists(path):
        os.makedirs(path)
        log_info(f"디렉토리 생성 완료: {path}")

def save_json(data, file_path):
    """데이터를 JSON 형식으로 저장합니다."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        log_info(f"파일 저장 성공: {file_path}")
        return True
    except Exception as e:
        log_error(f"파일 저장 실패: {str(e)}")
        return False

def load_json(file_path):
    """JSON 파일을 불러옵니다."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except Exception as e:
        log_error(f"파일 읽기 실패: {str(e)}")
        return None

def save_dataframe(df, file_path):
    """Pandas DataFrame을 CSV로 저장합니다."""
    try:
        df.to_csv(file_path, index=False, encoding='utf-8-sig')
        log_info(f"데이터프레임 저장 성공: {file_path}")
        return True
    except Exception as e:
        log_error(f"데이터프레임 저장 실패: {str(e)}")
        return False