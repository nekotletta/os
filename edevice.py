import socket
import sys 
import random
import time 

for _ in range(5):
  id = str(sys.argv[1])
  job_time = random.randint(1, 3)
  id_time = (str(id) + ":" + str(job_time))
  print(id_time)
  bytesToSend = str.encode(id_time)
  serverAddressPort = (sys.argv[2], int(sys.argv[3])) 
  
  bufferSize = 1000
  
  UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

  UDPClientSocket.sendto(bytesToSend, serverAddressPort)

  time.sleep(random.randint(1,3))
