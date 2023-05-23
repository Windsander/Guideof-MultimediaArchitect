/*
 * Copyright (c) 2023 Arikan.Li [Updated]
 * Created by Arikan.Li on 2014/8/24.
 * <last modified at> 2023/5/05 [commit:: prepare playground for Chapter_1 examples]
 *
 * tiny tools for reading glsl from files directly
 */

utils = {};

utils.allShaders = {};
utils.SHADER_TYPE_VERTEX = "x-shader/x-vertex";
utils.SHADER_TYPE_FRAGMENT = "x-shader/x-fragment";

utils.addShaderProg = function (gl, vs, fs) {
    utils.loadShader(vs, utils.SHADER_TYPE_VERTEX);
    utils.loadShader(fs, utils.SHADER_TYPE_FRAGMENT);

    var bits_vs = utils.getShader(gl, vs);
    var bits_fs = utils.getShader(gl, fs);

    return tdl.programs.loadProgram(bits_vs, bits_fs);
};

utils.loadShader = function (name, type) {
    var cache, shader;

    $.ajax({
        async: false, // need to wait... todo: deferred?
        url: "../Shaders/" + name + '.glsl', //todo: use global config for shaders folder?
        success: function (result) {
            cache = {id: name, text: result, type: type};
        }
    });

    // store in global cache
    utils.allShaders[name] = cache;
};

utils.getShader = function (gl, id) {
    //get the shader object from our main.shaders repository
    var shaderObj = utils.allShaders[id];
    return shaderObj.text;
};//end:getShader
