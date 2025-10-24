from flask import Blueprint
from src.services.implementation.TransactionService import TransactionService
transactionController = Blueprint('transactionController', url_prefix="/transactions")


transactionController.route('/')
def buy():
    return

transactionController.route('/sell')
def sell():
    return 


transactionController.route('/store')
def view():
    return