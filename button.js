// to be executed when the button's clicked

// if text is empty, return error and exit

// if text is invalid, return error and exit

// display image on the screen
function analyzeTone(){
	// display preview text
	document.getElementById("previewText").innerHTML = "Preview:"

	// get image link
	var text = document.getElementById("field").value;

	// display image
	document.getElementById("preview").src = text;

	// get tone information from the back-end python

	// display results
	document.getElementById("resultsTitle").innerHTML = "Results:";
	document.getElementById("tone1").innerHTML = "Tone1: 50%";
	document.getElementById("tone2").innerHTML = "Tone2: 18%";
	document.getElementById("tone3").innerHTML = "Tone3: 72%";
	document.getElementById("tone4").innerHTML = "Tone4: 89%";
	document.getElementById("tone5").innerHTML = "Tone6: 65%";

	// for some reason the next 2 lines breaks the program
	//document.getElementById("resultsDiv").style.background-color = "black";
	//document.getElementById("resultsDiv").style.opacity = ".5";
}
