import requests
import json
import sys
import math
import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By

options = Options()
	
options.headless = True

driver = webdriver.Firefox(options=options)

#driver = webdriver.Firefox()

driver.implicitly_wait(3)

description = []
seller = []
price = []
make = []
model = []
year = []
mileage = []
bodystyle = []
colour = []
co2emission = []
doors = []
transmission = []
wasStolen = []
wasWriteOff = []
wasScrapped = []
engineSize = []
fuelType = []

carList = pd.read_csv('carlist.csv')

baseURL = "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=TRUE"
postcode = "&postcode=PO16+7GZ"
pagination = "0"

print(carList)

i = 0
a = len(carList.index)


while i < a:
	
	Make = carList.at[i, 'Make']
	Model = carList.at[i, 'Model']	
	driver.get(baseURL + postcode + "&make=" + Make + "&model=" + Model)
	try:
		pagination = driver.find_elements_by_class_name('pagination--li')[-2].find_element(By.XPATH, './/a').get_attribute('data-paginate')
	except:
		pagination = driver.find_elements_by_class_name('pagination--li')[-2].get_attribute('innerHTML')
	paginationLen = int(pagination)
	b = 1
	
	while b <= paginationLen:
		searchURL = baseURL + postcode + "&make=" + Make + "&model=" + Model + "&page=" + str(b)
		driver.get(searchURL)
		print("Scraping page " + str(b) + " of " + str(paginationLen) + " Make: " + Make + " Model: " + Model)
		SERPitems = driver.find_elements_by_class_name('search-page__result')
		URLS = []
		for item in SERPitems:
			URLS.append(item.find_element(By.XPATH, './/a').get_attribute('href'))
		for url in URLS:
			driver.get(url)
			print("Scraping car " + str(URLS.index(url)) + " of " + str(len(URLS)) + " in serps page " + str(b) + " of " + str(paginationLen))
			colour.append('')
			make.append(Make)
			model.append(Model)
			try:
				driver.find_elements_by_class_name('tClsIcn')[0].click()
			except:
				print('No modal visible')
			try:
				driver.find_elements_by_class_name('truncated-text__view-more')[0].click()
			except:
				print('description not truncated')	
			try:
				description.append(bs(driver.find_elements_by_class_name('truncated-text')[0].get_attribute('innerHTML'), "lxml").get_text(strip=True))
			except:
				print('description missing')
				description.append('n/a')
			try:
				seller.append(bs(driver.find_elements_by_class_name('seller-name')[0].get_attribute('innerHTML'), "lxml").get_text(strip=True))
				price.append(bs(driver.find_elements_by_class_name('advert-price__cash-price')[0].get_attribute('innerHTML'), "lxml").get_text(strip=True))	
			except:
				print('seller and price missing')
				seller.append('')
				price.append('')
			try:
				co2emission.append(bs(driver.find_elements_by_class_name('info-list')[1].find_elements(By.XPATH, './/li')[9].get_attribute('innerHTML'), "lxml").get_text(strip=True))
			except:
				print('info list missing')
				co2emission.append('n/a')
			try:
				year.append(bs(driver.find_elements_by_class_name('key-specifications')[0].find_elements(By.XPATH, './/li')[0].get_attribute('innerHTML'), "lxml").get_text(strip=True))
				mileage.append(bs(driver.find_elements_by_class_name('key-specifications')[0].find_elements(By.XPATH, './/li')[2].get_attribute('innerHTML'), "lxml").get_text(strip=True))
				bodystyle.append(bs(driver.find_elements_by_class_name('key-specifications')[0].find_elements(By.XPATH, './/li')[1].get_attribute('innerHTML'), "lxml").get_text(strip=True))
				doors.append(bs(driver.find_elements_by_class_name('key-specifications')[0].find_elements(By.XPATH, './/li')[6].get_attribute('innerHTML'), "lxml").get_text(strip=True))
				transmission.append(bs(driver.find_elements_by_class_name('key-specifications')[0].find_elements(By.XPATH, './/li')[4].get_attribute('innerHTML'), "lxml").get_text(strip=True))
				engineSize.append(bs(driver.find_elements_by_class_name('key-specifications')[0].find_elements(By.XPATH, './/li')[3].get_attribute('innerHTML'), "lxml").get_text(strip=True))
				fuelType.append(bs(driver.find_elements_by_class_name('key-specifications')[0].find_elements(By.XPATH, './/li')[5].get_attribute('innerHTML'), "lxml").get_text(strip=True))
			except:
				print('key specifications missing')
				year.append('n/a')
				mileage.append('n/a')
				bodystyle.append('n/a')
				doors.append('n/a')
				transmission.append('n/a')
				engineSize.append('n/a')
				fuelType.append('n/a')
			if driver.find_elements_by_class_name('vehicle-check-unavailable'):
				print('Vehicle check could not be complete')
				wasStolen.append('n/a')
				wasWriteOff.append('n/a')
				wasScrapped.append('n/a')
			else:
				try:
					wasStolen.append(bs(driver.find_elements_by_class_name('basic-check-m__check-list')[0].find_elements(By.XPATH, './/li')[0].get_attribute('innerHTML'), "lxml").get_text(strip=True))
					wasWriteOff.append(bs(driver.find_elements_by_class_name('basic-check-m__check-list')[0].find_elements(By.XPATH, './/li')[2].get_attribute('innerHTML'), "lxml").get_text(strip=True))
					wasScrapped.append(bs(driver.find_elements_by_class_name('basic-check-m__check-list')[0].find_elements(By.XPATH, './/li')[1].get_attribute('innerHTML'), "lxml").get_text(strip=True))
				except:
					wasStolen.append(bs(driver.find_elements_by_class_name('completed-checks__list')[0].find_elements(By.XPATH, './/li')[0].get_attribute('innerHTML'), "lxml").get_text(strip=True))
					wasWriteOff.append(bs(driver.find_elements_by_class_name('completed-checks__list')[0].find_elements(By.XPATH, './/li')[2].get_attribute('innerHTML'), "lxml").get_text(strip=True))
					wasScrapped.append(bs(driver.find_elements_by_class_name('completed-checks__list')[0].find_elements(By.XPATH, './/li')[1].get_attribute('innerHTML'), "lxml").get_text(strip=True))	
		b += 1
	
	
	
	i += 1

data = {
	'description': description,
	'seller': seller,
	'price': price,
	'make': make,
	'model': model,
	'year': year,
	'mileage': mileage,
	'bodystyle': bodystyle,
	'colour': colour,
	'co2emission': co2emission,
	'doors': doors,
	'transmission': transmission,
	'wasStolen': wasStolen,
	'wasWriteOff': wasWriteOff,
	'wasScrapped': wasScrapped,
	'engineSize': engineSize,
	'fuelType': fuelType
}


df = pd.DataFrame.from_dict(data)
	
with open("finaloutput.csv", "w+", encoding="utf-8") as file:
	file.write(df.to_csv())

	
driver.quit()
