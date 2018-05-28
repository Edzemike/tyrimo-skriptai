import time
import stomp
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

class MyListener(object):
    def on_error(self, headers, message):
        print 'received an error %s' % message
    def on_message(self, headers, message):
        print 'received a message %s' % message

conn = stomp.Connection(host_and_ports=[('185.80.128.169', 61613)])
conn.set_listener('', MyListener())
conn.start()
conn.connect('edita', 'test', wait=True)


time_to_stop = time.time() + 30 * 60
time_to_sync = time.time() + 1 * 60

print "begin at: ", datetime.datetime.now() + offset
conn.send('testtopic', "begin")
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
        conn.send('testtopic', str(datetime.datetime.now()+offset))
        print str(datetime.datetime.now()+offset)
    except:
        print "failed to send"
    time.sleep(0.5)

conn.send("testtopic", "end")
conn.disconnect()
# conn.send("/queue/test", "my message")
print "ended at: ", datetime.datetime.now() + offset



