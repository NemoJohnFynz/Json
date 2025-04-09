import json
from datetime import datetime
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(CURRENT_DIR, "..", "json")



def load_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
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
                print(f"Dữ liệu trong {filename} không hợp lệ!")
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Không thể tải dữ liệu từ {filename}!")
        return []

def save_data(filename, data):
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        
def get_user_info(user_id, users):
    user = next((u for u in users if u["userId"] == user_id), None)
    if user:
        return user
    return None

# Lớp quản lý máy tính
class Computer:
    def __init__(self, computer_id, monitor, cpu, ram, storage, status):
        self.computer_id = computer_id
        self.monitor = monitor
        self.cpu = cpu
        self.ram = ram
        self.storage = storage
        self.status = status

# Lớp quản lý phòng
class Room:
    def __init__(self, room_id, name, computers):
        self.room_id = room_id
        self.name = name
        self.computers = computers

# Lớp quản lý người chơi
class User:
    def __init__(self, user_id, full_name, username, password, balance=0, role="player"):
        self.user_id = user_id
        self.full_name = full_name
        self.username = username
        self.password = password
        self.balance = balance
        self.role = role

    def play_game(self, minutes):
        cost = minutes * 1000
        if self.balance >= cost:
            self.balance -= cost
            print(f"Bạn đã chơi {minutes} phút. Số dư còn lại: {self.balance} VND")
        else:
            print("Không đủ tiền trong tài khoản!")

    def deposit_money(self, amount):
        self.balance += amount
        print(f"Nạp thành công {amount} VND. Số dư hiện tại: {self.balance} VND")

# Lớp quản lý nhân viên
class Employee(User):
    def __init__(self, user_id, full_name, username, password, address, phone, role="employee"):
        super().__init__(user_id, full_name, username, password, role=role)
        self.address = address
        self.phone = phone

    def report_violation(self, user, reason):
        print(f"Báo cáo vi phạm: {user.full_name} - Lý do: {reason}")

# Lớp quản lý quản trị viên
class Admin(User):
    def __init__(self, user_id, full_name, username, password, role="admin"):
        super().__init__(user_id, full_name, username, password, role=role)

    def view_revenue(self):
        transactions = load_data("transition.json")
        today = datetime.now().date()
        total_revenue = sum(t["amount"] for t in transactions if datetime.fromisoformat(t["timestamp"]).date() == today)
        print(f"Tổng doanh thu hôm nay: {total_revenue} VND")
        
    def view_computer_status(self, computers, status):
        print(f"Danh sách máy tính có trạng thái {status}:")
        for comp in computers:
            if comp["status"] == status:
                print(f"Máy {comp['computerId']}: {comp['cpu']}, {comp['ram']}, {comp['storage']}")
    def view_violations(self, violations, users):
        print("Danh sách vi phạm:")
        for violation in violations:
            violator_info = get_user_info(violation["violator"], users)
            if violator_info:
                print(f"Vi phạm của người dùng {violator_info['fullName']} ({violator_info['username']}) - Lý do: {violation['reason']}")
            else:
                print(f"Không tìm thấy thông tin người dùng với ID {violation['violator']}")
            
    def create_employee_account():
        users = load_data("user.json")
        
        user_id = len(users) + 1
        full_name = input("Nhập họ và tên nhân viên: ")
        username = input("Nhập tên đăng nhập: ")
        password = input("Nhập mật khẩu: ")

        new_employee = {
            "user_id": user_id,
            "full_name": full_name,
            "username": username,
            "password": password,
            "role": "employee"
        }

        users.append(new_employee)
        save_data("user.json", users)
        print("Tạo tài khoản nhân viên thành công!")

    def create_user_account():
        users = load_data("user.json")

        user_id = len(users) + 1
        full_name = input("Nhập họ và tên: ")
        username = input("Nhập tên đăng nhập: ")
        password = input("Nhập mật khẩu: ")
        balance = 0  # Ban đầu số dư = 0

        new_user = {
            "user_id": user_id,
            "full_name": full_name,
            "username": username,
            "password": password,
            "balance": balance,
            "role": "user"
        }

        users.append(new_user)
        save_data("user.json", users)
        print("Tạo tài khoản người chơi thành công!")


