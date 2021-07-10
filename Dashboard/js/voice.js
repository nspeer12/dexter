function trainModel()
{
    var xhr = new XMLHttpRequest();
    var url = 'http://localhost:8000/train-assistant';
    xhr.open("POST", url);
    xhr.send();
}

function getIntents()
{
    var xhttp = new XMLHttpRequest();
    var url = 'http://localhost:8000/get-intents/';
    xhttp.open("GET", url);
    xhttp.send();

    xhttp.onload = function() {
        var data = JSON.parse(xhttp.responseText);
        var intents = data["intents"];

        console.log(intents);
    }
}