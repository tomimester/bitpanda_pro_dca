import http.client
import ast
import yaml
import time

credentials = yaml.load(open('/home/tomi/auth/auth.yml'), Loader=yaml.FullLoader)

api_key = credentials['bitpanda_api']

conn = http.client.HTTPSConnection("api.exchange.bitpanda.com")

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Authorization': "Bearer " + api_key
    }

##################
#GETTING BTC PRICE
##################
conn.request("GET", "/public/v1/order-book/BTC_EUR", headers=headers)
res = conn.getresponse()
data = res.read()
input1 = data.decode("utf-8")
lowest_btc_price = ast.literal_eval(input1)['asks'][3]['price']
print(lowest_btc_price)

####################################
#BUYING BTC FIRST FOR 15 EUROS
####################################
payload = {
    "instrument_code": "BTC_EUR",
    "side": "BUY",
    "price": lowest_btc_price,
    "time_in_force": "GOOD_TILL_CANCELLED",
    "type": "LIMIT",
    "amount": str(format(15/float(lowest_btc_price), '.5f'))
    
}

payload = str(payload)

conn.request("POST", "/public/v1/account/orders", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

time.sleep(5)

####################################
#GETTING REMAINING BALANCE
####################################

conn = http.client.HTTPSConnection("api.exchange.bitpanda.com")

headers = {
    'Accept': "application/json",
    'Authorization': "Bearer " + api_key
    }

conn.request("GET", "/public/v1/account/balances", headers=headers)

res = conn.getresponse()
data = res.read()

input1 = data.decode("utf-8")
balances = ast.literal_eval(input1)['balances']

for i in balances:
    if i['currency_code'] == 'EUR':
        euro_balance = float(i['available'])

print(euro_balance)
##################
#GETTING ETH PRICE
##################

conn.request("GET", "/public/v1/order-book/ETH_EUR", headers=headers)

res = conn.getresponse()
data = res.read()

input1 = data.decode("utf-8")
lowest_eth_price = ast.literal_eval(input1)['asks'][3]['price']

print(lowest_eth_price)

#############################################
#BUYING ETH FIRST FOR THE REST OF THE BALANCE
#############################################
conn = http.client.HTTPSConnection("api.exchange.bitpanda.com")

headers = {
    'Content-Type': "application/json",
    'Accept': "application/json",
    'Authorization': "Bearer " + api_key
    }

if euro_balance < 55:
	payload = {
	    "instrument_code": "ETH_EUR",
	    "side": "BUY",
	    "price": lowest_eth_price,
	    "time_in_force": "GOOD_TILL_CANCELLED",
	    "type": "LIMIT",
	    "amount": str(format((euro_balance-1)/float(lowest_eth_price), '.4f'))
	}
else:
	payload = {
	    "instrument_code": "ETH_EUR",
	    "side": "BUY",
	    "price": lowest_eth_price,
	    "time_in_force": "GOOD_TILL_CANCELLED",
	    "type": "LIMIT",
	    "amount": str(format(35/float(lowest_eth_price), '.4f'))
	}

payload = str(payload)

conn.request("POST", "/public/v1/account/orders", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))