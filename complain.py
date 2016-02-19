#!/usr/bin/python
import os
import sys
import csv
import datetime
import time
import twitter
 
def test():
 
       
        print 'running test'
        a = os.popen("python /home/pi/speedtest-cli --simple").read()
        print 'ran'
        #split the 3 line result (ping,down,up)
        lines = a.split('\n')
        print a
        ts = time.time()
        date =datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        #if speedtest could not connect set the speeds to 0
        if "Cannot" in a:
                p = 100
                d = 0
                u = 0
        #extract the values for ping down and up values
        else:
                p = lines[0][6:11]
                d = lines[1][10:14]
                u = lines[2][8:12]
        print date,p, d, u
        #save the data to file for local network plotting
        out_file = open('/var/www/assets/data.csv', 'a')
        writer = csv.writer(out_file)
        writer.writerow((ts*1000,p,d,u))
        out_file.close()
 
        #connect to twitter
        TOKEN="[TOKEN_CODE_HERE]"
        TOKEN_KEY="[TOKEN_PASS_HERE]"
        CON_SEC="[CONSUMER_CODE_HERE]"
        CON_SEC_KEY"[CONSUMER_PASS_HERE]"

        my_auth = twitter.OAuth(TOKEN,TOKEN_KEY,CON_SEC,CON_SEC_KEY)
        twit = twitter.Twitter(auth=my_auth)
 
        #try to tweet if speedtest couldnt even connet. Probably wont work if the internet is down
        if "Cannot" in a:
                try:
                        tweet="Hey @bsnlbroadband @BSNLCorporate why is my internet down? I pay for BBG Speed ULD 991 CS78, with 8Mbps down in Faridabad, Haryana. #BSNLwoes #BSNL"
                        twit.statuses.update(status=tweet)
                except:
                        pass
 
        # tweet if down speed is less than whatever I set. Here it is 8Mbps.
        elif eval(d)<8:
                print "trying to tweet"
                try:
                        # Write the twitter message. Make sure it's less than 140 characters long.
                        #You can post more than one tweet each time. Make sure not to break twitter API terms.
                        tweet="Hey @bsnlbroadband @BSNLCorporate why is my internet " + str(d) + "down\\" + str(u) + "up, when I pay for 8Mbps down in #Faridabad? @TelecomTalk @traigov999"
                        #tweet2=
                        #tweet3= 
                        
                        twit.statuses.update(status=tweet)
                        #twit.statuses.update(status=tweet2)
                        #twit.statuses.update(status=tweet2)
                        
                except Exception,e:
                        print str(e)
                        pass
        return
       
if __name__ == '__main__':
        test()
        print 'completed'

