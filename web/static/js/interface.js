// Profile choser
$(document).ready(function () {

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

    /// On change profile selection, load distillates list.
    $('#profiles').change(function () {
        // Clear list
        $('#distillates').empty();
        //Change the text of the default "loading" option.
        //$('#distillates').append('Select distillate');
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


});

