import paho.mqtt.client as paho
import time
import ntplib
import datetime

client_ntp = ntplib.NTPClient()
diff = None

broker_address= "185.80.128.169"  #Broker address
port = 8883                         #Broker port
user = "ed_test"                    #Connection username
password = "ed_test_01"            #Connection password
 
client = paho.Client("Python")               #create new instance
client.username_pw_set(user, password=password)    #set username and password

 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()

time_to_stop = time.time() + 60 * 60

client.publish("testtopic", "begin")
while time.time() < time_to_stop:
    try:
        client_ntp = ntplib.NTPClient()
        response = client_ntp.request('0.pool.ntp.org', version=3)
        if response:
            client.publish("testtopic", str(datetime.datetime.now()+datetime.timedelta(0,response.offset)))
        print "sent", str(datetime.datetime.now()+datetime.timedelta(0,response.offset))
    except:
        print "ntp connection failed"
        continue
    time.sleep(5)

client.publish("testtopic", "end")
client.loop_stop()
client.disconnect()
