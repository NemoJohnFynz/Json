import sys
import os
import importlib

# Thêm thư mục cha vào sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --- Sử dụng importlib để định nghĩa biến 'main' ---
main = None  # Khởi tạo biến main (quan trọng nếu import thất bại)
try:
    # Nhập module 'class.app' bằng tên dạng chuỗi
    app_module = importlib.import_module("class.app")

    # Lấy thuộc tính 'main' từ module và gán nó trực tiếp vào biến tên là 'main'
    main = getattr(app_module, "main")

except ImportError:
    print(f"Lỗi: Không thể tìm thấy hoặc nhập module 'class.app'.")
    print("Kiểm tra lại cấu trúc thư mục và sự tồn tại của file 'class/app.py'.")
    # Giữ main là None, hoặc có thể thêm sys.exit(1) nếu muốn dừng hẳn
except AttributeError:
    print(f"Lỗi: Module 'class.app' không có thuộc tính 'main'.")
    print("Kiểm tra xem hàm 'main' đã được định nghĩa trong 'class/app.py' chưa.")
    # Giữ main là None, hoặc có thể thêm sys.exit(1)
# --- Kết thúc phần import động ---


# Phần này giờ đây sẽ hoạt động như mong muốn
# nếu việc import ở trên thành công và gán giá trị hợp lệ cho biến 'main'
if __name__ == "__main__":
    if main:  # Kiểm tra xem 'main' có phải là một đối tượng hợp lệ không (không phải None)
        print("Bắt đầu thực thi main...")
        main()
        print("Kết thúc thực thi.")
    else:
        print("Không thể chạy chương trình do lỗi trong quá trình import.")