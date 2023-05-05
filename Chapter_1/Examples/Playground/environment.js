/*
 * Copyright (c) 2023 Arikan.Li [Updated]
 * Created by Arikan.Li on 2014/8/24.
 * <last modified at> 2023/5/05 [commit:: prepare playground for Chapter_1 examples]
 *
 * provide WebGL Environment
 */

tdl.require('tdl.fast');
tdl.require('tdl.math');
tdl.require('tdl.primitives');
tdl.require('tdl.shader');
tdl.require('tdl.programs');
tdl.require('tdl.log');
tdl.require('tdl.models');
tdl.require('tdl.buffers');
tdl.require('tdl.framebuffers');
tdl.require('tdl.textures');
tdl.require('tdl.webgl');

class Environment {
    // self-mark
    env_gl;

    // basement
    #driver;
    #canvas;
    #source;
    #effect;

    // renderer-control
    #canvas_aspect;
    #canvas_cacher;
    #start_at;
    #end_when;
    #current_processor = 0;
    #current_looper_id = -1;

    constructor(driver, canvas) {
        this.name = "Environment";
        this.env_gl = this;
        this.#start_at = 0;
        this.#driver = driver;
        this.#canvas = canvas;
        this.#source = new TestSources(driver);
        // this.#effect = new TestProcessor(this.#canvas.width, this.#canvas.height)
    }

    #effect_starts() {
        if (this.#current_processor !== 0) {
            this.#effect.begin();
        }
    }

    #source_render() {
        var current = ((new Date()).getTime() - this.#start_at) * 0.001;
        this.#source.render(this.#driver, this.#canvas_aspect, current);
        this.#canvas_aspect = this.#canvas.clientWidth / this.#canvas.clientHeight;
    }

    #effect_finish() {
        switch (postproc) {
            case 1:
                this.#effect.end(framebuffer, this.#effect.hypnoGlow, {x: 3, y: 3, sub: 0.2});
                break;
            case 2:
                this.#effect.end(framebuffer, this.#effect.blur, {x: 2, y: 2});
                break;
            case 3:
                this.#effect.end(framebuffer, this.#effect.radialBlur, {strength: 0.3, glow: 1.0});
                break;
        }
    }

    render_loop() {
        function do_render() {
            env_gl.render_loop();
        }

        // this.#effect_starts();
        this.#source_render();
        // this.#effect_finish();

        this.#current_looper_id = requestAnimationFrame(do_render);
    }

    change_effect(id) {
        this.#current_processor = id;
    }

    do_initial() {
        this.#start_at = (new Date()).getTime();
        this.#canvas_aspect = this.#canvas.clientWidth / this.#canvas.clientHeight
        this.#canvas_cacher = tdl.framebuffers.getBackBuffer(this.#canvas)
        this.#driver.disable(this.#driver.BLEND);
        this.#driver.depthFunc(this.#driver.LEQUAL);
        this.#driver.blendFunc(this.#driver.SRC_ALPHA, this.#driver.ONE_MINUS_SRC_ALPHA);
        this.render_loop();
        return true;
    }

    do_destroy() {
        cancelAnimationFrame(this.#current_looper_id);
        this.#end_when = (new Date()).getTime();
    }
}