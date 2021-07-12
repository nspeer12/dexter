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

    console.log('foo');
    xhttp.onload = function() {
        var data = JSON.parse(xhttp.responseText);
        intents = data["intents"];
        foo();
        console.log(intents);
        populateIntents(intents);
    }
    
}

function foo()
{
    console.log('fook');
}

function postIntents()
{
    var xhr = new XMLHttpRequest();
    var url = 'http://localhost:8000/voice-settings/';
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
    console.log(intents);
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
    
    var form = `<form>
                    <div class="form-group">
                        <label><h4>New Skill</h4></label>
                        <input type="text" class="form-control" placeholder="Skill Name">

                        <label><h4>Input</h4></label>
                        <textarea class="form-control" placeholder="what time is it?" rows="1"></textarea>
                        <textarea class="form-control" placeholder="what's the time?" rows="1"></textarea>
                        <textarea class="form-control" placeholder="do you have the time?" rows="1"></textarea>

                        <label><h4>Action</h4></label>
                        <textarea class="form-control" placeholder="Action" rows="1"></textarea>
                        <select class="form-control">
                            <option>Script</option>
                            <option>Open</option>
                            <option>Webhook</option>
                            <option>Reply</option>
                        </select>
                        <button type="submit" class="btn btn-form btn-default">Cancel</button>
                        <button type="submit" href='127.0.0.1:8000/get-intents' class="btn btn-form btn-primary" onclick="window.location.href='Voice.html'">OK</button>
                    </div>
                </form>`

    document.getElementById("CustomSkills").innerHTML += form;
}