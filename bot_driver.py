#Lending Bot Driver
#Taylor Webber

import time
import lending_account
import configure

#main function stub
def main():
    
    LendAcc = lending_account.LendingAccount(configure.currency)
    check = True
    times_run = 0
    lends_made = 0
    
    while check == True:
        #Implement check and cancel of open orders
        #LendAcc.findOpenOffers()
        print "Waiting..."
        time.sleep(5)
    
        #Uncomment these lines of code once app goes live
        if LendAcc.amount_available >= configure.lend_min:
            print "Amount available above minimun"
            LendAcc.getRate()
            response = LendAcc.makeLend(configure.days)
            #uncomment and delete line beneath when done testing
            #times_run = 0
            times_run += .5
            print "Lend posted"
            lends_made += 1
        else:
            print "No available currency to lend"
        
        LendAcc.updateWallet()
        times_run += 1
        print "Checked ", times_run, " times"
        print "Last check ", time.strftime("%a, %d %b %Y %H:%M:%S    ", time.localtime())
        #wait 60 minutes for next check (3600)
        print "Waiting..."
        time.sleep(5)
        
        if times_run >= 2:
            break;
        
    
# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
  main()