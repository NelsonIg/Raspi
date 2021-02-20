import sys
sys.path.insert(0, "..")
import time


from opcua import ua, Server


if __name__ == "__main__":
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
   myobj = objects.add_object(idx, "MyObject")
   myvar = myobj.add_variable(idx, "MyVariable", 6.7)
   myvar.set_writable()    # Set MyVariable to be writable by clients

   # starting!
   server.start()
    
   try:
       count = 0
       while True:
           time.sleep(1)
           count += 0.1
           myvar.set_value(count)
   finally:
       #close connection, remove subcsriptions, etc
       server.stop()
