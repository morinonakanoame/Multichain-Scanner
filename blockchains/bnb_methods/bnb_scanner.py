from decimal import Decimal
from typing import Optional

from .cfg import bnb_node

import aiohttp

headers = {
    'Content-Type': 'application/json'
}
    
async def process_bnb_scan(
    u_row: str
    ) -> Optional[dict]:
    
    req_block_number = {
        "jsonrpc":"2.0",
        "method": 'eth_blockNumber',
        "params": [],
        "id":1
        }
    async with aiohttp.ClientSession(
            headers=headers
            ) as ssn:
        async with ssn.post(
            url=bnb_node,
            json=req_block_number
            ) as rspc:
            if rspc.status == 200:
                data = await rspc.json()
                if 'result' in data:
                    num_block = data['result']
                else:
                    return None
            else:
                raise aiohttp.ServerConnectionError()
        
        req_block = {
            "jsonrpc": "2.0",
            "method": 'eth_getBlockByNumber',
            "params": [num_block, True],
            "id": 1
            }
        async with ssn.post(
            url=bnb_node,
            json=req_block
            ) as rspc:
            if rspc.status == 200:
                block = await rspc.json()
                if 'result' in block:
                    result = block['result']
                else:
                    return None
            else:
                raise aiohttp.ServerConnectionError()

            if isinstance(result, dict):
                if 'transactions' in result:
                    transactions = result['transactions']
                    for transaction in transactions:
                        if 'to' in transaction:
                            _to = transaction['to']                        
                            if _to.lower() == u_row.lower():
                                _to = 'Received'
                            else:
                                _to = None
                        if 'from' in transaction:
                            _from = transaction['from']  
                            if _from.lower() == u_row.lower():
                                _from = 'Sent'
                            else:
                                _from = None
                            
                        if _to is None and _from is None:
                            continue
                        else:
                            if 'hash' in transaction:
                                _hash = transaction['hash']
                                if 'value' in transaction:
                                    pre_value = transaction['value']
                                    pre_amount_tx = int(pre_value, 16)
                                    value_tx = Decimal(pre_amount_tx) / Decimal(10**18)
                                    
                                    return {
                                        'to': _to,
                                        'from': _from,
                                        'hash': _hash,
                                        'value': value_tx
                                    }
