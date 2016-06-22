# loop through a file and download all it's images
import urllib.request
import os

input_file = open("imageLinks.txt", 'r')
count = 0

for link in input_file:
	if count%2 == 0:
		print ("reading line", count+1)
		try:
			urllib.request.urlretrieve(str(link), str(int(count/2)+1)+'.jpg')
		# catch errors
		except urllib.error.HTTPError:
			print ("Error (HTTP): couldn't retrieve image at line", count+1)
		except urllib.error.URLError:
			print ("Error (URL): couldn't retrieve image at line", count+1)
	count += 1

input_file.close()
print ("Done")
