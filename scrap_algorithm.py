import requests
import pprint
import json

from bs4 import BeautifulSoup

class AlgorithmScrapper:
	BASE_URL = 'https://en.cppreference.com'
	URL = 'https://en.cppreference.com/w/cpp/algorithm'
	def __init__(self):
		self.page = requests.get(self.URL)
		self.soup = BeautifulSoup(self.page.text,'lxml')
		
		self.title = self.soup.find('h1',id='firstHeading').get_text()
		self.description = self.soup.find('div',id='mw-content-text').find('p')

		self.algorithm = self.soup.find_all('table',class_='t-dsc-begin')[1:-1]
		self.data = {}
		for i in range(len(self.algorithm)):
			self.module = self.algorithm[i].find_all('tr')
			current_block = ''
			for tag in self.module:
				try :
					tagClass = tag.find('div')['class'][0]
					# print(tagClass,current_block)
					if (tagClass == 't-dsc-member-div') :
						td = tag.find_all('td')
						datas = {
							"html-table-td0":td[0],
							"html-table-td1":td[1],
							"link":self.BASE_URL+td[0].find('a').get('href')
						}
						self.data[current_block].append(datas)
					else :
						continue
					
				except TypeError: 
					# print('asd')
					if current_block != tag.get_text().strip() :
						current_block = tag.get_text().strip()
						self.data[current_block] = []
						# print(current_block)
				except KeyError :
					continue
	def scrap(self):
		self.JsonWannabe = {'data':[]}
		for categories in self.data:
			print(categories+' start!')
			for data in self.data[categories]:
				URL = data['link']
				page = requests.get(URL)
				soup = BeautifulSoup(page.text,'lxml')
				
				id_data = '-'.join(URL.split('/')[-2:])
				title = soup.find('h1',id='firstHeading').get_text()
				html_code = soup.find('div',id='mw-content-text')
				
				data = {
					'id':id_data,
					'title':title,
					'categories':categories,
					'library':'Algorithm',
					'html':str(html_code)
				}
				self.JsonWannabe['data'].append(data)
				print('[+] '+id_data+' done!')
			print(categories+' done!')

	def debug(self):
		pprint.pprint(self.data)

	def debug2(self):
		pprint.pprint(self.JsonWannabe)

	def save_to_file(self):
		with open('algorithm.json','w') as f :
			JSON = json.dumps(self.JsonWannabe)
			f.write(JSON)


if __name__ == '__main__':
	Scraper = AlgorithmScrapper()
	Scraper.scrap()
	Scraper.debug2()
	Scraper.save_to_file()
	

		
