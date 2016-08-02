#Image-Tone Analyzer Front-End
By Chris O'Brien

I designed and built this front-end while working as a Business Intelligence Intern at IBM in the summer of 2016. I was part of a four-person team, building an application which combined IBM Watson's Tone Analysis and Visual Recognition APIs to take in an image link, and output the image's tone. If you're interested in how the back-end works, see static/backDoc.html (or click "Back-End Documentation" on the home page). While my teammates worked out how to leverage Watson and communicate with the API's, I built the interactive front-end, and the Flask server which connected the front-end to the Python back-end.

The result of our work was a wed front-end built with HTML, CSS, and JavaScript. When the 'Analyze!' button is clicked on the home page (assuming no errors in user input), button.js sends an AJAX request to '/_passLink' in welcome.py, the Python script that routes requests for the Flask server. 

Originally, the '/_passLink' route in welcome.py would send the image link to the Python back-end, which would process it using the Watson APIs and return a string of five numbers, each representing a tone: anger, disgust, fear, joy, and sadness. If something went wrong in this process, the string returned will either be empty (meaning the Watson API threw an exception when we attempted to access it, so some sort of limit has been reached), contain "0 0 0 0 0" (meaning something went wrong while trying to parse the results from the Watson API call in the python script), or contain some sort of error message (such as an HTTP 403 or 404 error). Again, see the back-end documentation for more information.

However, because of confidentiality issues, I decided not to include the Python code that makes up the back-end, so instead of calling a Python script, '/_passLink' just sends a string of five hard-coded numbers back to button.js.

Once button.js has the results of the analysis, it displays the image provided by the user, separates the string into five percent values, displays those numbers on each of the five bars, and fills each bar proportionally, according to that percent. This makes the results visual and much easier to understand for the user.

For further information on the development of the front-end, feel free to contact me at cobrien3@mail.smcvt.edu
