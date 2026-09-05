from decimal import Decimal
from typing import Optional

from .cfg import bnb_node

from aiomysql import Pool

import aiohttp

headers = {
    'Content-Type': 'application/json'
}
    
async def processing_bnb(
    u_row: str,
    pl: Pool
    ) -> Optional[dict]:
    json = {
        "jsonrpc":"2.0",
        "method": 'eth_blockNumber',
        "params": [],
        "id":1
        }
    
    async with aiohttp.ClientSession(
        headers=headers
        ) as ssn:
        try:
            async with ssn.post(
                url=bnb_node,
                json=json
                ) as rspc:
                if rspc.status == 200:
                    data = await rspc.json()
                    if 'result' in data:
                        num_block = data['result']
                    else:
                        return None
                else:
                    raise aiohttp.ServerConnectionError(
                        f'Server returned an incorrect response.'
                        f'Try it later.'
                    )
        except aiohttp.ServerConnectionError as error:
            print(
                f'Server is not responding. {error}'
                )
            return None

        req_block = {
            "jsonrpc": "2.0",
            "method": 'eth_getBlockByNumber',
            "params": [num_block, True],
            "id": 1
            }
        
        try:
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
                    raise aiohttp.ServerConnectionError(
                        f'An error occured while requesting a block.'
                        f'Try it later.'
                    )
        except aiohttp.ServerConnectionError as error:
            print(
                f'Server is not responding. {error}'
                )
            return None
    if isinstance(result, dict):
        if 'transactions' in result:
            trxns = result['transactions']
            for trxn in trxns:
                if 'to' in trxn:
                    _to = trxn['to']                        
                    if _to.lower() == u_row.lower():
                        _to = 'Received'
                    else:
                        _to = None
                if 'from' in trxn:
                    _from = trxn['from']  
                    if _from.lower() == u_row.lower():
                        _from = 'Sent'
                    else:
                        _from = None
                if _to is None and _from is None:
                    continue
                else:
                    if 'hash' in trxn:
                        _hash = trxn['hash']
                        if 'value' in trxn:
                            pre_value = trxn['value']
                            pre_amount_tx = int(pre_value, 16)
                            value_tx = Decimal(pre_amount_tx) / Decimal(10**18)
                            
                            return {
                                'to': _to,
                                'from': _from,
                                'hash': _hash,
                                'value': value_tx
                            }
