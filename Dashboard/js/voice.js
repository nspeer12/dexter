var intents = getIntents();


function trainModel()
{
    var xhr = new XMLHttpRequest();
    var url = 'http://localhost:8000/train-assistant';
    xhr.open("POST", url);
    xhr.send();
}

function getIntents()
{
    var xhttp = new XMLHttpRequest();
    var url = 'http://localhost:8000/get-intents/';
    xhttp.open("GET", url);
    xhttp.send();
    xhttp.onload = function() {
        var data = JSON.parse(xhttp.responseText);
        intents = data["intents"];
        populateIntents(intents);
    }
    
}

function postIntents()
{
    var xhr = new XMLHttpRequest();
    var url = 'http://localhost:8000/intent-settings/';
    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        data: data,
    }));
}

function populateIntents(intents) {

    //Get our table 
    let intentList = document.getElementById("intent-list");
    
    // var intents = getIntents()["intents"];
    // console.log(intents);
    //Populate each gesture to table
    intents.forEach(intent => {

        intentList.innerHTML += `<li class="list-group-item" id="intent-list">
                                    <div class="media-body">
                                        <strong>${intent["tag"]}</strong>
                                        <p>${intent["patterns"][0]}</p>
                                    </div>
                                </li>`;
    });    
}


function addSkillDropDown() {
    
    var form = `<form id="intent-form">
                    <div class="form-group">
                        <label><h4>New Skill</h4></label>
                        <input type="text" class="form-control" placeholder="Skill Name" id="new-intent-name"></input>

                        <label><h4>Input</h4></label>
                        <textarea class="form-control phrase" placeholder="what time is it?" rows="1"></textarea>
                        <textarea class="form-control phrase" placeholder="what's the time?" rows="1"></textarea>
                        <textarea class="form-control phrase" placeholder="do you have the time?" rows="1"></textarea>

                        <label><h4>Action</h4></label>
                        <textarea class="form-control" id="action-name" placeholder="Action Name" rows="1"></textarea>
                        <div style="margin-bottom:4px;">
                            <select class="form-control">
                                <option>Script</option>
                                <option>Open</option>
                                <option>Webhook</option>
                                <option>Reply</option>
                            </select>
                        </div>
                        <textarea class="form-control" id="action-path" placeholder="Path" rows="1"></textarea>
                        <button type="submit" class="btn btn-form btn-primary">OK</button>
                    </div>
                </form>`

    // append to top of list
    document.getElementById("CustomSkills").innerHTML += form;
    document.getElementById("intent-form").onsubmit = function () {
        var newIntentName = document.getElementById("new-intent-name").value;
        var phrases = document.getElementsByClassName("phrase");
        var actionName = document.getElementById("action-name").value
        console.log(actionName);
    }
}