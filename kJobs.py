import requests
from bs4 import BeautifulSoup
import pandas as pd

output = pd.DataFrame()
title= []
desc= []
time = []
add = []
links =[]
limit = input("Enter you page limit.... ")
for i in range(1,int(limit)):
	try:
		url = "https://www.kijiji.ca/b-jobs/gta-greater-toronto-area/page-"+str(i)+"/c45l1700272"
		print(url)
		x = requests.get(url,timeout=30)
		soup = BeautifulSoup(x.text, 'html.parser')
		
		description = soup.findAll("td", class_="description")
		location = soup.findAll("td", class_="posted")
		for d in description:
			urls = d.find('a')['href']
			links.append("https://www.kijiji.ca"+urls)
			titles = d.find('a',class_="title").text.strip()
			title.append(titles)
			descs = d.find('p').text.strip()
			desc.append(descs)
		for l in location:
			strs = ''.join(l.text.split())
			time.append(strs)
	except Exception as e: 
		print(e)
		break


output['time'] = time
output['title'] = title
output['desc'] = desc
output['links'] = links
print(len(time))
print(len(title))
print(len(desc))
print(output.head())
output.to_csv('/Users/a./Desktop/kijiji/'+'kijijiJobs.csv')