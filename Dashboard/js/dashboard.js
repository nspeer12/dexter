const { BrowserWindow } = require('electron');
var os = require('os');

const si = require('systeminformation');
var percentageMem;
var percentageGPU;
var percentageCPU;
var memGPU;
var tempGPU;
var fanCPU;
var tempCPU;
var clockCPU;
var fps;

var anim;
var barNumber = 27;

function scale (number, inMin, inMax, outMin, outMax) {
    return (number - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;
}

onchange = function(stream) {
    if (stream.__proto__ === MediaStream.prototype)
    {
        var context = new AudioContext();
        var src = context.createMediaStreamSource(stream);
        var analyser = context.createAnalyser();

        src.connect(analyser);
        analyser.fftSize = 512;
        analyser.smoothingTimeConstant = .8

        var bufferLength = analyser.frequencyBinCount;
        var bufferByBar = Math.round(bufferLength/barNumber);
        var dataArray = new Uint8Array(bufferLength);

        var list = document.getElementsByClassName("marks")[0]
        var marks = list.getElementsByTagName("li");
        var core = document.getElementsByClassName("core2")[0]

        var visualizerMode = "circle";

        var arc = document.getElementsByClassName("semi_arc_3 e5_3")[0];

        var arc = document.getElementById("arc");

        function renderFrame() {
            anim = requestAnimationFrame(renderFrame);
            analyser.getByteFrequencyData(dataArray);

            var intensity = 0
            var visualizer = true;

            
            if (visualizer == true)
            {
                for (var i = 0; i < marks.length; ++i) {
                    
                    intensity += dataArray[i];
                    // nick's flat bar
                    //marks[i].style.transform = "rotate(" + (i*6) + "deg)" + "translateY(" +  scale((dataArray[i] * 2 + dataArray[marks.length - i]) / 2, 1, 250, 150, 225) + "px);
        
                    if (visualizerMode === "flat")
                    {
                        marks[i].style.transform = "scaleY(" + ((dataArray[i] * 2) * 0.05)  + ")";
                        marks[i].style.transform += "translateX(-35vw) "
                        marks[i].style.transform += "translate(" +  (0, 27*i) + "px)";
                        marks[i].style.transform += "translateZ(-30px)";
                    }
                    else if (visualizerMode == "circle")
                    {
                        marks[i].style.transform = "rotate(" + (i*6) + "deg)" + "translateY(" +  scale((dataArray[i] + dataArray[marks.length - i] * 0.8), 1, 250, 150, 220) + "px) scaleY(" + ((dataArray[i] * 2 + dataArray[marks.length - i]) * 0.022) + ")";
                    }
                }

                var scalefactor = 1 + intensity * .00005;
                arc.style.transform = "scale(" + scalefactor + "," + scalefactor + ");";
            }
            

            intensity /= marks.length

            // for (var i = 0; i < marks.length; ++i) {
            //     marks[i].style.transform = "rotate(" + (i*6) + "deg) translateY(" +  scale(intensity, 0, 255, 130, 200) + "px)"
            // }

            core.style.background = "rgba(2, " + scale(0 ,0, 255, 200, 255) +", " + scale(0,0, 2 * i % 255, 200, 255) +", 0.8)";

            
            
            // core transformations
            
        }
        renderFrame();
    }
};

function start(){

    

    if(anim){
        window.cancelAnimationFrame(anim);
    }
    navigator.mediaDevices.getUserMedia({
        audio: true,
        video : false
    })
    .then((stream)=>{ onchange(stream); })
    .catch((e) => handleError(e))
    function handleError (e) {
        console.log(e)
    }

    getStatus();
}

start();





setInterval(function() {
    diagnostics();
  }, 3000);

setInterval(function() {
    clock();
  }, 1000);
  
var days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const months = ["January", "February", "March", "April", "May", "June",
  "July", "August", "September", "October", "November", "December"];


var lastAverage = cpuAverage()

function cpuAverage() {

    //Initialise sum of idle and time of cores and fetch CPU info
    var totalIdle = 0, totalTick = 0;
    var cpus = os.cpus();

    //Loop through CPU cores
    for(var i = 0, len = cpus.length; i < len; i++) {

        //Select CPU core
        var cpu = cpus[i];

        //Total up the time in the cores tick
        for(type in cpu.times) {
        totalTick += cpu.times[type];
        }     

        //Total up the idle time of the core
        totalIdle += cpu.times.idle;
    }

    //Return the average Idle and Tick times
    return {idle: totalIdle / cpus.length,  total: totalTick / cpus.length};
}


function clock() {
    var d = new Date();
    document.getElementById("time_local").innerHTML = d.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
    document.getElementById("time_day").innerHTML = days[d.getDay()]
    document.getElementById("time_date").innerHTML = d.getDate()
    document.getElementById("time_month").innerHTML = months[d.getMonth()]
}




function diagnostics() {

    si.mem(function(data) {
        percentageMem = Math.round(100 * data.used / data.total);
    });

    // si.graphics(function(data) {
    //         percentageGPU = data.controllers[0].utilizationGpu;
    //         memGPU = data.controllers[0].utilizationMemory;
    //         tempGPU = data.controllers[0].temperatureGpu;
            
    // });

    si.cpu(function(data) {
        clockCPU = data.main;
    });

    var tempPoll = cpuAverage();

    var idleDifference = tempPoll.idle - lastAverage.idle;
    var totalDifference = tempPoll.total - lastAverage.total;

    lastAverage = tempPoll;
  
    //Calculate the average percentage CPU usage
    var percentageCPU = 100 - ~~(100 * idleDifference / totalDifference);

    if (percentageCPU)
        document.getElementById("cpu").innerText = "CPU: " + percentageCPU + "%";
    
    if (clockCPU)
        document.getElementById("cpu-clock").innerText = "CPU Clock: " + clockCPU + "GHz";
    
        if (percentageMem)
        document.getElementById("ram").innerText = "RAM: " + percentageMem + "%";
    
    if (percentageGPU)
        document.getElementById("gpu").innerText = "GPU: " + percentageGPU + "%";

    if (memGPU)
        document.getElementById("gpu-mem").innerText = "GPU Mem: " + memGPU + "%";
    
    if (tempGPU)
        document.getElementById("gpu-temp").innerText = "GPU Temp: " + tempGPU + "°C";
    
    if (fps)
        document.getElementById("gpu-temp").innerText = "FPS: " + fps + " %";
}

async function consoleAPI(input) {

    let xhttp= new XMLHttpRequest();
    var url = new URL('http://127.0.0.1:8000/api/');
    url.searchParams.set('query', input);
    // console.log(url);
    xhttp.responseType = 'json';
    xhttp.open("GET", url, true);
    xhttp.send();
    xhttp.onload = function() {
      let res = JSON.parse(xhttp.response);
    //   console.log(res);
      var cons = document.getElementById("console");
      var textres = res["data"];
    //   textres.replace('"', '');
    //   console.log(res["data"]);
      cons.value += "- " + res["data"][1] + "\n";
      
    };
}


function consoleInput() {
    var cons = document.getElementById("console");
    var consoletext = document.getElementById("consoleInput");

    
    var text = consoletext.value;
    // console.log(text);
    consoletext.value = "";

    cons.value += "> " + text + "\n";

    consoleAPI(text);
}




window.addEventListener('load', (event) =>{

    document.getElementById("consolebutton").onclick=()=>{
        consoleInput();
    };

    document.getElementById("consoleInput").addEventListener("keyup", event => {
        if(event.key !== "Enter") return;
        document.getElementById("consolebutton").click(); 
        event.preventDefault();
    });

    document.getElementById("settings_button").onclick=()=>{

        var width = screen.width  * .8;
        var height = screen.height * .8;
        const win = window.open("../Pages/settings.html", "_blank", 
        `contextIsolation=no,
        nodeIntegration=yes,
        enableRemoteModule=yes,
        fullscreen=false,
        transparent=true,
        frame=true,
        width=${width},
        height=${height}`);
    };

    /*document.getElementById("computer_button").onclick=()=>{
        require('electron').shell.openExternal("/");
    };*/
});


function clickOnHover(id) {
    document.getElementById(id).click();
}

function hideArc()
{
    var arc = document.getElementById("arc");
    
    arc.style.display = "block";
    arc.style.display = "none";

}

function getStatus()
{
    let xhttp= new XMLHttpRequest();
    var url = new URL('http://127.0.0.1:8000/status/');

    xhttp.responseType = 'json';
    xhttp.onload = function() {
        
        res = JSON.parse(JSON.stringify(xhttp.response));
        // console.log(res);
        updateButtons(res);
    };

    xhttp.onerror = function() {
        status = {"core": "offline", "dexter": "offline", "gesture": "offline"};
        updateButtons(status);
    }

    xhttp.open("GET", url, true);
    xhttp.send();

}

var dexCmd = 'start';
var gestCmd = 'start';


function updateButtons(status)
{

    if (status["dexter"] == "online")
    {
        document.getElementById('startStopDexterButton').innerHTML = 'Stop Dexter';
        dexCmd = "stop";
    }
    else
    {
        document.getElementById('startStopDexterButton').innerHTML = 'Start Dexter';
        dexCmd = "start";
    }

    if (status["gesture"] == "online")
    {
        document.getElementById('startStopGestureButton').innerHTML = 'Stop Gesture';
        gestCmd = "stop";
    }
    else
    {
        document.getElementById('startStopGestureButton').innerHTML = 'Start Gesture';
        gestCmd = "start";
    }

    if (status["core"] == "online")
    {
        document.getElementById('core-status').innerHTML = 'Core: Online';
    }
    else
    {
        document.getElementById('core-status').innerHTML = 'Core: Offline';
    }  
}


function controlDexter(data)
{

    // console.log(dexCmd);
    if (dexCmd == "stop")
        document.getElementById('startStopDexterButton').innerHTML = "Stopping Dexter";
    else
     document.getElementById('startStopDexterButton').innerHTML = "Loading Dexter";

    var xhr = new XMLHttpRequest();
    var url = 'http://localhost:8000/dexter-control/?cmd=' + dexCmd;
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        data: data,
    }));
    
    //getStatus();
}


function controlGesture(data)
{
    if (gestCmd == "stop")
        document.getElementById('startStopGestureButton').innerHTML = "Stopping Gesture";
    else
        document.getElementById('startStopGestureButton').innerHTML = "Loading Gesture";


    var xhr = new XMLHttpRequest();
    var url = 'http://localhost:8000/gesture-control/?cmd=' + gestCmd;
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        data: data,
    }));
}

// pings Core server every 5 seconds to update status of processes
var checkStatus = window.setInterval(function() {
    var status = getStatus();
}, 5000)