import requests
import random
import web3
import zlib
import json


# load configs
conf = json.load(open("../config.json", "r"))
api_schema = json.load(open("block_cypher_schema.json", "r"))
w3 = web3.Web3(web3.HTTPProvider("https://ropsten.infura.io/v3/bfd4ab3b863846d2baf879c8f4cad664"))
nonce = 0


# set live vs testing variables
if conf["live"]:
    base_url = api_schema["base_url"]
    routes = api_schema["routes"]["main"]
else:
    base_url = api_schema["alt_base_url"]
    routes = api_schema["routes"]["test"]


# everything else
def send_str_msg(msg, to, pub_addr, priv_key):
    global nonce
    msg_obj = {
        "msg": msg,
        "to": to
    }
    msg_string = json.dumps(msg_obj)
    msg_bytes = zlib.compress(msg_string.encode("utf-8"))
    tx_obj = w3.eth.account.signTransaction({
        "nonce": nonce,
        "gas": 90000,
        "gasPrice": w3.eth.gasPrice,
        "from": pub_addr,
        "to": conf["hub"],
        "data": msg_bytes,
    }, priv_key).rawTransaction
    url = base_url + routes["routes"]["txs"]["routes"]["push"]["extension"]
    body = {
        "tx": tx_obj.hex()[2:]
    }
    resp = requests.post(url=url, json=body)
    print(resp.text)
    nonce += 1


def get_testing_key_pair():
    return requests.post(url=(base_url + routes["routes"]["addrs"]["extension"]), json=None).json()


keys = get_testing_key_pair()
print(keys)
send_str_msg(
    "this is my dumb message. this is my very dumb message. this is my super dumb message.",
    "0xd9BF0233BfB105b9A32352203c277912D828ab7E",
    w3.toChecksumAddress(keys["address"]),
    keys["private"]
)
