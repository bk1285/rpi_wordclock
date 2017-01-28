import json
import struct
import threading
import SocketServer

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    cfg = None

    def handle(self):
        print('Received new connection from ' + str(self.client_address[0]))
        print(self.wclk.config.get('plugin_time_default', 'language'))
        print('Plugin-index: ' + str(self.wclk.plugin_index))
        while True:
            jdata = self.recv_msg()
            #jdata = "{\"API\":1, \"GET_CONFIG\":0}"
            data = json.loads(jdata)
            json.dumps(data)

            if (data['API'] != 1 ):
                print 'Wrong API: Expected API = 1'
                return
            if 'GET_CONFIG' in data:
                plugins = []
                for i, plugin in enumerate(self.wclk.plugins):
                    plugins.append(plugin.name)
                msg = { 'PLUGINS': plugins, 'ACTIVE_PLUGIN': self.wclk.plugin_index, 'API': 1 }
                self.send_msg(json.dumps(msg))
            elif 'SET_ACTIVE_PLUGIN' in data:
#                self.wclk.set_plugin_index(int(data['SET_ACTIVE_PLUGIN']))
                print "Todo: Needs implementation"
            else:
                e_msg= "Can\'t handle json-request..."
                json_e_msg = json.dumps('ERROR_MSG:' + e_msg)
                self.send_msg(json_e_msg)
                print e_msg

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

