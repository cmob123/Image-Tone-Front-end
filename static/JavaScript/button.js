// to be executed when the button's clicked
// display image on the screen
$(document).ready(function(){
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
        $(this).fadeTo('fast', 1)
    }, function(){
        $(this).fadeTo('fast', 0.88)
    });
	$button.click(function(){ // handle button being clicked
		analyze()
	})
	$(document).keydown(function(key){ // handle enter being pressed
		if (parseInt(key.which,10) == 13)
			analyze();
	})
	$(window).resize(function(){
		detectOverflow() // detect whether or not scrollbars are needed
	})

	function analyze(){ // executed when used clicks button or presses enter
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

		if (input == "") { // check for empty text
			showError('ERROR: input field is empty!')
		}
		// SEND AJAX
		else {
			var data = { 'input': input }
			console.log('Sending ' + input + ' with AJAX')
			$.ajax({ // begin ajax request to welcome.py)
				url: '/_passLink',
				data: data,
				async: false,
				success: function(output){
					console.log(output)
					console.log('Recieved results: ' + String(output))

					// check for errors
					if (output.search('ERROR') != -1) {
						showError(output)
					} else {
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
				}
			}) // end ajax request
		}
	    $button.html('Analyze!')
	} // end sendAjax method

	$(document).ajaxComplete(function(){ // executed after success and error functions in AJAX call
	    console.log('ajax done!')
	    if(!error){
			hideError()
			showResults()

			$('#resultsDiv').css('background', 'rgba(0, 0, 0, .8)') // translucent black
			$('#previewTextDiv').css('background', 'rgba(0, 0, 0, 0.4)') // translucent black

			// display image
			$('#preview').fadeTo('slow', .95)
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
				outerWidth; // store width of the bar (without 'px')
			for(var i=0; i<5; i++){
				percentNum = Math.round(parseFloat(results[i])*100) // convert result from string to number
				outerWidth = $('.bar').width() // store width of the bar (without 'px')
				if (isNaN(percentNum)){ // check to see if output is 'NaN'
					// fill entire bar and return error
					outputString = 'ERROR: Not a Number :('
					percentNum = 100
				}
				else { // fill portion of bar and print result as a percentage
					outputString = String(percentNum) + '%' // add '%' to percentNum and make it a string
				}
				$('#fill' + String(i+1)).animate({width: String(percentNum)+'%'}, 1000) // animate bar filling up
				$('#fillNum' + String(i+1)).html(outputString) // display output
			} // end for
			detectOverflow() // detect whether or not scrollbars are needed
		} // end if
	}); // end ajaxComplete

	function detectOverflow(){ // dynamically check if scrollbars are needed (overflow is hidden by default)
		var $previewBottom = $('#previewDiv').offset().top + $('#previewDiv').height(), // bottom of the preview
			$resultsBottom = $('#resultsDiv').offset().top + $('#resultsDiv').height(), // bottom of the results
			$footerTop = $('#detailsBackground').offset().top; // start of the footer
		console.log('preview: ' + $previewBottom)
		console.log('results: ' + $resultsBottom)
		console.log('footer: ' + $footerTop)
		if($previewBottom > $footerTop || $resultsBottom > $footerTop)
			$('body').css('overflow-y', 'auto'); // add scrollbars
		else $('body').css('overflow-y', 'hidden'); // hide scrollbars (and overflow)
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
