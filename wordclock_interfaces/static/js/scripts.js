var IroColorPicker = window.iro.ColorPicker("#color-picker-container", {
	width: 320,
	color: "#fcc"
  });

var vm = new Vue(
{
	el: '#app',
	components: {
		IroColorPicker: IroColorPicker
	},
	data: {
		brightness: undefined,
		color_temperature: undefined,
        color: {
			r: undefined,
			g: undefined,
			b: undefined
        },
		apiData: undefined,
		selectedPlugin: {
		    name: undefined,
		    description: undefined
		},
		switchWords: true,
		switchMinutes: true,
		switchBackground: false,
		about: false,
		colorByTemp: false,
		date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
        menu: false,
        time: "",
        menu_t: false,
        textToScroll: "",
        textRepeat: 0,
        textEnable: false
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
			this.$http.get('/api/color_temperature').
			  then(this.successCallbackColorTemperature, this.errorCallback);
			this.$http.get('/api/scrolltext').
			  then(this.successCallbackScrolltext, this.errorCallback);
		},
		successCallbackPlugins: function(response) {
			this.apiData = response.data;
		},
		successCallbackPlugin: function(response) {
            this.selectedPlugin = response.data.plugin;
		},
		successCallbackColor: function(response) {
			this.color.r = response.data.words.red;
			this.color.g = response.data.words.green;
			this.color.b = response.data.words.blue;
		},
		successCallbackBrightness: function(response) {
            this.brightness = response.data;
		},
		successCallbackColorTemperature: function(response) {
            this.color_temperature = response.data;
		},
		successCallbackScrolltext: function(response) {
            this.textEnable = response.data.scrollenable; //.isChecked;
            console.log("textEnable: ",this.textEnable);
            this.textToScroll = response.data.scrolltext;
            this.date = response.data.scrolldate; 
            this.time = response.data.scrolltime;
            this.textRepeat = response.data.scrollrepeat;
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
		updateColorTemperature: function(color_temperature) {
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.open("POST", "/api/color_temperature");
			xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
			xmlhttp.send(JSON.stringify({ "color_temperature": color_temperature }));
		},
		setColourWheel: function(color) {
			var type;
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
			xmlhttp.send(JSON.stringify({ "blue": color.rgb.b, "green": color.rgb.g, "red": color.rgb.r , "type": type}));
		},
       	updateScrolltext: function() {
            console.log("updateScrolltext", this.textEnable, this.textToScroll, this.date, this.time, this.textRepeat)
			var xmlhttp = new XMLHttpRequest();
			xmlhttp.open("POST", "/api/scrolltext");
			xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
			xmlhttp.send(JSON.stringify({ scrollenable: this.textEnable, scrolltext: this.textToScroll, scrolldate: this.date, scrolltime: this.time, scrollrepeat: this.textRepeat}));
        }
	},
	beforeMount(){
		this.loadApi();
	}
});

IroColorPicker.on('input:move', vm.setColourWheel);
IroColorPicker.on('input:end', vm.setColourWheel);
