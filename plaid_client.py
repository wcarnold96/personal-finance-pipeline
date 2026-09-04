import plaid
import os
from dotenv import load_dotenv
from plaid.api import plaid_api

load_dotenv()
envs = {"sandbox": plaid.Environment.Sandbox, "production": plaid.Environment.Production}
env = os.getenv("PLAID_ENV")
configuration = plaid.Configuration(
    host = envs[env],
    api_key={
        'clientId': os.getenv("PLAID_CLIENT_ID"),
        'secret' : os.getenv("PLAID_SECRET")
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)
