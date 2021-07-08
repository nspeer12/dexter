function trainAssistant()
{
    var xhr = new XMLHttpRequest();
    var url = 'http://localhost:8000/train-assistant';
    xhr.open("POST", url);
    xhr.send();
}

function getIntents()
{
    var xhr = new XMLHttpRequest();
    var url = 'http://localhost:8000/get-intents';
    xhr.open("GET", url);
    xhr.send();

    var intents;

    xhr.onreadystatechange=(e)=>{
      intents = JSON.parse(xhr.responseText)['intents'];
      //console.log(intents);
    }

    for (var key in intents)
    {
      console.log(key);
    }
}

function addSkill()
{
    console.log('hello');
}