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

    name = request.form['name']
    print("name: " + name)
    plugins = web_interface.app.wclk.plugins
    pluginindex=[i for i,plugins in enumerate(plugins) if plugins.name == name][0]

    web_interface.app.wclk.runNext(pluginindex)

@web_interface.app.route('/list', methods=['POST', 'GET'])
def list():
    plugins = [{"NAME": plugin.name, "PRETTY_NAME": plugin.pretty_name, "DESCRIPTION": plugin.description} for plugin in web_interface.app.wclk.plugins]
    return jsonify({'PLUGINS': plugins})

@web_interface.app.route('/active', methods=['POST', 'GET'])
def active():
    index = web_interface.app.wclk.plugin_index
    plugin = web_interface.app.wclk.plugins[index]
    return jsonify({ 'INDEX': index, 'NAME': plugin.name, 'PRETTY_NAME': plugin.pretty_name, 'DESCRIPTION': plugin.description })
