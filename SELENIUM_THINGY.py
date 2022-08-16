import time
import os
import re
import pyperclip
import pynput
import codecs
import traceback
import sys
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from pynput.keyboard import Key, Controller
from pynput import keyboard
from inspect import currentframe, getframeinfo
from getpass import getpass
from datetime import datetime
from datetime import date
from selenium.webdriver.common.keys import Keys
import tk
#from tk import tk
#import tkinter as tk
#from tk import filedialog as fd
# REMEMBER TO ADD FUNCTIONALITY WHERE IF THERE'S A PERIOD AT THE START OF THE TITLE (E.G. ".38 SPECIAL"), IT REMOVES IT



keyboard = Controller()

Number_of_Times_to_Scroll1 = 0
LOGIN_EMAIL = "BLANK"
LOGIN_PW = "BLANK"
STUFF = "BLANK"
path = "BLANK"
song_file = "BLANK"
video_start = 1
video_end = 1
video_number = 0
Loop_Toggle = 0
line_num = 1
LOOK_FOR_TITLE = 0
Start_Upload = -1
Look_For_Channel_URL = 0
Look_For_Channel_Name = 0

print("What is your Odysee email?")# GET LOGIN INFO FROM USER
LOGIN_EMAIL = input()
while LOGIN_EMAIL == "BLANK":
	time.sleep(0.5)

print("What is your Odysee password? (I promise this will not be recorded outside of using this program)")
LOGIN_PW = getpass()
while LOGIN_PW == "BLANK":
	time.sleep(0.5)

print("What video do you want to start at?")
video_start = int(input())
while video_start == -1:
	time.sleep(0.5)

print("What video do you want to end at? If you're not sure how many videos there are and want to do them all, just type a super big number that you're reasonably sure is bigger than the playlist size and it will run through them all.")
video_end = int(input())
while video_end == -1:
	time.sleep(0.5)

print("Where is your song playlist file?")
song_file = input()
while song_file == "BLANK":
	time.sleep(0.5)

print("What is the folder that your video, thumbnail,and description files located?")
STUFF = input()
while STUFF == "BLANK":
	time.sleep(0.5)

print("Please show me where your webdriver is located, including the file name.")
path = input()
while path == "BLANK":
	time.sleep(0.5)


driver = webdriver.Chrome(path)
driver.get("https://odysee.com/$/signin")

while True:
	try:
		login = driver.find_element_by_id("username")
		login.send_keys(str(LOGIN_EMAIL))
		login.send_keys(Keys.RETURN)
	except Exception as e:
		print(e)
		time.sleep(0.5)
	else:
		break

while True:
	try:
		login = driver.find_element_by_id("password")
		login.send_keys(str(LOGIN_PW))
		login.send_keys(Keys.RETURN)
	except Exception as e:
		time.sleep(0.5)
		print(e)
		print('Line ~100')
	else:
		break



songs = codecs.open(str(song_file))

now = datetime.now()
today = date.today()

Current_Time = today.strftime("%d_%m_%Y")+"_With_Time:"+now.strftime("%H:%M:%S")
LOG_FILE = open("Uploadathon_Log_On_Date:"+str(Current_Time)+".txt", "x") # MAKE THE LOG FILE. THIS IS FUCKING IMPORTANT.


