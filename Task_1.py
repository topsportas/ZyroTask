from selenium import webdriver
import os
import urllib.request
import itertools
import json
import threading



def downloader(url, path, name):
    full_path = os.path.join(path, name + ".jpg")
    urllib.request.urlretrieve(url, full_path)
    print(full_path)


def scraperText():
    texts = driver.find_elements_by_class_name("font_9")
    all_texts = [i.text for i in texts]
    dict_of_all_text = dict(enumerate(all_texts))
    with open('all_texts.json', 'w') as f:
        json.dump(dict_of_all_text, f, indent=4)


def scraperIMG():
    images = driver.find_elements_by_css_selector('wix-image')
    img_urls = []
    img_names = []
    threads_list = []
    for single_image in images:
        url = single_image.get_attribute("data-src")
        name = single_image.get_attribute("id")
        img_urls.append(url)
        img_names.append(name)

    urls_names_list = zip(img_urls, img_names)
    new_folder = "Downloaded pictures"
    try:
        os.mkdir(new_folder)
    except OSError:
        print("Creation of the directory %s failed" % os.getcwd())
    else:
        print("Successfully created the directory %s " % os.getcwd())
    new_path = os.path.join(os.getcwd(), new_folder)

    for url, name in urls_names_list:
        threads_list.append(threading.Thread(target=downloader, args=(url, new_path, name)))
    for t in threads_list:
        t.start()
    for t in threads_list:
        t.join()

if __name__ == "__main__":
    startTime = datetime.now()
    threads = []
    chromedriver = os.path.realpath("chromedriver.exe")
    driver = webdriver.Chrome(chromedriver)
    driver.get("https://mekass.wixsite.com/website")
    scraperText()
    scraperIMG()
    driver.close()
