import sys
sys.path.insert(0, "..")
import time


from opcua import ua, Server

from gpiozero import Motor, Button


edge = False
old_edge = False
new_edge = False
rpm_is = False
downtime = None
puls = Button(14)
#motor = Motor(26, 20)
speed = 0
callback_flag, callback_count = False, 0

def callback_rpm():
   global old_edge, new_edge, rpm_is, edge, callback_flag
   edge = True
   old_edge = new_edge
   new_edge = time.clock_gettime_ns(time.CLOCK_MONOTONIC)
   callback_flag = True

def rpm():
   global old_edge, new_edge, callback_flag, callback_count, rpm_is
   if callback_flag:
      callback_flag , callback_count = False, 0
      if old_edge and new_edge:
         return int(60/(((new_edge-old_edge)*10**(-9))*20))
      else:
         return -1
   else:
      if callback_count >10:
         return 0
      return -1


def setup_server():
   '''
  To avoid problems with opc toolbox from matlab use one of the following
  to indicate the host ip:
     - '192.168.0.183' change if needed
     - 'pi.local' mdns name
     DO NOT USE '0.0.0.0' or localhost!!!
   '''
   # setup our server
   server = Server()
   server.set_endpoint("opc.tcp://pi.local:4840/opcua")

   # setup our own namespace, not really necessary but should as spec
   uri = "http://examples.freeopcua.github.io"
   idx = server.register_namespace(uri)

   # get Objects node, this is where we should put our nodes
   objects = server.get_objects_node()

   # populating our address space
   myobj = objects.add_object(idx, "MyCar")
   myvar = myobj.add_variable(idx, "RPM", 0)
   myvar.set_writable()    # Set MyVariable to be writable by clients
   return server, myvar


def main():
   # set up server
   server, myvar = setup_server()

   # start server
   server.start()

   try:
        while True:
            time.sleep(1)
            rpm_val = rpm()
            print(rpm_val)
            if rpm_val >1:
               myvar.set_value(rpm_val)
   finally:
      #close connection, remove subcsriptions, etc
      server.stop()









if __name__ == "__main__":
   '''
  To avoid problems with opc toolbox from matlab use one of the following
  to indicate the host ip:
     - '192.168.0.183' change if needed
     - 'pi.local' mdns name
     DO NOT USE '0.0.0.0' or localhost!!!
   '''

   puls.when_pressed = callback_rpm # set callback
   main()

   # setup our server
#   server = Server()
#   server.set_endpoint("opc.tcp://pi.local:4840/opcua")
#
#   # setup our own namespace, not really necessary but should as spec
#   uri = "http://examples.freeopcua.github.io"
#   idx = server.register_namespace(uri)
#
#   # get Objects node, this is where we should put our nodes
#   objects = server.get_objects_node()
#
#   # populating our address space
#   myobj = objects.add_object(idx, "MyCar")
#   myvar = myobj.add_variable(idx, "RPM", 0)
#   myvar.set_writable()    # Set MyVariable to be writable by clients

   # starting!
#   server.start()
#    
#   try:
#       while True:
#           time.sleep(1)
#           count += 0.1
#           myvar.set_value(count)
#   finally:
#       #close connection, remove subcsriptions, etc
#       server.stop()
