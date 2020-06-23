
var GAMEVIEW_DIMS = null;
var GAME_DIMS = null;
var GAMEVIEW_INITS = null;


function clear_game_view(){
    var canvas = document.getElementById("gameview");
    var ctx = canvas.getContext("2d");

    ctx.beginPath();
    ctx.rect(0, 0, GAMEVIEW_WIDTH, GAMEVIEW_HEIGHT);
    ctx.fillStyle = "lightgrey";
    ctx.fill();
}

function calc_inits(item_h, item_w, view_h, view_w){
    var inits = {};
    inits['x0'] = view_w/2 - item_w/2;
    inits['y0'] = view_h/2 - item_h/2;
    inits['x1'] = view_w/2 + item_w/2;
    inits['y1'] = view_h/2 + item_h/2;
    return inits;
}

function calc_view_dims(view){
    var canvas = document.getElementById(view);
    var width = canvas.width;
    var height = canvas.height;
    var dims = {};
    dims['width'] = width;
    dims['height'] = height;
    return dims;
}

function to_PNG(b64){
    var img = new Image();
    img.src = "data:image/png;base64," + b64;
    return img;
}

function calc_image_dims(image, mul){
    var dims = {};
    dims['width'] = image.width * mul;
    dims['height'] = image.height * mul;
    return dims;
}










//// TEST ZONE
$(document).ready(function () {
    var gamecanvas = document.getElementById("gameview");
    var gamectx = gamecanvas.getContext("2d");

    var img = "iVBORw0KGgoAAAANSUhEUgAAAKAAAADSCAIAAABCR1ywAAACh0lEQVR4nO3bPUoDURhAUSMD2lu4CDdgaZeVWNq6GVeSzjIbcBEp0sfOJsg0EgPODLmeUwXyMw8uHw/mTVZXP3h5ffjpLS7Ias6Qz0+nr/X2/jHDSuZx+Nyc/MztzXrSNVxP+ussTuA4geOGpS483mt/szdfuvFe+5u9+a+Y4DiB4wSOEzhO4DiB4wSOEzhO4DiB4wSOW+xe9H+4/zw25/3nMRMcJ3CcwHGzPpPF/ExwnMBxw3a3X3oNTMgExwkcJ3CcwHECxwkcJ3CcwHECxw2P93dLr4EJmeA4geMEjhM4TuA4geMEjhM4TuA4geOOgbe7vafvkkxwnMBxAscd/x/s0LDKBMcJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHDcsvQBOO3xuvl/f3qzP+q4JjhM4TuA4geMEjhM4TuA4geMEjhM4TuA4geMEjhM4TuA458EX4Nwz4DETHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHCdwnMBxAscJHDdsd/ul18CETHCcwHECxwkcJ3CcwHECxwkcJ3CcwHECxwkcJ3CcwHECx30Bu1ci6JJ73gAAAAAASUVORK5CYII="
    img = to_PNG(img);

    img.onload = function() {
        GAME_DIMS = calc_image_dims(img, 1.75);
        GAMEVIEW_DIMS = calc_view_dims('gameview');
        GAMEVIEW_INITS = calc_inits(GAME_DIMS['height'], GAME_DIMS['width'], GAMEVIEW_DIMS['width'], GAMEVIEW_DIMS['height']);
        gamectx.drawImage(this, GAMEVIEW_INITS['x0'], GAMEVIEW_INITS['y0'], GAME_DIMS['width'], GAME_DIMS['height']);
        console.log(GAME_DIMS);
}


})