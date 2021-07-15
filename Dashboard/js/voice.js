var defaultIntents;
var customIntents;
var userGestures;
var functionTypes;

var currentMacroRow;
var macroPresses = [];

function postCustomGestures() {

    //TODO: yo this is where you convert the customIntents object to JSON data and post it to the endpoint
    console.log(customIntents);
}

function getDefaultSkills() {

    //TODO: yo this is where the default intents end point is called and you set the default intents string to this string
	let defaultIntentsString = `{
        "intents":
        [
            {"tag": "greeting",
            "patterns": ["Hi", "How are you", "Is anyone there?", "Hello", "Good day", "Whats up", "Hey", "greetings"],
            "responses": ["Hello!", "Good to see you again!", "Hi there, how can I help?"]
            },
            {"tag": "introduction",
            "patterns": ["who are you","what are you"],
            "responses": ["I am Dexter"]
            },
            {"tag": "goodbye",
            "patterns": ["cya", "See you later", "Goodbye", "I am Leaving", "Have a Good day", "bye", "see ya"],
            "responses": ["Sad to see you go :(", "Talk to you later", "Goodbye!"]
            },
            {"tag": "question",
            "patterns": ["who was the first man on the moon?", "what is the capital of china", "what is the meaning of life",
                         "can you do a backflip?", "is AI good or evil", "what is the internet", "what is blockchain",
                         "what is cryptocurrency", "how does a computer work", "who was the fifth president of the united states",
                         "what is your favorite food", "what is bitcoin"],
            "responses": ["Sad to see you go :(", "Talk to you later", "Goodbye!"]
            },
            {"tag": "wiki",
                "patterns": ["who is Gucci Mane","what is the capital of Bangledesh","who are the Chicago Bears","what is a blackhole",
                             "what is Chicago", "what as the Seattle Fire", "where is Florida", "what's the history of Clevland",
                             "What is quantum physics"],
                "responses": [] 
            },
            {"tag": "math",
                "patterns": ["1 + 2", "3 / 4", "5 * 6", "7 - 8", "9 % 0","what is 1 + 2", "what is 3 / 4", "what is 5 * 6", "what is 7 - 8",
                             "what is 9 % 0", "what is seventy four times 9", "what is eighty two divided by sixity nine", "what is the square root of thirteen",
                             "can you tell me what 99 * 52 is", "what is the integral of x squared", "what is the derivative of y to the power of 3",
                             "what is the derivative of 2 x ^ 2", "what's the √ 2"],
                "responses": []
            },
            {"tag": "news",
                "patterns": ["what is the news", "news"],
                "responses": []
            },
            {"tag": "play",
                "patterns": ["play", "play ram ranch", "play ariana grande", "play metallica on youtube"],
                "responses": []
            },
            {"tag": "resume",
                "patterns": ["resume","continue"],
                "responses": []
            },
            {"tag": "pause",
                "patterns": ["pause"],
                "responses": []
            },
            {"tag": "increaseVolume",
                "patterns": ["increase volume", "increase sound"],
                "responses": []
            },
            {"tag": "decreaseVolume",
                "patterns": ["decrease volume", "decrease sound"],
                "responses": []
            },
            {"tag": "mute",
                "patterns": ["mute","sound off"],
                "responses": []
            },
            {"tag": "unmute",
                "patterns": ["unmute","sound on", "turn up", "let's turn up", "let's get lit"],
                "responses": []
            },
            {"tag": "fullscreen",
                "patterns": ["fullscreen", "full screen", "exit full screen", "exit fullscreen"],
                "responses": []
            },
            {"tag": "restart",
                "patterns": ["reset", "restart"],
                "responses": []
            },
            {"tag": "shutDown",
                "patterns": ["shut down", "turn off"],
                "responses": []
            },
            {"tag": "sleep",
                "patterns": ["sleep"],
                "responses": []
            },
            {"tag": "minimize",
                "patterns": ["minimize"],
                "responses": []
            },
            {"tag": "maximize",
                "patterns": ["maximize"],
                "responses": []
            },
            {"tag": "restore",
                "patterns": ["restore"],
                "responses": []
            },
            {"tag": "switchApplications",
                "patterns": ["switch applications", "switch app"],
                "responses": []
            },
            {"tag": "switchDesktop",
                "patterns": ["switch desktop"],
                "responses": []
            },
            {"tag": "openApplication",
                "patterns": ["open application named"],
                "responses": []
            },
            {"tag": "openFile",
                "patterns": ["open file named"],
                "responses": []
            },
            {"tag": "date",
                "patterns": ["what date is today?"],
                "responses": []
            },
            {"tag": "time",
                "patterns": ["what is the time?", "what time is it?"],
                "responses": []
            },
            {"tag": "day",
                "patterns": ["what is day today?", "what's the day of the week", "what day of the week is it", "what's today"],
                "responses": []
            },
            {"tag": "bitcoin_price",
                "patterns": ["what is the price of bitcoin", "how much does bitcoin cost"],
                "responses": []
            },
            {"tag": "convo",
                "patterns": ["what is your favorite sport", "who are you", "what are you", "what can you do", "are you intelligent",
                             "what is your favorite movie", "what music do you listen to", "what is your favorite food", "can you tell me your secrets",
                             "Would you rather sacrifice one adult to save two children, or two children to save five adults, and why?",
                             "Do you know what humans are", "what do humans want in life", "do you know about life on earth",
                             "can you tie your shoe or not", "are you human", "can you do things that people can do"],
                "responses": []
            },
            {"tag": "print_chat_log",
                "patterns": ["print the chat log", "print our conversation", "print our current history", "print our conversation history"],
                "responses": []
            }
        ]
    }`

    defaultIntents = JSON.parse(defaultIntentsString);
    defaultIntents = defaultIntents.intents;
}

