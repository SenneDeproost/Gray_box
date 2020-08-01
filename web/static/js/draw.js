var GAMEVIEW_DIMS = null;
var GAME_DIMS = null;
var GAMEVIEW_INITS = null;

var TREEVIEW_DIMS = null;
var TREE_DIMS = null;
var TREEVIEW_INITS = null;

////////////////////
/// INITIALIZERS ///
////////////////////

function clear_game_view() {
    var canvas = document.getElementById("gameview");
    var ctx = canvas.getContext("2d");
    ctx.beginPath();
    ctx.rect(0, 0, GAMEVIEW_DIMS['width'], GAMEVIEW_DIMS['height']);
    ctx.fillStyle = "lightgrey";
    ctx.fill();
}

function clear_tree_view() {
    var canvas = document.getElementById("treeview");
    var ctx = canvas.getContext("2d");
    ctx.beginPath();
    ctx.rect(0, 0, ctx.canvas.clientWidth, ctx.canvas.clientHeight);
    ctx.fillStyle = "white";
    ctx.fill();
}

function calc_inits(item_h, item_w, view_h, view_w) {
    var inits = {};
    inits['x0'] = view_w / 2 - item_w / 2;
    inits['y0'] = view_h / 2 - item_h / 2;
    inits['x1'] = view_w / 2 + item_w / 2;
    inits['y1'] = view_h / 2 + item_h / 2;
    return inits;
}

function calc_view_dims(view) {
    var canvas = document.getElementById(view);
    var width = canvas.width;
    var height = canvas.height;
    var dims = {};
    dims['width'] = width;
    dims['height'] = height;
    return dims;
}

function to_PNG(b64) {
    var img = new Image();
    img.src = "data:image/png;base64," + b64;
    return img;
}

function to_SVG(b64) {
    var img = new Image();
    img.src = "data:image/svg+xml;base64," + b64;
    return img;
}

function calc_image_dims(image, mul) {
    var dims = {};
    dims['width'] = image.width * mul;
    dims['height'] = image.height * mul;
    return dims;
}


////////////
/// PLAY ///
///////////

export function first_game_render(b64) {
    var gamecanvas = document.getElementById("gameview");
    var gamectx = gamecanvas.getContext("2d");

    var img = to_PNG(b64);

    img.onload = function () {
        GAME_DIMS = calc_image_dims(img, 1.50);
        GAMEVIEW_DIMS = calc_view_dims('gameview');
        GAMEVIEW_INITS = calc_inits(GAME_DIMS['height'], GAME_DIMS['width'], GAMEVIEW_DIMS['width'], GAMEVIEW_DIMS['height']);
        clear_game_view();
        gamectx.drawImage(this, GAMEVIEW_INITS['x0'], GAMEVIEW_INITS['y0'], GAME_DIMS['width'], GAME_DIMS['height']);

    }
}

export function game_render_frame(b64) {
    var gamecanvas = document.getElementById("gameview");
    var gamectx = gamecanvas.getContext("2d");

    var img = to_PNG(b64);

    img.onload = function () {
        clear_game_view();
        gamectx.drawImage(this, GAMEVIEW_INITS['x0'], GAMEVIEW_INITS['y0'], GAME_DIMS['width'], GAME_DIMS['height']);

    }
}

////////////
/// VIEW ///
///////////

export function tree_render(b64){
    var treecanvas = document.getElementById("treeview");
    var treectx = treecanvas.getContext("2d");

    var img = to_SVG(b64);

    img.onload = function () {
        clear_tree_view();
        treectx.drawImage(this, 0, 0, ctx.canvas.clientWidth, ctx.canvas.clientHeight);

    }
}

