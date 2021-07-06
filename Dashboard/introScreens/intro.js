
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
  })
 

  

  

  