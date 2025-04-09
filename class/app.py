from .utils import load_data
from .user import User
from .employee import Employee
from .admin import Admin

def main():
    users = load_data("user.json")
    rooms = load_data("room.json")
    transitions = load_data("transition.json")
    computers = load_data("computer.json")
    violations = load_data("violation.json")
    
    if not users:
        print("Không có dữ liệu người chơi!")
        return
    if not rooms:
        print("Không có dữ liệu phòng!")
        return
    if not transitions:
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
            admin_snake_case = {
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