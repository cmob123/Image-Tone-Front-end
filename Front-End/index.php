<!-- Main html document for an image-tone analyzer, leveraging APIs from IBM's Watson. 
Front-end written by Chris O'Brien. -->

<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<meta name="description" content="Image-Tone Analyzer">
		<meta name="keywords" content="IBM, Watson, Image, Tone">
		<meta name="author" content="Chris O'Brien">

	    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.2/jquery.min.js"></script>
        <script src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.11.1/jquery-ui.min.js"></script>	    
	    <script src="button.js"></script>
	    <noscript>Sorry, your browser does not support JavaScript! :(</noscript>

		<link type="text/css" rel="stylesheet" href="stylesheet.css"/>
		<link href="css/bootstrap.min.css" rel="stylesheet">
	    <link href="css/landing-page.css" rel="stylesheet">

	    <!-- Custom Fonts -->
	    <link href="font-awesome/css/font-awesome.min.css" rel="stylesheet" type="text/css">
	    <link href="http://fonts.googleapis.com/css?family=Lato:300,400,700,300italic,400italic,700italic" rel="stylesheet" type="text/css">

		<title>Image-Tone Translator</title>
	</head>
	<body background = "https://i.ytimg.com/vi/8o44asJt8ZA/maxresdefault.jpg">
	    <div id="header">
	    	<h1 id="title" class="text">Image-Tone Analyzer</h1>	
	    </div>
	    <div id="formDiv">
		    <form id="form" onsubmit="return false">
		    	<p class="text" id="prompt">Image Link: </p>
		    	<input type="text" id="field">
		    </form>
	    </div>
	    <div id="button" class="text">
	    	Analyze!
	    </div>
	    <div id="error" class="text"></div>
	    <center>
	    	<div id="previewTextDiv" class="results">
	    	<h4 class="results text" id="previewText"></h4>
	    	</div>
	    	<img src="" id="preview" align="middle" class="results">
		    <div id="resultsDiv" class="results">
		    	<h3 id="resultsTitle" class="results text"></h3>
		    	<ul id="list" class="results text">
		    		<li id="tone1"></li>
		    		<li id="tone2"></li>
		    		<li id="tone3"></li>
		    		<li id="tone4"></li>
		    		<li id="tone5"></li>
		    	</ul>
		    </div>
		</center>
	    <div id="details">
	    	<h4 class="text">How'd we do this? (link to documentation? separate page?)</h4>
	    </div>
	</body>
</html>