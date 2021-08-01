var userIntent;
var defaultIntents;
var customIntents;
var functionTypes;

var currentMacroRow;
var macroPresses = [];

function updateIntents() {
    var totalIntent = defaultIntents.concat(customIntents);
    var intentSettings = {"intents" : totalIntent};
    // console.log("trying to update intent")
    var xhttp = new XMLHttpRequest();
    var url = 'http://localhost:8000/intent-settings/'
    xhttp.open("POST", url);
    xhttp.setRequestHeader('Content-Type', 'application/json');
    xhttp.send(JSON.stringify(intentSettings));
    // console.log(intentSettings)
    // xhttp.onload = function() {
    //     console.log(JSON.parse(xhttp.responseText));
    // }
}

function getIntent() {
    // console.log("trying to get intents")
    var xhttp = new XMLHttpRequest();
    var url = 'http://localhost:8000/get-intents/';
    xhttp.open("GET", url, true);
    xhttp.send();

    var intentDatJson;

    xhttp.onload = function() {
        intentDatJson= JSON.parse(xhttp.responseText);
        userIntent = JSON.parse(intentDatJson)["intents"];
        // console.log(userIntent);
        getCustomIntent();
        getDefaultIntent();
        populateDefaultSkillsTable();
        populateCustomSkillsTable();
    }
}

function getDefaultIntent(){
    defaultIntents = userIntent.filter(function (intent)
    {
        return intent.customizable == false;
    });
    // console.log(defaultIntents);
}

function getCustomIntent() {

    customIntents = userIntent.filter(function (intent){
        return intent.customizable == true
    });
    // console.log(customIntents)
}

function populateDefaultSkillsTable() {

    defaultIntents.forEach(intent => {
        let tag = intent.tag.charAt(0).toUpperCase() + intent.tag.slice(1);
        let pattern = intent.patterns[0];
        if (intent["tag"] != "idk" && intent["tag"] != "Print Chat Log")
            $("#default-skills-list").append(
                `<li class="list-group-item">
                    <div class="media-body">
                        <strong>${tag}</strong>
                        <p>"${pattern}"</p>
                    </div>
                </li>`);
    });
}

function populateCustomSkillsTable() {
    let functionTypesJson = `[{"function" : "default action"}, {"function" : "macro"}, {"function" : "script"}, {"function" : "file"}, {"function" : "application"}]`
    functionTypes = JSON.parse(functionTypesJson);
    //Populate each gesture to table
    customIntents.forEach(intent => {
        appendIntentEntry(intent); 
    });    
}

function generateActionRow(skill) {
    let predefinedJson = `[
        {"name":"Greeting"},
        {"name":"Introduction"},
        {"name":"Goodbye"},
        {"name":"Resume"},
        {"name":"Pause"},
        {"name":"Increase Volume"},
        {"name":"Decrease Volume"},
        {"name":"Mute"},
        {"name":"Unmute"},
        {"name":"Shutdown"},
        {"name":"Sleep"},
        {"name":"Minimize"},
        {"name":"Maximize"},
        {"name":"Restore"},
        {"name":"Switch Applications"},
        {"name":"Switch Desktop"},
        {"name":"Date"},
        {"name":"Time"},
        {"name":"Weather"}]`;

    //Get our predefined function names
    let predefinedFunctions = JSON.parse(predefinedJson);

    switch(skill["actionType"]) {
        case 'default action':
        case 'default_action':
            
            //Start our drop down list
            let predefinedFunctionList = `<select class="form-control drop-down predefined-list">\n`;
            
            //Populate list items
            predefinedFunctions.forEach(predef => {
                let selected = predef.name === skill['default_action_name'] ? "selected" : "";
                if (predef.name == "")
                    predefinedFunctionList += `<option ${selected} value="${predef.name}">Select a Function</option>\n`
                else
                    predefinedFunctionList += `<option ${selected} value="${predef.name}">${predef.name}</option>\n`
            });
            
            //Finish our list
            predefinedFunctionList += `</select>\n`;
            
            return `<td class="td-action predef-skill">${predefinedFunctionList}</td>`;
        case 'macro':
            if (skill["macro"] == "")
                return `<td class="td-action macro-skill">Click to Start Recording</td>`;
            else
                return `<td class="td-action macro-skill">${skill["macro"]}</td>`;
        case 'script':
            if (skill["script"] == "")
                return `<td class="td-action script-skill">Click to Choose Script</td>`;
            else
                return `<td class="td-action script-skill">${skill["script"]}</td>`;
        case 'file':
            if (skill["file_path"] == "")
                return `<td class="td-action file-skill">Click to Choose File</td>`;
            else
                return `<td class="td-action file-skill">${skill["file_path"]}</td>`;
        case 'application':
            if (skill["application"] == "")
                return `<td class="td-action application-skill">Click to Choose Application</td>`;
            else
                return `<td class="td-action application-skill">${skill["application"]}</td>`;
        default:
            // console.log(skill)
            return `<td>Undefined Function Type</td>`;
    }
}

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

    if (key == "control")
        key = "ctrl";

    //The user has release the first key pressed so stop recording and post gestures
    if(macroPresses.length != 0 && macroPresses[0] === key)
    {
        macroPresses.length = 0;
        window.removeEventListener("keydown", keyDownCallback);
        window.removeEventListener("keyup", keyUpCallback);

        //Update gesture with new keys
        intent = customIntents[currentMacroRow.rowIndex - 1];
        intent['macro'] = currentMacroRow.cells[3].innerHTML;
    }
}

