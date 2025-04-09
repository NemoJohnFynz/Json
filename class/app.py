from .utils import load_data, save_data, get_user_info, update_computer_status, report_violation
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
        
        elif choice == "2": # Xử lý đăng nhập NHÂN VIÊN
            username = input("Nhập tên đăng nhập: ")
            user_dict = next((u for u in users if u.get("username") == username and u.get("role") == "employee"), None)

            if not user_dict:
                print("Nhân viên không tồn tại!")
                continue
            password = input("Nhập mật khẩu: ")
            # !!! Nhắc lại: Cần thay thế bằng kiểm tra hash mật khẩu !!!
            if user_dict["password"] != password:
                print("Mật khẩu không chính xác!")
                continue

            try:
                # Tạo đối tượng Employee
                employee_data = {
                    "user_id": user_dict["userId"],
                    "full_name": user_dict["fullName"],
                    "username": user_dict["username"],
                    "password": user_dict["password"],
                    "address": user_dict["address"],
                    "phone": user_dict["phone"],
                    "role": user_dict["role"]
                }
                employee = Employee(**employee_data)

                # ----- Hiển thị lời chào theo yêu cầu -----
                print(f"\n----XIN CHAO NHAN VIEN {employee.full_name.upper()}----")
                # ------------------------------------------

                # ----- BẮT ĐẦU VÒNG LẶP MENU CỦA NHÂN VIÊN -----
                while True:
                    # ----- Hiển thị menu theo yêu cầu -----
                    # Thêm khoảng trắng giữa các lựa chọn cho dễ nhìn hơn một chút
                    print("\n1. Bao cao tinh trang may")
                    print("2. Bao cao vi pham")
                    print("3. Thoat")
                    employee_choice = input("Lua chon: ")
                    # ---------------------------------------

                    if employee_choice == "1":
                        # --- Chức năng 1: Báo cáo tình trạng máy (THEO SỐ PHÒNG, SỐ MÁY) ---
                        print("\n-- Báo cáo tình trạng máy --")
                        room_id_input = input("Nhập số phòng/ID phòng: ")
                        computer_num_input = input("Nhập số thứ tự máy trong phòng: ")

                        # --- Tìm computerId dựa trên roomId và computerNumber ---
                        target_computer_id = None
                        try:
                            # Tải lại computers mỗi lần để đảm bảo dữ liệu mới nhất
                            # Hoặc bạn có thể truyền biến 'computers' vào nếu muốn tối ưu
                            current_computers = load_data("computer.json")
                            if not isinstance(current_computers, list):
                                print("Lỗi: Không thể tải hoặc dữ liệu máy tính không hợp lệ.")
                                continue # Quay lại menu nhân viên

                            for comp in current_computers:
                                # Giả định key là "roomId" và "computerNumber". Sửa nếu cần.
                                # So sánh dạng chuỗi để linh hoạt
                                if str(comp.get("roomId")) == room_id_input and str(comp.get("computerId")) == computer_num_input:
                                    target_computer_id = comp.get("computerId")
                                    break

                            if target_computer_id is None:
                                print(f"Lỗi: Không tìm thấy máy tính số {computer_num_input} trong phòng {room_id_input}.")
                                continue # Quay lại menu nhân viên

                        except Exception as e:
                            print(f"Lỗi khi tìm kiếm máy tính: {e}")
                            continue # Quay lại menu nhân viên

                        print("Chọn trạng thái mới:")
                        print("  1. Đang hoạt động")
                        print("  2. Đang bảo trì")
                        print("  3. Đang hư hỏng")
                        status_choice = input("Nhập lựa chọn trạng thái (1-3): ")
                        status_map = {"1": "Đang hoạt động", "2": "Đang bảo trì", "3": "Đang hư hỏng"}
                        new_status = status_map.get(status_choice)

                        if new_status and target_computer_id:
                            # Gọi phương thức với computerId đã tìm được
                            success = update_computer_status(target_computer_id, new_status)
                            print(f"Trạng thái máy tính {target_computer_id} đã được cập nhật thành '{new_status}'.")
                        elif not new_status:
                            print("⚠️ Lựa chọn trạng thái không hợp lệ!")
                        # (Trường hợp không tìm thấy target_computer_id đã được xử lý ở trên)


                    elif employee_choice == "2":
                        print("\n-- Báo cáo vi phạm --")
                        violator_username_input = input("Nhập tên đăng nhập của người dùng vi phạm: ")
                        reason_input = input("Nhập lý do/hành vi vi phạm: ")

                        violator = next((u for u in users if u.get("username") == violator_username_input), None)
                        if not violator:
                            print(f"Lỗi: Không tìm thấy người dùng với tên đăng nhập '{violator_username_input}'.")
                            continue

                        success = report_violation(employee.user_id, violator["userId"], reason_input)
                        if not success:
                            print("Báo cáo vi phạm thất bại.")

                    elif employee_choice == "3":
                        print(f"\nNhân viên {employee.full_name} đã đăng xuất.")
                        break # Thoát khỏi vòng lặp menu nhân viên

                    else:
                        print("⚠️ Lựa chọn không hợp lệ! Vui lòng chọn lại.")

            except KeyError as e:
                print(f"\nLỗi Dữ Liệu: Không tìm thấy thông tin cần thiết ({e}) cho nhân viên '{username}'.")
                print("Vui lòng kiểm tra file user.json hoặc đảm bảo tài khoản nhân viên được tạo đầy đủ.")
            except Exception as e:
                print(f"\nĐã xảy ra lỗi không mong muốn khi xử lý cho nhân viên: {e}")

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