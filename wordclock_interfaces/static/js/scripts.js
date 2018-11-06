var ColorPicker = window.VueColorPicker;
new Vue(
{
	el: '#app',
	components: {
                ColorPicker: ColorPicker
	},
	data: {
		brightness: undefined,
        color: {
            hue: undefined,
            saturation: undefined,
            luminosity: undefined,
            alpha: 1
        },
		apiData: undefined,
		selectedPlugin: {
		    name: undefined,
		    description: undefined
		},
		switchWords: true,
		switchMinutes: true,
		switchBackground: false,
		about: false
	},
	methods: {
		loadApi: function () {
			this.$http.get('/api/plugin').
			  then(this.successCallbackPlugin, this.errorCallback);
			this.$http.get('/api/plugins').
			  then(this.successCallbackPlugins, this.errorCallback);
			this.$http.get('/api/color').
			  then(this.successCallbackColor, this.errorCallback);
			this.$http.get('/api/brightness').
			  then(this.successCallbackBrightness, this.errorCallback);
		},
		successCallbackPlugins: function(response) {
			this.apiData = response.data;
		},
		successCallbackPlugin: function(response) {
            this.selectedPlugin = response.data.plugin;
		},
		successCallbackColor: function(response) {
			var h,s,l,r,g,b;
			r = response.data.words.red;
			g = response.data.words.green;
			b = response.data.words.blue;
			[h,s,l] = rgbToHsl(r, g, b);
			this.color.hue = h * 360;
			this.color.saturation = s * 100;
			this.color.luminosity = l * 100;
		},
		successCallbackBrightness: function(response) {
            this.brightness = response.data;
		},
		errorCallback: function(response) {
			console.log('errorCallback response:' , response);
		},
		selectionChanged: function(selectedPlugin) {
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.open("POST", "/api/plugin");
			xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
			xmlhttp.send(JSON.stringify({ name: selectedPlugin.name}));
		},
		buttonClick: function(buttonClicked) {
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.open("POST", "/api/button");
			xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
			xmlhttp.send(JSON.stringify({ button: buttonClicked}));
		},
		setColour: function(r,g,b) {
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
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.open("POST", "/api/brightness");
			xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
			xmlhttp.send(JSON.stringify({ "brightness": brightness }));
		},
		setColourWheel: function(wheel) {
			var r,g,b,type;
			[r,g,b] = hslToRgb(wheel.hue/360, wheel.saturation/100, wheel.luminosity/100);
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

/**
 * Converts an RGB color value to HSL. Conversion formula
 * adapted from http://en.wikipedia.org/wiki/HSL_color_space.
 * Assumes r, g, and b are contained in the set [0, 255] and
 * returns h, s, and l in the set [0, 1].
 *
 * @param   {number}  r       The red color value
 * @param   {number}  g       The green color value
 * @param   {number}  b       The blue color value
 * @return  {Array}           The HSL representation
 */
function rgbToHsl(r, g, b){
    r /= 255, g /= 255, b /= 255;
    var max = Math.max(r, g, b), min = Math.min(r, g, b);
    var h, s, l = (max + min) / 2;

    if(max == min){
        h = s = 0; // achromatic
    }else{
        var d = max - min;
        s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
        switch(max){
            case r: h = (g - b) / d + (g < b ? 6 : 0); break;
            case g: h = (b - r) / d + 2; break;
            case b: h = (r - g) / d + 4; break;
        }
        h /= 6;
    }

    return [h, s, l];
}
