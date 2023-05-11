/*
 * Copyright (c) 2023 Arikan.Li [Updated]
 * Created by Arikan.Li on 2014/8/24.
 * <last modified at> 2023/5/05 [commit:: prepare playground for Chapter_1 examples]
 *
 * provide effects based on Chapter_1 examples
 */

/*================================== Prepare ==================================*/
/**
 * Calculate single pixel bias for kernel offset
 *
 * @param width Input Texture(Screen) Width
 * @param height Input Texture(Screen) Height
 */
function pixel_bias(width, height) {
    return new Float32Array([
        1.0 / width, 1.0 / height
    ]);
}

/**
 * Calculate gaussian kernel for wight matrix
 *
 * @param step Convolution Kernel step
 * @param delta Gaussian Distribution Factor
 */
function calculate_gaussian_kernel(step, delta) {
    let n = step * 2 + 1;
    let kernel = new Float32Array(n * n);
    let factor_1 = 1.0 / (Math.sqrt(2.0 * Math.PI) * delta);
    let factor_2 = 1.0 / (2.0 * delta * delta);

    let normalize_div = 0;
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            let diff = Math.pow(i - step, 2) + Math.pow(j - step, 2);
            kernel[j + n * i] = factor_1 * Math.exp(-diff * factor_2);
            normalize_div += kernel[i];
        }
    }
    for (let i = 0; i < kernel.length; i++) {
        kernel[i] /= normalize_div;
    }
    return kernel;
}

/**
 * Calculate gaussian kernel for wight matrix
 *
 * @param step Convolution Kernel step
 * @param delta_d Gaussian Distribution Factor
 */
function calculate_bilateral_kernel(step, delta_d, delta_r) {
    let n = step * 2 + 1;
    let kernel = new Float32Array(n * n);
    let factor_1 = 1.0 / (Math.sqrt(2.0 * Math.PI) * delta_d * delta_r);
    let factor_d = 1.0 / (2.0 * delta_d * delta_d);
    let factor_r = 1.0 / (2.0 * delta_r * delta_r);

    let normalize_div = 0;
    for (let i = 0; i < n; i++) {
        for (let j = 0; j < n; j++) {
            let diff = Math.pow(i - step, 2) + Math.pow(j - step, 2);
            kernel[j + n * i] = factor_1 * Math.exp(-diff * factor_d);
            normalize_div += kernel[i];
        }
    }
    for (let i = 0; i < kernel.length; i++) {
        kernel[i] /= normalize_div;
    }
    return kernel;
}

/*================================== Process ==================================*/

class TestProcess {
    #driver;
    #source_buffer;
    #target_buffer;

    #attribute;
    #positions;
    #pixel_bias;
    #gaussian_kernel;
    #bilateral_range;

    #effect_gaussian_norm;
    #effect_gaussian_fast;
    #effect_bilateral_norm;
    #effect_sobel;
    #effect_NMS;

    constructor(driver, w, h) {
        this.#driver = driver;
        this.#source_buffer = tdl.framebuffers.createFramebuffer(w, h, true);
        this.#positions = driver.createBuffer();
        this.#pixel_bias = new Float32Array([
            1.0 / w, 1.0 / h
        ]);
        this.#attribute = new Float32Array([
            -1.0, -1.0, 0.0, //0.0, 0.0,
            +1.0, -1.0, 0.0, //1.0, 0.0,
            -1.0, +1.0, 0.0, //0.0, 1.0,
            +1.0, +1.0, 0.0, //1.0, 1.0
        ]);

        this.#effect_gaussian_norm = utils.addShaderProg(driver, 'filter_common_vs', 'filter_gaussian_norm_ps');
        this.#effect_gaussian_fast = utils.addShaderProg(driver, 'filter_common_vs', 'filter_gaussian_fast_ps');
        this.#effect_bilateral_norm = utils.addShaderProg(driver, 'filter_common_vs', 'filter_bilateral_norm_ps');
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
        this.#bilateral_range = effect_params.gaussian_range;
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
                this.#effect_gaussian_norm.use();
                this.#effect_gaussian_norm.setUniform("target_texture", this.#source_buffer.texture)
                this.#effect_gaussian_norm.setUniform("gaussian_matrix", this.#gaussian_kernel)
                this.#effect_gaussian_norm.setUniform("pixel_bias", this.#pixel_bias)
                this.#draw_effect(this.#effect_gaussian_norm);
                break;
            }
            case 2: {
                this.#effect_gaussian_fast.use();
                this.#effect_gaussian_fast.setUniform("target_texture", this.#source_buffer.texture)
                this.#effect_gaussian_fast.setUniform("gaussian_matrix", this.#gaussian_kernel)
                this.#effect_gaussian_fast.setUniform("pixel_bias", this.#pixel_bias)
                this.#draw_effect(this.#effect_gaussian_fast);
                break;
            }
            case 3: {
                this.#effect_bilateral_norm.use();
                this.#effect_bilateral_norm.setUniform("target_texture", this.#source_buffer.texture)
                this.#effect_bilateral_norm.setUniform("gaussian_matrix", this.#gaussian_kernel)
                this.#effect_bilateral_norm.setUniform("gaussian_range", this.#bilateral_range)
                this.#effect_bilateral_norm.setUniform("pixel_bias", this.#pixel_bias)
                this.#draw_effect(this.#effect_bilateral_norm);
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