var userGestures;


function populateGesturesTable() {

    let functionTypesJson = `[{"function" : "default action"}, {"function" : "macro"}, {"function" : "script"}]`
    let functionTypes = JSON.parse(functionTypesJson);

    //Get our table 
    let tableBody = document.getElementById("gestures-table-body");

    //Populate each gesture to table
    userGestures.forEach(gesture => {

        //Begin list of available action types
        let functionList = `<select class="form-control drop-down function-list">\n`;

        functionTypes.forEach(funcType => {
            //Add selected tag to current selected action
            let selected = funcType.function === gesture["action"] ? "selected" : "";
            functionList += `<option ${selected} value="${funcType.function}">${funcType.function}</option>\n`
        });
                
        //Finish our list
        functionList += `</select>\n`;

        action = generateActionRow(gesture);

        $(tableBody).append(`<tr><td>${gesture["name"]}</td><td>${functionList}</td>${action}</tr>`);
    });    
}

function postUpdatedGestures() {
    var gestureSettings = {"settings": userGestures}

    var xhttp = new XMLHttpRequest();
    var url = 'http://localhost:8000/gesture-settings/'
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    
    xhttp.send(JSON.stringify(gestureSettings));
}

function getGestures() {

    var xhttp = new XMLHttpRequest();
    var url = 'http://localhost:8000/get-gestures/';
    xhttp.open("GET", url, true);
    xhttp.send();

    var gestureDataJson;

    xhttp.onload = function() {
        gestureDataJson = JSON.parse(xhttp.responseText);
        
        userGestures = JSON.parse(gestureDataJson)["settings"];

        console.log(userGestures);
        populateGesturesTable();
    };
}

function generateActionRow(gesture) {
    let predefinedJson = `[
        {"name":""},
        {"name":"Track"},
        {"name":"Left Click"},
        {"name":"Double Click"},
        {"name":"Right Click"},
        {"name":"Zoom In"},
        {"name":"Zoom Out"},
        {"name":"Scroll Up"},
        {"name":"Scroll Down"},
        {"name":"Go Back"},
        {"name":"Go Forward"},
        {"name":"Switch App"},
        {"name":"Switch Desktop"},
        {"name":"Slide App Left"},
        {"name":"Slide App Right"},
        {"name":"Window Right"},
        {"name":"Window Left"},
        {"name":"Close Window"},
        {"name":"Fullscreen"},
        {"name":"Maximize App"},
        {"name":"Minimize App"},
        {"name":"Play"},
        {"name":"Pause"},
        {"name":"Next Track"},
        {"name":"Previous Track"},
        {"name":"Increase Volume"},
        {"name":"Decrease Volume"},
        {"name":"Unmute"},
        {"name":"Mute"}]`;

    //Get our predefined function names
    let predefinedFunctions = JSON.parse(predefinedJson);

    switch(gesture["action"]) {
        case 'default_action':
            
            //Start our drop down list
            let predefinedFunctionList = `<select class="form-control drop-down predefined-list">\n`;
            
            //Populate list items
            predefinedFunctions.forEach(predef => {
                let selected = predef.name === gesture['default_action_name'] ? "selected" : "";
                predefinedFunctionList += `<option ${selected} value="${predef.name}">${predef.name}</option>\n`
            });
            
            //Finish our list
            predefinedFunctionList += `</select>\n`;
            
            return `<td class="td-action">${predefinedFunctionList}</td>`;
        case 'macro':
            return `<td class="td-action" onclick="startRecording(event)">${gesture["macro"]}</td>`;
        case 'script':
            return `<td class="td-action" onclick="getScriptPath(event)">${gesture["path"]}</td>`;
        default:
            return `<td>Undefined Function Type</td>`;
    }
}

var currentMacroRow;
var macroPresses = [];

const keyDownCallback = keyPressed.bind(this);
const keyUpCallback = keyReleased.bind(this);

function parseKey(key)
{
    key = key.toLowerCase()

    if(key.includes("arrow"))
        return key.replace("arrow", "")

    if(key === "meta")
        return "home";

    if(key.includes("audio"))
        return key.replace("audio", "")

    return key
}

function keyReleased(event)
{
    let key = parseKey(event.key)

    //The user has release the first key pressed so stop recording and post gestures
    if(macroPresses.length != 0 && macroPresses[0] === key)
    {
        macroPresses.length = 0;
        window.removeEventListener("keydown", keyDownCallback);
        window.removeEventListener("keyup", keyUpCallback);
        postUpdatedGestures();
    }

    //Update gesture with new keys
    let gestureName = currentMacroRow.cells[0].innerHTML;
    userGestures.forEach((gesture) => {
        if(gesture.name === gestureName) {

            gesture['macro'] = currentMacroRow.cells[2].innerHTML;
        }
    });
}

function keyPressed(event) {

    //Prevent default actions like alt-tab
    event.preventDefault();  

    let key = parseKey(event.key)

    //Dont listen to repeat key events
    if(event.repeat || macroPresses.includes(key)) 
        return;

    //Get the cell with the string value
    let macroCell = currentMacroRow.cells[2]

    if(macroPresses.length === 0)
    {
        macroCell.innerHTML = key;
    }
    else
    {
        macroCell.innerHTML += " + " + key;
    }

    macroPresses.push(key)
}

function startRecording(event)
{
    //Get the table cell of the script
    let td = event.srcElement;
    let tr = td.parentElement;
    currentMacroRow = tr;
    tr.cells[2].innerHTML = "";
    macroPresses.length = 0;

    window.addEventListener("keydown", keyDownCallback);
    window.addEventListener("keyup", keyUpCallback);
}

function getScriptPath(event)
{
    //Get the table cell of the script
    let td = event.srcElement;
    let tr = td.parentElement;
    let gestureName = tr.cells[0].innerHTML;

    //Promise is resolved when user selects file
    let promise = parent.getPath();
    promise.then((result)=> {

        //Validate Input
        if(result.filePaths.length >= 1)
        {
            //Replace file path
            td.innerHTML  = result.filePaths[0];

            userGestures.forEach((gesture) => {
                if(gesture.name === gestureName) {
    
                    gesture['path'] = result.filePaths[0];
                    let newRow = generateActionRow(gesture);
                }
            });

            postUpdatedGestures();
        }
    });
}

window.addEventListener('DOMContentLoaded', () => {

    getGestures();
    populateGesturesTable();

    $(".function-list").on("change", (event) => {
            
        //Get the table cell of the script
        let select = event.originalEvent.target;
        let tableRow = select.parentElement.parentElement;
        let gestureName = tableRow.cells[0].innerHTML;

        let selectedVal = $(select).val() 

        userGestures.forEach((gesture) =>{
            if(gesture.name === gestureName) {

                gesture['action'] = selectedVal;
                let newRow = generateActionRow(gesture);
                tableRow.cells[2].outerHTML = newRow;
                postUpdatedGestures();
            }
        });
    })

    $(".predefined-list").on("change", (event) => {
            
        //Get the table cell of the script
        let select = event.originalEvent.target;
        let tableRow = select.parentElement.parentElement;
        let gestureName = tableRow.cells[0].innerHTML;

        let selectedVal = $(select).val() 

        userGestures.forEach((gesture) =>{
            if(gesture.name === gestureName) {

                gesture['default_action_name'] = selectedVal;
                postUpdatedGestures();
            }
        });
    })

});