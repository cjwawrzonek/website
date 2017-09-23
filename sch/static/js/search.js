$(document).ready(function() { 
    // General form submission and api search script

    $('#search-form').submit( function( event ) {
        var ids = decodeURIComponent($('#search-form').serialize().split('=')[1]).split(/,| /);
        ids = ids.filter(Number);
        event.preventDefault();

        if (ids.length > 0) {
            url = "./api/appts?id=";
            for (i = 0; i < ids.length; i++) {
                url = url.concat(ids[i].toString());
                if (i != ids.length) {
                    url = url.concat(',');
                }
            }
            $.ajax({
                type: "GET",
                url: url
            }).done(function(response) {
                displayResults(response);
            }).fail(function( jqXHR, textStatus ) {
                alert('Ajax error! '.concat(textStatus));
            }); 
        }
    });
});

var displayResults = function(results) {
    var rows = [];
    for (var i in results) {
        rows.push(buildRow(results[i]));
    }
    $(".results").empty().append(rows.join("\n"));
}

var buildRow = function(data) {
    var startmin = data.start % 60;
    if (startmin < 10) startmin = '0'.concat(startmin.toString());
    starmin = startmin.toString();

    var endmin = data.end % 60;
    if (endmin < 10) endmin = '0'.concat(endmin.toString());
    endmin = endmin.toString();

    // yeah yeah, no html in js...
    return'<div class="box">' +
        '<div class="row">' +
            '<div class="col-sm-8">' +
                '<h3 class="page-header">ID: ' + data.id + '</h3>' +
                '<p class="summary">Date: ' + data.date + '</p>' +
                '<p class="summary">Start Time: ' + Math.floor(data.start/60) + ':' + starmin + '</p>' +
                '<p class="summary">End Time: ' + Math.floor(data.end/60) + ':' + endmin + '</p>' +
            '</div>' +
        '</div>' +
    '</div>';
}

var getAllAppts = function() {
    $.ajax({
        type: "GET",
        url: './api/appts'
    }).done(function(response) {
        displayResults(response);
    }).fail(function( jqXHR, textStatus ) {
        alert('Ajax error! '.concat(textStatus));
    }); 
}