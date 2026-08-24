import os
import json
import plaid
from plaid.api import plaid_api
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode

from dotenv import load_dotenv

from flask import Flask, jsonify, request, render_template
app = Flask(__name__)

load_dotenv()
access_token = None
item_id = None
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': os.getenv("PLAID_CLIENT_ID"),
        'secret' : os.getenv("PLAID_SECRET")
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)
  
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_link_token", methods=['POST'])
def create_link_token():
    # Get the client_user_id by searching for the current user
    user_id = "Caleb"
    # Create a link_token for the given user
    request = LinkTokenCreateRequest(
            products=[Products("auth")],
            client_name="Plaid Test App",
            country_codes=[CountryCode('US')],
            language='en',
            user=LinkTokenCreateRequestUser(
                client_user_id=user_id
            )
        )
    response = client.link_token_create(request)

    # Send the data to the client
    return jsonify(response.to_dict())


@app.route("/exchange_public_token", methods=['POST'])
def exchange_public_token():
    global access_token
    exchange_request = ItemPublicTokenExchangeRequest(
            public_token = request.get_json()['public_token']
    )
    
    institution = request.get_json()['institution']

    exchange_response = client.item_public_token_exchange(exchange_request)
    
    # These values should be saved to a persistent database and
    # associated with the currently signed-in user
    access_token = exchange_response['access_token']
    item_id = exchange_response['item_id']
    print(exchange_response, institution)
    log_token_locally(institution, access_token, item_id)
    return jsonify({'public_token_exchange': 'complete'})


def log_token_locally(institution, access_token, item_id):
    try:
        with open("tokens.json", "r") as f:
            data = json.load(f)
    except:
        data = {}
        
    data[item_id] = {'institution': institution, 'access_token': access_token, 'cursor': None}
    
    with open("tokens.json", "w") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    print(app.url_map)
    app.run(debug=True, port=5000)
