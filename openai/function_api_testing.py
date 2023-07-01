import openai
import json
import os
openai.api_key = os.getenv('OPENAI_API_KEY')

# Our hardcoded transactions
transactions = [
    {"date": "2023-06-01", "amount": 50.00, "category": "groceries", "vendor": "Supermarket A"},
    {"date": "2023-06-10", "amount": 20.00, "category": "entertainment", "vendor": "Movie Theater"},
    {"date": "2023-06-15", "amount": 75.00, "category": "groceries", "vendor": "Supermarket B"},
    {"date": "2023-06-20", "amount": 120.00, "category": "utilities", "vendor": "Electric Company"},
    {"date": "2023-06-25", "amount": 60.00, "category": "dining", "vendor": "Restaurant C"},
]

# Our function that filters transactions
def get_transactions(**kwargs):
    print(f"get_transactions called ", kwargs)
    results = [t for t in transactions]
    for key, value in kwargs.items():
        results = [t for t in results if str(t.get(key)) == value]
    return results

# The user's question
user_question = input("Enter your question: ")

# Call the OpenAI API
response1 = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {"role": "user", "content": user_question},
    ],
    functions=[
        {
            "name": "get_transactions",
            "description": "Search for transactions based on their properties",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string"},
                    "amount": {"type": "string"},
                    "category": {"type": "string"},
                    "vendor": {"type": "string"},
                },
            },
        },
    ],
)

# If the API has decided to call our function
if 'function_call' in response1['choices'][0]['message']:
    function_call = response1['choices'][0]['message']['function_call']
    function_name = function_call['name']
    function_args = json.loads(function_call['arguments'])

    # Call our function and get the results
    if function_name == 'get_transactions':
        results = get_transactions(**function_args)

        # Send the results back to the API
        response2 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=[
                {"role": "user", "content": user_question},
                {"role": "assistant", "content": None, "function_call": function_call},
                {"role": "function", "name": "get_transactions", "content": json.dumps(results)}
            ],
        )

        # Print the final response
        print(response2['choices'][0]['message']['content'])

# If the API has not decided to call our function, just print the response
else:
    print(response1['choices'][0]['message']['content'])
