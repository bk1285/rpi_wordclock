import json
import struct
import threading
import SocketServer
from wordclock_interfaces.event_handler import event_handler as eh

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    cfg = None

    def handle(self):
        print('Received new connection from ' + str(self.client_address[0]))
        while True:
            try:
                jdata = self.recv_msg()
                if not jdata:
                    raise
            except:
                print "Connection to {} terminated" % str(self.client_address[0]) 
                return
            
            try:
                data = json.loads(jdata)
            except:
                print "Invalid data from {}" % str(self.client_address[0])
                return

            if (data['API'] != 1 ):
                print 'Wrong API: Expected API = 1'
                return
            if 'GET_CONFIG' in data:
                plugins = map(lambda plugin: plugin.name, self.wclk.plugins)
                msg = { 'PLUGINS': plugins, 'ACTIVE_PLUGIN': self.wclk.plugin_index, 'API': 1 }
                self.send_msg(json.dumps(msg))
            elif 'SET_ACTIVE_PLUGIN' in data:
                self.wclk.runNext(int(data['SET_ACTIVE_PLUGIN']))
                self.wclk.wci.setEvent(eh.EVENT_EXIT_PLUGIN)
            else:
                e_msg= "Can\'t handle json-request..."
                self.send_msg(json.dumps({ 'ERROR_MSG' : e_msg, 'API': 1 }))
                print e_msg
                return

    def send_msg(self, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        self.request.sendall(msg)

    def recv_msg(self):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(msglen)

    def recvall(self, n):
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

