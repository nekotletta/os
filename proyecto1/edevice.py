import socket
import sys
import random
import time
import threading 

#EL BONO SE IMPLEMENTO USANDO FUNCIONES PARA QUE FUERA FACIL
#CORRER EL PROGRAMA SIN EL BONO POR SI CAUSABA PROBLEMAS
#QUE NO SE DAÑARA NADA QUE YA ESTUVIERA CPMPLETADO
bufferSize = 10000
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
def ejecutar():
  global bufferSize
  msg = ''
  MsgFromServer = UDPClientSocket.recvfrom(bufferSize)
  msg = MsgFromServer[0]
  print(msg)
    
for _ in range(5): 
  id = str(sys.argv[1])
  job_time = random.randint(1, 3)
  id_time = (str(id) + ":" + str(job_time))
  print(id_time)
  bytesToSend = str.encode(id_time)
  serverAddressPort = (sys.argv[2], int(sys.argv[3]))

  UDPClientSocket.sendto(bytesToSend, serverAddressPort)
  ejecutar()