Song_Number = 0
for line in songs:  # GET THE FILE CONTAINING ALL OUR SONG TITLES + URLS AND SET TO VARIABLES SO WE CAN TYPE THEM IN
	line_num += 1 # Keep track of what line we're on.
	if str("Now playing") in line:
		video_number += 1 # Keep track of what video we're on by using a string that appears once per video.
		print("now on video number" + str(video_number))

	if video_number >= video_start and video_number <= video_end: # We want to increase the video number always so we know where we are, but only actually upload if the video number is within specifications.

		if str("Now playing") in line:
			driver.get("https://odysee.com/$/upload") # The string "Now playing" occurs exactly once per video, so it's a good marker for going to the upload page.

		if LOOK_FOR_TITLE == 1 and str('      <https://www.youtube.com/watch?v=') in line: # IF THE URL IS THERE, GET THE PART OF IT. THIS ALSO TELLS US THAT THE TITLE IS DONE SO UNFLAG THE VARIABLE TO STOP GETTING TITLE.
			print(title)
			URL_PART_1 = line.partition('watch?v=')[2]
			URL_PART_2 = URL_PART_1.partition('&list=')[0]
			Original_URL_Part_1 = line.partition('<')[2]
			Original_URL = Original_URL_Part_1.partition("&list")[0] # This is because I intent to credit original video in description.
			LOOK_FOR_TITLE = 0
			Look_For_Channel_URL = line_num + 3 # This is because I also intent to credit original *channel* and link it in description.
			Start_Upload = line_num + 6 # SINCE WE'RE DONE WITH THE TITLE AND HAVE THE URL, IT'S OKAY TO FLAG THIS NUMBER SO ON THE NEXT LINE WE CAN ACTUALLY START UPLOADING.

		if LOOK_FOR_TITLE == 1 and str('      <https://www.youtube.com/watch?v=') not in line:# and line != str("\n"):  # IF THE URL IS NOT THERE, KEEP GETTING THE TITLE FOR THE UPLOAD TITLE AND DO NOT FLAG THE VARIABLE TO STOP IT
			print(str(title))
			if line != "\n":
				if title == "":
					title = line
				else:
					title = title + str(" ") + line	

		if str('<https://www.youtube.com/watch?v=') in line and str('      <https://www.youtube.com/watch?v=') not in line and video_number >= 1: # WE'RE PAST THE URL, SO FLAG THE VARIABLE TO START GETTING TITLE
			LOOK_FOR_TITLE = 1
			title = ("")
			Song_Number += 1

		if Look_For_Channel_URL == line_num:		# Once we've gotten 3 lines later, we know it's the line with the channel URL, so get it via .partition.
			Channel_URL_Part_One = line.partition("https://www.youtube.com/")[2]
			Channel_URL_Part_Two = Channel_URL_Part_One.partition('>')[0]
			Channel_URL = str('https://www.youtube.com/') + str(Channel_URL_Part_Two)
			Look_For_Channel_Name = line_num + 2

		if Look_For_Channel_Name == line_num:			# Once we've gotten another 2 lines later, we know the channel name is there, and since this the one part without any bs, we can just take the whole line.
			Channel_Name = str(line)
			
			#At this point, we have all the necessary variables for the video, so start inputting them into Odysee.
			while True:# Input URL
				try:
					URL_Field = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/main/div/section[1]/div/div/div/fieldset-group/fieldset-section[2]/input")
					URL_Field.send_keys(URL_PART_2) #this is the part of the URL used in a URL search, present so such a search will return the vid being uploaded.
				except Exception as e:
					print(e)
					print('Line ~172')
					time.sleep(1.0)
				else:
					break
			Loop_Toggle = 0
			time.sleep(1)

			while Loop_Toggle == 0:# Get THE TITLE IN THE TITLE FIELD
				try:
					Title_Field = driver.find_element_by_xpath('/html/body/div[1]/div/div[3]/div[2]/main/div/section[1]/div/div/div/div[1]/fieldset-section/input')
				except Exception as e:
					print(e)
					print('Line - 177')
					time.sleep(1.0)
				else:
					Loop_Toggle = 1
			Loop_Toggle = 0
			time.sleep(1)
			title = title.replace("      ", "") # So we don't have extra space in our title.
			Title_Field.send_keys(Keys.SPACE)
			Title_Field.send_keys(Keys.BACKSPACE)
			keyboard = Controller()
			pyperclip.copy(title)
			keyboard.press(Key.ctrl)
			keyboard.press("v")
			keyboard.release(Key.ctrl)
			keyboard.release("v")
		# CONVERT TITLE TO WHAT THE FILE WILL BE CALLED SO WE CAN SEARCH.
			# We already got rid of instances of 6 white space created as an artifact from saving the playlist as .txt.
			# I tested this: Youtube won't let you have a title with more than 1 whitespace in a row, so that won't be a problem.
			# Also replace all slashes in the title with underlines because that's what youtube-DL did when saving to avoid error.
			# This pertains to Youtube-DL's file naming artifacts.
			# Actually, only convert if the default title is unacceptable.


			video_filename = str(title)
			print(str(video_filename[len(video_filename)-1]))
			print(title)
			print(video_filename)
			while True:
				if "*" or "|" or ":" or ":" or "?" or "__" in video_filename:
					print("Modifying filename as variant of title")
					video_filename = video_filename.replace("://", " -_")
					video_filename = video_filename.replace('/', '_')
					video_filename = video_filename.replace("\n", "")
					if video_filename[len(video_filename)-1] == "*" or video_filename[len(video_filename)-1] == str("|"):
						print("Yes, final character is asterisk")
						video_filename = video_filename[0:(len(video_filename)-1)]#This while loop is because if the final character is a | or a *
				#	print(str(video_filename))			                      #Then instead of replacing it, youtube-dl removes it in the naming
	                                                                         #process instead of replacing it with an underscore or different 
					if video_filename[0] == str('-'):                                             #character. A while loop is safer than if.
						video_filename = ("_" + video_filename.partition("-")[2]) 


					video_filename = video_filename.replace("**", "_")                    #I may find other characters that need a similar treatment.
					video_filename = video_filename.replace("*", "_") #This part was really wierd. Apparantly it replaces asterisks
					video_filename = video_filename.replace("||", "|")#with underscores UNLESS the asterisk is the final character.
					video_filename = video_filename.replace("|", "_") # I don't have a clue why it would do this since they're both
					video_filename = video_filename.replace(": ", " - ")# allowed characters, but ah well.
					video_filename = video_filename.replace(":", "_")
					video_filename = video_filename.replace(":", "'")
					video_filename = video_filename.replace("?", "")
					video_filename = video_filename.replace("__", "_")
					print('String is:')
					print(str(video_filename))
				else:
					break
				for file in os.listdir(str(STUFF)):
					if str(video_filename) in file and str(".mp4") in file and str(".mp4_") not in file and str(".jpg") not in file:
						print("Found it!")
						video_filename = str(file)
						break
