import socket
import json
import time

s = socket.create_connection(('localhost',2508))
data = {'t':'login','l':'nikkey2x2','p':'322'}
data2 = {'t':'logout'}
json_data = bytes(json.dumps(data),'utf-8')
json_data2 = bytes(json.dumps(data2),'utf-8')
print("Sending:", json_data)
s.send(json_data)
print("Got:",s.recv(1024))
print("Waiting 3 secs")
time.sleep(3)
print("Sending again...")
s.send(json_data2)
#print("Got:",s.recv(1024))
s.close()
print("Closed and done")