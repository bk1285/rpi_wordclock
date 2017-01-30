import json
import struct
import threading
import SocketServer
from wordclock_interfaces.event_handler import event_handler as eh

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print('Received new connection from ' + str(self.client_address[0]))
        self.wclk.wcs.allClients.add(self)
        self.mainloop()
        self.wclk.wcs.allClients.discard(self)
        print "Connection to {0} terminated".format(str(self.client_address[0]))
        
    def mainloop(self):
        while True:
            try:
                jdata = self.recv_msg()
                if not jdata:
                    return
            except:
                return
            
            try:
                data = json.loads(jdata)
            except:
                print "Invalid data from {0}".format(str(self.client_address[0]))
                return

            if (data['API'] != 1 ):
                print 'Wrong API: Expected API = 1'
                return
            
            if 'GET_CONFIG' in data:
                plugins = [plugin.name for plugin in self.wclk.plugins]
                msg = { 'PLUGINS': plugins, 'ACTIVE_PLUGIN': self.wclk.plugin_index }
                self.send_json(msg)
            elif 'SET_ACTIVE_PLUGIN' in data:
                self.wclk.runNext(int(data['SET_ACTIVE_PLUGIN']))
                self.wclk.wci.setEvent(eh.EVENT_EXIT_PLUGIN)
            else:
                e_msg= "Can\'t handle json-request..."
                self.send_json({ 'ERROR_MSG' : e_msg })
                print e_msg
                return

    def send_json(self, jsonobj):
        # Prefix each message with a 4-byte length (network byte order)
        jsonobj['API'] = 1
        msg = json.dumps(jsonobj)
        msg = struct.pack('>I', len(msg)) + msg
        self.request.sendall(msg)

    def recv_msg(self):
        # Read message length and unpack it into an integer
        raw_msglen = self.__recvall(4)
        if not raw_msglen:
            raise
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.__recvall(msglen)

    def __recvall(self, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = ''
        while len(data) < n:
            packet = self.request.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class wordclock_socket:
    '''
    A class providing a json api for the wordclock
    '''

    def __init__(self, wordclock):
        '''
        Setup wordclock_socket
        '''
        self.allClients = set()
        
        print('Setting up wordclock socket')
        class ThreadedTCPRequestHandlerWithConfig(ThreadedTCPRequestHandler):
            wclk = wordclock

        HOST, PORT = "0.0.0.0", 8081
        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandlerWithConfig)

        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()
    
    def sendCurrentPlugin(self, index):
        self.__sendToAll({'ACTIVE_PLUGIN': index})
    
    def __sendToAll(self, jsonobj):
        for client in self.allClients:
            try:
                client.send_json(jsonobj)
            except:
                pass
