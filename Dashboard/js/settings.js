function navItemClicked(clickEvent) {

  var mainWindow = document.getElementById("main-content");
  var clickedBtn = clickEvent.srcElement 

  //Get all highlighted buttons
  var activeButtons = document.querySelectorAll(".active");

  //Unhighlight button
  [].forEach.call(activeButtons, function(btn) {
    btn.classList.remove("active");
  });

  //Highlight the clicked button
  clickedBtn.classList.add("active");

  mainWindow.src = "../Pages/" + clickedBtn.id.replace("settings-", "") + ".html"
} 

window.addEventListener('load', (event) =>{

  document.getElementById("settings-general").addEventListener('click', navItemClicked)
  document.getElementById("settings-user").addEventListener('click', navItemClicked)
  document.getElementById("settings-gestures").addEventListener('click', navItemClicked)
  document.getElementById("settings-voice").addEventListener('click', navItemClicked)
  document.getElementById("settings-privacy").addEventListener('click', navItemClicked)
  document.getElementById("settings-about").addEventListener('click', navItemClicked)

});

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

function trainAssistant()
{
    var xhr = new XMLHttpRequest();
    var url = 'http://localhost:8000/train-assistant';
    xhr.open("POST", url);
    xhr.send();
    
}