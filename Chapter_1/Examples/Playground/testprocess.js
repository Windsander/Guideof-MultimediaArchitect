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
 * Calculate laplacian kernel for wight matrix
 *
 * @param step Convolution Kernel step
 * @param way_count Laplacian Kernel Direction Count, is 2^n
 * @param str_factor Laplacian Intensity Factor
 */
function calculate_laplacian_kernel(step, way_count, str_factor) {
    let n = step * 2 + 1;
    let max_way = (n - 1) * 2;
    let cur_way = Math.min(way_count, max_way);
    let way_step = Math.floor(max_way / cur_way);
    let kernel = new Float32Array(n * n);

    for (let i = 0; i < n * n; i = i + way_step) {
        kernel[i] = str_factor;
    }
    kernel[step + n * step] = -cur_way * (n - 1) * str_factor;
    return kernel;
}

/**
 * Calculate sobel kernel for wight matrix
 *
 * @param use_horizontal Sobel Kernel Direction [horizontal/vertical]
 * @param str_factor Sobel Intensity Factor
 */
function calculate_sobel_kernel(use_horizontal, str_factor) {
    let kernel = new Float32Array(use_horizontal ? [
        -1.0, 0.0, +1.0,
        -2.0, 0.0, +2.0,
        -1.0, 0.0, +1.0
    ] : [
        +1.0, +2.0, +1.0,
        0.0, 0.0, 0.0,
        -1.0, -2.0, -1.0
    ])

    for (let i = 0; i < 9; i++) {
        kernel[i] *= str_factor;
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
    #laplacian_2way_kernel;
    #laplacian_4way_kernel;
    #sobel_kernel_x;
    #sobel_kernel_y;

    #effect_gaussian_norm;
    #effect_gaussian_fast;
    #effect_bilateral_norm;
    #effect_bilateral_fast;
    #effect_laplacian_2way;
    #effect_laplacian_4way;
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

        this.#effect_gaussian_norm = utils.addShaderProg(driver, 'common_filter_vs', 'filter_gaussian_norm_ps');
        this.#effect_gaussian_fast = utils.addShaderProg(driver, 'common_filter_vs', 'filter_gaussian_fast_ps');
        this.#effect_bilateral_norm = utils.addShaderProg(driver, 'common_filter_vs', 'filter_bilateral_norm_ps');
        this.#effect_bilateral_fast = utils.addShaderProg(driver, 'common_filter_vs', 'filter_bilateral_fast_ps');
        this.#effect_laplacian_2way = utils.addShaderProg(driver, 'common_filter_vs', 'filter_laplacian_2way_ps');
        this.#effect_laplacian_4way = utils.addShaderProg(driver, 'common_filter_vs', 'filter_laplacian_4way_ps');
        this.#effect_sobel = utils.addShaderProg(driver, 'common_filter_vs', 'filter_sobel_norm_ps');
        // this.#effect_NMS = utils.addShaderProg(driver, 'common_filter_vs', 'filter_NMS_ps');
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
        this.#laplacian_2way_kernel = calculate_laplacian_kernel(
            effect_params.laplacian_step,
            2,
            effect_params.laplacian_factor
        );
        this.#laplacian_4way_kernel = calculate_laplacian_kernel(
            effect_params.laplacian_step,
            4,
            effect_params.laplacian_factor
        );
        this.#sobel_kernel_x = calculate_sobel_kernel(true, effect_params.sobel_factor);
        this.#sobel_kernel_y = calculate_sobel_kernel(false, effect_params.sobel_factor);
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
                this.#effect_bilateral_fast.use();
                this.#effect_bilateral_fast.setUniform("target_texture", this.#source_buffer.texture)
                this.#effect_bilateral_fast.setUniform("gaussian_matrix", this.#gaussian_kernel)
                this.#effect_bilateral_fast.setUniform("gaussian_range", this.#bilateral_range)
                this.#effect_bilateral_fast.setUniform("pixel_bias", this.#pixel_bias)
                this.#draw_effect(this.#effect_bilateral_fast);
                break;
            }
            case 5: {
                this.#effect_laplacian_2way.use();
                this.#effect_laplacian_2way.setUniform("target_texture", this.#source_buffer.texture)
                this.#effect_laplacian_2way.setUniform("laplacian_matrix", this.#laplacian_2way_kernel)
                this.#effect_laplacian_2way.setUniform("pixel_bias", this.#pixel_bias)
                this.#draw_effect(this.#effect_laplacian_2way);
                break;
            }
            case 6: {
                this.#effect_laplacian_4way.use();
                this.#effect_laplacian_4way.setUniform("target_texture", this.#source_buffer.texture)
                this.#effect_laplacian_4way.setUniform("laplacian_matrix", this.#laplacian_4way_kernel)
                this.#effect_laplacian_4way.setUniform("pixel_bias", this.#pixel_bias)
                this.#draw_effect(this.#effect_laplacian_4way);
                break;
            }
            case 7: {
                this.#effect_sobel.use();
                this.#effect_sobel.setUniform("target_texture", this.#source_buffer.texture)
                this.#effect_sobel.setUniform("sobel_matrix_x", this.#sobel_kernel_x)
                this.#effect_sobel.setUniform("sobel_matrix_y", this.#sobel_kernel_y)
                this.#effect_sobel.setUniform("pixel_bias", this.#pixel_bias)
                this.#draw_effect(this.#effect_sobel);
                break;
            }
            case 8: {

                break;
            }
            default: {

                break;
            }
        }
    }
}