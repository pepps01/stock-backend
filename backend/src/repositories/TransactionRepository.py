from src.databases.models.Transaction import Transaction

transaction = Transaction()

class TransactionRepository:
    def __init__(self):
        pass

    def get_all(self):
        return transaction.query.all()

    def get_transactions(self):
        pass

    def create_transactions(self):
        pass

    def update_transactions(self):
        pass