
class Transaction:
    """
   The Transaction class is used to represent a financial transaction.

   Attributes
   ----------
   account_id : str
       The unique identifier of the account associated with the transaction.
       Example: "EQbbLWQvbjU4RoRqNg8ESVMQ4J9ygjugLmrBq"

   amount : float
       The amount of the transaction.
       Example: 12.0

   date : str
       The date of the transaction.
       Example: "2023-06-26"

   name : str
       The name or description of the transaction.
       Example: "McDonald's"

   merchant_name : str
       The name of the merchant involved in the transaction.
       Example: "McDonald's"

   category_detailed : str
       The detailed category of the transaction.
       Example: "FOOD_AND_DRINK_FAST_FOOD"

   category_primary : str
       The primary category of the transaction.
       Example: "FOOD_AND_DRINK"
   """
    def __init__(self, account_id: str, amount: float, date: str, name: str, merchant_name: str, category_detailed: str, category_primary: str):
        self.account_id = account_id
        self.amount = amount
        self.date = date
        self.name = name
        self.category_detailed = category_detailed
        self.category_primary = category_primary
        self.merchant_name = merchant_name
