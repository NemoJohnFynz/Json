import json
from datetime import datetime

def load_data(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
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
    def __init__(self, user_id, full_name, username, password, balance):
        self.user_id = user_id
        self.full_name = full_name
        self.username = username
        self.password = password
        self.balance = balance

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

class Employee:
    def __init__(self, user_id, full_name, username, password):
        self.user_id = user_id
        self.full_name = full_name
        self.username = username
        self.password = password

    def report_violation(self, user, reason):
        print(f"Báo cáo vi phạm: {user.full_name} - Lý do: {reason}")

class Admin:
    def __init__(self, user_id, full_name, username, password):
        self.user_id = user_id
        self.full_name = full_name
        self.username = username
        self.password = password

    def view_revenue(self):
        print("Tổng doanh thu hôm nay: 500000 VND")

# Chạy chương trình chính
def main():
    users = load_data("user.json")
    rooms = load_data("room.json")
    
    while True:
        print("--- HỆ THỐNG QUẢN LÝ PHÒNG NET ---")
        print("1. Người chơi")
        print("2. Nhân viên")
        print("3. Quản trị viên")
        print("4. Thoát")
        choice = input("Lựa chọn: ")
        
        if choice == "1":
            username = input("Nhập tên đăng nhập: ")
            user = next((u for u in users if u["username"] == username), None)
            if not user:
                print("Người chơi không tồn tại!")
                continue
            player = User(**user)
            while True:
                print("1. Chơi game")
                print("2. Nạp tiền")
                print("3. Thoát")
                player_choice = input("Lựa chọn: ")
                if player_choice == "1":
                    minutes = int(input("Nhập số phút chơi: "))
                    player.play_game(minutes)
                elif player_choice == "2":
                    amount = int(input("Nhập số tiền muốn nạp: "))
                    player.deposit_money(amount)
                elif player_choice == "3":
                    break
                else:
                    print("Lựa chọn không hợp lệ!")
            
        elif choice == "4":
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
