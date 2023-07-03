import io
from typing import List
import csv
from plaid.model.transactions_get_response import TransactionsGetResponse as PlaidTransactionsGetResponse
from plaid.model.transaction import Transaction as PlaidTransaction

from models.Transaction import Transaction
from services.plaid_service import PlaidService


class FinancialDataService:
    def __init__(self):
        self.hello = 'hello'
        self.plaid_service = PlaidService()

    def get_transactions(self) -> List[Transaction]:
        plaid_get_transactions_response = self.plaid_service.get_transactions()
        domain_transactions = convert_to_domain_transactions(plaid_get_transactions_response)
        return domain_transactions


def convert_to_domain_transactions(plaid_get_transactions_result: PlaidTransactionsGetResponse) -> List[Transaction]:
    plaid_transactions = plaid_get_transactions_result.transactions
    domain_transactions = list(
        map(lambda plaid_transaction: convert_plaid_transaction_to_domain_transaction(plaid_transaction),
            plaid_transactions))
    return domain_transactions


def convert_plaid_transaction_to_domain_transaction(plaid_transaction: PlaidTransaction) -> Transaction:
    # print(f"plaid_transaction.personal_finance_category is: {plaid_transaction.personal_finance_category}")
    return Transaction(
        account_id=plaid_transaction.account_id,
        amount=plaid_transaction.amount,
        date=plaid_transaction.date,
        name=plaid_transaction.name,
        merchant_name=plaid_transaction.merchant_name,
        category_primary=plaid_transaction.personal_finance_category.primary if plaid_transaction.personal_finance_category else None,
        category_detailed=plaid_transaction.personal_finance_category.detailed if plaid_transaction.personal_finance_category else None,
    )


def convert_to_csv(domain_transactions: List[Transaction]) -> str:
    """
    Convert a list of transactions to csv format, which is nice for sending to ChatGPT in a somewhat compressed format which it understands.
    :param domain_transactions:
    :return:
    """
    fieldnames = ["amount", "date", "name", "merchant_name", "category_detailed", "category_primary"]

    with io.StringIO() as csv_string:
        writer = csv.DictWriter(csv_string, fieldnames=fieldnames)
        writer.writeheader()
        for transaction in domain_transactions:
            transaction_dict = vars(transaction)
            transaction_dict.pop("account_id", None) # Exclude account_id, otherwise you get: ValueError: dict contains fields not in fieldnames: 'account_id'
            writer.writerow(vars(transaction))

        return csv_string.getvalue()
