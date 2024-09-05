import json

import requests

base_url = "http://localhost:8000"

url = f"{base_url}/api/v1/query"
def main():
    while True:
        query = input("Query: ")
        payload = {
            "query": query
        }
        resp = requests.post(url,json=payload)
        data = json.loads(resp.content.decode('utf-8'))
        print(resp.status_code,data)

if __name__ == "__main__":
    main()
