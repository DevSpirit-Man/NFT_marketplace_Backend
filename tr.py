import requests
import json

url = "https://opt-goerli.g.alchemy.com/v2/q_d_3EQ2efRDKPvIw9vouYxYtK4qiQQe"
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}
payload = {
    "id": 0,
    "jsonrpc": "2.0",
    "method": "eth_newFilter",
    "params": [
         {
            "fromBlock": "safe",
            "toBlock": "latest"
        }
    ]
}

response = requests.post(url, json=payload, headers=headers)
r_json = json.loads(response.text)
filter_id = r_json["result"]

print(filter_id,'..')
payload2 = {
    "id": 0,
    "jsonrpc": "2.0",
    "params": [filter_id],
    "method": "eth_getFilterLogs"
}

response2 = requests.post(url, json=payload2, headers=headers)
r_json2 = json.loads(response2.text)
print(r_json2)