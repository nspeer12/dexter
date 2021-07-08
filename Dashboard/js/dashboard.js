const { BrowserWindow } = require('electron');
var os = require('os');

var anim;
var barNumber = 27;

function scale (number, inMin, inMax, outMin, outMax) {
    return (number - inMin) * (outMax - outMin) / (inMax - inMin) + outMin;
}

onchange = function(stream) {

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

    function renderFrame() {
        anim = requestAnimationFrame(renderFrame);
        analyser.getByteFrequencyData(dataArray);

        var intensity = 0

        for (var i = 0; i < marks.length; ++i) {
            intensity += dataArray[i]
            marks[i].style.transform = "rotate(" + (i*6) + "deg)" + "translateY(" +  scale((dataArray[i] * 1.5 + dataArray[marks.length - i]) / 2, 1, 250, 150, 225) + "px) scaleY(" + ((dataArray[i] * 1.5 + dataArray[marks.length - i]) * 0.025) + ")";
        
        }

        intensity /= marks.length

        // for (var i = 0; i < marks.length; ++i) {
        //     marks[i].style.transform = "rotate(" + (i*6) + "deg) translateY(" +  scale(intensity, 0, 255, 130, 200) + "px)"
        // }

        core.style.background = "rgba(2, " + scale(0 ,0, 255, 200, 255) +", " + scale(0,0, 255, 200, 255) +", 0.8)"
    }
    renderFrame();
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
}

start();

var dexCmd = 'start'
function controlDexter(data)
{

    var xhr = new XMLHttpRequest();
    var url = 'http://localhost:8000/dexter-control/?cmd=' + dexCmd;
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        data: data,
    }));
    
    if (dexCmd == 'start')
    {
        dexCmd = 'stop';
        document.getElementById('startStopDexterButton').innerHTML = 'Stop Dexter';
    }
    else if (dexCmd == 'stop')
    {
        dexCmd = 'start';
        document.getElementById('startStopDexterButton').innerHTML = 'Start Dexter';
    }
    
    

}

var gestCmd = 'start'
function controlGesture(data)
{
    var xhr = new XMLHttpRequest();
    var url = 'http://localhost:8000/gesture-control/?cmd=' + gestCmd;
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        data: data,
    }));

    if (gestCmd == 'start')
    {
        gestCmd = 'stop';
        document.getElementById('startStopGestureButton').innerHTML = 'Stop Gesture';
    }
    else if (gestCmd == 'stop')
    {
        gestCmd = 'start';
        document.getElementById('startStopGestureButton').innerHTML = 'Start Gesture';
    }
}





setInterval(function() {
    diagnostics();
  }, 2000);

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
    var tempPoll = cpuAverage();

    var idleDifference = tempPoll.idle - lastAverage.idle;
    var totalDifference = tempPoll.total - lastAverage.total;

    lastAverage = tempPoll;
  
    //Calculate the average percentage CPU usage
    var percentageCPU = 100 - ~~(100 * idleDifference / totalDifference);

    document.getElementById("cpu").innerText = "CPU: " + percentageCPU + "%";
    document.getElementById("ram").innerText = "Memory: " + Math.round(os.freemem() / (1000000)) + " MB";
}

window.addEventListener('load', (event) =>{

    document.getElementById("consolebutton").onclick=()=>{
        var console = document.getElementById("console")
        var consoletext = document.getElementById("consoleInput")
    
        var text = consoletext.value
        consoletext.value = ""
    
        console.value += "LOG> " + text + "\n"    
    };

    document.getElementById("settings_button").onclick=()=>{

        var width = screen.width  * .8;
        var height = screen.height * .8;
        const win = window.open("../Pages/settings.html", "_blank", 
        `contextIsolation=no,
        nodeIntegration=yes,
        enableRemoteModule=yes,
        fullscreen=false,
        transparent=true,
        frame=false,
        width=${width},
        height=${height}`);
    };

    document.getElementById("computer_button").onclick=()=>{
        require('electron').shell.openExternal("/");
    };
});