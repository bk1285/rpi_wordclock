from flask import Flask, render_template, request, jsonify
import thread


class web_interface():
    app = Flask(__name__)

    def __init__(self, wordclock):
        self.app.wclk = wordclock
        self.app.debug = False
        self.app.api_version = 3
        thread.start_new_thread(self.threadedApp, ())

    def threadedApp(self):
        self.app.run(host='0.0.0.0', port=80)


@web_interface.app.route('/')
def index():
    return render_template('form.html')


@web_interface.app.route('/get/list', methods=['POST', 'GET'])
def list():
    plugins = [{"NAME": plugin.name, "PRETTY_NAME": plugin.pretty_name, "DESCRIPTION": plugin.description} for plugin in
               web_interface.app.wclk.plugins]
    return jsonify({
        'PLUGINS': plugins,
        'API': web_interface.app.api_version
    })


@web_interface.app.route('/get/active', methods=['POST', 'GET'])
def active():
    idx = web_interface.app.wclk.plugin_index
    plugin = web_interface.app.wclk.plugins[idx]
    return jsonify({
         'INDEX': idx,
         'NAME': plugin.name,
         'PRETTY_NAME': plugin.pretty_name,
         'DESCRIPTION': plugin.description,
         'API': web_interface.api_version
    })


@web_interface.app.route('/set/plugin', methods=['POST'])
def api():
    name = request.form['name']
    print("name: " + name)
    plugins = web_interface.app.wclk.plugins
    pluginindex = [i for i, plugins in enumerate(plugins) if plugins.name == name][0]

    web_interface.app.wclk.runNext(pluginindex)


@web_interface.app.route('/set/color', methods=['POST'])
def color():
    name = request.form['name']
    print("name: " + name)
    plugins = web_interface.app.wclk.plugins
    pluginidx = [i for i, plugins in enumerate(plugins) if plugins.name == name][0]

    web_interface.app.wclk.runNext(pluginidx)