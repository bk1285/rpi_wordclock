from flask import Flask, render_template, request, jsonify
import thread
import wsgiserver
from wordclock_interfaces.event_handler import event_handler as eh

class web_interface():
    app = Flask(__name__)

    def __init__(self, wordclock):
        self.app.wclk = wordclock
        self.app.debug = False
        thread.start_new_thread(self.threadedApp, ())

    def threadedApp(self):
        self.app.run(host='0.0.0.0', port=80)

@web_interface.app.route('/')
def index():
    return render_template('form.html')

@web_interface.app.route('/api', methods=['POST'])
def api():

    email = request.form['email']
    name = request.form['name']

    if name and email:
        newName = name[::-1]
        print("name: " + name)

    data = {"affe": "bla"}

    if 'GET_CONFIG' in data:
        plugins = [{"NAME": plugin.pretty_name, "DESCRIPTION": plugin.description} for plugin in self.wclk.plugins]
        msg = { 'PLUGINS': plugins, 'ACTIVE_PLUGIN': self.wclk.plugin_index }
        return jsonify(msg)
    elif 'SET_ACTIVE_PLUGIN' in data:
        self.wclk.runNext(int(data['SET_ACTIVE_PLUGIN']))
        self.wclk.wci.setEvent(eh.EVENT_EXIT_PLUGIN)
    elif 'SEND_EVENT' in data:
        self.wclk.wci.setEvent(int(data['SEND_EVENT']))
    else:
        e_msg= "Can\'t handle json-request..."
        print e_msg
        web_interface.app.wclk.runNext(4)
        web_interface.app.wclk.wci.setEvent(eh.EVENT_EXIT_PLUGIN)
        return jsonify({"error" : name + " " + e_msg})
