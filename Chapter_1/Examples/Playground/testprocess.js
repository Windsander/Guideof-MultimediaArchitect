/*
 * Copyright (c) 2023 Arikan.Li [Updated]
 * Created by Arikan.Li on 2014/8/24.
 * <last modified at> 2023/5/05 [commit:: prepare playground for Chapter_1 examples]
 *
 * provide effects based on Chapter_1 examples
 */

function calculate_gaussian_kernel(step, delta) {
    let n = step * 2 + 1;
    let kernel = new Float32Array(n * n);
    let factor_1 = 1.0 / (Math.sqrt(2.0 * Math.PI) * delta);
    let factor_2 = 1.0 / (2.0 * delta * delta);

    let normalize_div = 0;
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            let diff = (i - step) ^ 2 + (j - step) ^ 2;
            kernel[j + n * i] = factor_1 * Math.exp(-diff * factor_2);
            normalize_div += kernel[i];
        }
    }
    for (let i = 0; i < kernel.length; i++) {
        kernel[i] /= normalize_div;
    }
    return kernel;
}

class TestProcess {
    #driver;
    #source_buffer;
    #target_buffer;

    #attribute;
    #positions;
    #gaussian_kernel;

    #effect_gaussian;
    #effect_bilateral;
    #effect_sobel;
    #effect_NMS;

    constructor(driver, w, h) {
        this.#driver = driver;
        this.#source_buffer = tdl.framebuffers.createFramebuffer(w, h, true);
        this.#positions = driver.createBuffer();
        this.#attribute = new Float32Array([
            -1.0, -1.0, 0.0, //0.0, 0.0,
            +1.0, -1.0, 0.0, //1.0, 0.0,
            -1.0, +1.0, 0.0, //0.0, 1.0,
            +1.0, +1.0, 0.0, //1.0, 1.0
        ]);

        this.#effect_gaussian = utils.addShaderProg(driver, 'filter_common_vs', 'filter_gaussian_ps');
        // this.#effect_bilateral = utils.addShaderProg(driver, 'filter_common_vs', 'filter_bilateral_ps');
        // this.#effect_sobel = utils.addShaderProg(driver, 'filter_common_vs', 'filter_sobel_ps');
        // this.#effect_NMS = utils.addShaderProg(driver, 'filter_common_vs', 'filter_NMS_ps');
    }

    #draw_effect(effect_program) {
        // this.#driver.disable(gl.DEPTH_TEST);
        // this.#driver.disable(gl.CULL_FACE);
        // this.#driver.disable(gl.BLEND);
        this.#driver.activeTexture(gl.TEXTURE0);
        this.#driver.bindBuffer(this.#driver.ARRAY_BUFFER, this.#positions);
        this.#driver.bufferData(this.#driver.ARRAY_BUFFER, this.#attribute, this.#driver.STATIC_DRAW);
        this.#driver.enableVertexAttribArray(effect_program.attribLoc["position"]);
        this.#driver.vertexAttribPointer(effect_program.attribLoc["position"], 3, this.#driver.FLOAT, false, 0, 0);
        this.#driver.drawArrays(this.#driver.TRIANGLE_STRIP, 0, 4)
    }

    config(effect_params) {
        this.#gaussian_kernel = calculate_gaussian_kernel(effect_params.gaussian_step, effect_params.gaussian_delta);
    }

    bind() {
        this.#source_buffer.bind();
    }

    unbind() {
        this.#source_buffer.unbind();
    }

    render(effect_id) {
        switch (effect_id) {
            case 0: {
                break;
            }
            case 1: {
                this.#effect_gaussian.use();
                this.#effect_gaussian.setUniform("target_texture", this.#source_buffer.texture)
                this.#effect_gaussian.setUniform("gaussian_matrix", this.#gaussian_kernel)
                this.#draw_effect(this.#effect_gaussian);
                break;
            }
            case 2: {

                break;
            }
            case 3: {

                break;
            }
            case 4: {

                break;
            }
            default: {

                break;
            }
        }
    }
}