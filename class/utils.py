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

def update_computer_status(computer_id_to_update, new_status):

    valid_statuses = ["Đang hoạt động", "Đang bảo trì", "Đang hư hỏng"]
    if new_status not in valid_statuses:
        print(f"Lỗi: Trạng thái '{new_status}' không hợp lệ.")
        return False

    try:
        computers = load_data("computer.json")
        if not isinstance(computers, list):
             print("Lỗi: Không thể xử lý dữ liệu máy tính (không phải danh sách).")
             return False

        computer_found = False
        for comp in computers:
            if str(comp.get("computerId")) == str(computer_id_to_update):
                comp["status"] = new_status
                computer_found = True
                break 

        if not computer_found:
            print(f"Lỗi: Không tìm thấy máy tính nào có ID '{computer_id_to_update}'.")
            return False

        if save_data("computer.json", computers):
            print(f"Đã cập nhật trạng thái máy tính {computer_id_to_update} thành '{new_status}' thành công.")
            return True
        else:
            return False

    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn khi cập nhật trạng thái máy tính: {e}")
        return False

def report_violation(reported_by, violator_id, reason):
    try:
        users = load_data("user.json")
        if not users:
            print("Lỗi: Không thể tải danh sách người dùng.")
            return False


        reporter = get_user_info(reported_by, users)
        if not reporter or reporter["role"] != "employee":
            print(f"Lỗi: ID '{reported_by}' không phải nhân viên hợp lệ.")
            return False

        violator = get_user_info(violator_id, users)
        if not violator:
            print(f"Lỗi: Không tìm thấy người dùng với ID '{violator_id}'.")
            return False

        if violator["role"] in ["employee", "admin"]:
            print(f"Lỗi: chú không có đủ trình để báo cáo anh biết anh là {violator['role']} (ID: '{violator_id}').")
            return False

        violations_data = load_data("violation.json")
        if not isinstance(violations_data, list):
            violations_data = [] 

        violation_count = len(violations_data) + 1
        new_violation_id = f"V{violation_count:03d}" 

        new_violation = {
            "violationId": new_violation_id,
            "reportedBy": reported_by,
            "violator": violator_id,
            "reason": reason
        }
        
        violations_data.append(new_violation)
        save_data("violation.json", {"violations": violations_data})
        print(f"Đã báo cáo vi phạm của người dùng {violator_id} (Lý do: {reason}) thành công.")
        return True

    except Exception as e:
        print(f"Đã xảy ra lỗi khi báo cáo vi phạm: {e}")
        return False