// to be executed when the button's clicked

// if text is empty, return error and exit

// if text is invalid, return error and exit

// display image on the screen
function displayImage(){
	// display preview text
	document.getElementById("previewText").innerHTML = "Preview:"

	// get image link
	var text = document.getElementById("field").value;

	// display image
	document.getElementById("preview").src = text;
	//document.getElementById("previewWrapper").style.margin = auto;
}
