from flask import Flask, render_template
import thread
from flask_restplus import Api, Resource, fields
import wordclock_tools.wordclock_colors as wcc


class web_interface:
    app = Flask(__name__)
    api = Api(app,
              validate=True,
              version='4.3',
              title='Wordclock API',
              description='The API to access the raspberry wordclock',
              contact='Bernd',
              security=None,
              doc='/api',
              prefix='/api',
              default='API',
              default_label='Endpoints to access and control the wordclock',
              ordered=False)
    plugin_model = api.model('plugin', {
        'name': fields.String(description='Plugin name in a single word'),
        'pretty_name': fields.String(
            description='Pretty plugin name, which may hold capital + special characters or spaces'),
        'description': fields.String(description='Sentence, which describes the plugins functionality')
    })
    plugin_name_model = api.model('plugin_name', {
        'name': fields.String(required=True,
                              example='time_default',
                              description='Plugin name in a single word')
    })
    button_model = api.model('button', {
        'button': fields.String(enum=['left', 'right', 'return'],
                                required=True,
                                example='return',
                                description='Name of a button, which will be triggered')
    })
    color_model = api.model('color', {
        'red': fields.Integer(min=0, max=255, example=50, required=True, description='Red value'),
        'green': fields.Integer(min=0, max=255, example=200, required=True, description='Green value'),
        'blue': fields.Integer(min=0, max=255, example=100, required=True, description='Blue value'),
        'type': fields.String(enum=['all', 'words', 'minutes', 'background'],
                              required=False,
                              example='all',
                              description='Set color only to specified parts of the wordclock. Defaults to all.')
    })
    brightness_model = api.model('brightness', {
        'brightness': fields.Integer(min=0, max=255, example=180, required=True, description='Brightness value')
    })
    color_temperature_model = api.model('color_temperature', {
        'color_temperature': fields.Integer(min=1000, max=40000, example=2000, required=True, description='Color temperature in Kelvin')
    })

    def __init__(self, wordclock):
        self.app.wclk = wordclock
        self.app.debug = False
        thread.start_new_thread(self.threaded_app, ())

    def threaded_app(self):
        port = 8080 if self.app.wclk.developer_mode_active else 80
        self.app.run(host='0.0.0.0', port=port)


@web_interface.app.route('/')
def index():
    return render_template('app.html')


@web_interface.api.route('/plugins')
class Plugins(Resource):
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
class Plugin(Resource):
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
            406: 'Bad plugin name supplied'})
    @web_interface.api.expect(web_interface.plugin_name_model)
    def post(self):
        name = web_interface.api.payload.get('name')
        plugin_list = web_interface.app.wclk.plugins
        try:
            pluginindex = [i for i, plugin_list in enumerate(plugin_list) if plugin_list.name == name][0]
        except IndexError:
            web_interface.api.abort(406, 'Request must contain a valid plugin name. Received ' + name)
        web_interface.app.wclk.runNext(pluginindex)
        return "Set current plugin to " + name


@web_interface.api.route('/button')
class Button(Resource):
    @web_interface.api.doc(
        description='Takes a name of the button, to be pressed: left, right, return',
        responses={
            200: 'Success',
            400: 'Bad request'})
    @web_interface.api.expect(web_interface.button_model)
    def post(self):
        button_type = web_interface.api.payload.get('button')
        event = web_interface.app.wclk.wci.BUTTONS.get(button_type)
        web_interface.app.wclk.wci.setEvent(event)
        return "Button " + button_type + " triggered"


@web_interface.api.route('/color')
class Color(Resource):
    @web_interface.api.doc(
        description='Returns 8bit RGB color values of the displayed time',
        responses={
            200: 'Success',
            400: 'Bad request'})
    def get(self):
        default_plugin = web_interface.app.wclk.plugins[web_interface.app.wclk.default_plugin]
        channel_wise = lambda(x): {'red': x.r, 'green': x.g, 'blue': x.b}

        return {
            'background': channel_wise(default_plugin.bg_color),
            'words': channel_wise(default_plugin.word_color),
            'minutes': channel_wise(default_plugin.minute_color)
        }

    @web_interface.api.doc(
        description='Takes 8bit RGB color values to display the time with',
        responses={
            200: 'Success',
            400: 'Bad request'})
    @web_interface.api.expect(web_interface.color_model)
    def post(self):
        supplied_color = wcc.Color(web_interface.api.payload.get('red'),
                                   web_interface.api.payload.get('green'),
                                   web_interface.api.payload.get('blue'))

        supplied_type = web_interface.api.payload.get('type')
        supplied_type = 'all' if supplied_type is None else supplied_type

        default_plugin_idx = web_interface.app.wclk.default_plugin
        web_interface.app.wclk.runNext(default_plugin_idx)
        default_plugin = web_interface.app.wclk.plugins[default_plugin_idx]
        if supplied_type == 'all':
            default_plugin.bg_color = wcc.BLACK
            default_plugin.word_color = supplied_color
            default_plugin.minute_color = supplied_color
        elif supplied_type == 'words':
            default_plugin.word_color = supplied_color
        elif supplied_type == 'minutes':
            default_plugin.minute_color = supplied_color
        elif supplied_type == 'background':
            default_plugin.bg_color = supplied_color
        default_plugin.show_time(web_interface.app.wclk.wcd, web_interface.app.wclk.wci, animation=None)
        return "Wordclock color set to " + supplied_type


@web_interface.api.route('/brightness')
class Brightness(Resource):
    @web_interface.api.doc(
        description='Returns 8bit value representing the current wordclock brightness',
        responses={
            200: 'Success',
            400: 'Bad request'})
    def get(self):
        return web_interface.app.wclk.wcd.getBrightness()

    @web_interface.api.doc(
        description='Takes an 8bit value to set the wordclock brightness',
        responses={
            200: 'Success',
            400: 'Bad request'})
    @web_interface.api.expect(web_interface.brightness_model)
    def post(self):
        brightness = web_interface.api.payload.get('brightness')
        web_interface.app.wclk.wcd.setBrightness(brightness)
        return "Wordclock brightness set to " + str(brightness)


@web_interface.api.route('/color_temperature')
class ColorTemperature(Resource):
    @web_interface.api.doc(
        description='Takes an integer value to set the wordclock color temperature',
        responses={
            200: 'Success',
            400: 'Bad request'})
    @web_interface.api.expect(web_interface.color_temperature_model)
    def post(self):
        color_temperature = web_interface.api.payload.get('color_temperature')
        default_plugin_idx = web_interface.app.wclk.default_plugin
        web_interface.app.wclk.runNext(default_plugin_idx)
        default_plugin = web_interface.app.wclk.plugins[default_plugin_idx]
        default_plugin.bg_color = wcc.BLACK
        default_plugin.word_color = wcc.color_temperature_to_rgb(color_temperature)
        default_plugin.minute_color = wcc.color_temperature_to_rgb(color_temperature)
        default_plugin.show_time(web_interface.app.wclk.wcd, web_interface.app.wclk.wci)
        return "Wordclock color temperature set to " + str(color_temperature)
