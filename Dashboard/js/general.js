
window.addEventListener('load', (event) =>{

    navigator.mediaDevices.enumerateDevices()
    .then(function(devices) {

        var outputList = document.getElementById("output-device-list");
        var inputList = document.getElementById("input-device-list");


        devices.forEach(function(device) {
            var dev = document.createElement("option");
            dev.text = device.label

            if(device.kind == "audioinput") {
                inputList.add(dev);
            }
            else if(device.kind == "audiooutput") {
                outputList.add(dev);
            }
    });
    })

    // document.getElementById("consolebutton").onclick=()=>{
    //     var console = document.getElementById("console")
    //     var consoletext = document.getElementById("consoleInput")
    
    //     var text = consoletext.value
    //     consoletext.value = ""
    
    //     console.value += "LOG> " + text + "\n"    
    // };
});