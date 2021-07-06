var userGestures;


function populateGesturesTable() {

    let functionTypesJson = `[{"function" : "pre-defined function"}, {"function" : "macro"}, {"function" : "script"}]`
    let functionTypes = JSON.parse(functionTypesJson);

    //Get our table 
    let tableBody = document.getElementById("gestures-table-body");

    //Populate each gesture to table
    userGestures.forEach(gesture => {

        //Begin list of available action types
        let functionList = `<select class="form-control drop-down function-list">\n`;

        functionTypes.forEach(funcType => {
            //Add selected tag to current selected action
            let selected = funcType.function === gesture['function'] ? "selected" : "";
            functionList += `<option ${selected} value="${funcType.function}">${funcType.function}</option>\n`
        });
                
        //Finish our list
        functionList += `</select>\n`;

        action = generateActionRow(gesture);

        $(tableBody).append(`<tr><td>${gesture["name"]}</td><td>${functionList}</td>${action}</tr>`);
    });    
}

function postUpdatedGestures() {
    //TODO: Turn this into API call to main application to post custom gesture data
    console.log("here")
    //console.log('here ');
    var gestureSettings = {"settings": userGestures}
   
    console.log(gestureSettings)

    var xhttp = new XMLHttpRequest();
    var url = 'http://localhost:8000/gesture-settings/'
    xhttp.open("POST", url, true);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    
    xhttp.send(JSON.stringify(gestureSettings));
}

function getCustomGestures() {

    //TODO: Turn this into API call to main application to get custom gesture data
    // Load this from a file
	let gestureDataJson = `[
        {"starting_position" : "pointer", "ending_position" : "close", "motion": "none", "name": "lower index", "action": "macro", "default_action_name":"Left Click", "macro":"Alt+F4", "path": ""},
        {"starting_position" : "bunny ears", "ending_position" : "close", "motion": "none", "name": "lower index and middle", "action": "script", "default_action_name":"Right Click", "macro":"", "path": "C:/script.py"},
        {"starting_position" : "ok", "ending_position" : "open", "motion": "none", "name": "Zoom in 2 Fingers", "action": "default_action", "default_action_name":"Zoom In", "macro":"", "path": ""},
        {"starting_position" : "open", "ending_position" : "ok", "motion": "none", "name": "Zoom out 2 Fingers", "action": "default_action", "default_action_name":"Zoom Out", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "3 fingers", "motion": "up", "name": "Slide up 3 Fingers", "action": "default_action", "default_action_name":"Scroll Up", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "3 fingers", "motion": "down", "name": "Slide down 3 Fingers", "action": "default_action", "default_action_name":"Scroll Down", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "3 fingers", "motion": "left", "name": "Slide left 3 Fingers", "action": "default_action", "default_action_name":"Go Back", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "3 fingers", "motion": "right", "name": "Slide right 3 Fingers", "action": "default_action", "default_action_name":"Go Forward", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "4 fingers", "motion": "right", "name": "Slide right 4 Fingers", "action": "default_action", "default_action_name":"Switch App", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "4 fingers", "motion": "up", "name": "slide up 4 Fingers", "action": "default_action", "default_action_name":"Switch Desktop", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "open", "motion": "left", "name": "Slide left 5 Fingers", "action": "default_action", "default_action_name":"Slide App Left", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "open", "motion": "right", "name": "Slide right 5 Fingers", "action": "default_action", "default_action_name":"Slide App Right", "macro":"", "path": ""},
        {"starting_position" : "duck finger", "ending_position" : "open", "motion": "none", "name": "Zoom out 5 Fingers", "action": "default_action", "default_action_name":"Maximize App", "macro":"", "path": ""},
        {"starting_position" : "open", "ending_position" : "duck finger", "motion": "none", "name": "Zoom in 5 Fingers", "action": "default_action", "default_action_name":"Minimize App", "macro":"", "path": ""},
        {"starting_position" : "close", "ending_position" : "open", "motion": "none", "name": "Open Hand", "action": "default_action", "default_action_name":"Play", "macro":"", "path": ""},
        {"starting_position" : "open", "ending_position" : "close", "motion": "none", "name": "Close Hand", "action": "default_action", "default_action_name":"Pause", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "close", "motion": "right", "name": "Sliding right Closed Fist", "action": "default_action", "default_action_name":"Next Track", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "close", "motion": "left", "name": "Sliding left Closed Fist", "action": "default_action", "default_action_name":"Previous Track", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "thumbs up", "motion": "up", "name": "Sliding up Thumbs up", "action": "default_action", "default_action_name":"Increase Volume", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "thumbs down", "motion": "down", "name": "Sliding down Thumbs down", "action": "default_action", "default_action_name":"Decrease Volume", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "thumbs up", "motion": "left", "name": "Sliding left Thumbs up", "action": "default_action", "default_action_name":"Unmute", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "thumbs up", "motion": "right", "name": "Sliding right Thumbs up", "action": "default_action", "default_action_name":"Unmute", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "thumbs down", "motion": "left", "name": "Sliding left Thumbs down", "action": "default_action", "default_action_name":"Mute", "macro":"", "path": ""},
        {"starting_position" : "none", "ending_position" : "thumbs down", "motion": "right", "name": "Sliding right Thumbs down", "action": "default_action", "default_action_name":"Mute", "macro":"", "path": ""}]`

    userGestures = JSON.parse(gestureDataJson);
}

function generateActionRow(gesture) {
    let predefinedJson = `[
        {"name":"Left Click"},
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

    switch(gesture['function']) {
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


const keyDownCallback = keyPressed.bind(this);
const keyUpCallback = keyReleased.bind(this);

function keyReleased(event)
{
    window.removeEventListener("keydown", keyDownCallback);
    window.removeEventListener("keyup", keyUpCallback);

    let gestureName = currentMacroRow.cells[0].innerHTML;
    userGestures.forEach((gesture) => {
        if(gesture.name === gestureName) {

            gesture['macro'] = currentMacroRow.cells[2].innerHTML;
        }
    });

    postUpdatedGestures();
}

function keyPressed(event){

    event.preventDefault();  

    let macroCell = currentMacroRow.cells[2]

    if(macroCell.innerHTML === "")
    {
        macroCell.innerHTML += event.key; 
    }
    else
    {
        macroCell.innerHTML += ' + ' + event.key; 
    }
}

function startRecording(event)
{
    //Get the table cell of the script
    let td = event.srcElement;
    let tr = td.parentElement;
    currentMacroRow = tr;
    tr.cells[2].innerHTML = "";

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

    getCustomGestures();
    populateGesturesTable();

    $(".function-list").on("change", (event) => {
            
        //Get the table cell of the script
        let select = event.originalEvent.target;
        let tableRow = select.parentElement.parentElement;
        let gestureName = tableRow.cells[0].innerHTML;

        let selectedVal = $(select).val() 

        userGestures.forEach((gesture) =>{
            if(gesture.name === gestureName) {

                gesture['function'] = selectedVal;
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

                gesture['pre-defined function'] = selectedVal;
                postUpdatedGestures();
            }
        });
    })

});