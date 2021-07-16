
const { app, BrowserWindow } = require('electron')
function createWindow () {
    const win = new BrowserWindow({
      width: 1200,
      height: 600
    })
  
    win.loadFile('introScreen.html')
  }

  
  
  app.whenReady().then(() => {
    createWindow();
    document.getElementById("demo").opacity = 0
    document.getElementById("demo").opacity = 1
    document.getElementById("input-device-list").value = userSettings["input_device"];
    document.getElementById("output-device-list").value = userSettings["output_device"];
    document.getElementById("camera_device-list").value = userSettings["camera_device"];
    var inputList = document.getElementById("input-device-list");
    var outputList = document.getElementById("output-device-list");
    var cameraList = document.getElementById("camera_device-list");

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

  
 

  

  

  