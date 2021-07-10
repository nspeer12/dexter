// Modules to control application life and create native browser window
const { app, BrowserWindow } = require('electron')
const path = require('path')
const { countReset } = require('console')
const spawn = require("child_process");
var http = require('http');
var express = require('express')

var server = express()

// The server object listens on port 3000
console.log("server start at port 3000");

try 
{
    require('electron-reloader')(module)
} 
catch (_) {}


function createWindow() {
    
    // Create the browser window.
    const mainWindow = new BrowserWindow({
        fullscreen: true,
        transparent: true,
        acceptFirstMouse: true,
        titleBarStyle: 'hidden-inset',
        frame: false,
        enableRemoteModule: true,
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            preload: path.join(__dirname, 'preload.js')
        }
    });

    // and load the index.html of the app.
    mainWindow.loadURL('file://' + __dirname + '/Pages/Dashboard.html');
    //mainWindow.webContents.openDevTools()
          
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
    createWindow()

    app.on('activate', function() {
        // On macOS it's common to re-create a window in the app when the
        // dock icon is clicked and there are no other windows open.
        if (BrowserWindow.getAllWindows().length === 0) createWindow()
    })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', function() {
    if (process.platform !== 'darwin') app.quit()
})

function startCore() {
    
    const ls = exec('dir', function (error, stdout, stderr) {
        if (error) {
          console.log(error.stack);
          console.log('Error code: '+error.code);
          console.log('Signal received: '+error.signal);
        }
        console.log('Child Process STDOUT: '+stdout);
        console.log('Child Process STDERR: '+stderr);
      });
      
      ls.on('exit', function (code) {
        console.log('Child process exited with exit code '+code);
      });
    
}
