from selenium import webdriver
import os
import urllib.request
import itertools
import json

def downloader(url, path, name):
	full_path = path + name + ".jpg"
	urllib.request.urlretrieve(url,full_path)

path = os.getcwd() + "\\"
chromedriver = path + "chromedriver.exe" 
driver = webdriver.Chrome(chromedriver)
driver.get("https://mekass.wixsite.com/website")
texts = driver.find_elements_by_class_name("font_9")
all_texts = []
for text in texts:
	all_texts.append(text.text)

dictOfWords = { i : all_texts[i] for i in range(0, len(all_texts) ) }
with open('all_texts.json', 'w') as f:
	json.dump(dictOfWords,f, indent=4)

images = driver.find_elements_by_css_selector('wix-image') 
img_urls = []
img_names = []
for single_image in images:
	url = single_image.get_attribute("data-src")
	name = single_image.get_attribute("id")
	img_urls.append(url)
	img_names.append(name)

urls_names_list = list(itertools.zip_longest(img_urls, img_names))
new_folder = "Downloaded pictures"
try:
	os.mkdir(new_folder)
except OSError:
	print("Creation of the directory %s failed" % path)
else:
	print ("Successfully created the directory %s " % path)
new_path = path + new_folder + "\\"
for url, name in urls_names_list:
	downloader(url,new_path,name)

driver.close()