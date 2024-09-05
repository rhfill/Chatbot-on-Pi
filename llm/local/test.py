import json

import requests

def main():
    host_ip = input("Enter host IP: ")
    base_url = f"http://{host_ip}:8000"
    url = f"{base_url}/api/v1/chat"
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
