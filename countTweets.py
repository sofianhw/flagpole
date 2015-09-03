import argparse
import time
from wiringx86 import GPIOEdison as GPIO
from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager
gpio = GPIO(debug=False)
pin1 = 3
pin2 = 4
pin3 = 5
pin4 = 6
COUNT = 100 # search download batch size

def setup():
        print 'Setting up pin %d' % pin1
        gpio.pinMode(pin1, gpio.OUTPUT)
        print 'Setting up pin %d' % pin2
        gpio.pinMode(pin2, gpio.OUTPUT)
        print 'Setting up pin %d' % pin3
        gpio.pinMode(pin3, gpio.OUTPUT)
        print 'Setting up pin %d' % pin4
        gpio.pinMode(pin4, gpio.OUTPUT)                          
                                                                 
def puter():                                                     
        print "muter"                                            
        for i in range(10):                                     
                gpio.digitalWrite(pin4, gpio.LOW)                
                gpio.digitalWrite(pin2, gpio.HIGH)               
                time.sleep(0.01)                  
                                                  
                gpio.digitalWrite(pin1, gpio.LOW) 
                gpio.digitalWrite(pin3, gpio.HIGH)
                time.sleep(0.01)                  
                                                  
                gpio.digitalWrite(pin2, gpio.LOW) 
                gpio.digitalWrite(pin4, gpio.HIGH)
                time.sleep(0.01)                  
                                                  
                gpio.digitalWrite(pin3, gpio.LOW) 
                gpio.digitalWrite(pin1, gpio.HIGH)
                time.sleep(0.01)                  
                                                  
def count_old_tweets(api, word_list): 
        words = ' OR '.join(word_list)                           
        count = 0                                                
        while True:                                              
                pager = TwitterRestPager(api, 'search/tweets', {'q':words, 'coun
                for item in pager.get_iterator():                               
                        if 'text' in item:                                      
                                count += 1                                      
                                print(count)                                    
                        elif 'message' in item:                                 
                                if item['code'] == 131:                         
                                        continue # ignore internal server error 
                                elif item['code'] == 88:                        
                                        print('Suspend search until %s' % search
                                raise Exception('Message from twitter: %s' % ite
                                                                                
                                                                                
def count_new_tweets(api, word_list):                                           
        words = ','.join(word_list)                                             
        count = 0                                                               
        total_skip = 0                                                          
        while True:                                                             
                skip = 0                                                        
                try:          
                        r = api.request('statuses/filter', {'track':words})     
                        while True:                                             
                                for item in r.get_iterator():                   
                                        if 'text' in item:                      
                                                count += 1                      
                                                puter()                         
                                                print(count + skip + total_skip)
                                        elif 'limit' in item:                   
                                                skip = item['limit'].get('track'
                                                #print('\n\n\n*** Skipping %d tw
                                        elif 'disconnect' in item:              
                                                raise Exception('Disconnect: %s'
                except Exception as e:                                          
                        print('*** MUST RECONNECT %s' % e)                      
                total_skip += skip                                              
                                                                                
                                                                                
if __name__ == '__main__':                                                      
        parser = argparse.ArgumentParser(description='Count occurance of word(s)
        parser.add_argument('-past', action='store_true', help='search historic 
        parser.add_argument('-oauth', metavar='FILENAME', type=str, help='read O
        parser.add_argument('words', metavar='W', type=str, nargs='+', help='wor
        args = parser.parse_args() 
        
        oauth = TwitterOAuth.read_file(args.oauth)                              
        api = TwitterAPI(oauth.consumer_key, oauth.consumer_secret, oauth.access
                                                                                
        try:                                                                    
                setup()                                                         
                if args.past:                                                   
                        count_old_tweets(api, args.words)                       
                else:                                                           
                        count_new_tweets(api, args.words)                       
        except KeyboardInterrupt:                                               
                print('\nTerminated by user\n')                                 
                gpio.digitalWrite(pin1, gpio.LOW)                               
                gpio.digitalWrite(pin2, gpio.LOW)                               
                gpio.digitalWrite(pin3, gpio.LOW)                               
                gpio.digitalWrite(pin4, gpio.LOW)                               
                                                                                
                # Do a general cleanup. Calling this function is not mandatory. 
                gpio.cleanup()                                                  
        except Exception as e:                                                  
                print('*** STOPPED %s\n' % e)  