# Chạy chương trình chính
def main():
    users = load_data("user.json")
    rooms = load_data("room.json")
    trasitions = load_data("transition.json")
    computers = load_data("computer.json")
    violations = load_data("violation.json")
    
    if not users:
        print("Không có dữ liệu người chơi!")
        return
    if not rooms:
        print("Không có dữ liệu phòng!")
        return
    if not trasitions:
        print("Không có dữ liệu doanh thu!")
        return
    if not computers:
        print("Không có dữ liệu máy tính!")
        return
    if not violations:
        print("Không có dữ liệu vi phạm!")
        return

    while True:
        print("--- HỆ THỐNG QUẢN LÝ PHÒNG NET ---")
        print("1. Người chơi")
        print("2. Nhân viên")
        print("3. Quản trị viên")
        print("4. Thoát")
        choice = input("Lựa chọn: ")
        
        if choice == "1":
            username = input("Nhập tên đăng nhập: ")
            user = next((u for u in users if u.get("username") == username and u.get("role") == "player"), None)
            if not user:
                print("Người chơi không tồn tại!")
                continue
            password = input("Nhập mật khẩu: ")
            if user["password"] != password:
                print("Mật khẩu không chính xác!")
                continue
            # Chuyển đổi camelCase sang snake_case
            user_snake_case = {
                "user_id": user["userId"],
                "full_name": user["fullName"],
                "username": user["username"],
                "password": user["password"],
                "balance": user.get("balance", 0),
                "role": user["role"]
            }
            player = User(**user_snake_case)
            
            while True:
                print("Đăng nhập thành công!!!")
                print("1. Chơi game")
                print("2. Nạp tiền")
                print("3. Thoát")
                player_choice = input("Lựa chọn: ")
                if player_choice == "1":
                    try:
                        minutes = int(input("Nhập số phút chơi: "))
                        player.play_game(minutes)
                    except ValueError:
                        print("Vui lòng nhập một số nguyên hợp lệ!")
                elif player_choice == "2":
                    try:
                        amount = int(input("Nhập số tiền muốn nạp: "))
                        player.deposit_money(amount)
                    except ValueError:
                        print("Vui lòng nhập một số nguyên hợp lệ!")
                elif player_choice == "3":
                    break
                else:
                    print("Lựa chọn không hợp lệ!")
        
        elif choice == "2":
            username = input("Nhập tên đăng nhập: ")
            user = next((u for u in users if u.get("username") == username and u.get("role") == "employee"), None)
            if not user:
                print("Nhân viên không tồn tại!")
                continue
            password = input("Nhập mật khẩu: ")
            if user["password"] != password:
                print("Mật khẩu không chính xác!")
                continue
            employee = {
                "user_id": user["userId"],
                "full_name": user["fullName"],
                "username": user["username"],
                "password": user["password"],
                "address": user["address"],
                "phone": user["phone"],
                "role": user["role"]
            }
            employee = Employee(**employee)
            print(f"Chào mừng nhân viên {employee.full_name}!")

        elif choice == "3":
            username = input("Nhập tên đăng nhập: ")
            user = next((u for u in users if u.get("username") == username and u.get("role") == "admin"), None)
            if not user:
                print("Quản trị viên không tồn tại!")
                continue
            password = input("Nhập mật khẩu: ")
            if user["password"] != password:
                print("Mật khẩu không chính xác!")
                continue
            admin_snake_case ={
                "user_id": user["userId"],
                "full_name": user["fullName"],
                "username": user["username"],
                "password": user["password"],
                "role": user["role"]
            }
            admin = Admin(**admin_snake_case)
            
            while True:
                print("----XIN CHAO ADMIN----")
                print("1. Tong doanh thu trong ngay")
                print("2. Xem tinh trang may")
                print("3. Xem bao cao vi pham")
                print("4. Tạo tài khoản nhân viên")
                print("5. Tạo tài khoản người chơi")
                print("6. Thoat")
                admin_choice = input("Lựa chọn: ")
                if admin_choice == "1":
                    admin.view_revenue()
                elif admin_choice == "2":
                    print("Chọn trạng thái máy cần xem: 1. Đang hoạt động, 2. Đang bảo trì, 3. Đang hư hỏng")
                    status_choice = input("Nhập lựa chọn: ")
                    status_map = {"1": "Đang hoạt động", "2": "Đang bảo trì", "3": "Đang hư hỏng"}
                    status = status_map.get(status_choice, "")
                    if status:
                        admin.view_computer_status(load_data("computer.json"), status)
                    else:
                        print("⚠️ Lựa chọn không hợp lệ!")
                elif admin_choice == "3":
                    admin.view_violations(violations, users)
                elif admin_choice == "4":
                    admin.create_employee_account()
                elif admin_choice == "5":
                    admin.create_user_account()
                elif admin_choice == "6":
                    break
                else:
                    print("⚠️ Lựa chọn không hợp lệ!")

        elif choice == "4":
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
