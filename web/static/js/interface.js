///import render_first_from './draw.js'
import {first_game_render, game_render_frame, tree_render} from './draw.js'

// Profile choser
$(document).ready(function () {

    //////////////////////
    /// Select options ///
    //////////////////////

    ////////////////////////////////////////////// On document load

    /// Load profiles for selection
    $.ajax({
        url: '/api/list_profiles',
        type: 'get',
        success: function (data) {

            $.each(data, function (key, modelName) {
                //Use the Option() constructor to create a new HTMLOptionElement.
                var option = new Option(modelName, modelName);
                //Convert the HTMLOptionElement into a JQuery object that can be used with the append method.
                $(option).html(modelName);
                //Append the option to our Select element.
                $("#profiles").append(option);
            });

            //Change the text of the default "loading" option.
            $('#loading_profiles').text('Select profile');

        }
    });

    ////////////////////////////////////////////// On profile select

    /// On change profile selection, load distillates list.
    $('#profiles').change(function () {
        $('#distillates').empty();
        $('#distillates').append(new Option("Select model", "-"));
        $.ajax({
            url: '/api/list_distillates',
            data: {profile: $('#profiles option:selected').text()},
            type: 'get',
            success: function (data) {

                $.each(data, function (key, modelName) {
                    //Use the Option() constructor to create a new HTMLOptionElement.
                    var option = new Option(modelName, modelName);
                    //Convert the HTMLOptionElement into a JQuery object that can be used with the append method.
                    $(option).html(modelName);
                    //Append the option to our Select element.
                    $("#distillates").append(option);
                });
            }
        });
    });

    ////////////////////////////////////////////// On type change

    // On change type list
    $('#type').change(function () {

    })



////////////////////////////////////////////// On type distillate

    /// On change distillate selection, load algorithm list.
    $('#distillates').change(function () {
        // Clear list
        $('#algorithms').empty();
        $('#algorithms').append(new Option("Select algorithm", "-"));
        //Change the text of the default "loading" option.
        //$('#distillates').append('Select distillate');
        $.ajax({
            url: '/api/list_algorithms',
            type: 'get',
            success: function (data) {

                $.each(data, function (key, modelName) {
                    //Use the Option() constructor to create a new HTMLOptionElement.
                    var option = new Option(modelName, modelName);
                    //Convert the HTMLOptionElement into a JQuery object that can be used with the append method.
                    $(option).html(modelName);
                    //Append the option to our Select element.
                    $("#algorithms").append(option);
                });


            }
        });
    });

    ////////////////////////////////////////////// On type algorithm

    /// On change distillate selection, load algorithm list.
    $('#algorithms').change(function () {
        // Clear list
        $('#environments').empty();
        $('#environments').append(new Option("Select environment", "-"));
        //Change the text of the default "loading" option.
        //$('#distillates').append('Select distillate');
        $.ajax({
            url: '/api/list_environments',
            type: 'get',
            success: function (data) {

                $.each(data, function (key, modelName) {
                    //Use the Option() constructor to create a new HTMLOptionElement.
                    var option = new Option(modelName, modelName);
                    //Convert the HTMLOptionElement into a JQuery object that can be used with the append method.
                    $(option).html(modelName);
                    //Append the option to our Select element.
                    $("#environments").append(option);
                });


            }
        });
    });


    /////////////////////////
    /// Start new session ///
    /////////////////////////
    $('#load_session').click(function () {

        // Request load_session
        $.ajax({
            url: '/api/load_session',
            data: {
                profile: $('#profiles option:selected').text(),
                distillate: $('#distillates option:selected').text(),
                algorithm: $('#algorithms option:selected').text(),
                environment: $('#environments option:selected').text()
            },
            type: 'get',
            success: function (data) {

                first_game_render(data['game']);
                tree_render(data['tree']);

            }


        });
    });


    /////////////////////////
    /// Step in a session ///
    /////////////////////////
    $('#session_step').click(function () {

        // Request session_step
        $.ajax({
            url: '/api/session_step',
            type: 'get',
            success: function (data) {

                tree_render(data['tree']);
                game_render_frame(data['game']);
            }
        });
    });


    //////////////////////
    /// Play a session ///
    //////////////////////

    var pause = false;

    function play() {
        // Request session_step
        $.ajax({
            url: '/api/session_step',
            type: 'get',
            success: function (data) {

                if (data['game'] == "done") {

                    console.log('Game over.')

                } else if (pause){

                    console.log('Game paused.')
                }

                else {
                    tree_render(data['tree']);
                    game_render_frame(data['game']);
                    play();
                }

            }
        })
    }


    $('#session_play').click(function () {
        pause = false;
        play();
    });

        $('#session_stop').click(function () {
        pause = true;
    });

});


