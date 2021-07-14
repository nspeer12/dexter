
window.addEventListener('DOMContentLoaded', (event) =>{
    navigator.mediaDevices.enumerateDevices()
    .then(function(devices) {

        var outputList = document.getElementById("output-device-list");
        var inputList = document.getElementById("input-device-list");
        var cameraList = document.getElementById("camera_device-list")

        var i = 0;
        devices.forEach(function(device) {
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
    var dexter_on_startup = document.getElementById("dex-on-start").value;
    var gesture_on_startup = document.getElementById("gest-on-start").value;

    // index value in list
    var output_device = document.getElementById("output-device-list").value;
    var input_device = document.getElementById("input-device-list").value;

    var camera_device = document.getElementById("camera-device").value;

    var settings = {
        "dexter_on_startup": dexter_on_startup,
        "gesture_on_startup": gesture_on_startup,
        "output_device": output_device,
        "input_device": input_device,
        "camera_device": camera_device
    }
    
    console.log(settings);

    var xhttp = new XMLHttpRequest();
    var url = 'http://localhost:8000/settings/';
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader("Content-Type", "application/json")
    xhttp.send(JSON.stringify(settings));

    xhttp.onreadystatechange=(e)=>{
      console.log(xhttp.responseText);
    }
}