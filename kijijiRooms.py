import requests 
from bs4 import BeautifulSoup
import pandas as pd

title= []
desc= []
time = []
add = []
links =[]
prices = []
locations = []

output = pd.DataFrame()
while True:
	try:
		limit = input("How many pages to scrape ....? ")
		if(int(limit)<2):
			raise Exception("Sorry 2 is the least ...")
		else:
			break
	except Exception as e:
		print(e)
loader = "*"
for i in range(1,int(limit)):
	try:
		url = "https://www.kijiji.ca/b-room-rental-roommate/markham-york-region/village/page-"+str(i)+"k0c36l1700274?radius=29.0&address=10+Freshway+Dr%2C+Concord%2C+ON+L4K+1S3%2C+Canada&ll=43.794232,-79.509205&rb=true"
		loader = loader+"*"
		print(loader)
		x = requests.get(url,timeout=30)
		soup = BeautifulSoup(x.text, 'html.parser')
		info_container = soup.findAll("div", class_="info-container")
		description = soup.findAll("div",class_="description")
		price = soup.findAll("div",class_="price")
		location = soup.findAll("div",class_="location")
		for i in info_container:
			urls = i.find('a')['href']
			links.append("https://www.kijiji.ca"+urls)
			titles = i.find('div',class_="title").text.strip()
			title.append(titles)
		for p in price:
			strs = ''.join(p.text.split())
			prices.append(strs)

		for d in description:
			strs = ' '.join(d.text.split())
			desc.append(strs)
		for l in location:
			locs = l.find('span')
			strs = ' '.join(locs.text.split())
			locations.append(strs)
			# print(locations)
	except Exception as e:
		print(e)
		break

output["Title"] = title
output["Location"] = locations
output["Price"] = prices
output["description"] = desc
output["Links"] = links

name = input("csv save name? ...")
output.to_csv("/Users/a./Desktop/kijiji/Kijiji-Scraper/"+name+".csv")
print("Done")
print("Saved at ...")
print("/Users/a./Desktop/kijiji/Kijiji-Scraper/"+name+".csv")