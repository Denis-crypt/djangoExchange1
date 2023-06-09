import json
import time

from binance.client import Client

api_key = 'mU0tXd9sLQS4vPHEwFFkn3w8j2F0Ln9Q4qKGdor7lDCfPbTXKbgiCPEZAs2EuG0Z'
api_secret = 'cCzulCgOb24XCnFrE8Wmm1S3i2swkMXN2v4d5EMUxbkY8hloSHyfhtHKzSBSppvG'

client = Client(api_key, api_secret)

print(client.futures_account_balance())
