// Requires file I/O within node/ 
const fs = require("fs");

// below consts. are used for importing jquery and using that to populate HTML table. Did not work :(
const { JSDOM } = require( "jsdom" );
const { window } = new JSDOM( "" );
const $ = require( "jquery" )( window );


fs.readFile("../../Core/gesture/csv/gestureSettings.json", "utf8", (err, jsonString) => {
  if (err) {
    console.log("Error reading file from disk:", err);
    return;
  }
  try {
    const gesture = JSON.parse(jsonString);
    // prints names to log, just checking it was getting to the file
    console.log("Gesture Name is:", gesture[0].name); 

    // this for loop does not work, nothing it updated in gesturemenu.html
    for(var i in gesture)  {
        console.log(gesture[i].name)
        var row =   `<tr>
                        <td>${gesture[i].name}</td>
                        <td>${gesture[i].name}</td>
                        <td>${gesture[i].name}</td>
                    </tr>`

        var table = $('#table-body')
        table.append(row)
    }
  } catch (err) {
    console.log("Error parsing JSON string:", err);
  }

    
});

//updating a .json file code from https://heynode.com/tutorial/readwrite-json-files-nodejs/

function jsonReader(filePath, cb) {
  fs.readFile(filePath, (err, fileData) => {
    if (err) {
      return cb && cb(err);
    }
    try {
      const object = JSON.parse(fileData);
      return cb && cb(null, object);
    } catch (err) {
      return cb && cb(err);
    }
  });
}



// update a file // 

jsonReader("../../Core/gesture/csv/gestureSettings.json", (err, gesture) => {
    if (err) {
      console.log("Error reading file:", err);
      return;
    }
    // update file from HTML input

    fs.writeFile("../../Core/gesture/csv/gestureSettings.json", JSON.stringify(gesture), err => {
      if (err) console.log("Error writing file:", err);
    });
  });
  




const { app, BrowserWindow, DownloadItem } = require('electron')
function createWindow () {
    const win = new BrowserWindow({
      width: 800,
      height: 600
    })
  
    win.loadFile('gestureMenu.html')
  }
  
  
  app.whenReady().then(() => {
    createWindow()
  })

 