function keyPressed(event) {

    //Prevent default actions like alt-tab
    event.preventDefault();  
    let key = parseKey(event.key);

    if (key == "control")
        key = "ctrl";

    //Dont listen to repeat key events
    if(event.repeat || macroPresses.includes(key)) 
        return;

    //Get the cell with the string value
    let macroCell = currentMacroRow.cells[3];

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

function appendIntentEntry(intent) {

    //Begin list of available action types
    let functionList = `<select class="form-control drop-down function-list">\n`;

    functionTypes.forEach(funcType => {
        //Add selected tag to current selected action
        let selected = funcType.function === intent["actionType"] ? "selected" : "";
        functionList += `<option ${selected} value="${funcType.function}">${funcType.function}</option>\n`
    });
            
    //Finish our list
    functionList += `</select>\n`;

    action = generateActionRow(intent);

    let tableBody = document.getElementById("skills-table-body");
    $(tableBody).append(`<tr>
            <td><span class="icon icon-cancel-squared delete-btn"></span><input class="skill-name-input" placeholder="Skill Name" value="${intent.tag}"></td>
            <td><input class="skill-pattern-input" placeholder="Intent Patterns" value="${intent.patterns}"></input></td>
            <td>${functionList}</td>
            ${action}
            </tr>`);
}

window.addEventListener('DOMContentLoaded', () => {

    getIntent();

    $("#skills-table-body").on('change', '.function-list', function(e){
        let select = e.target;
        let tableRow = select.parentElement.parentElement;
        let intent = customIntents[tableRow.rowIndex - 1];
        let selectedVal = $(select).val();
    
        intent['actionType'] = selectedVal;
        tableRow.cells[3].outerHTML = generateActionRow(intent);
      });

      $("#skills-table-body").on('click', '.delete-btn', function(e){
      
        let span = e.target;
        let tr = span.parentElement.parentElement;
        intent = customIntents[tr.rowIndex - 1];
        // console.log(intent)

        customIntents.splice(tr.rowIndex - 1, 1);
        tr.remove()
    });

      $("#skills-table-body").on('click', '.macro-skill', function(e){
      
          let td = e.target;
          let tr = td.parentElement;
          currentMacroRow = tr;
          tr.cells[3].innerHTML = "Recording";
          macroPresses.length = 0;
      
          window.addEventListener("keydown", keyDownCallback);
          window.addEventListener("keyup", keyUpCallback);
      });

      $("#skills-table-body").on('input', ".skill-name-input", function(e){

        let input = e.target;
        let tableRow = input.parentElement.parentElement;
        intent = customIntents[tableRow.rowIndex - 1];
        intent['tag'] = $(input).val();
    });

    $("#skills-table-body").on('input', ".skill-pattern-input", function(e){

        let input = e.target;
        let tableRow = input.parentElement.parentElement;
        intent = customIntents[tableRow.rowIndex - 1];
        
        //Split patterns by comma and remove empty strings
        patterns = $(input).val().split(',').filter(e =>  e);

        intent['patterns'] = patterns;
    });

      $("#skills-table-body").on('change', '.predef-skill', function(e){
        let select = e.target;
        let tableRow = select.parentElement.parentElement;
        intent = customIntents[tableRow.rowIndex - 1];
        intent['default_action_name'] = $(select).val();
      });

      $("#skills-table-body").on('click', '.script-skill', function(e){

        //Get the table cell of the script
        let td = e.target;
        let tr = td.parentElement;
        intent = customIntents[tr.rowIndex - 1];
        
        //Promise is resolved when user selects file
        let promise = parent.getPath();
        promise.then((result)=> {
        
            //Validate Input
            if(result.filePaths.length >= 1)
            {
                //Replace file path
                td.innerHTML  = result.filePaths[0];

                intent['script'] = result.filePaths[0];
            }
        });
    });

      $("#skills-table-body").on('click', '.file-skill', function(e){

        //Get the table cell of the script
        let td = e.target;
        let tr = td.parentElement;
        intent = customIntents[tr.rowIndex - 1];
        
        //Promise is resolved when user selects file
        let promise = parent.getPath();
        promise.then((result)=> {
        
            //Validate Input
            if(result.filePaths.length >= 1)
            {
                //Replace file path
                td.innerHTML  = result.filePaths[0];

                intent['file_path'] = result.filePaths[0];
            }
        });
    });

    $("#skills-table-body").on('click', '.application-skill', function(e){

        //Get the table cell of the script
        let td = e.target;
        let tr = td.parentElement;
        intent = customIntents[tr.rowIndex - 1];
        
        //Promise is resolved when user selects file
        let promise = parent.getPath();
        promise.then((result)=> {
        
            //Validate Input
            if(result.filePaths.length >= 1)
            {
                //Replace file path
                td.innerHTML  = result.filePaths[0];

                intent['application'] = result.filePaths[0];
            }
        });
    });
    $("#save-skills-btn").on('click', (event)=>{
        event.preventDefault();
        updateIntents();
    });

    $("#add-skill-btn").on('click', (event)=> {
        event.preventDefault();  

        let intent = { 
            tag: "",
            patterns: [""],
            customizable : true,
            actionType: "default_action",
            default_action_name: "", 
            macro : "",
            script : "",
            file : "",
            application : ""
        };
        customIntents.push(intent);
        appendIntentEntry(intent);   
    
    })
});

