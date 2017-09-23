$(document).ready(function() { 
    // General form submission and api call to create new appt

    $('#create-form').submit( function( event ) {
        var form = $('#create-form').serializeArray();
        var data = {};
        for (var i = 0; i < form.length; i++){
            data[form[i]['name']] = form[i]['value'];
        }
        event.preventDefault();

        // Check date format (must of of form MM-DD-YYYY)
        var regx = new RegExp('^[0-9]{1,2}-[0-9]{1,2}-[0-9]{4}$');
        if (regx.test(data.date) !== true) {
            alert('Incorrect date format. Must be of the form MM-DD-YYYY');
            return;
        }

        // Check format of start / end (must of of form *#:*#)
        regx = new RegExp('^[0-9]{1,2}:[0-9]{1,2}$');
        if (regx.test(data.start) !== true) {
            alert('Incorrect format for start time. Must be of the form hh:mm');
            return;
        } else if (regx.test(data.end) !== true) {
            alert('Incorrect format for end time. Must be of the form hh:mm');
            return;
        }

        // Parse the start and end times into ints
        if (data.hasOwnProperty('start')) {
            var starttime = data.start.split(':');
            data.start = (60 * parseInt(starttime[0])) + parseInt(starttime[1]);
        }
        if (data.hasOwnProperty('end')) {
            var endtime = data.end.split(':');
            data.end = (60 * parseInt(endtime[0])) + parseInt(endtime[1]);
        }
        $.ajax({
            type: 'POST',
            url:  './api/appts',
            data: JSON.stringify([data]),
            contentType: 'application/json'
        }).done(function(response) {
            alert('Succesfully created your appointment.')
        }).fail(function( jqXHR, textStatus ) {
            alert('Ajax error! '.concat(textStatus));
        }); 
    });
});