""" Sending and recieving money with Dwolla """

import dwollav2 as dw
from pprint import pprint

def send_money(amount):

    with open("secrets.txt") as file:
        secrets = file.read().split(",")

    # Navigate to https://dashboard.dwolla.com/applications (production) or https://dashboard-sandbox.dwolla.com/applications (Sandbox) for your application key and secret.
    app_key = secrets[0]
    app_secret = secrets[1]
    client = dw.Client(key=app_key,
                       secret=app_secret,
                       environment='sandbox')

    app_token = client.Auth.client()

    # Make sure amount is valid
    if type(amount) != str or len(amount) != 4:
        print("Invalid amount")
        return


    request_body = {
        '_links': {
            "self": {
                "href": "https://api-sandbox.dwolla.com/sandbox-simulations",
                "type": "application/vnd.dwolla.v1.hal+json",
                "resource-type": "sandbox-simulation"
            },
            'source': {
                'href': f'https://api-sandbox.dwolla.com/funding-sources/{secrets[2]}'
            },
            'destination': {
                'href': f'https://api-sandbox.dwolla.com/funding-sources/{secrets[3]}'
            }
        },
        'amount': {
            'currency': 'USD',
            'value': amount
        }
    }

    transfer = app_token.post('transfers', request_body)
    return transfer.headers


if __name__ == "__main__":
    amount = input("How much to send? >")
    pprint(send_money(amount))
