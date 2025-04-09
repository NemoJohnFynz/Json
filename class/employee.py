from .user import User

class Employee(User):
    def __init__(self, user_id, full_name, username, password, address, phone, role="employee"):
        super().__init__(user_id, full_name, username, password, role=role)
        self.address = address
        self.phone = phone

    def report_violation(self, user, reason):
        print(f"Báo cáo vi phạm: {user.full_name} - Lý do: {reason}")