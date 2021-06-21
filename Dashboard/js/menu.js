var remote = require('remote')
var Menu = remote.require('menu')
var MenuItem = remote.require('menu-item')

// Import the pug module
const pug = require('pug');

// Compile the template (with the data not yet inserted)
const templateCompiler = pug.compileFile('homes.pug');

// Insert your data into the template file
console.log(templateCompiler({ name: 'Eris' }));

// Build our new menu
var menu = new Menu()
menu.append(new MenuItem({
  label: 'Delete',
  click: function() {
    // Trigger an alert when menu item is clicked
    alert('Deleted')
  }
}))
menu.append(new MenuItem({
  label: 'More Info...',
  click: function() {
    // Trigger an alert when menu item is clicked
    alert('Here is more information')
  }
}))
menu.append(new MenuItem({
  label: 'Testing',
  click: function() {
    // Trigger an alert when menu item is clicked
    alert('Here is more information')
  }
}))

function init() { 
  document.getElementById("nav-group-item").addEventListener("click", function (e) {
       var window = BrowserWindow.getFocusedWindow();
       window.minimize(); 
  });

// Add the listener
document.addEventListener('DOMContentLoaded', function () {
  document.querySelector('.js-context-menu').addEventListener('click', function (event) {
    menu.popup(remote.getCurrentWindow());
  })
})


window.addEventListener('DOMContentLoaded', () => {

	const observer = new IntersectionObserver(entries => {
		entries.forEach(entry => {
			const id = entry.target.getAttribute('id');
			if (entry.intersectionRatio > 0) {
				document.querySelector(`nav li a[href="#${id}"]`).parentElement.classList.add('active');
			} else {
				document.querySelector(`nav li a[href="#${id}"]`).parentElement.classList.remove('active');
			}
		});
	});

	// Track all sections that have an `id` applied
	document.querySelectorAll('section[id]').forEach((section) => {
		observer.observe(section);
	});
	
});

$(document).ready(function(){

  var w = window.innerWidth;
  var h = window.innerHeight;

  var boxAmount = 10;
  if (w > 1000) {
    boxAmount += 10
  } else if (w < 500) {
    boxAmount -= 5;
  }

  for (var i = 0; i < boxAmount; i++) {

      $('.grid').append('<div class="ani ani'+i+'">');
      num = Math.random() * h + 1;
      num2 = Math.random() * w + 1;
      $('.ani'+i+'').css('top',num).css('left',num2);
      
  }


  $('.start').on('click', function(){
    $(this).addClass('op');
    setTimeout (function(){
      $('.start').remove();
      $('.shape-contain').append('<div class="container">'
        + '<div class="p1"></div>'
        + '<div class="p2"></div>'
        + '</div>');
    },1000);
    setTimeout (function(){
      $('.container').append('<div class="p3"></div>');
    },2500);
    setTimeout (function(){
      $('.container').append('<div class="p4"></div><div class="p5"></div>');
    },3000);
    setTimeout (function(){
      $('.container').append('<div class="p4"></div><div class="p6"></div><div class="p7"></div><div class="p23"></div><div class="p32"></div>');
    },3200);
    setTimeout (function(){
      $('.container').append('<div class="p33"></div><div class="p34"></div><div class="p35"></div><div class="p8"></div><div class="p9"></div><div class="p10"></div><div class="p11"></div><div class="p12"></div><div class="p13"></div><div class="p14"></div><div class="p15"></div><div class="p16"></div><div class="p17"></div><div class="p18"></div><div class="p19"></div><div class="p20"></div><div class="p21"></div><div class="p22"></div>');
    },3700);
    setTimeout (function(){
      $('.container').append('');
    },3800);

  });

});

$(window).scroll(function(e){
  parallax();
});
function parallax(){
  var scrolled = $(window).scrollTop();
  $('.bg').css('top',-(scrolled*0.2)+'px');
}