#						Loop_Toggle = 0
#				if Loop_Toggle == 1:
					#print(video_filename)
#					else:
				break

#			Loop_Toggle = 1



			while True:
				try:
					upload = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/main/div/section[1]/div/div/div/fieldset-section/input-submit/button/span/span")
					upload.click()
				except Exception as e:
					time.sleep(1.0)
					print(e)
					print("Line ~247")
				else:
					break
			Loop_Toggle = 0


			time.sleep(2)
			keyboard = Controller()
			keyboard.press(Key.ctrl)# - this is from when I was trying to type it with sendkeys. Hopefully unnecessary.
			keyboard.press('l')     # - Okay, once I figure out how to interact with Odysee's file menu directly, this will
			keyboard.release('l')   # - become unnecessary. However, currently I am focused on ensuring Kanji accuracy.
			keyboard.release(Key.ctrl)
			time.sleep(2)
			print(str(STUFF)+ "/" + str(video_filename))
			pyperclip.copy(str(STUFF)+"/"+str(video_filename))
			time.sleep(0.5)
			keyboard.press(Key.ctrl)
			keyboard.press("v")
			keyboard.release(Key.ctrl)
			keyboard.release("v")
			time.sleep(2)
			keyboard.press(Key.enter)
			keyboard.release(Key.enter)
			time.sleep(2)
			#FIND DESCRIPTION AND CHECK THAT OUT

			print('typing description')
			#while True:
			#		try:
			while True:
				try:
					Description_Field = driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/main/div/section[2]/div/div/fieldset-section/div/div/div/textarea[1]")
					Description_Field.send_keys("This was uploaded by an AI. Original URL was/is: ")
				except Exception as e:
					keyboard.press(Key.enter)
					keyboard.release(Key.enter)
					time.sleep(1.0) #I think what's happening here is Description_Field exists without being interactable. So it passes to the else
					print(e)
					print("Line ~293")
				else:
   					break
			while True:
				try:
					Description_Field = driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/main/div/section[2]/div/div/fieldset-section/div/div/div/textarea[1]")
					Description_Field.send_keys(str(Original_URL) + "\n\n Original uploader name was/is: ")
					pyperclip.copy(Channel_Name)
					time.sleep(0.5)
					keyboard.press(Key.ctrl)
					keyboard.press("v")
					keyboard.release(Key.ctrl)
					keyboard.release("v")
					Description_Field.send_keys("\n\nOriginal uploader's channel's URL was/is: " + str(Channel_URL) + "\n\n Original, title, and thumbnail have been typed and uploaded here. Original description was/is:\n")
				except Exception as e:
					print(e)
					print("Line ~307")
					print('delaying for some reason')
					time.sleep(1.0)    #and then fails it. Solution: Simply have the else *as* the try and loop until it goes through. Do that tomorrow.
				else:
					break
			Loop_Toggle = 0

			video_filename = video_filename.partition(".mp4")[0]
			current_file = codecs.open(STUFF+"/"+str(video_filename)+".description", "r")
			print(str(current_file))
			for line in current_file:
				while True:
					try:
						Description_Field.send_keys(Keys.RETURN)
						Description_Field.send_keys(Keys.BACKSPACE)
						Description_Field = driver.find_element_by_id("content_description") 
						pyperclip.copy(str(line))
						keyboard.press(Key.ctrl)
						keyboard.press("v")
						keyboard.release(Key.ctrl)
						keyboard.release("v")								 #basically everything, we're going to
						Description_Field.send_keys(Keys.RETURN)							 #have to start with a search to determine
					except Exception as e:																	 #if we have any weird characters. If we do
						print(e)
						print("Line ~352")
						print('delaying and trying again')				 #then we have to print each one with \u or
						time.sleep(1.0)														 #the equivalent keyboard hotkeys.
					else:
						break
			Description_Field.send_keys(Keys.BACKSPACE)
			time.sleep(2)

			#UPLOAD THUMBNAIL
			also_path = "file:///home/wind/TEST/STUFF/"
			video_filename = video_filename.partition(".description")[0]
			for file in os.listdir(str(STUFF)):
				if str(video_filename) in file and str(".mp4_3.jpg") in file:
					video_filename = str(file)
					print(str(video_filename))
				if str(video_filename) in file and str(".mp4_2.jpg") in file:
					video_filename = str(file)
					print(str(video_filename))

			while True:
				try:
					Upload_Thumnail = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div[2]/main/div/div/section[1]/div/div/div/div[2]/fieldset-section/input-submit/button/span/span")
				except Exception as e:
					print("can't find thumbnail upload. Trying something else.")
					print(e)
					try:
						Thumbnail_Upload_Tool = driver.find_element_by_xpath("/html/body/div/div/div/div/main/div/div[2]/section[2]/div/div/div/div[2]/div/button/span/span")
						time.sleep(1)
						Thumbnail_Upload_Tool.click()
					except Exception as e:
						print(e)
						print("Line ~399")
						print("okay something's seriously wrong here")
						time.sleep(1.0)
					else:
						print("Okay, we found the other button, let's it and see if we get to ")
				else:
					try:
						Upload_Thumnail.click()
					except Exception as e:
						print(e)
						print("Line ~409")
						time.sleep(1.0)
					else:
						break
			time.sleep(2)

			keyboard.press(Key.ctrl)
			keyboard.press('l')
			keyboard.release('l')
			keyboard.release(Key.ctrl)
			pyperclip.copy(str(STUFF)+"/"+str(video_filename))
			time.sleep(0.5)
			keyboard.press(Key.ctrl)
			keyboard.press("v")
			keyboard.release(Key.ctrl)
			keyboard.release("v")
			print(str(STUFF)+str(video_filename))
			time.sleep(1)
			keyboard.press(Key.enter)
			keyboard.release(Key.enter)
			time.sleep(1)
			keyboard.press(Key.enter)
			keyboard.release(Key.enter)


