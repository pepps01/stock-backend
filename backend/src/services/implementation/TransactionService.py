from src.repositories.TransactionRepository import TransactionRepository

transactionRepository = TransactionRepository()

class TransactionService:
    def __init__(self):
        self.transactionRepostory =  transactionRepository
    
    def get_single_transactions(self):
        self.transactionRepository.get_all()

    def get_transactions(self):
        self.transactionRepository.get_one()