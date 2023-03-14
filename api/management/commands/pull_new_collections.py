import json

import requests
from api.models import BlockchainState
from api.utils.constants import ALCHEMY_URL, w3
from api.utils.contract_utils import get_or_create_contract
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Pull new contracts"

    def handle(self, *args, **kwargs):
        block, _created = BlockchainState.objects.get_or_create(
            key="collection_filter_block"
        )
        if _created:
            block.value = "0x1"
            block.save()

        print(block.value,'value')
        data = {
            "jsonrpc": "2.0",
            "method": "eth_newFilter",
            "params":[{
                "fromBlock": "earliest",
                "toBlock": "latest"
            }],
            "id": 1
        }

        r = requests.post(ALCHEMY_URL, json=data)
        r_json = json.loads(r.text)

        filter_id = r_json["result"]

        data2 = {
            "jsonrpc": "2.0",
            "method": "eth_getFilterLogs",
            "params": [filter_id],
            "id": 1,
        }
        r = requests.post(ALCHEMY_URL, json=data2)
        r_json = json.loads(r.text)

        print(r_json,'.rjson')
        if "result" in r_json:
            for log in r_json["result"]:
                try:
                    address = log["address"]
                except Exception:
                    return
                get_or_create_contract(address=address)

            # block.value = hex(w3.eth.block_number)
            # block.save()
