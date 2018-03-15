// Display dogs owned by shelter in list view 
function listView() {
	var containers = document.getElementsByClassName("dogContainer");
	for (var i=0; i < containers.length; i++) {
		containers[i].style.width = "100%"; 
	}
}

// Display dogs owned by shelter in tile view
function tileView() {
	var containers = document.getElementsByClassName("dogContainer");
	for (var i=0; i < containers.length; i++) {
		containers[i].style.width = "50%"; 
	}
}