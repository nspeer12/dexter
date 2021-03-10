// Modules to control application life and create native browser window
const { app, BrowserWindow } = require('electron')
const path = require('path')
const ipc = require('node-ipc')
const { countReset } = require('console')

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

    function openSocket() {
        ipc.config.id = 'dexter';
        ipc.config.retry = 1500;

        ipc.connectTo(
            'core',
            function() {
                ipc.of.world.on(
                    'connect',
                    function() {
                        ipc.log('## connected to world ##'.rainbow, ipc.config.delay);
                        ipc.of.world.emit(
                            'message', //any event or message type your server listens for
                            'hello'
                        )
                    }
                );
                ipc.of.world.on(
                    'disconnect',
                    function() {
                        ipc.log('disconnected from world'.notice);
                    }
                );
                ipc.of.world.on(
                    'message', //any event or message type your server listens for
                    function(data) {
                        ipc.log('got a message from world : '.debug, data);
                    }
                );
            }
        );
    }

    // and load the index.html of the app.
    mainWindow.loadURL('file://' + __dirname + '/index.html');

    //mainWindow.setOpacity(.7);
    // Open the DevTools.
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

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.