<?php
// Serves as a messenger between client-side JavaScript and server-side Python. Written by Chris O'Brien
echo exec("python Back-End/processImage.py " . $_POST["input"]); // run python script to proces image
?>