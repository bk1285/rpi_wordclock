import json
import struct
import threading
import web
import socket
import struct
import threading
import os

urls = (
    '/', 'web_interface',
    '/(js|css|images|icons)/(.*)', 'static',
    '/activateplugin', 'web_interface_post'
)

render = web.template.render('wordclock_webinterface/')
webapp = web.application(urls, globals())

class wordclock_webinterface:
    '''
        The class, providing a web server for the wordclock
    '''
    def __init__(self, wordclock):
        web_thread = threading.Thread(target=webapp.run)
        # Exit the server thread when the main thread terminates
        web_thread.daemon = True
        web_thread.start()



class static:
    '''
        Class for reading static files from disk
    '''
    def GET(self, media, file):
        try:            
            f = open(os.path.dirname(os.path.abspath(__file__)) + '/' + media+'/'+file, 'r')            
            return f.read()
        except IOError as e:
            print(e)
            return '' # you can send an 404 error here if you want

class web_interface:
    '''
        The class, which is used by web py packet (is initialized on every request)
    '''
    def __init__(self):        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        
        HOST, PORT = "0.0.0.0", 8081
        self.s.connect((HOST, PORT))

    def send_json(self, jsonobj):
        # Prefix each message with a 4-byte length (network byte order)
        jsonobj['API'] = 2
        msg = json.dumps(jsonobj)
        msg = struct.pack('>I', len(msg)) + msg
        self.s.send(msg)

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
            packet = self.s.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

    def POST(self):
        data = json.loads(web.data())
        postType = data["type"]
        if postType == "activate_plugin":
            plugin = int(data["value"])
            jsonobj = {"API": 2, "SET_ACTIVE_PLUGIN": plugin}
            self.send_json(jsonobj)
        elif postType == "send_event":
            event = int(data["value"])
            jsonobj = {"API": 2, "SEND_EVENT": event}
            self.send_json(jsonobj)
        return ""

    def GET(self):
        jsonobj = {"API": 2, "GET_CONFIG": 0}
        self.send_json(jsonobj)
        message = self.recv_msg()
        data = json.loads(message)
        print(data)
        plugins = data["PLUGINS"]        
        pluginKeys = []
        for key in plugins:
            pluginKeys.append(key["NAME"])
        return render.index(pluginKeys)
            