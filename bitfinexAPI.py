#Bitfinex account and trade
#Taylor Webber

import configure
import requests
import json
import base64
import hashlib
import time
import httplib
import urllib
import hmac

url = 'https://api.bitfinex.com'

class BitfinexLender:
    __api_key	= '';
    __api_secret	= '';
    __nonce_v	= 1;
    __wait_for_nonce = False

    def __init__(self,api_key,api_secret,wait_for_nonce=False):
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__wait_for_nonce = wait_for_nonce

    def __nonce(self):
        time.sleep(1)
        self.__nonce_v = str(time.time()).split('.')[0]

    def __signature(self, payload):
        m = hmac.new(self.__api_secret, payload, hashlib.sha384)
        m = m.hexdigest()
        return m

    def __api_call(self,request,params):
        self.__nonce()
        params['request'] = request
        params['nonce'] = str(self.__nonce_v)
        
        payload_json = json.dumps(params)
        #print payload_json
 
        payload = str(base64.b64encode(payload_json))
        #print payload
        
        headers = {
           'X-BFX-APIKEY' : self.__api_key,
           'X-BFX-PAYLOAD' : base64.b64encode(payload_json),
           'X-BFX-SIGNATURE' : self.__signature(payload)
           }
        
        call_url = url + request   
        r = requests.post(call_url, data={}, headers=headers)
        
        data = r.json()
        
        return data
 
    def getBalances(self):
        params = {
            'options':{}
            }
        return self.__api_call('/v1/balances', params)

    def TradeHistory(self, tpair, ttime):
        params = {
                "symbol"	: tpair,
                "timestamp"	: ttime
                }
        return self.__api_call('/v1/mytrades', params)
 
    def BalanceHistory(self, tcurrency):
        params = {
                "currency": tcurrency
            }
        return self.__api_call('/v1/history', params)

    def ActiveOrders(self):
        params = {
            'options': {}
            }
        return self.__api_call('/v1/orders', params)

    def Trade(self, tpair, tamount, tprice, tside, ttype):
        params = {
                "symbol": tpair,
                "amount": tamount,
                "price"	: tprice,
                "exchange": 'bitfinex',
                "side": tside,
                "type": ttype
                }
        return self.__api_call('/v1/order/new', params)
    
    def OrderStatus(self, torder_id):
        params = { 
                "order_id" : torder_id
            }
        return self.__api_call('/v1/order/status', params)
        
    def CancelOrder(self, torder_id):
        params = { 
                "order_id" : torder_id
            }
        return self.__api_call('/v1/order/cancel', params)
        
    def Lend(self, tcurrency, tamount, trate, tperiod, tdirection):
        params = {
                "currency": tcurrency,
                "amount": tamount,
                "rate"	: trate,
                "period": tperiod,
                "direction": tdirection
                }
        return self.__api_call('/v1/offer/new', params)

    def CancelOffer(self, toffer_id):
        params = { 
                "offer_id" : toffer_id
            }
        return self.__api_call('/v1/offer/cancel', params)
        
    def ActiveOffers(self):
        params = {
            'options': {}
            }
        return self.__api_call('/v1/offers', params)
    
    def ActiveCredits(self):
        params = {
            'options': {}
            }
        return self.__api_call('/v1/credits', params)