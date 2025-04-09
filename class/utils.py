import json
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(CURRENT_DIR, "..", "json")

def load_data(filename):
    filepath = os.path.join(BASE_DIR, filename)
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, dict) and "users" in data and isinstance(data["users"], list):
                return data["users"]
            if isinstance(data, dict) and "rooms" in data and isinstance(data["rooms"], list): 
                return data["rooms"]
            if isinstance(data, dict) and "transitions" in data and isinstance(data["transitions"], list):
                return data["transitions"]
            if isinstance(data, dict) and "reports" in data and isinstance(data["reports"], list):
                return data["reports"]
            if isinstance(data, dict) and "violations" in data and isinstance(data["violations"], list):
                return data["violations"]
            if isinstance(data, dict) and "computers" in data and isinstance(data["computers"], list):
                return data["computers"]
            elif isinstance(data, list):
                return data
            else:
                print(f"Dữ liệu trong {filepath} không hợp lệ!")
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Không thể tải dữ liệu từ {filepath}!")
        return []

def save_data(filename, data):
    filepath = os.path.join(BASE_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def get_user_info(user_id, users):
    user = next((u for u in users if u["userId"] == user_id), None)
    if user:
        return user
    return None