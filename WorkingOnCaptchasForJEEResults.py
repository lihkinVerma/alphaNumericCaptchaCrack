
#-----------------------------------------------------------------------------------
# *
# * Code Developed solely for 
# * Education Institute of Engineering and Technology 
# * that give admission to students using JEE exam results
# *
# * Developer: Nikhil Verma
# * Present Location: Noida, Uttar Pradesh, India
# * Ph:- 6283273195, email:- lih.verma@gmail.com
# * 
#-----------------------------------------------------------------------------------

print( "-*- -*- -*- -*- -*- -*- Code Starts Here -*- -*- -*- -*- -*- -*- ")

#-----------------------------------------------------------------------------------
# Importing required libraries
#-----------------------------------------------------------------------------------
import time,random, sys
import pandas as pd
import logging,os
import shutil as sh
import pytesseract as pt
from PIL import Image 

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
print( "#----------------------------------------------")
print( "# Imported all required Libraries")
print( "#----------------------------------------------")

#-----------------------------------------------------------------------------------
# Create directory to Save the captchas while processing
#-----------------------------------------------------------------------------------
directory = "data1/"
now= os.getcwd()
if not os.path.exists(directory):
    os.makedirs(directory)
print( "#----------------------------------------------")
print( "# Made directory to save Captchas while processing")
print( "#----------------------------------------------")

#-----------------------------------------------------------------------------------
# Load the Browser
#-----------------------------------------------------------------------------------
startTime= time.time()
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
#driver = webdriver.Chrome(chrome_options=options)
driver.get("https://jeemain.nic.in/JeeMainApp/Root/AuthCandWithDob.aspx?enc=m2D7TosKDxSG8zxkQNDLug==")
wait = WebDriverWait(driver, 500)
print( "#----------------------------------------------" )
print( "# Loaded Browser Successfully" )
print( "#----------------------------------------------" )

#----------------------------------------------------------------------------------
# Read data from input file having valid application numbers
#----------------------------------------------------------------------------------
df= pd.read_csv(sys.argv[1])

# some data processing
df['Date of Birth'] = pd.to_datetime(df['Date of Birth'], format='%d/%m/%Y')
os.chdir(os.getcwd()+'/data1')
print( "#----------------------------------------------" )
print( "# Input Data fetched successfully" )
print( "#----------------------------------------------" )

#-----------------------------------------------------------------------------------
# Create data structure to save the results
#-----------------------------------------------------------------------------------
res= pd.DataFrame(index= range(len(df)), columns=[	'Application Number', \
							'Candidate Name', \
							'Mother Name', \
							'Father Name', \
							'category', \
							'Gender', \
							'State Code of Eligibility', \
							'Roll Number', \
							'Person with Disability', \
							'Nationality', \
							'Physics', \
							'Chemistry', \
							'Mathematics', \
							'Total' \
						])
print( "#----------------------------------------------" )
print( "# Created Empty Result Data Structure for storing" )
print( "#----------------------------------------------" )

#-----------------------------------------------------------------------------------
# defining function to predict text from captcha
#-----------------------------------------------------------------------------------
def get_captcha_text(location, size, name):   
	im = Image.open(name)   
	left = location['x']    
	top = location['y']    
	right = location['x'] + size['width']     
	bottom = location['y'] + size['height']
	im = im.crop((left, top, right, bottom)) # defines crop points
	im.save(name) 
	captcha_text = pt.image_to_string(name)
	return captcha_text

