class AccountLoginDetails:

    def __init__(self, email: str, password: str):
        self.email: str = email
        self.password: str = password

    def __str__(self) -> str:
        return self.email + ", " + self.password

    def __eq__(self, other):
        return self.email == other.email and self.password == other.password