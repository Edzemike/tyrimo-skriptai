import paho.mqtt.client as paho
import time
import ntplib
import datetime

offset = None
while offset==None:
    try:
        client_ntp = ntplib.NTPClient()
        response = client_ntp.request('0.pool.ntp.org', version=3)
        offset = datetime.timedelta(0,response.offset)
        print "laiko sikrtumas: ", offset
    except:
        print "ntp connection failed"
        
broker_address= "185.80.128.169"  #Broker address
port = 8883                         #Broker port
user = "ed_test"                    #Connection username
password = "ed_test_01"            #Connection password
 
client = paho.Client("Python")               #create new instance
client.username_pw_set(user, password=password)    #set username and password

 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()

time_to_stop = time.time() + 30 * 60
time_to_sync = time.time() + 1 * 60

print "begin at: ", datetime.datetime.now() + offset
client.publish("testtopic", "begin")
while time.time() < time_to_stop:
    if time.time() > time_to_sync:
        time_to_sync = time.time() + 1 * 60
        try:
            client_ntp = ntplib.NTPClient()
            response = client_ntp.request('0.pool.ntp.org', version=3)
            offset = datetime.timedelta(0,response.offset)
            print offset
        except:
            print "ntp connection failed"
    try:
        client.publish("testtopic", str(datetime.datetime.now()+offset))
        print "sent"
    except:
        print "failed to publish"
    time.sleep(0.5)

client.publish("testtopic", "end")
client.loop_stop()
client.disconnect()

print "ended at: ", datetime.datetime.now() + offset
