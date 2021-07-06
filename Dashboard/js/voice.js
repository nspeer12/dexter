function trainModel()
{
    console.log('here');
    var xhttp = new XMLHttpRequest();
    var url = "http://localhost:8000/train-assistant/";
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send();
}

function getIntents()
{
    var xhttp = new XMLHttpRequest();
    // update elements on server response
    xhttp.onreadystatechange = function() {
      if (this.readyState == 4 && this.status == 200) {
        console.log('here');
        //console.log(this.responseText);
        //document.getElementById("test").innerHTML = this.responseText;
        var intents = JSON.parse(this.responseText);
        console.log(intents['intents'])
        document.getElementById("test").innerHTML = "poop";
      }
    };


    
    var url = "http://localhost:8000/get-intents/";
    xhttp.open("GET", url, false);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send();
    console.log(xhttp.status)
    //document.getElementById("test").innerHTML = xhr.responseText;
}