#-----------------------------------------------------------------------------------
# Iterate the code through all Application numbers
#-----------------------------------------------------------------------------------
i, j= 0, 0
while i<len(df):
	if(j==0):
		print( "#----------------------------------------------" )
		print( "# Fetching results for : ", str(int(df['JEE Main-Jan 2019 Application No.'][i])) )
		print( "#----------------------------------------------" ) 
	try:
		# Put Application number
		try:
			text_area = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_txtRegNo"]')
			text_area.send_keys(int(df['JEE Main-Jan 2019 Application No.'][i]))
		except:
			print( "Not found text box for Application Number" )

		# Put Day 
		try:
			s1=Select(driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ddlday"]'))
			s1.select_by_index(df['Date of Birth'][i].day)
		except:
			print( "Not found day" )

		# Put Month
		try:
			s1=Select(driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ddlmonth"]'))
			s1.select_by_index(df['Date of Birth'][i].month)
		except:
			print( "Not found month" )

		# Put Year
		try:
			s1=Select(driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_ddlyear"]'))
			s1.select_by_value(str(df['Date of Birth'][i].year))
		except:
			print( "Not found year" )
		
		# Find captcha and predict the text
		try:
			captcha= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_captchaimg"]')
			location = captcha.location    
			size = captcha.size    
			driver.save_screenshot("captcha"+str(i)+".png")
 
			# download the image
			captcha_text = get_captcha_text(location, size, "captcha"+str(i)+".png") 
			os.rename("captcha"+str(i)+".png", captcha_text+".png")
			if (len(captcha_text)!=6 or not captcha_text.isalnum()):
				raise Exception("Length is small, Invalid prediction")
			
			# Put text in textarea
			text_area = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_Secpin"]')
			text_area.send_keys(captcha_text)
		except:
			# Click Refresh Button
			refresh_button=driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_bttRegCaptcha"]')
			refresh_button.click()
			j= j+1
			continue
		# Click Login Button		
		try:
			time.sleep(10)
			login_button=driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_Submit1"]')
			login_button.click()
			obj = driver.switch_to.alert
			# obj.text
			obj.accept()
			j= j+1
			continue
		except:
			i=i+1
		
		# Save data if result page opened successfully
		try:
			res['Application Number'][i-1]= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblAppno"]').text
			res['Candidate Name'][i-1]= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblName"]').text
			res['Mother Name'][i-1]= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblMName"]').text
			res['Father Name'][i-1]= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblFname"]').text
			res['category'][i-1]= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblCategory"]').text
			res['Gender'][i-1]= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblGender"]').text
			res['State Code of Eligibility'][i-1]= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblStateofEligiblity"]').text
			res['Roll Number'][i-1]= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblRollno"]').text
			res['Person with Disability'][i-1]= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblPh"]').text
			res['Nationality'][i-1]= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblNationality"]').text
			res['Physics'][i-1]= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblPaper1Physics"]').text
			res['Chemistry'][i-1]= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblPaper1Chemistry"]').text
			res['Mathematics'][i-1]= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lblPaper1Math"]').text
			res['Total'][i-1]= driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolder1_lbltotalPaper1"]').text
		
			print( "Data Collected Successfully" )
			print( res.loc[i-1] )
		except:
			print( "Not found someresult" )
		time.sleep(10)
		
		# close the Browser for safety purposes		
		driver.close()
		print( "#----------------------------------------------" )
		print( "# Done with Application Number: ",str(df['JEE Main-Jan 2019 Application No.'][i-1]) )
		print( "#----------------------------------------------")
		time.sleep(10)
		j=0
		if i< len(df):
			# Reopen the Browser for another applicant
			driver = webdriver.Chrome(chrome_options=options)
			driver.get("https://jeemain.nic.in/JeeMainApp/Root/AuthCandWithDob.aspx?enc=m2D7TosKDxSG8zxkQNDLug==")
			wait = WebDriverWait(driver, 500);

		#-------------------------------------------------------------
		# Save results fetched as in result.csv file
		#-------------------------------------------------------------
		res.to_csv("results.csv")
	except Exception as e:
		print((e))
		continue

#-----------------------------------------------------------------------------------
# End of Code
#-----------------------------------------------------------------------------------
sh.copy('results.csv', now)
os.chdir(now)
sh.rmtree('data1')
print( "Total time taken to run the script is: ", str( time.time()- startTime), "seconds" )
print( "#----------------------------------------------")
print( "# Result in results.csv")
print( "#----------------------------------------------")

print( "-*- -*- -*- -*- -*- -*- Code Ends Here -*- -*- -*- -*- -*- -*- ")
