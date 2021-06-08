const { app, BrowserWindow } = require('electron')
function createWindow () {
    const win = new BrowserWindow({
      width: 800,
      height: 600
    })
  
    win.loadFile('introScreen.html')
  }
  
  app.whenReady().then(() => {
    createWindow()
  })

