from .user import User
from .utils import load_data, save_data, get_user_info
from datetime import datetime

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

    def create_employee_account(self):
        users = load_data("user.json")
        user_id = len(users) + 1
        full_name = input("Nhập họ và tên nhân viên: ")
        username = input("Nhập tên đăng nhập: ")
        password = input("Nhập mật khẩu: ")

        new_employee = {
            "userId": user_id,
            "fullName": full_name,
            "username": username,
            "password": password,
            "role": "employee"
        }

        users.append(new_employee)
        save_data("user.json", users)
        print("Tạo tài khoản nhân viên thành công!")

    def create_user_account(self):
        users = load_data("user.json")
        user_id = len(users) + 1
        full_name = input("Nhập họ và tên: ")
        username = input("Nhập tên đăng nhập: ")
        password = input("Nhập mật khẩu: ")
        balance = 0

        new_user = {
            "userId": user_id,
            "fullName": full_name,
            "username": username,
            "password": password,
            "balance": balance,
            "role": "user"
        }

        users.append(new_user)
        save_data("user.json", users)
        print("Tạo tài khoản người chơi thành công!")