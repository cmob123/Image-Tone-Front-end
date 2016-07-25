// to be executed when the button's clicked
// display image on the screen
$(document).ready(function(){
	//$('#loadText').hide() // hide loading message
	var error, // error flag
		input, // image link provided by user
		results, // array to store output recieved from AJAX request
		$button = $('#mainButton')
	hideResults()
	hideError()

	$(document).ajaxStart(function(){
	    console.log('ajax started!')
	});


	// LISTENERS
	$button.hover(function(){ // fade button in and out based on hovering
	    //$("#loadText").show();
        $(this).fadeTo('fast', 1)
	    //$('#loadText').html('Analyzing Image...')
	    //$button.html('Analyzing...')
    }, function(){
	    //$("#loadText").hide();
        $(this).fadeTo('fast', 0.88)
	    //$('#loadText').html('')
	    //$button.html('Analyze!')
    });
	$button.click(function(){ // handle button being clicked
		//$button.html('Analyzing...')
		main()
	})
	$(document).keydown(function(key){ // handle enter being pressed
		//$button.html('Analyzing...')
		if (parseInt(key.which,10) == 13)
			main();
	})

	function main(){ // executed when used clicks button or presses enter
	    $button.html('Analyzing...')
		error = false // global variable for error checking
		results = []
		// Move everything up to make room for the preview and results
		$('#header').animate({marginTop: '30px'}, 'slow')
		$('#form').animate({marginTop: '50px'}, 'slow', sendAjax)
	} // end main method

	function sendAjax(){
		input = $('#field').val() // get inputted link
		input = input.split('?')[0] // remove GET parameters

		// ERROR CHECKING
		//var urlChecker = new RegExp("(http|ftp|https)://[\w-]+(\.[\w-]*)+([\w.,@?^=%&amp;:/~+#-]*[\w@?^=%&amp;/~+#-])?") 
						// found on Stack Overflow, checks to see if text is a link
		//var imageChecker = new RegExp(".(jpg|gif|png)$") // checks if link leads to image (these should be combined)
		if (input == "") { // check for empty text
			showError('ERROR: input field is empty!')
		}
		//else if (urlChecker.test(input)) { // test if input is a link
		//	showError("ERROR: input isn't a link!")
		//}
		/*else if (!imageChecker.test(input)){ // test if input is an image
			showError("ERROR: input doesn't link to an image!")
		}
		*/
		// SEND AJAX
		else {
			var data = { 'input': input }
			console.log('Sending ' + input + ' with AJAX')
			$.ajax({ // begin ajax request to welcome.py)
				//type: 'POST',
				url: '/_passLink',
				data: data,
				async: false,
				//dataType: 'json',
				success: function(output){
					console.log(output)
					console.log('Recieved results: ' + String(output))

					// check for errors
					if (output === '0 0 0 0 0') {
						showError('ERROR: Message to server Failed')
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
					showError('ERROR: Message to server failed')
					console.log('ERROR:')
					console.log('  XMLhttpRequest: ' + xhr)
					console.log('  Status: ' + status)
					console.log('  Error: ' + err)
				},

			}) // end ajax request
			//results = ['.40', '.56', '.43', '.24', '.39']
		}
	    $button.html('Analyze!')
	} // end sendAjax method

	/*function displayOutput(){
		hideError()
		showResults()

		$('#resultsDiv').css('background', 'rgba(0, 0, 0, .8)') // translucent black
		$('#previewTextDiv').css('background', 'rgba(0, 0, 0, 0.4)') // translucent black

		// display image
		$('#preview').fadeTo('slow', .95, function(){


		})
		$('#preview').attr('src', input)
		
		// populate results
		$('#resultsTitle').html('Results:')

		$('#output1').html('Anger')
		$('#output2').html('Disgust')
		$('#output3').html('Fear')
		$('#output4').html('Joy')
		$('#output5').html('Sadness')

		$('.bar').css('background', 'rgba(255, 255, 255, .8)')

		// display bars
		var percentNum, // convert result from string to number
			outputString, // initialized in if/else
			outerWidth, // store width of the bar (without 'px')
			newWidth; // width of the bar's fill, initialized in if/else
		for(var i=0; i<5; i++){
			percentNum = Math.round(parseFloat(results[i])*100) // convert result from string to number
			outerWidth = $('.bar').css('width').replace('px', "") // store width of the bar (without 'px')

			if (isNaN(percentNum)){ // check to see if output is 'NaN'
				// fill entire bar and return error
				outputString = 'ERROR: Not a Number :('
				newWidth = outerWidth
			}
			else { // fill portion of bar and print result as a percentage
				outputString = String(percentNum) + '%' // add '%' to percentNum and make it a string
				newWidth = percentNum/100 * outerWidth
			}
			$('#fill' + String(i+1)).animate({width: String(newWidth)+'px'}, 1000) // animate bar filling up
			$('#fillNum' + String(i+1)).html(outputString) // display output
		} // end for
	} // end displayOutput method*/

	$(document).ajaxComplete(function(){ // executed after success and error functions in AJAX call
	    console.log('ajax done!')
	    if(!error){
			hideError()
			showResults()

			$('#resultsDiv').css('background', 'rgba(0, 0, 0, .8)') // translucent black
			$('#previewTextDiv').css('background', 'rgba(0, 0, 0, 0.4)') // translucent black

			// display image
			$('#preview').fadeTo('slow', .95, function(){


			})
			$('#preview').attr('src', input)
			
			// populate results
			$('#resultsTitle').html('Results:')

			$('#output1').html('Anger')
			$('#output2').html('Disgust')
			$('#output3').html('Fear')
			$('#output4').html('Joy')
			$('#output5').html('Sadness')

			$('.bar').css('background', 'rgba(255, 255, 255, .8)')

			// display bars
			$('#header').animate({height: '47px'}, 4000, fillBars) // animation that does nothing, delay so the user sees the bars fill
		} // end if
	}); // end ajaxComplete

	function fillBars(){
		var percentNum, // convert result from string to number
			outputString, // initialized in if/else
			outerWidth, // store width of the bar (without 'px')
			newWidth; // width of the bar's fill, initialized in if/else
		for(var i=0; i<5; i++){
			percentNum = Math.round(parseFloat(results[i])*100) // convert result from string to number
			outerWidth = $('.bar').css('width').replace('px', "") // store width of the bar (without 'px')

			if (isNaN(percentNum)){ // check to see if output is 'NaN'
				// fill entire bar and return error
				outputString = 'ERROR: Not a Number :('
				newWidth = outerWidth
			}
			else { // fill portion of bar and print result as a percentage
				outputString = String(percentNum) + '%' // add '%' to percentNum and make it a string
				newWidth = percentNum/100 * outerWidth
			}
			$('#fill' + String(i+1)).animate({width: String(newWidth)+'px'}, 1000) // animate bar filling up
			$('#fillNum' + String(i+1)).html(outputString) // display output
		} // end for
	}

	function showError(msg){
		error = true
		$('#error').show()
		$('#error').css('background', 'rgba(0, 0, 0, 0.6)')
		$('#error').html(msg) 
		$('.results').fadeOut('fast')
	}
	function hideError(){
    	$('#error').hide()
		$('#error').html("")
	}
	function showResults(){
		error = false
		$('.results').fadeIn('slow')
	}
	function hideResults(){ 
		$('.results').fadeOut('fast')
	}

	// add listeners to fade in and out based on mouse position
	$('#preview').hover(function(){ // image preview
        $('#preview').fadeTo('fast', 1)
    }, function(){
        $('#preview').fadeTo('slow', 0.93)
    })
	$('#detailsBackground').hover(function(){ // footer
		$(this).fadeTo('fast', .95)
    }, function(){
        $(this).fadeTo('fast', .6)
    });	
}); // end .ready()