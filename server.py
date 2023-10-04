import socket
import threading
from threading import Thread
import time

#EL BONO FUE IMPLEMENTADO EN UNA FUNCION PARA QUE FUERA FACIL
#CORRRER EL PROGRAMA SIN EL EN CASO DE QUE DIERA PROBLEMAS. 
#PARA NO DAÑAR NADA YA HECHO

#SERVER
localIP = 'localhost'
localPort = int(sys.argv[1]) #para que lea el puerto desde el terminal
bufferSize = 10000
mesage = ''
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UDPServerSocket.bind((localIP, localPort))
print("UDP server up and listening")
bytesAddressPair = ()


#THREADS / PROCESO
JOB_QUEUE = []
empty_slots = threading.Semaphore(bufferSize)
full_slots = threading.Semaphore(0)
critical_reg = threading.Semaphore(1)
sumatoria = []
suma = {}
FINISHED = False
PROCESOS_COMP = 0

def display():
  for times in sumatoria:
    for dev, dur in times.items():
      print("Device " + str(dev) + " consumed " + str(dur) + "s of CPU time")
#BONO
def avisar(bytesAddressPair):
    MsgFromServer = "Termine, puedes insertar"
    msg = str.encode(MsgFromServer)
    address = bytesAddressPair[1]
    critical_reg.acquire()
    UDPServerSocket.sendto(msg, address)
    critical_reg.release()

class Producer(Thread):

  def __init__(self):
    Thread.__init__(self)

  def run(self):
    global FINISHED
    global bytesAddressPair
    while not FINISHED:
      bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
      message = str(bytesAddressPair[0])
      substring = message[message.find("'") + 1:message.find(",")]
      split = substring.split(":")
      jobs = {}
      jobs[int(split[0])] = int(split[1])  #equivalente to 'produce_item'
      empty_slots.acquire()
      critical_reg.acquire()
      JOB_QUEUE.append(jobs)  #equivalent to 'insert_item'
      critical_reg.release()
      full_slots.release()

class Consumer(Thread):

  def __init__(self):
    Thread.__init__(self)

  def sumar(self, jobs):
    global sumatoria
    sumatoria = []
    for dev, sec in jobs.items():
      if dev in suma:
        suma[dev] += sec
      else:
        suma[dev] = sec
    for key, dev in suma.items():
      sumatoria.append({key: dev})
    sumatoria = sumatoria = sorted(sumatoria, key=lambda d: list(d.keys())[0])
  
  def run(self):
    global LJF
    global sumatoria
    global PROCESOS_COMP
    global bytesAddressPair
    LJF = []
    critical_reg.acquire()
    LJF = sorted(JOB_QUEUE, key=lambda d: list(d.values())[0], reverse=True)
    critical_reg.release()
    while not FINISHED:
      full_slots.acquire()
      critical_reg.acquire()
      LJF = sorted(JOB_QUEUE, key=lambda d: list(d.values())[0], reverse=True)
      top_dict = LJF[0]
      id = list(top_dict.keys())[0]
      len = list(top_dict.values())[0]
      print("Device " + str(id) + " durmiendo por " + str(len) + "s")
      time.sleep(len)
      nueva_adquisicion = LJF.pop(0)
      JOB_QUEUE.remove(nueva_adquisicion)
      critical_reg.release()
      empty_slots.release()
      self.sumar(nueva_adquisicion)
      PROCESOS_COMP += 1
      avisar(bytesAddressPair)
      if PROCESOS_COMP == 20:
        display()

producer_thread = Producer()
producer_thread.start()
consumer_thread = Consumer()
consumer_thread.start()
producer_thread.join()
consumer_thread.join()
