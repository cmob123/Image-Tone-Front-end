// to be executed when the button's clicked
// display image on the screen
$(document).ready(function(){
	var error = false // global variable for error checking
	text = $('#button').html()
	hideResults()
	hideError()

	// LISTENERS
	$('#button').hover(function(){ // fade button in and out based on hovering
        $(this).fadeTo('fast', 1)
    }, function(){
        $(this).fadeTo('fast', 0.88)
    });
	$('#button').click(function(){ // handle button being clicked
		main()
	})
	$(document).keydown(function(key){ // handle enter being pressed
		if (parseInt(key.which,10) == 13)
			main();
	})

	function main(){ // executed when used clicks button or presses enter
		var input = $('#field').val() // get inputted link
		input = input.split('?')[0] // remove GET parameters

		// ERROR CHECKING
		var urlChecker = new RegExp("(http|ftp|https)://[\w-]+(\.[\w-]*)+([\w.,@?^=%&amp;:/~+#-]*[\w@?^=%&amp;/~+#-])?") 
						// found on Stack Overflow, checks to see if text is a link
		var imageChecker = new RegExp(".(jpg|gif|png)$") // checks if link leads to image (these should be combined)
		if (input == "") { // check for empty text
			showError('ERROR: input field is empty!')
		}
		else if (urlChecker.test(input)) { // test if input is a link
			showError("ERROR: input isn't a link!")
			console.log("got here")
		}
		else if (!imageChecker.test(input)){ // test if input is an image
			showError("ERROR: input isn't an image!")
		}

		// SEND AJAX
		else {
			var results = [],
				data = { 'input': input }; // initialize variables
			console.log('Sending ' + input + ' with AJAX')
			$.ajax({ // begin ajax request to ajax.php (which passes to processImage.py)
				type: 'POST',
				url: 'ajax.php',
				data: data,
				async: false,
				success: function(output){
					console.log(output)
					console.log('Recieved results: ' + String(output))

					if (output === '0 0 0 0 0') {
						showError('ERROR: AJAX Message Failed')
						console.log('ERROR: Python returned all zeroes')
					}
					else if (output === "") {
						showError('ERROR: Daily limits reached :(')
						console.log('ERROR: AJAX call returned an empty string')
					}
					else if (output.search('ERROR') != -1) showError(output)
					else {
						results = output.split(' ')
						console.log('Array: ' + results)
					}
				},
				error: function(xhr, status, err){
					showError('ERROR: Ajax Message Failed')
					console.log('ERROR: ')
					console.log('  XMLhttpRequest: ' + xhr)
					console.log('  Status: ' + status)
					console.log('  Error: ' + err)
				}
			}) // end ajax request
		}

		// DISPLAY RESULTS
		if (!error) {
			hideError()
			showResults()
			$('#previewTextDiv').css('background', 'rgba(0, 0, 0, 0.4)')
			// display preview text
			$('#previewText').html('Preview:')
			// display image
			$('#preview').fadeTo('slow', .95)
			$('#preview').attr('src', input)

			// convert results from decimals to percentages
			for(var i=0; i<results.length; i++) results[i] = String(Math.round(parseFloat(results[i])*100)) + '%'
			
			// populate results
			$('#resultsTitle').html('Results:')
			$('#tone1').html('Anger: ' + results[0])
			$('#tone2').html('Disgust: ' + results[1])
			$('#tone3').html('Fear: ' + results[2])
			$('#tone4').html('Joy: ' + results[3])
			$('#tone5').html('Sadness: ' + results[4])

			$('#resultsDiv').css('background', 'rgba(0, 0, 0, 0.6)')

			// add listeners to fade in and out based on mouse position
			$('#preview').hover(function(){
		        $('#preview').fadeTo('fast', 1)
		    }, function(){
		        $('#preview').fadeTo('slow', 0.95)
		    });			
			$('#resultsDiv').hover(function(){
		        $('#resultsDiv').css('background', 'rgba(0, 0, 0, .8)')
		    }, function(){
		        $('#resultsDiv').css('background', 'rgba(0, 0, 0, 0.6)')
		    });			
		} // end displaying results
	} // end main method

	function showError(msg){
		$('#error').show()
		$('#error').css('background', 'rgba(0, 0, 0, 0.4)')
		$('#error').html(msg) 
		$('.results').fadeOut('fast')
		error = true
	}
	function hideError(){
    	$('#error').hide()
		$('#error').html("")
	}
	function showResults(){
		$('.results').fadeIn('slow')
		error = false
	}
	function hideResults(){ 
		$('.results').fadeOut('fast')
	}

	// add listener to fade footer based on mouse position
    $details = $('#details')
	$details.hover(function(){
		$(this).fadeTo('fast', .85)
    }, function(){
        $(this).fadeTo('fast', .6)
    });	
}); // end .ready()