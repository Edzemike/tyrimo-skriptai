import time
import stomp
import ntplib
import datetime

class MyListener(object):
    def on_error(self, headers, message):
        print 'received an error %s' % message
    def on_message(self, headers, message):
        print 'received a message %s' % message

conn = stomp.Connection(host_and_ports=[('185.80.128.169', 61613)])
conn.set_listener('', MyListener())
conn.start()
conn.connect('edita', 'test', wait=True)
#conn.subscribe('/queue/test', 1)

client_ntp = ntplib.NTPClient()
time_to_stop = time.time() + 60 * 60

conn.send('testtopic', "begin")
while time.time() < time_to_stop:
    try:
        client_ntp = ntplib.NTPClient()
        response = client_ntp.request('0.pool.ntp.org', version=3)
        #ctime(response.tx_time) #converts time to string
        if response:
            conn.send('testtopic', str(datetime.datetime.now()+datetime.timedelta(0,response.offset)))
            print str(datetime.datetime.now()+datetime.timedelta(0,response.offset))
            print "offset: ", response.offset
    except:
        print "ntp connection failed"
        continue
    time.sleep(5)

conn.send("testtopic", "end")
conn.disconnect()
# conn.send("/queue/test", "my message")




