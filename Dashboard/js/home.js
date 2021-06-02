var remote = require('remote')
var Menu = remote.require('menu')
var MenuItem = remote.require('menu-item')


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


$(window).scroll(function(e){
  parallax();
});
function parallax(){
  var scrolled = $(window).scrollTop();
  $('.bg').css('top',-(scrolled*0.2)+'px');
}