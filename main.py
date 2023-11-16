#Import Modules 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

#Credentials 
MoussaEmail = "moussamobarak44@gmail.com"
MoussaPass = "Bahadur04@0"

#Signing Into Dice
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.dice.com/dashboard/login")
email = driver.find_element(By.ID,"email")
email.send_keys(MoussaEmail)
password = driver.find_element(By.ID, "password")
password.send_keys(MoussaPass)
Submit = driver.find_element(By.XPATH, '//*[@id="loginDataSubmit"]/div[3]/div/button')
Submit.click()

#Switching to Job page
JobPage = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'submitSearch-button')))
JobPage.click()
JobPageWait = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="singleCheckbox"]/span/button/i')))

#Selecting Quick Apply
EasyApply = driver.find_element(By.XPATH, '//*[@id="singleCheckbox"]/span/button/i')
EasyApply.click()

#Filtering for roles
Role = driver.find_element(By.XPATH, '//*[@id="typeaheadInput"]')
Role.send_keys("Azure")
SubmitRole = driver.find_element(By.XPATH, '//*[@id="submitSearch-button"]')
SubmitRole.click() 

#Filtering by Date
Date = driver.find_element(By.XPATH, '//*[@id="facets"]/dhi-accordion[2]/div[2]/div/js-single-select-filter/div/div/button[2]')
Date.click()

#Change job count to 100
JobCount100 = driver.find_element(By.XPATH, '//*[@id="pageSize_2"]/option[4]')
JobCount100.click()


#Get IDs of each job card
no2 = driver.find_element(By.XPATH, "/html/body/dhi-js-dice-client/div/dhi-search-page-container/dhi-search-page/div/dhi-search-page-results/div/div[3]/js-search-display/div/div[4]/div[1]/js-search-pagination-container/pagination/ul/li[3]")
no2.click()
time.sleep(10)
jobIDs = []
for i in range(1,100):
	try:
		xpathString = '/html/body/dhi-js-dice-client/div/dhi-search-page-container/dhi-search-page/div/dhi-search-page-results/div/div[3]/js-search-display/div/div[3]/dhi-search-cards-widget/div/dhi-search-card[{}]/div/div[1]/div/div[2]/div[1]/h5/a'.format(i)
		jobSelect = driver.find_element(By.XPATH, xpathString)
	except:
		print("path not valid")
	else:
		try: #filter out jobs already applied to
			xpathString = '/html/body/dhi-js-dice-client/div/dhi-search-page-container/dhi-search-page/div/dhi-search-page-results/div/div[3]/js-search-display/div/div[3]/dhi-search-cards-widget/div/dhi-search-card[{}]/div/div[1]/div/div[1]/dhi-status-ribbon'.format(i)
			driver.find_element(By.XPATH, xpathString)
		except:
			job = jobSelect.get_attribute(By.ID)
			jobIDs.append(job)
			


#Print out jobIds that will be applied to 
print("\nTodays JobIDs:\n")
for jobID in jobIDs:
	print(jobID)
print("\n")


#apply to gathered jobIDs
currentWindow = 0
for jobID in jobIDs:

	print("CURRENTLY ITERATING ON: {}".format(jobID))
	time.sleep(3)

	driver.get("https://www.dice.com/job-detail/{}".format(jobID))

	ableToBeginApply = False

	for i in range(10):

		#polling shadow root
		try:
			shadowRoot = driver.find_element(By.CSS_SELECTOR, "apply-button-wc[job-id='{}']".format(jobID)).shadow_root
		except:
			print("WAITING ON APPLY BUTTON: {}".format(i))
			time.sleep(2)
		else:
			time.sleep(2)
			for i in range(5):

				#polling shadow content
				try:	
					shadowContent = shadowRoot.find_element(By.CSS_SELECTOR, 'apply-button[class="job-app hydrated"]')
				except:
					print("WAITING ON SHADOW CONTENT: {}".format(i))
					time.sleep(2)
				else:
					shadowContent.click()
					ableToBeginApply = True
					break
			break

	if ableToBeginApply == True:
		nextButton =  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[4]/div/div[1]/div/div/span/div/main/div[4]/button[2]')))
		nextButton.click()

		try:
			applyAttempt = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[4]/div/div[1]/div/div/span/div/main/div[3]/button[2]/span'))).text
		except:
			print("ERROR ON JOB APPLICATION SUBMISSION")
		else:
			if applyAttempt == "Apply":
				applyButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[4]/div/div[1]/div/div/span/div/main/div[3]/button[2]')))
				applyButton.click()
				print("JOB SUBMITTED: {}\n".format(jobID))
			else:
				print("JOB FAILED TO SUBMIT (ADDITIONAL INFO REQUIRED): {}\n".format(jobID))
				driver.execute_script("window.open('');")
				driver.close()
				driver.switch_to.window(driver.window_handles[currentWindow]) 
	else:
		print("JOB SUBMISSION FAILURE")
		driver.execute_script("window.open('');")
		driver.close()
		driver.switch_to.window(driver.window_handles[currentWindow]) 



print("\nSCRIPT COMPLETE\n")

time.sleep(1000)
driver.close()
