import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
URL_API = os.getenv("URL_API")

# MQTT Configuration
BROKER_ADDRESS = os.getenv("BROKER_ADDRESS")
PORT = int(os.getenv("PORT", "1883"))  # Default to 1883 if not set
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
KEY = os.getenv("KEY")
KEEPALIVE = int(os.getenv("KEEPALIVE", "60"))  # Default to 60 if not set
TIMEOUT_WAIT = int(os.getenv("TIMEOUT_WAIT", "60"))  # Default to 30 seconds if not set

# MQTT Topics
TOPIC_SEND_DEVICE_STATUS = (f"{KEY}/control/device-status", 2)
TOPIC_SEND_SENSOR_STATUS = (f"{KEY}/sensor/status", 2)

TOPICS_RECEIVE_DEVICE_STATUS = (f"{KEY}/devices/control", 2)
TOPICS_RECEIVE_CONFIG_DATA = (f"{KEY}/config/data", 2)

# Default Configuration
DEFAULT_CONFIG = {
    "setting": {
        "mode": "auto",
        "updateTime": 120,  # thời gian update data
        "keyLora": [],  # Danh sách node để request dữ liệu 
        "tempOnSetpoint": -19, # nhiệt độ bật máy ở chế độ Tự động ưu tiên chạy máy và sạc PCM 
        "tempOffSetpoint": -20, # nhiệt độ tắt máy ở chế độ Tự động ưu tiên chạy máy và sạc PCM 
        "tempOnSetpointUsing": -16,	# nhiệt độ bật máy ở chế độ Tự động ưu tiên xả PCM để tiết kiệm điện 
        "tempOffSetpointUsing": -18,	# nhiệt độ tắt máy ở chế độ Tự động ưu tiên xả PCM để tiết kiệm điện
        "time_on_charging_hour": 22,  # thời điểm bắt đầu chế độ Tự động ưu tiên chạy máy và sạc PCM 
        "time_on_charging_min": 0,  # min
        "time_off_charging_hour": 7,  # thời điểm bắt đầu chế độ Tự động ưu tiên xả PCM để tiết kiệm điện 
        "time_off_charging_min": 0,  # min
        "def_cycle": 6,  # Thời gian lặp lại chu kỳ xả đá (giờ)
        "def_time": 15,  # Thời gian xả đá (phút)
        "def_drip": 60,  # Thời gian nhỏ giọt sau xả đá (Bắt buộc lớn hơn 1s - chống nhiễu) (giây)
        "def_delay": 10,  # Thời gian trễ trước khi vào xả đá (Bắt buộc lớn hơn 1s - chống nhiễu) (giây)
        "tempOffDef": 10,  # Nhiệt độ dừng xả đá (C degree)
        "timeoutSerial": 5, #Thời gian đọc cảm biến
    },
    "control": {
        "compressor": 1,
        "fan": 1,
        "defrost": 0
    }
} 