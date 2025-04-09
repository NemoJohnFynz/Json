from .utils import load_data, save_data
from datetime import datetime, timezone
import re 

class User:
        def __init__(self, user_id, full_name, username, password, balance=0, role="player"):
            # ... (existing attributes) ...
            self.user_id = user_id
            self.full_name = full_name
            self.username = username
            self.password = password # Remember to hash!
            self.balance = balance
            self.role = role

        def play_game(self, minutes):
            # ... (existing code) ...
            pass # Placeholder

        def deposit_money(self, amount):
            if amount <= 0:
                print("Số tiền nạp phải lớn hơn 0.")
                return # Don't proceed if amount is invalid

            # 1. Update balance (do this first conceptually)
            self.balance += amount

            # 2. Record the transaction
            try:
                # Load existing transactions (assuming load_data returns the list)
                transactions = load_data("transition.json")
                if not isinstance(transactions, list):
                     # Handle case where load_data didn't return a list as expected
                     print("Lỗi: Dữ liệu giao dịch không hợp lệ. Không thể ghi giao dịch mới.")
                     # Potentially revert balance update or log error severely
                     # For now, just prevent saving transaction
                     print(f"Nạp {amount} VND thành công (NHƯNG KHÔNG GHI LOG GIAO DỊCH). Số dư hiện tại: {self.balance} VND")
                     return

                # Generate new transaction ID
                last_id_num = 0
                for t in transactions:
                    # Use regex to find numbers in transactionId, be flexible
                    match = re.search(r'\d+$', t.get('transactionId', ''))
                    if match:
                        last_id_num = max(last_id_num, int(match.group()))

                new_id_num = last_id_num + 1
                new_transaction_id = f"T{new_id_num:03d}" # Format as T001, T002...

                # Get current timestamp in ISO format (UTC)
                current_timestamp = datetime.now(timezone.utc).isoformat()

                # Create new transaction dictionary
                new_transaction = {
                    "transactionId": new_transaction_id,
                    "userId": self.user_id, # Use user's ID from the object
                    "amount": amount,
                    "type": "deposit",
                    "timestamp": current_timestamp
                }

                # Append to the list
                transactions.append(new_transaction)

                # Save the updated list back to the file
                save_data("transition.json", transactions) # Assumes save_data saves the list directly

                print(f"Nạp thành công {amount} VND. Giao dịch đã được ghi lại. Số dư hiện tại: {self.balance} VND")

            except Exception as e:
                # Catch potential errors during file I/O or processing
                print(f"Đã xảy ra lỗi khi ghi lại giao dịch: {e}")
                # Inform user balance was updated but log failed
                print(f"Nạp {amount} VND thành công (NHƯNG GHI LOG GIAO DỊCH THẤT BẠI). Số dư hiện tại: {self.balance} VND")



# class User:
#     def __init__(self, user_id, full_name, username, password, balance=0, role="player"):
#         self.user_id = user_id
#         self.full_name = full_name
#         self.username = username
#         self.password = password
#         self.balance = balance
#         self.role = role

#     def play_game(self, minutes):
#         cost = minutes * 1000
#         if self.balance >= cost:
#             self.balance -= cost
#             print(f"Bạn đã chơi {minutes} phút. Số dư còn lại: {self.balance} VND")
#         else:
#             print("Không đủ tiền trong tài khoản!")

#     def deposit_money(self, amount):
#         self.balance += amount
#         print(f"Nạp thành công {amount} VND. Số dư hiện tại: {self.balance} VND")