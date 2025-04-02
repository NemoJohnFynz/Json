import json
from datetime import datetime

def load_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, dict) and "users" in data and isinstance(data["users"], list):
                return data["users"]
            if isinstance(data, dict) and "rooms" in data and isinstance(data["rooms"], list):
                return data["rooms"]
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
        print("Tổng doanh thu hôm nay: 500000 VND")

# Chạy chương trình chính
def main():
    users = load_data("user.json")
    rooms = load_data("room.json")
    trasitions = load_data("trasition.json")
    computers = load_data("computer.json")
    violations = load_data("violation.json")
    
    if not users:
        print("Không có dữ liệu người chơi!")
        return
    if not rooms:
        print("Không có dữ liệu phòng!")
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
                print("---- CHAO MUNG BAN DEN VOI THE GIOI GAME----")
                print("1. Tong thoi gian ban muon choi game")
                print("2. kiem tra so tien trong tai khoan")
                print("3. Nap tien vao tai khoan")
                print("4. Thoát")
                player_choice = input("Lựa chọn: ")
                if player_choice == "1":
                    try:
                        minutes = int(input("Nhập số phút chơi: "))
                        player.play_game(minutes)
                    except ValueError:
                        print("Vui lòng nhập một số nguyên hợp lệ!")
                elif player_choice == "2":
                    print(f"Số tiền trong tài khoản: {player.balance} VND")
                elif player_choice == "3":
                    try:
                        amount = int(input("Nhập số tiền muốn nạp: "))
                        player.deposit_money(amount)
                    except ValueError:
                        print("Vui lòng nhập một số nguyên hợp lệ!")
                elif player_choice == "4":
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
            admin ={
                "user_id": user["userId"],
                "full_name": user["fullName"],
                "username": user["username"],
                "password": user["password"],
                "role": user["role"]
            }
            admin = Admin(**admin)
            print(f"Chào mừng quản trị viên {admin.full_name}!")
            admin.view_revenue()

        elif choice == "4":
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
