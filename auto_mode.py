# 26/03/2025
def AUTO_MODE(setting, sensors):
    """
    Xử lý chế độ tự động
    Args:
        setting: Cấu hình hệ thống
        sensors: Dữ liệu cảm biến
    Returns:
        dict: Trạng thái điều khiển các thiết bị
    """
    try:
        # Lấy giá trị từ config
        temp_on = config["setting"]["tempOnSetpoint"]
        temp_off = config["setting"]["tempOffSetpoint"]
        
        # Lấy giá trị từ cảm biến
        temp_ac = sensors["air_conditioner"]
        temp_storage = sensors["storage"]
        temp_battery = sensors["cold_battery"]
        
        # Logic điều khiển tự động
        if temp_storage > temp_on:
            return {
                "compressor": 1,
                "fan": 1
            }
        elif temp_storage <= temp_off:
            return {
                "compressor": 0,
                "fan": 0
            }
        else:
            return {
                "compressor": 0,
                "fan": 1
            }
            
    except Exception as e:
        logger.error(f"Lỗi trong chế độ tự động: {e}")
        return {
            "compressor": 0,
            "fan": 0
        } 