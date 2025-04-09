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