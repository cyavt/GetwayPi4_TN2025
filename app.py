###################### 26/03/2025 ###################
import paho.mqtt.client as mqtt
import json
import time
import requests
import threading
from auto_mode import AUTO_MODE
from config import (
    BROKER_ADDRESS, PORT, USERNAME, PASSWORD, KEY, TOPICS_RECEIVE_DEVICE_STATUS, TOPICS_RECEIVE_CONFIG_DATA, TOPIC_SEND_DEVICE_STATUS, TOPIC_SEND_SENSOR_STATUS, URL_API, DEFAULT_CONFIG, KEEPALIVE, TIMEOUT_WAIT
)

################## VARIABLES PUBLIC #################
client = mqtt.Client(f"RaspberryPi_{KEY}")
config = DEFAULT_CONFIG.copy()
connected = False
response_received = threading.Event()
response_payload = None

##################### API/HTTP #####################
def api(method, uri, data):
    url = URL_API + uri
    response = requests.request(method, url, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None

################### MQTT FUNCTION ##################
def on_connect(client, userdata, flags, rc):
    global connected
    if rc == 0:
        print("Đã kết nối đến MQTT Broker!")
        client.subscribe([TOPICS_RECEIVE_DEVICE_STATUS, TOPICS_RECEIVE_CONFIG_DATA])
        connected = True
        send_status()
    else:
        connected = False

def on_disconnect(client, userdata, rc):
    global connected
    connected = False

def connect_with_retry():
    global connected
    while not connected:
        try:
            print("Đang kết nối đến MQTT Broker...")
            client.connect(BROKER_ADDRESS, PORT, KEEPALIVE)
            connected = True
        except Exception as e:
            print(f"Kết nối thất bại: {e}. Thử lại sau 5 giây...")
            time.sleep(5)
            
def on_message(client, userdata, msg):
    global config, response_payload, response_received
    try:
        topic = msg.topic
        payload = msg.payload.decode()
        if topic == TOPICS_RECEIVE_CONFIG_DATA[0]:
            isMode = json.loads(payload).get("mode")
            if isMode:
                config["setting"] = json.loads(payload)
                print(f"Config: {config['setting']}")
                # Break wait AI mode
                response_received.set()
        elif topic == TOPICS_RECEIVE_DEVICE_STATUS[0] and config["setting"]["mode"] == "manual":
            config["control"] = json.loads(payload)
            print(f"Control: {config['control']}")
            send_status()
            # Break wait AI mode
            response_received.set()
        elif topic == TOPICS_RECEIVE_DEVICE_STATUS[0] and config["setting"]["mode"] == "ai":
            response_payload = json.loads(payload)
            print(f"Response Payload: {response_payload}")
            # Break wait AI mode
            response_received.set()

    except json.JSONDecodeError:
        print("Lỗi: Tin nhắn không đúng định dạng JSON")
    except Exception as e:
        print(f"Lỗi xử lý lệnh: {e}")

def send_status():
    global config
    if connected:
        control_device(config["control"])
        device_states = json.dumps(config["control"])
        client.publish(TOPIC_SEND_DEVICE_STATUS[0], device_states, TOPIC_SEND_DEVICE_STATUS[1])

def send_sensor_status_and_wait(sensor_data):
    global response_payload
    if not connected:
        return None
    sensor_json = json.dumps(sensor_data)
    response_received.clear()
    response_payload = None
    client.publish(TOPIC_SEND_SENSOR_STATUS[0], sensor_json, TOPIC_SEND_SENSOR_STATUS[1])
    if response_received.wait(timeout=TIMEOUT_WAIT):
        return response_payload
    else:
        return None

def control_device(control):
    print(f"control: {control}")
    # if control["compressor"]:
    #     print("Compressor State")
    # if control["fan"]:
    #     print("Fan State")

################### CALLBACK ####################
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message

################### MQTT LOOP ####################
def mqtt_loop():
    connect_with_retry()
    client.loop_forever()

################# DEFROST MODE LOOP ###############
def defrost_mode_loop():
    global config
    while True:
          time.sleep(5)

#################### MAIN LOOP ####################
try:
    # config_from_server = api("GET", "/config", None)
    # if config_from_server: config = config_from_server
    # else: exit()

    mqtt_thread = threading.Thread(target=mqtt_loop)
    mqtt_thread.daemon = True
    mqtt_thread.start()

    defrost_thread = threading.Thread(target=defrost_mode_loop)
    defrost_thread.daemon = True
    defrost_thread.start()

    while True:
        try:
            # Lấy dữ liệu cảm biến từ cảm biến
            sensors = {"air_conditioner": 20.5, "storage": 18.2, "cold_battery": 15.7, "air_conditioner_energy": 2.75 }
            
            if config["setting"]["mode"] == "ai":
                    device_states = send_sensor_status_and_wait(sensors)
                    if device_states:
                        config["control"] = device_states
                        send_status()
                    else:
                        print("No response from device of AI mode, AGAIN...")
            elif config["setting"]["mode"] == "auto":
                    device_states = AUTO_MODE(config["setting"], sensors)
                    if device_states:
                        config["control"] = device_states
                        send_status()
            elif config["setting"]["mode"] == "manual":
                    # Nothing to do
                    print("Manual mode")
            elif config["setting"]["mode"] == "off":
                    device_states = {"air_conditioner": False, "storage": False, "cold_battery": False, "air_conditioner_energy": False}
                    config["control"] = device_states
                    send_status()
            else:
                print("Defrost mode")
                
        except Exception as e:
            pass
        
        time.sleep(5)

except KeyboardInterrupt:
     print("STOPPED")