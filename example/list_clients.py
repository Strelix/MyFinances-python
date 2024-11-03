import json

from myfinances import MyFinancesClient
import pprint

def main():
    client = MyFinancesClient(api_key=input("API KEY: "), base_url="http://127.0.0.1:8000/api/public")

    response = client.clients.list_clients()
    print(response.json())

    response = client.clients.create_client(name="nerd")

    print(f"Created user with the ID of {response.data.client_id}")

    print(response.json())
    #
    response = client.clients.list_clients()
    print(response.json())

if __name__ == "__main__":
    main()