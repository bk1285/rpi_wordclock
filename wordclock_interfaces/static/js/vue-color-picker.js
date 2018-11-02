(function (global, factory) {
    typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
    typeof define === 'function' && define.amd ? define(factory) :
    (global.VueColorPicker = factory());
}(this, (function () { 'use strict';

    var commonjsGlobal = typeof window !== 'undefined' ? window : typeof global !== 'undefined' ? global : typeof self !== 'undefined' ? self : {};

    function createCommonjsModule(fn, module) {
    	return module = { exports: {} }, fn(module, module.exports), module.exports;
    }

    var colorWheel_umd = createCommonjsModule(function (module, exports) {
    (function (global, factory) {
        module.exports = factory();
    }(commonjsGlobal, (function () {
        /**
         * Modified version of Lea Verou's
         * {@link https://github.com/leaverou/conic-gradient conic-gradient}.
         *
         * @example
         * paintColorWheelToCanvas(document.querySelector('#canvas'), 250);
         *
         * @param   {HTMLCanvasElement} canvas Canvas to paint the color wheel
         * @param   {Number}            size   Color wheel radius in pixels
         * @returns {HTMLCanvasElement} canvas The passed canvas for easier chaining
         */
        function paintColorWheelToCanvas(canvas, size) {
            var half = size / 2;
            var radius = Math.sqrt(2) * half;
            var deg = Math.PI / 180;
            var pi2 = Math.PI * 2;

            canvas.width = canvas.height = size;
            var ctx = canvas.getContext('2d');

            // .02: To prevent empty blank line and corresponding moire
            // only non-alpha colors are cared now
            var thetaOffset = 0.5 * deg + 0.02;

            // Transform coordinate system so that angles start from the top left, like in CSS
            ctx.translate(half, half);
            ctx.rotate(-Math.PI / 2);
            ctx.translate(-half, -half);

            for (var i = 0; i < 360; i += 0.5) {
                ctx.fillStyle = 'hsl(' + i + ', 100%, 50%)';
                ctx.beginPath();
                ctx.moveTo(half, half);

                var beginArg = i * deg;
                var endArg = Math.min(pi2, beginArg + thetaOffset);

                ctx.arc(half, half, radius, beginArg, endArg);

                ctx.closePath();
                ctx.fill();
            }

            return canvas;
        }

        return paintColorWheelToCanvas;

    })));
    });

    var rotator_umd = createCommonjsModule(function (module, exports) {
    (function (global, factory) {
        module.exports = factory();
    }(commonjsGlobal, (function () {
        var TO_DEGREES = 180 / Math.PI;

        var normalizeAngle = function normalizeAngle(angle) {
            var mod = angle % 360;

            return mod < 0 ? 360 + mod : mod;
        };

        var getRotationFromCoords = function getRotationFromCoords(_ref, rect) {
            var x = _ref.x,
                y = _ref.y;

            var cx = rect.left + rect.width / 2;
            var cy = rect.top + rect.height / 2;

            return Math.atan2(y - cy, x - cx) * TO_DEGREES;
        };

        var noop = function noop() {};

        var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

        function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

        /**
         * Modified version of Denis Radin's
         * {@link https://github.com/PixelsCommander/Propeller Propeller}.
         */

        var Rotator = function () {
            function Rotator(element, options) {
                _classCallCheck(this, Rotator);

                this.active = false;
                this._angle = 0;
                this.element = element;
                this.element.style.willChange = 'transform';

                this.initOptions(options);
                this.updateCSS();
                this.bindHandlers();
                this.addListeners();
            }

            _createClass(Rotator, [{
                key: 'initOptions',
                value: function initOptions(options) {
                    options = options || {};

                    this.onRotate = options.onRotate || noop;
                    this.onDragStart = options.onDragStart || noop;
                    this.onDragStop = options.onDragStop || noop;

                    this._angle = options.angle || 0;
                }
            }, {
                key: 'bindHandlers',
                value: function bindHandlers() {
                    this.onRotationStart = this.onRotationStart.bind(this);
                    this.onRotated = this.onRotated.bind(this);
                    this.onRotationStop = this.onRotationStop.bind(this);
                }
            }, {
                key: 'addListeners',
                value: function addListeners() {
                    this.element.addEventListener('touchstart', this.onRotationStart, { passive: true });
                    this.element.addEventListener('touchmove', this.onRotated);
                    this.element.addEventListener('touchend', this.onRotationStop, { passive: true });
                    this.element.addEventListener('touchcancel', this.onRotationStop, { passive: true });

                    this.element.addEventListener('mousedown', this.onRotationStart, { passive: true });
                    this.element.addEventListener('mousemove', this.onRotated);
                    this.element.addEventListener('mouseup', this.onRotationStop, { passive: true });
                    this.element.addEventListener('mouseleave', this.onRotationStop);
                }
            }, {
                key: 'removeListeners',
                value: function removeListeners() {
                    this.element.removeEventListener('touchstart', this.onRotationStart);
                    this.element.removeEventListener('touchmove', this.onRotated);
                    this.element.removeEventListener('touchend', this.onRotationStop);
                    this.element.removeEventListener('touchcancel', this.onRotationStop);

                    this.element.removeEventListener('mousedown', this.onRotationStart);
                    this.element.removeEventListener('mousemove', this.onRotated);
                    this.element.removeEventListener('mouseup', this.onRotationStop);
                    this.element.removeEventListener('mouseleave', this.onRotationStop);
                }
            }, {
                key: 'destroy',
                value: function destroy() {
                    this.onRotationStop();
                    this.removeListeners();
                }
            }, {
                key: 'onRotationStart',
                value: function onRotationStart(event) {
                    this.initDrag();
                    this.onDragStart(event);
                }
            }, {
                key: 'onRotationStop',
                value: function onRotationStop() {
                    if (this.active) {
                        this.active = false;
                        this.onDragStop();
                    }

                    this.active = false;
                }
            }, {
                key: 'onRotated',
                value: function onRotated(event) {
                    if (this.active) {
                        event.preventDefault();

                        var point = event.targetTouches ? event.targetTouches[0] : event;

                        this.updateAngleToMouse({
                            x: point.clientX,
                            y: point.clientY
                        });

                        this.updateCSS();
                        this.onRotate(this._angle);
                    }
                }
            }, {
                key: 'setAngleFromEvent',
                value: function setAngleFromEvent(ev) {
                    var newAngle = getRotationFromCoords({ x: ev.clientX, y: ev.clientY }, this.element.getBoundingClientRect());

                    // atan2 gives values between -180 to 180 deg
                    // add 90 degrees offset so that it starts from 0 deg (or red)
                    // and then normalize negative values
                    this._angle = normalizeAngle(newAngle + 90);

                    this.updateCSS();
                    this.onRotate(this._angle);
                }
            }, {
                key: 'updateAngleToMouse',
                value: function updateAngleToMouse(newPoint) {
                    var newMouseAngle = getRotationFromCoords(newPoint, this.element.getBoundingClientRect());

                    if (!this.lastMouseAngle) {
                        this.lastElementAngle = this._angle;
                        this.lastMouseAngle = newMouseAngle;
                    }

                    this._angle = normalizeAngle(this.lastElementAngle + newMouseAngle - this.lastMouseAngle);
                }
            }, {
                key: 'initDrag',
                value: function initDrag() {
                    this.active = true;
                    this.lastMouseAngle = undefined;
                    this.lastElementAngle = undefined;
                }
            }, {
                key: 'updateCSS',
                value: function updateCSS() {
                    this.element.style.transform = 'rotate(' + this._angle + 'deg)';
                }
            }, {
                key: 'angle',
                get: function get() {
                    return this._angle;
                },
                set: function set(value) {
                    if (this._angle !== value) {
                        this._angle = normalizeAngle(value);
                        this.updateCSS();
                    }
                }
            }]);

            return Rotator;
        }();

        return Rotator;

    })));
    });

    var rotator;

    var ColorPicker = {render: function(){var _vm=this;var _h=_vm.$createElement;var _c=_vm._self._c||_h;return _c('div',{staticClass:"color-picker",attrs:{"tabindex":"0"},on:{"keyup":function($event){if(!('button' in $event)&&_vm._k($event.keyCode,"enter",13,$event.key,"Enter")){ return null; }return _vm.selectColor($event)},"keydown":[function($event){if(!('button' in $event)&&_vm._k($event.keyCode,"up",38,$event.key,["Up","ArrowUp"])&&_vm._k($event.keyCode,"right",39,$event.key,["Right","ArrowRight"])){ return null; }if('button' in $event && $event.button !== 2){ return null; }$event.preventDefault();_vm.rotate($event, true);},function($event){if(!('button' in $event)&&_vm._k($event.keyCode,"down",40,$event.key,["Down","ArrowDown"])&&_vm._k($event.keyCode,"left",37,$event.key,["Left","ArrowLeft"])){ return null; }if('button' in $event && $event.button !== 0){ return null; }$event.preventDefault();_vm.rotate($event, false);}]}},[_c('div',{staticClass:"palette",class:_vm.isPaletteIn ? 'is-in' : 'is-out',on:{"transitionend":_vm.toggleKnob}},[_c('canvas',{ref:"palette"})]),_vm._v(" "),_c('div',{ref:"rotator",staticClass:"rotator",class:{ 'disabled': _vm.isDisabled, 'dragging': _vm.isDragging },on:{"dblclick":function($event){if($event.target !== $event.currentTarget){ return null; }return _vm.rotateToMouse($event)},"transitionend":_vm.hidePalette}},[_c('div',{staticClass:"knob",class:_vm.isKnobIn ? 'is-in' : 'is-out'})]),_vm._v(" "),_c('div',{staticClass:"ripple",class:{ 'is-rippling': _vm.isRippling },style:({ borderColor: _vm.color }),on:{"animationend":_vm.stopRipple}}),_vm._v(" "),_c('button',{staticClass:"selector",class:{ 'is-pressed': _vm.isPressed },style:({ backgroundColor: _vm.color }),attrs:{"type":"button"},on:{"animationend":_vm.togglePicker,"click":_vm.selectColor}})])},staticRenderFns: [],
        name: 'vue-color-picker',
        props: {
            value: {
                default: function () { return ({ hue: 0, saturation: 100, luminosity: 50, alpha: 1 }); },
            },
            step: {
                default: 2,
            },
            mouseScroll: {
                default: false,
            },
            paletteHide: {
                default: false,
            },
        },
        data: function data() {
            return {
                isPaletteIn: true,
                isKnobIn: true,
                isPressed: false,
                isRippling: false,
                isDragging: false,
                isDisabled: false,
            }
        },
        computed: {
            color: function color() {
                var ref = this.value;
                var hue = ref.hue;
                var saturation = ref.saturation; if ( saturation === void 0 ) saturation = 100;
                var luminosity = ref.luminosity; if ( luminosity === void 0 ) luminosity = 50;
                var alpha = ref.alpha; if ( alpha === void 0 ) alpha = 1;

                return ("hsla(" + hue + ", " + saturation + "%, " + luminosity + "%, " + alpha + ")");
            }
        },
        watch: {
            'value.hue': function(newAngle, oldAngle) {
                if (newAngle != oldAngle) {
                    rotator.angle = newAngle;
                }
            },
        },
        mounted: function mounted() {
            var this$1 = this;

            if (this.mouseScroll) {
                this.$refs.rotator.addEventListener('wheel', this.onScroll);
            }

            colorWheel_umd(this.$refs.palette, this.$el.offsetWidth || 280);

            rotator = new rotator_umd(this.$refs.rotator, {
                angle: this.value.hue,
                onRotate: this.updateColor,
                onDragStart: function () {
                    this$1.isDragging = true;
                },
                onDragStop: function () {
                    this$1.isDragging = false;
                },
            });
        },
        methods: {
            onScroll: function onScroll(ev) {
                if (this.isDisabled)
                    { return; }

                ev.preventDefault();

                if (ev.deltaY > 0) {
                    rotator.angle += this.step;
                } else {
                    rotator.angle -= this.step;
                }

                this.updateColor(rotator.angle);
            },
            rotate: function rotate(ev, isIncrementing) {
                if (this.isDisabled)
                    { return; }

                var multiplier = isIncrementing ? 1 : -1;

                if (ev.ctrlKey) {
                    multiplier *= 6;
                } else if (ev.shiftKey) {
                    multiplier *= 3;
                }

                rotator.angle += this.step * multiplier;
                this.updateColor(rotator.angle);
            },
            updateColor: function updateColor(hue) {
                this.$emit('input', {
                    hue: hue,
                    saturation: this.value.saturation || 100,
                    luminosity: this.value.luminosity || 50,
                    alpha: this.value.alpha || 1,
                });
            },
            rotateToMouse: function rotateToMouse(ev) {
                if (this.isDisabled)
                    { return; }

                rotator.setAngleFromEvent(ev);
            },
            selectColor: function selectColor() {
                this.isPressed = true;

                if (!this.isDisabled) {
                    this.$emit('select', this.value);
                    this.isRippling = true;
                } else {
                    this.isPaletteIn = true;
                }
            },
            togglePicker: function togglePicker() {
                if (this.isDisabled) {
                    this.isKnobIn = true;
                } else {
						if (this.paletteHide) {
							this.isKnobIn = false; //Disable picker
						} else {
							this.isKnobIn = true; //Keep picker enabled
						}
                }

                this.isPressed = false;
            },
            hidePalette: function hidePalette() {
                if (!this.isDisabled) {
					if (this.paletteHide) {
						this.isPaletteIn = false; //Hide palette
					} else {
						this.isPaletteIn = true; //Palette stays visible
					}
                } else {
                    this.isDisabled = false;
                }
            },
            stopRipple: function stopRipple() {
                this.isRippling = false;
            },
            toggleKnob: function toggleKnob(ev) {
                // 'transitionend' fires for every transitioned property
                if (ev.propertyName === 'transform') {
                    if (this.isDisabled) {
                        this.isKnobIn = true;
                    } else {
                        this.isDisabled = true;
                    }
                }
            },
        },
        beforeDestroy: function beforeDestroy() {
            rotator.destroy();
            rotator = null;
        },
    };

    return ColorPicker;

})));
