var userGestures;

function populateGesturesTable() {
	let jsonData = `[ {"starting position" : "pointer", "ending position" : "close", "motion": "none", "name": "lower index", "function": "macro", "pre-defined function name":"Left Click", "macro":"Alt+F4", "path": ""},
        {"starting position" : "bunny ears", "ending position" : "close", "motion": "none", "name": "lower index and middle", "function": "script", "pre-defined function name":"Right Click", "macro":"", "path": "C:/script.py"},
        {"starting position" : "ok", "ending position" : "open", "motion": "none", "name": "Zoom in 2 Fingers", "function": "pre-defined function", "pre-defined function name":"Zoom In", "macro":"", "path": ""},
        {"starting position" : "open", "ending position" : "ok", "motion": "none", "name": "Zoom out 2 Fingers", "function": "pre-defined function", "pre-defined function name":"Zoom Out", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "3 fingers", "motion": "up", "name": "Slide up 3 Fingers", "function": "pre-defined function", "pre-defined function name":"Scroll Up", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "3 fingers", "motion": "down", "name": "Slide down 3 Fingers", "function": "pre-defined function", "pre-defined function name":"Scroll Down", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "3 fingers", "motion": "left", "name": "Slide left 3 Fingers", "function": "pre-defined function", "pre-defined function name":"Go Back", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "3 fingers", "motion": "right", "name": "Slide right 3 Fingers", "function": "pre-defined function", "pre-defined function name":"Go Forward", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "4 fingers", "motion": "right", "name": "Slide right 4 Fingers", "function": "pre-defined function", "pre-defined function name":"Switch App", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "4 fingers", "motion": "up", "name": "slide up 4 Fingers", "function": "pre-defined function", "pre-defined function name":"Switch Desktop", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "open", "motion": "left", "name": "Slide left 5 Fingers", "function": "pre-defined function", "pre-defined function name":"Slide App Left", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "open", "motion": "right", "name": "Slide right 5 Fingers", "function": "pre-defined function", "pre-defined function name":"Slide App Right", "macro":"", "path": ""},
        {"starting position" : "duck finger", "ending position" : "open", "motion": "none", "name": "Zoom out 5 Fingers", "function": "pre-defined function", "pre-defined function name":"Maximize App", "macro":"", "path": ""},
        {"starting position" : "open", "ending position" : "duck finger", "motion": "none", "name": "Zoom in 5 Fingers", "function": "pre-defined function", "pre-defined function name":"Minimize App", "macro":"", "path": ""},
        {"starting position" : "close", "ending position" : "open", "motion": "none", "name": "Open Hand", "function": "pre-defined function", "pre-defined function name":"Play", "macro":"", "path": ""},
        {"starting position" : "open", "ending position" : "close", "motion": "none", "name": "Close Hand", "function": "pre-defined function", "pre-defined function name":"Pause", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "close", "motion": "right", "name": "Sliding right Closed Fist", "function": "pre-defined function", "pre-defined function name":"Next Track", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "close", "motion": "left", "name": "Sliding left Closed Fist", "function": "pre-defined function", "pre-defined function name":"Previous Track", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "thumbs up", "motion": "up", "name": "Sliding up Thumbs up", "function": "pre-defined function", "pre-defined function name":"Increase Volume", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "thumbs down", "motion": "down", "name": "Sliding down Thumbs down", "function": "pre-defined function", "pre-defined function name":"Decrease Volume", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "thumbs up", "motion": "left", "name": "Sliding left Thumbs up", "function": "pre-defined function", "pre-defined function name":"Unmute", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "thumbs up", "motion": "right", "name": "Sliding right Thumbs up", "function": "pre-defined function", "pre-defined function name":"Unmute", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "thumbs down", "motion": "left", "name": "Sliding left Thumbs down", "function": "pre-defined function", "pre-defined function name":"Mute", "macro":"", "path": ""},
        {"starting position" : "none", "ending position" : "thumbs down", "motion": "right", "name": "Sliding right Thumbs down", "function": "pre-defined function", "pre-defined function name":"Mute", "macro":"", "path": ""}]`

    userGestures = JSON.parse(jsonData);
    let tableBody = document.getElementById("gestures-table-body");

    userGestures.forEach(gesture => {

        switch(gesture['function']) {
            case 'pre-defined function':
                $(tableBody).append(`<tr><td>${gesture["name"]}</td><td>${gesture["function"]}</td><td class="td-action">${gesture["pre-defined function name"]}</td></tr>`);
                break;
            case 'macro':
                $(tableBody).append(`<tr><td>${gesture["name"]}</td><td>${gesture["function"]}</td><td class="td-action">${gesture["macro"]}</td></tr>`);
                break;
            case 'script':
                $(tableBody).append(`<tr><td>${gesture["name"]}</td><td>${gesture["function"]}</td><td class="td-action">${gesture["path"]}</td></tr>`);
                break;
            default:
                $(tableBody).append(`<tr><td>${gesture["name"]}</td><td>${gesture["function"]}</td><td>Invalid Function Type</td></tr>`);
                break;
            }
    });
}

window.addEventListener('DOMContentLoaded', () => {

    populateGesturesTable();
    $("#gestures-table-body").on('click', ".td-action", (event) => {

    var $row = $(this).closest("tr");       // Finds the closest row <tr> 
    $tds = $row.find("td");             // Finds all children <td> elements
    
    $.each($tds, function() {               // Visits every single <td> element
        console.log($(this).text());        // Prints out the text within the <td>
    });
    });

    console.log(userGestures);

});