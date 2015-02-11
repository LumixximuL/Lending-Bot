#Bitfinex Lending Account object
#Taylor Webber

import bitfinexAPI
import configure
from urllib2 import urlopen
import json
import file_printer

url = 'https://api.bitfinex.com/v1'
wallet_url = url + '/balances'
lend_url = url + '/lendbook/'
    
class LendingAccount():
    def __init__(self, currency):
        self.currency = currency
        print "Creating Bitfinex trader"
        self.bitfinex_lender = bitfinexAPI.BitfinexLender(configure.bitfinex_key, configure.bitfinex_secret)
        self.updateWallet()
    
    #make authenticated call to wallet balances for an update
    def updateWallet(self):
        output = self.bitfinex_lender.getBalances()
        
        # Uncomment to view JSON output from API   
        #f = open('output_bitfinex_update.json', 'w')
        #f.write(json.dumps(output, indent=4))
        #f.close()
        
        count = 0
        while count < 9:
            if output[count]['type'] == "deposit":
            
                # Uncomment to view JSON output from API   
                #f = open('output_bitfinex_balances.json', 'w')
                #f.write(json.dumps(output, indent=4))
                #f.close()
                
                self.amount_available = float(output[count]['available'])
                #self.currency = output[count]['currency']
                self.total = float(output[count]['amount'])
                count = 10
                
            count += 1
        
    #get rate of lowest posted ask   
    def getRate(self):
        print "Generating competitive rate"
        response = urlopen(lend_url + 'usd')
        json_obj = json.load(response)
        
        # Uncomment to view JSON output from API   
        #f = open('output_bitfinex_rates.json', 'w')
        #f.write(json.dumps(json_obj, indent=4))
        #f.close()
        
        low_rate = float(json_obj['asks'][0]['rate'])
        #to position rate, subtract 0.0365
        self.rate = low_rate - 0.0365
        
        print "Acquired rate"
        
    #make call to new offer to create offer    
    def makeLend(self, tperiod):
        response = self.bitfinex_lender.Lend(configure.currency, str(self.amount_available), str(self.rate), tperiod, "lend")
        
        # Uncomment to view JSON output from API   
        f = open('output_bitfinex_lend.json', 'w')
        f.write(json.dumps(response, indent=4))
        f.close()
        
        #ID of offer completed
        self.offer_id = response['id']
        file_printer.document_trans("Lend", tperiod, configure.currency, self.rate, self.amount_available, self.offer_id)
        
        return response
        
    #check for open offers
    def findOpenOffers(self):
        print "Finding open offers"
        response = self.bitfinex_lender.ActiveOffers()
        
        # Uncomment to view JSON output from API   
        f = open('output_bitfinex_offers.json', 'w')
        f.write(json.dumps(response, indent=4))
        f.close()
        
        empty = []
        
        if (response == empty):
            #Do nothing
            print "No open offers"
        else:
            print "Open offer found"
            self.close_id = response[0]['id']
            self.closeOffer(self.close_id)
        
        
    #close offer
    def closeOffer(self, offer_id):
        print "Canceling open offers"
        cancel_response = self.bitfinex_lender.CancelOffer(offer_id)
    
        # Uncomment to view JSON output from API   
        f = open('output_bitfinex_close_offer.json', 'w')
        f.write(json.dumps(cancel_response, indent=4))
        f.close()
        
        file_printer.document_trans("Cancel", "", configure.currency, "", "", self.close_id)
        
        
