import asyncio
import aiohttp
import time
from bs4 import BeautifulSoup
import pandas as pd
import sys


detail = []
delay_per_request = 0.5

def main(pages : int):
	output = pd.DataFrame()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(get_html_in_range(pages,loop))
	# print(detail)
	parse_output(detail,output)
	print("Done ...")

def parse_output(detail,output):
	title = []
	description = []
	location = []
	link = []
	price = []
	for titles,locations,prices,desc,links in detail:
		#Problem in the way that I'm setting the data, response coming as 200 as expected
		title=title + titles
		location = location + locations
		price = price + prices
		description = description + desc
		link = link + links
	# print(link)
	output["title"] = title
	output["location"] = location
	output["description"] = description
	output["price"] = price
	output["link"] = link
	# print(len(price))
	output.to_csv("KijjijiRooms.csv")







async def get_html(page_number:int) -> str:
	try:
		url = "https://www.kijiji.ca/b-room-rental-roommate/mississauga-peel-region/room-for-rent/page-"+str(page_number)+"/k0c36l1700276?radius=14.0&address=19+Pefferlaw+Cir%2C+Brampton%2C+ON+L6Y+0K1%2C+Canada&ll=43.647230,-79.759084&rb=true"
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as resp:
				resp.raise_for_status()
				print(resp.status)
				html = await resp.text()
				return html
	except Exception as e:
		print(e)

async def get_html_in_range(ranges:int, loop):
	tasks = []
	delay_per_request = 0.5
	if(ranges<=100):
		delay_per_request = 0.2
	for i in range(0,ranges):
		tasks.append((loop.create_task(get_html(i)),i))
		await asyncio.sleep(delay_per_request)
	for task,i in tasks:
		html = await task
		url = "https://www.kijiji.ca/b-room-rental-roommate/mississauga-peel-region/room-for-rent/page-"+str(i)+"/k0c36l1700276?radius=14.0&address=19+Pefferlaw+Cir%2C+Brampton%2C+ON+L6Y+0K1%2C+Canada&ll=43.647230,-79.759084&rb=true"
		detail.append(get_details_from_html(html,url))
		print("NUMBER " + str(i))




def get_details_from_html(html:str, urls:str):
	title= []
	desc= []
	links =[]
	prices = []
	locations = []
	print("processing.....")
	soup = BeautifulSoup(html,'html.parser')
	try:
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
			strs = ' '.join(p.text.split())
			print(strs)
			prices.append(strs)

		for d in description:
			strs = ' '.join(d.text.split())
			desc.append(strs)
		for l in location:
			locs = l.find('span')
			strs = ' '.join(locs.text.split())
			locations.append(strs)

		return (title,locations,prices,desc,links)
	except Exception as e:
		print(e)




if __name__ == "__main__":
	pages = input("How many pages ? ")
	main(int(pages))
