import threading
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from wordclock_interfaces.event_handler import event_handler as eh

class wordclock_socket():

    def __init__(self, wordclock):

        print('Setting up wordclock socket')

	global wclk 
	wclk = wordclock

	server = SimpleWebSocketServer('', 8081, webs)
        server_thread = threading.Thread(target=server.serveforever)
        
	server_thread.daemon = True
	server_thread.start()

class webs(WebSocket):
    def handleConnected(self):
        print('Recieved new connenction from ' +str(self.address))

    def handleClose(self):
        print('Connection to ' +str(self.address) +' terminated')

    def handleMessage(self):
        print('WSrecieved: ' +self.data)

	if self.data == 'left':
	    wclk.wci.setEvent(eh.EVENT_BUTTON_LEFT)

	if self.data == 'return':
	    wclk.wci.setEvent(eh.EVENT_BUTTON_RETURN)

	if self.data == 'right':
	    wclk.wci.setEvent(eh.EVENT_BUTTON_RIGHT)
	self.sendMessage(u'OK')
