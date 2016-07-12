#Communicating Results from Watson APIs (Server-Side) to JavaScript (Client-Side)
By Chris O'Brien

Once we had a rough idea of how our visual classifiers were going to work, we started thinking of how we would communicate our results with the user. We decided we'd build a website using Bluemix and display it there, and I took over getting the front-end ready. It took a lot of research and more than a few hours on stack overflow and w3schools, but eventually I was looking at a working front-end.

Most of the site's design and aesthetics were done with HTML, CSS, and JavaScript (or JQuery). While this took a significant amount of time to accomplish, the focus of this documentation is not on the front-end itself, but rather on how to link this front-end with the server-side back-end.

This link was established by sending an AJAX request (containing the link inputted by the user) from JQuery (in button.js) on the front-end to PHP in the back-end. The PHP (ajax.php) recieves this AJAX request and runs a Python script (using the 'exec' command), passing it the link it recieved from the request as the script's input. The script (back-end/processImage.py) then returns a string to the PHP program, which in turn returns that string to the JQuery.

If everything went well, this string contains 5 numbers, each separated by a space (for example, ".58 .93 .34 .67 .52"). Each of these numbers represents the output from one of the visual classifiers (of which there are thirteen, but as noted in the back-end documentation, we chose to only show the five 'emotional' classifiers: Anger, Disgust, Fear, Joy, and Sadness).

If something went wrong in this process, the string returned will either be empty (meaning the Watson API threw an exception when we attempted to access it, so some sort of limit has been reached), contain "0 0 0 0 0" (meaning something went wrong while trying to parse the results from the Watson API call in the python script), or contain some sort of error message (such as an HTTP 403 or 404 error)

Finally, back in the JQuery, this string is interpreted, and either the results are outputted to the user (along with a small copy of the image they inputted), or an error message is generated.

For further information on the development of the front-end, feel free to contact me at cmobrien@us.ibm.com or cobrien3@mail.smcvt.edu

For further information on the back-end of this project, see BTV-visual-sentiment/README.md
