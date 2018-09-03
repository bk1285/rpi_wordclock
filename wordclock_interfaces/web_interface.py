from flask import Flask, render_template, request
import thread
from flask_restplus import Api, Resource, fields


class web_interface:
    app = Flask(__name__)
    api = Api(app, version='4.0', title='Wordclock API', description='The rpi_wordclock api')
    plugin_model = api.model('plugin', {
        'name': fields.String('Plugin name in a single word'),
        'pretty_name': fields.String('Pretty plugin name, which may hold capital + special characters or spaces'),
        'description': fields.String('Sentence, which describes the plugins functionality')
    })
    plugin_name_model = api.model('plugin_name', {
        'name': fields.String('Plugin name in a single word')
    })
    button_model = api.model('button', {
        'button': fields.String('Name of a button, which will be triggered: left, right, return')
    })

    def __init__(self, wordclock):
        self.app.wclk = wordclock
        self.app.debug = False
        thread.start_new_thread(self.threaded_app, ())

    def threaded_app(self):
        port = 8080 if self.app.wclk.developer_mode_active else 80
        self.app.run(host='0.0.0.0', port=port)


@web_interface.api.route('/plugins')
class plugins(Resource):
    @web_interface.api.marshal_with(
        web_interface.plugin_model,
        envelope='plugins')
    @web_interface.api.doc(
        description='Returns a list of all available plugins',
        responses={
            200: 'Success',
            400: 'Bad request'})
    def get(self):
        return web_interface.app.wclk.plugins


@web_interface.api.route('/plugin')
class plugin(Resource):
    @web_interface.api.marshal_with(
        web_interface.plugin_model,
        envelope='plugin')
    @web_interface.api.doc(
        description='Returns the currently active plugin',
        responses={
            200: 'Success',
            400: 'Bad request'})
    def get(self):
        return web_interface.app.wclk.plugins[web_interface.app.wclk.plugin_index]

    @web_interface.api.doc(
        description='Takes a valid plugin name to make it the active plugin',
        responses={
            200: 'Success',
            400: 'Bad request',
            406: 'Bad key or plugin name supplied'})
    @web_interface.api.expect(web_interface.plugin_name_model)
    def post(self):
        if 'name' not in web_interface.api.payload:
            web_interface.api.abort(406, 'Request must contain \"name\" key')
        name = web_interface.api.payload.get('name')
        plugin_list = web_interface.app.wclk.plugins
        try:
            pluginindex = [i for i, plugin_list in enumerate(plugin_list) if plugin_list.name == name][0]
        except IndexError:
            web_interface.api.abort(406, 'Request must contain a valid plugin name. Received ' + name)
        web_interface.app.wclk.runNext(pluginindex)
        return "Set current plugin to " + name


@web_interface.api.route('/button')
class button(Resource):
    @web_interface.api.doc(
        description='Takes a name of the button, to be pressed: left, right, return',
        responses={
            200: 'Success',
            400: 'Bad request',
            406: 'Invalid button supplied'})
    @web_interface.api.expect(web_interface.button_model)
    def post(self):
        if 'button' not in web_interface.api.payload:
            web_interface.api.abort(406, 'Request must contain \"button\" key')
        button = web_interface.api.payload.get('button')
        if button not in web_interface.app.wclk.wci.BUTTONS:
            web_interface.api.abort(406, 'Request must contain a valid button name. Received ' + button)
        event = web_interface.app.wclk.wci.BUTTONS.get(button)
        web_interface.app.wclk.wci.setEvent(event)
        return "Button " + button + " triggered"



