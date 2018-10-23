var ColorPicker = window.VueColorPicker;
new Vue(
{
	el: '#app',
	components: {
                ColorPicker: ColorPicker
	},
	data: {
		brightness: 50,
                color: {
                    hue: 50,
                    saturation: 100,
                    luminosity: 50,
                    alpha: 1
                },
		apiData: undefined,
		selectedPlugin: {
		    name: 'time_default'
		},
		currentPlugin: {
		    name: 'time_default'
		},
		switchWords: true,
		switchMinutes: true,
		switchBackground: false
	},
	methods: {
		loadApi: function () {
			this.$http.get('/api/plugin').
			  then(this.successCallbackPlugin, this.errorCallback);
			this.$http.get('/api/plugins').
			  then(this.successCallbackPlugins, this.errorCallback);
		},
		successCallbackPlugins: function(response) {
			this.apiData = response.data;
			console.log('successCallback this.apiData:' , this.apiData);
		},
		successCallbackPlugin: function(response) {
			this.currentPlugin = response.data.plugin;
			console.log('successCallback this.currentPlugin:' , this.currentPlugin);
		},
		errorCallback: function(response) {
			console.log('errorCallback response:' , response);
		},
		selectionChanged: function(selectedPlugin) {
			console.log('selectionChanged: ', selectedPlugin);
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.open("POST", "/api/plugin");
			xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
			xmlhttp.send(JSON.stringify({ "name": selectedPlugin.name}));
		},
		buttonClick: function(buttonClicked) {
			console.log('buttonClicked', buttonClicked );
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.open("POST", "/api/button");
			xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
			xmlhttp.send(JSON.stringify({ button: buttonClicked}));
		},
		setColour: function(r,g,b) {
			console.log('setColour:' , r,g,b);
			if (this.switchWords) {
				type = "words"
			};
			if (this.switchMinutes) {
				type = "minutes"
			};
			if (this.switchWords && this.switchMinutes) {
				type = "all"
			};
			if (this.switchBackground) {
				type = "background"
			};
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.open("POST", "/api/color");
			xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
			xmlhttp.send(JSON.stringify({ "blue": b, "green": g, "red": r , "type": type}));
		},
		updateBrightness: function(brightness) {
			console.log('updateBrightness:' , brightness);
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.open("POST", "/api/brightness");
			xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
			xmlhttp.send(JSON.stringify({ "brightness": brightness }));
		},
		setColourWheel: function(wheel) {
			var r,g,b,type;
			[r,g,b] = hslToRgb(wheel.hue/360, wheel.saturation/100, wheel.luminosity/100);
			console.log('setColourWheel:' , r,g,b);
			if (this.switchWords) {
				type = "words"
			};
			if (this.switchMinutes) {
				type = "minutes"
			};
			if (this.switchWords && this.switchMinutes) {
				type = "all"
			};
			if (this.switchBackground) {
				type = "background"
			};
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.open("POST", "/api/color");
			xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
			xmlhttp.send(JSON.stringify({ "blue": b, "green": g, "red": r , "type": type}));
		}
	},
	beforeMount(){
		this.loadApi();
	},
	created() {
		setTimeout(() => {
			this.selectedPlugin = this.currentPlugin;
			console.log('currentPlugin:', this.currentPlugin);
			console.log('selectedPlugin:', this.selectedPlugin);
		}, 1000);
	}
}
);

/**
 * Converts an HSL color value to RGB. Conversion formula
 * adapted from http://en.wikipedia.org/wiki/HSL_color_space.
 * Assumes h, s, and l are contained in the set [0, 1] and
 * returns r, g, and b in the set [0, 255].
 *
 * @param   {number}  h       The hue
 * @param   {number}  s       The saturation
 * @param   {number}  l       The lightness
 * @return  {Array}           The RGB representation
 */
function hslToRgb(h, s, l){
    var r, g, b;

    if(s == 0){
        r = g = b = l; // achromatic
    }else{
        var hue2rgb = function hue2rgb(p, q, t){
            if(t < 0) t += 1;
            if(t > 1) t -= 1;
            if(t < 1/6) return p + (q - p) * 6 * t;
            if(t < 1/2) return q;
            if(t < 2/3) return p + (q - p) * (2/3 - t) * 6;
            return p;
        }

        var q = l < 0.5 ? l * (1 + s) : l + s - l * s;
        var p = 2 * l - q;
        r = hue2rgb(p, q, h + 1/3);
        g = hue2rgb(p, q, h);
        b = hue2rgb(p, q, h - 1/3);
    }

    return [Math.round(r * 255), Math.round(g * 255), Math.round(b * 255)];
}