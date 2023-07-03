import json
from datetime import datetime

import plaid
from plaid.api import plaid_api
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from plaid.model.transactions_get_response import TransactionsGetResponse


class PlaidService:
    def __init__(self):
        client_id = "jason"
        secret = "jason"
        self.access_token = "access-sandbox-6e3fdd93-0897-4891-9ba7-381b9affa567"

        # Set your environment: 'Production', 'Development', or 'Sandbox'
        self.environment = 'Sandbox' # Change this to the appropriate environment

        # Create a PlaidApi object
        configuration = plaid.Configuration(
            host=plaid.Environment.__dict__[self.environment],
            api_key={
                'clientId': client_id,
                'secret': secret,
            }
        )

        # Create a client object
        api_client = plaid.ApiClient(configuration)
        self.client = plaid_api.PlaidApi(api_client)

    def get_transactions(self) -> TransactionsGetResponse:
        date_format = "%m/%d/%Y"
        # Create a request to retrieve transactions
        request = TransactionsGetRequest(
            access_token=self.access_token,
            start_date=datetime.strptime("04/01/2023", date_format).date(),
            end_date=datetime.strptime("7/01/2023", date_format).date(),
            options=TransactionsGetRequestOptions(include_personal_finance_category=True)
        )

        try:
            # Call the Plaid API
            response = self.client.transactions_get(request)
            # Convert the response to JSON
            # json_string = json.dumps(response.to_dict(), default=str)
            # print(json_string)
            return response

        except plaid.ApiException as e:
            response = json.loads(e.body)
            print(f"Error: {response['error_code']}")
            raise
