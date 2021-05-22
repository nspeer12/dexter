// Modules to control application life and create native browser window
const { app, BrowserWindow } = require('electron')
const path = require('path')
const { countReset } = require('console')
const zmq = require("zeromq")


function createWindow() {
    
    // Create the browser window.
    const mainWindow = new BrowserWindow({
        fullscreen: true,
        transparent: true,
        acceptFirstMouse: true,
        titleBarStyle: 'hidden-inset',
        frame: false,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    })

    // and load the index.html of the app.
    mainWindow.loadURL('file://' + __dirname + '/index.html');
    //mainWindow.webContents.openDevTools()
    
    
    async function ipc_test() 
    {
        const sock = new zmq.Request
      
        sock.connect("tcp://127.0.0.1:5555")
        console.log("Client bound to port 5555\nSending 'Hello'...")
      
        await sock.send("Hello")
        const [result] = await sock.receive()
      
        console.log("Got response: " + result.toString('ascii'))
      }

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

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.