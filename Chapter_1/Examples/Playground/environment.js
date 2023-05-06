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
    #canvas_buffer;
    #effect_config;
    #start_at;
    #end_when;
    #current_source_id = 0;
    #current_effect_id = 0;
    #current_looper_id = -1;

    constructor(driver, canvas) {
        this.name = "Environment";
        this.env_gl = this;
        this.#start_at = 0;
        this.#driver = driver;
        this.#canvas = canvas;
        this.#source = new TestSources(driver, this.#canvas.width, this.#canvas.height);
        this.#effect = new TestProcess(driver, this.#canvas.width, this.#canvas.height);
        this.#effect_config = {
            gaussian_step: 1.0,
            gaussian_delta: 3.0,
        };
    }

    change_source(id) {
        this.#current_source_id = id;
    }

    change_effect(id) {
        this.#effect.config( this.#effect_config);
        this.#current_effect_id = id;
    }

    #source_render() {
        var current = ((new Date()).getTime() - this.#start_at) * 0.001;
        this.#canvas_aspect = this.#canvas.clientWidth / this.#canvas.clientHeight;
        this.#canvas_buffer.bind();

        if (this.#current_effect_id !== 0) this.#effect.bind();
        this.#source.render(this.#canvas_aspect, this.#current_source_id, current);
        if (this.#current_effect_id !== 0) this.#effect.unbind();
        this.#canvas_buffer.bind();
        if (this.#current_effect_id !== 0) this.#effect.render(this.#current_effect_id);
    }

    do_render() {
        function render_loop() {
            env_gl.do_render();
        }

        this.#source_render();
        this.#current_looper_id = requestAnimationFrame(render_loop);
    }

    do_initial() {
        this.#start_at = (new Date()).getTime();
        this.#canvas_aspect = this.#canvas.clientWidth / this.#canvas.clientHeight
        this.#canvas_buffer = tdl.framebuffers.getBackBuffer(this.#canvas)
        this.#driver.disable(this.#driver.BLEND);
        this.#driver.depthFunc(this.#driver.LEQUAL);
        this.#driver.blendFunc(this.#driver.SRC_ALPHA, this.#driver.ONE_MINUS_SRC_ALPHA);
        this.do_render();
        return true;
    }

    do_destroy() {
        cancelAnimationFrame(this.#current_looper_id);
        this.#end_when = (new Date()).getTime();
    }
}