function getCustomSkills() {

    let functionTypesJson = `[{"function" : "default action"}, {"function" : "macro"}, {"function" : "script"}]`
    functionTypes = JSON.parse(functionTypesJson);

    //TODO: yo this is where the custom intents end point is called and you set the custom intents string to this string
	let customIntentsString = `{
        "intents":
        [
            {"tag": "Custom Skill 1",
            "patterns": ["hey sexy", "howdy", "yerrr"],
            "action": "default_action", 
            "default_action_name":"Increase Volume", 
            "macro":"", 
            "path": ""
            }
        ]
    }`

    customIntents = JSON.parse(customIntentsString);
    customIntents = customIntents.intents;
}


function populateDefaultSkillsTable() {

    defaultIntents.forEach(intent => {
        let tag = intent.tag.charAt(0).toUpperCase() + intent.tag.slice(1);
        let pattern = intent.patterns[0];

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

    //Populate each gesture to table
    customIntents.forEach(intent => {
        appendIntentEntry(intent); 
    });    
}

function generateActionRow(skill) {
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

    switch(skill["action"]) {
        case 'default_action':
        case 'default action':
            
            //Start our drop down list
            let predefinedFunctionList = `<select class="form-control drop-down predefined-list">\n`;
            
            //Populate list items
            predefinedFunctions.forEach(predef => {
                let selected = predef.name === skill['default_action_name'] ? "selected" : "";
                predefinedFunctionList += `<option ${selected} value="${predef.name}">${predef.name}</option>\n`
            });
            
            //Finish our list
            predefinedFunctionList += `</select>\n`;
            
            return `<td class="td-action predef-skill">${predefinedFunctionList}</td>`;
        case 'macro':
            return `<td class="td-action macro-skill">${skill["macro"]}</td>`;
        case 'script':
            return `<td class="td-action script-skill">${skill["path"]}</td>`;
        default:
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
        let selected = funcType.function === intent["action"] ? "selected" : "";
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

    getDefaultSkills();
    getCustomSkills();

    populateDefaultSkillsTable();
    populateCustomSkillsTable();

    $("#skills-table-body").on('change', '.function-list', function(e){
        let select = e.target;
        let tableRow = select.parentElement.parentElement;
        let intent = customIntents[tableRow.rowIndex - 1];
        let selectedVal = $(select).val();
    
        intent['action'] = selectedVal;
        tableRow.cells[3].outerHTML = generateActionRow(intent);
      });

      $("#skills-table-body").on('click', '.delete-btn', function(e){
      
        let span = e.target;
        let tr = span.parentElement.parentElement;
        intent = customIntents[tr.rowIndex - 1];
        console.log(intent)

        customIntents.splice(tr.rowIndex - 1, 1);
        tr.remove()
    });

      $("#skills-table-body").on('click', '.macro-skill', function(e){
      
          let td = e.target;
          let tr = td.parentElement;
          currentMacroRow = tr;
          tr.cells[3].innerHTML = "";
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

                    intent['path'] = result.filePaths[0];
                }
            });
      });

    $("#save-skills-btn").on('click', (event)=>{
        event.preventDefault();  
        postCustomGestures();
    });

    $("#add-skill-btn").on('click', (event)=> {
        event.preventDefault();  

        let intent = { 
            tag: "",
            patterns: [""],
            action: "default_action", 
            default_action_name:"Increase Volume", 
            macro:"", 
            path: ""
        };
        customIntents.push(intent);
        appendIntentEntry(intent);   
    
    })
});
