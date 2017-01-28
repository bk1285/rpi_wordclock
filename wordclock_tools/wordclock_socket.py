import json
import threading
import SocketServer

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    cfg = None

    def handle(self):
        print('Received new connection from ' + str(self.client_address[0]))
        print(self.cfg.get('plugin_time_default', 'language'))
        for i, plugin in enumerate(self.plgs):
            print ('{' + str(i) + ': ' + plugin.name + '}')
        while True:
            data = self.request.recv(1024)
            cur_thread = threading.current_thread()
            response = "{}: {}".format(cur_thread.name, data)
            self.request.sendall(response)

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

    def __init__(self, config, plugins):
        '''
        Setup wordclock_socket
        '''
        print('Setting up wordclock socket')
        class ThreadedTCPRequestHandlerWithConfig(ThreadedTCPRequestHandler):
            cfg = config
            plgs = plugins

        HOST, PORT = "0.0.0.0", 8081
        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandlerWithConfig)
        server.config = config


        # Start a thread with the server -- that thread will then start one
        # more thread for each request
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

