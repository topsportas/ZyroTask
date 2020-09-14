from bs4 import BeautifulSoup as bs
import requests
import json
from json import JSONEncoder
import pandas as pd

class Car:
    def __init__(self, make="-", model="-", year="-", mileage="-", price=0.0, features="-"):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.price = price
        self.features = features

class CarEncoder(JSONEncoder):
        def default(self, o):
            return o.__dict__        

def ParseAd(url):
    r = requests.get(url)
    soup = bs(r.content, "lxml")
    make = str(soup.h1).split(",")[0].split(">")[1].split(" ")[0]
    model = str(soup.h1).split(",")[0].split(make+" ")[1]
    year = ""
    mileage = ""
    price = soup.select("div.price")[0].text.strip().replace(" ", "").replace("\u20ac", "")
    features = {}
    params = soup.findAll("div", {"class":"parameter-row"})
    for p in params:
        label = p.select("div.parameter-label")
        value = p.select("div.parameter-value")
        if label and value:
            if label[0].string.strip() == "Date of manufacture":         
                year = value[0].string.strip()
            if label[0].string.strip() == "Mileage":
                mileage = value[0].string.strip()
 
    feats = soup.findAll("div", {"class":"feature-row"})
    for f in feats:
        label = f.select("div.feature-label")
        value = f.select("div.feature-list")
        if label and value:
            features[label[0].string.strip()] = [x.string.strip() for x in value[0].findAll("span")]       

    return Car(
        make = make,
        model = model,
        year = year,
        mileage = mileage,
        price = price,
        features = features                           
    )


baseURL = "https://en.autoplius.lt/ads/used-cars?make_id=99"
pageLinks = [baseURL + "&page_nr=" + str(x+1) for x in range(5)]
carAdLinks = []
results = []
   
for link in pageLinks:
    r = requests.get(link)
    soup = bs(r.content, "lxml")
    elems = soup.findAll("a", {"class":"announcement-item"})
    for e in elems:
        carAdLinks.append(e.get("href"))

for ad in carAdLinks:
    results.append(ParseAd(ad))

allCars = json.dumps(results, indent=4, cls=CarEncoder)
with open("all_cars.json", "wb") as f:
    f.write(allCars.encode("utf-8"))
    f.close()

prices = []
mileages = []
models = []
equipment = []


for car in results:
    prices.append(int(car.price))
    mileages.append(car.mileage.replace("km","").replace(" ", ""))
    models.append(car.model)
    count_features = list(car.features.values())
    count = sum([len(listElem) for listElem in count_features])
    equipment.append(count)
    
mileages = [int('0' + i) for i in mileages] 
df = pd.DataFrame(list(zip(models, prices, mileages,equipment)), columns=['models','prices', 'mileages', 'features/equipment'])
avg_prc_mile_by_model = df.groupby(['models'])[["prices", "mileages"]].mean().round(0)
unique_models = df['models'].nunique()
features_for_every_model = df.groupby(['models'])[["features/equipment"]].sum()
print("Average price and mileage by model")
print(avg_prc_mile_by_model)
print("\n")
print("\n")
print("Unique models count is: " + str(unique_models))
print("\n")
print("\n")
print("Total count of features for every model")
print(features_for_every_model)
