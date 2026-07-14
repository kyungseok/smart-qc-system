# C:\smart_qc_system\utils\logger.py 수정본
import logging
import os
from datetime import datetime

# 1. 절대 경로를 사용하여 로그 저장 위치를 확실하게 지정합니다
log_dir = r"C:\smart_qc_system\data\logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"system_{datetime.now().strftime('%Y%m%d')}.log")

# 2. 로거 설정: force=True로 설정을 갱신하고 즉시 기록을 유도합니다
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(log_file, encoding='utf-8'),
        logging.StreamHandler()
    ],
    force=True 
)

def log_info(message):
    """일반 정보 기록 및 즉시 파일 반영"""
    logging.info(message)
    # 로그 발생 시 즉시 파일에 쓰도록 핸들러를 flush 합니다
    for handler in logging.getLogger().handlers:
        handler.flush()

def log_error(message):
    """에러 발생 기록 및 즉시 파일 반영"""
    logging.error(message)
    for handler in logging.getLogger().handlers:
        handler.flush()

def log_warning(message):
    """경고 메시지 기록 및 즉시 파일 반영"""
    logging.warning(message)
    for handler in logging.getLogger().handlers:
        handler.flush()