#			while True:
#				try:
#					Yes_Im_Sure_Upload = driver.find_element_by_xpath('/html/body/div[5]/div/div/div/button[1]/span/span')
#					Yes_Im_Sure_Upload.click()
#				except:
#					print("Line ~410")
#				else:
#					break
			time.sleep(1)
			while True:
				print('searching for Yes_Im_Sure')
				try:
					Yes_Im_Sure = driver.find_element_by_xpath('/html/body/div[6]/div/div/div/button[1]/span/span')
					Yes_Im_Sure.click()
				except Exception as e:
					print('trying again')
					print(e)
					print("Line ~424")
					time.sleep(1.0)
				else:
					break
			

			while True:
				try:
					print("Searching for upload button...")
					Upload_Button = driver.find_element_by_xpath("/html/body/div/div/div[3]/div[2]/main/div/section[3]/div/button[1]/span/span")
				except Exception as e:
					print("Upload button not found. Sleeping and trying again...")
					print(e)
					print("Line ~517")
					keyboard.press(Key.end)
					keyboard.release(Key.end)
					time.sleep(1.0)
				else:
					print("Upload button found. Ending search loop.")
					break
			while True:
				try:
					print("Attempting to click upload button...")
					Upload_Button.click()
				except Exception as e:
					print(e)
					print("Line ~430")
					print("Upload button unclickable. Sleeping and trying again...")
					keyboard.press(Key.end)
					keyboard.release(Key.end) ##pressing the end key is so that if an ad has popped up and is in the way, we can skip past it.
					time.sleep(1.0)
				else:
					print("Upload button clicked successfully. Ending attempt loop.")
					break
					time.sleep(1)

			driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			while True:
				try:
					Upload_Button2 = driver.find_element_by_xpath("/html/body/div[6]/div/div/form/section/div/div[3]/div[1]/button[1]/span/span")
				except Exception as e:
					print(e)
					print("Line ~498")
					time.sleep(1.0)
				else:
					break
			while True:
				try:
					Upload_Button2.click()
				except Exception as e:
					keyboard.press(Key.end)
					keyboard.release(Key.end)
					print(e)
					print("Line ~452")
				else:
					break
		
			while True:
				try:
					driver.find_element_by_xpath("/html/body/div[6]/div/div/section/div/div[3]/div/button[1]/span/span")
				except Exception as e:
					print(e)
					print("Line ~520")
					time.sleep(1.0)
				else:
					Loop_Toggle = 1
					print("okay we're at the end of the loop")
					LOG_FILE.write('Video "'+str(title)+'" successfully uploaded! \n \n \n')
					break
		#Go to the uploads page so we know it's working (and to HOPEFULLY void the thing there the info for the last vid is still there)
		#		Loop_Toggle = 1
		#		while Loop_Toggle == 0:
		#			try:
		#				driver.find_element_by_tag_name('Your content will be live shortly.')
		#			except:
		#				print("Tried, waiting again.")
		#				time.sleep(5.0)
		#			else:
		#				Loop_Toggle = 1

					# OKAY GOYIMS THE NEXT STEP IS TO ADD A THING WHERE WHEN IT'S TYPING THE DESCRIPTION IF THE CHARACTER
					# IS UNSUPPORTED BY WEBDRIVER THEN IT SAYS [UNSUPPORTED CHARACTER: UNICODE = "xxxxx"] WHERE "xxxxx" IS
					# EQUAL TO WHATEVER TEH UNICODE OF THE UNSUPPORTED CHARACTER IS.


		#		keyboard.release(Key.enter)
		#		time.sleep(2)
		#		keyboard.press(Key.tab)
		#		keyboard.release(Key.tab)
		#		time.sleep(1)
		#		keyboard.press(Key.enter)
		#		keyboard.release(Key.enter)
		#		time.sleep(10)
		#		driver.quit()
		#				print("\n\n\n\n\n\n OKAY GOYIMS WE'RE DONE WITH THAT FIRST FILE'S DESCRIPTION!!")
					# OKAY BOIS NEXT TIME WE'RE GOING TO GO ADD A THING WHERE IT CLICKS THE DESCRIPTION AND ADDS THE LINE TO IT
					# ALSO REMOVE THE LNE ABOUT GOYIMS BECAUSE THAT'S NOT ACCURATE TO THE DESCRIPTION (and if it is it would 
					# still render the description inaccurate because it would be redundant since the top line would cover it 
					# and then we'd have one more line containing that phrase in the description than is supposed to be there.

		# OKAY GOYIMS GREAT NEWS! The XPATH for the "success" message after upload *should* be done is
		# 		/html/body/div[4]/div/div/section/div/div[1]/div[1]/div/h2
		# Without the spaces or hashtag, ofc

		# OKAY GOYIMS IT SEEMS TO HAVE HAVING ISSUES GETTING SECONDARY BUTTONS BUT WE'LL WORRY ABOUT THAT LATER

		# OKAY GOYIMS THE PROBLEM WITH THE DESCRIPTION FIELD IN ODYSEE IS THAT YOU GOTTA UPLOAD A FILE FIRST. SO DO THAT MY DUDE!!!!!!!

		#		youtube-dl -f, --write-all-thumbnails --write-description --format mp4 https://www.youtube.com/playlist?list=PL1DX5hVfxc_f18xRVIyqfP-hdybOboPNz 

		#		Make sure you add the audio tag, too

		#		ALSO AND I'M ACTUALLY SERIOUS ABOUT THIS: CTRL-L LET'S YOU ACCESS THE FILE PATH FROM THE FILE-BROWSER POPUP.
		#		USE THIS BECAUSE I'M SURE IT'S GONNA BE MORE RELIABLE THAN DOWN ARROWS AND SEARCHING FOR IT. Remember you can 
		#		use your variables to find the path to type.




		# So far so good. Adds URL, Title and file properly*. Still need to figure a way to add description and Thumbnail.
		# I suspect description will involve pulling from the .description files after listing them with os.listdir and
		# the thumbnails will be found by a similar search technique to the one used to find video files.
		# Also make sure to implement something that ensures the video is fully uploaded (and working(?)) before proceeding
		# to the next one. This could take a while.... (to run, I mean, not to develop).
		#
		# *By "properly" I mean it *will* work properly because currently the fact that I was using coincidence detector
		#  screwed it up because some of the "titles" according to the document of it have ((( ))) around them while the
		#  files themselves don't. Since I'm going to need to redownload anyway, in order to get the description and the
		#  thumbnails, I'll fix it then.











		#		keyboard.press(Key.enter)
		#		keyboard.release(Key.enter)
		#		time.sleep(5)
		#		driver.quit()
		#time.sleep(0.2)
		#keyboard.type(GAY)
		#	THINGY = open("WTF.txt", "r")
		#	HOMOSEXUAL = 4
		#for line in WTF.txt:
		#	if HOMOSEXUAL == line.getlinenumber()
		#	print(line)
		#<button aria-label="Browse" class="button button--secondary" type="button"><span class="button__content"><span dir="auto" class="button__label">Browse</span></span></button>


		#   print(getframeinfo(currentframe()))
		#	- this is a cool function. Keep it around for later.
