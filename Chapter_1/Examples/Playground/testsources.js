/*
 * Copyright (c) 2023 Arikan.Li [Updated]
 * Created by Arikan.Li on 2014/8/24.
 * <last modified at> 2023/5/05 [commit:: prepare playground for Chapter_1 examples]
 *
 * provide Classic 4D-Cube Rotation-Anim as Basement-input
 */

class TestSources {
    #driver
    #model;
    #arrays;
    #program;
    #textures;

    #proj;
    #view;
    #world;
    #temp_vps;
    #temp_wvp;

    #observe_from;
    #targets_upon;
    #orient_up;

    constructor(driver, w, h) {
        this.#driver = driver;
        this.#textures = [];
        this.#program = utils.addShaderProg(driver, 'source_vs', 'source_fs');
        this.#arrays = tdl.primitives.createFlaredCube(0.75, 3.0, 800);
        this.#arrays.texcoord = this.#arrays.texCoord;
        this.#model = new tdl.models.Model(this.#program, this.#arrays, this.#textures);

        this.#proj = new Float32Array(16);
        this.#view = new Float32Array(16);
        this.#world = new Float32Array(16);
        this.#temp_vps = new Float32Array(16);
        this.#temp_wvp = new Float32Array(16);

        this.#observe_from = new Float32Array([+0.0, 0.0, 3.0]);
        this.#targets_upon = new Float32Array([-0.3, 0.0, 0.0]);
        this.#orient_up = new Float32Array([0.0, +1.0, 0.0]);
    }

    render(aspect, type, time) {
        tdl.fast.matrix4.lookAt(this.#view, this.#observe_from, this.#targets_upon, this.#orient_up);
        tdl.fast.matrix4.perspective(this.#proj, tdl.math.degToRad(60), aspect, 0.1, 100);
        tdl.fast.matrix4.rotationY(this.#world, time * 0.2);
        tdl.fast.matrix4.mul(this.#temp_vps, this.#view, this.#proj);
        tdl.fast.matrix4.mul(this.#temp_wvp, this.#world, this.#temp_vps);
        let cube_configs = {
            u_type: type,
            u_time: time,
            u_color_major: TestSources.#hsv2rgb((time * 0.10100) % 1.0, 0.8, 0.1, 1.0),
            u_color_minor: TestSources.#hsv2rgb((time * 0.22124) % 1.0, 0.7, 0.1, 0.0),
        };
        let cube_posture = {
            u_wvp: this.#temp_wvp
        };

        this.#driver.clearColor(0.1, 0.2, 0.3, 1);
        this.#driver.clear(this.#driver.COLOR_BUFFER_BIT | this.#driver.DEPTH_BUFFER_BIT);
        this.#driver.disable(this.#driver.DEPTH_TEST);
        this.#driver.disable(this.#driver.CULL_FACE);
        this.#driver.enable(this.#driver.BLEND);
        this.#driver.blendFunc(this.#driver.ONE, this.#driver.ONE);
        this.#model.drawPrep(cube_configs);
        this.#model.draw(cube_posture);
        this.#driver.disable(this.#driver.BLEND);
    }

    static #hsv2rgb(h, s, v, a) {
        h *= 6
        let i = Math.floor(h);
        let f = h - i;
        if (!(i & 1)) f = 1 - f; // reverse when even
        let m = v * (1 - s);
        let n = v * (1 - s * f);
        switch (i) {
            case 0:
                return [v, n, m, a];
            case 1:
                return [n, v, m, a];
            case 2:
                return [m, v, n, a];
            case 3:
                return [m, n, v, a];
            case 4:
                return [n, m, v, a];
            case 5:
                return [v, m, n, a];
            case 6:
                return [v, n, m, a];
        }
    }
}