
window.addEventListener('DOMContentLoaded', (event) =>{

    var userSettings;

    var xhttp = new XMLHttpRequest();
    var url = 'http://localhost:8000/get-settings/';
    xhttp.open("GET", url, true);
    xhttp.send();

    xhttp.onload = function() {        
        userSettings = JSON.parse(JSON.parse(xhttp.responseText));
        // console.log(userSettings);
        // console.log(userSettings["input_device"]);
        document.getElementById("input-device-list").value = userSettings["input_device"];
        document.getElementById("output-device-list").value = userSettings["output_device"];
        document.getElementById("camera_device-list").value = userSettings["camera_device"];
        document.getElementById("name").value = userSettings["name"];
        document.getElementById("dex-on-start").checked = userSettings["dexter_on_startup"];
        document.getElementById("gest-on-start").checked = userSettings["gesture_on_startup"];
    };


    navigator.mediaDevices.enumerateDevices()
    .then(function(devices) {
        var inputList = document.getElementById("input-device-list");
        var outputList = document.getElementById("output-device-list");
        var cameraList = document.getElementById("camera_device-list");

        var i = 0;
        devices.forEach(function(device) {
            // console.log(device);
            var dev = document.createElement("option");
            dev.text = device.label
            dev.value = i.toString();
            ++i;
            if(device.kind == "audioinput") {
                inputList.add(dev);
            }
            else if(device.kind == "audiooutput") {
                outputList.add(dev);
            }
            else if (device.kind == "videoinput"){
                cameraList.add(dev);
            }
        });
    })

    // document.getElementById("settings-button").onclick => {
    //     console.log('here');
    //     //saveGeneralSettings();
    // }

});

function saveGeneralSettings()
{   
    var name = document.getElementById("name").value;
    var dexter_on_startup = document.getElementById("dex-on-start").checked;
    var gesture_on_startup = document.getElementById("gest-on-start").checked;

    // index value in list
    var output_device = document.getElementById("output-device-list").value;
    var input_device = document.getElementById("input-device-list").value;

    var camera_device = document.getElementById("camera_device-list").value;

    var settings = {
        "debug": "true",
        "name" : name,
        "dexter_on_startup": dexter_on_startup,
        "gesture_on_startup": gesture_on_startup,
        "output_device": output_device,
        "input_device": input_device,
        "camera_device": camera_device
    }
    
    console.log(JSON.stringify(settings));

    var xhttp = new XMLHttpRequest();
    var url = 'http://localhost:8000/update-settings/';
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-Type", "application/json")
    xhttp.send(JSON.stringify(settings));

    xhttp.onreadystatechange=(e)=>{
      console.log(xhttp.responseText);
    }
}