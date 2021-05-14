#encoding:UTF-8
# __author__ ='cc'

import pymysql
import urllib
import urllib.request
import ssl
import time
import re

ssl._create_default_https_context=ssl._create_unverified_context

class Script(object):
	"""资质通鉴解析"""
	p_title=r'itemprop="name headline"><a.*?>(.*?)</a>'
	p_create_at=r'datePublished[^>]*>(.*?)</time'
	p_next_page=r'nav-next"><a href="([^"]*)'
	p_content=r'<div class="entry-content e-content" itemprop="description articleBody">(.*?)</div'

	p_r_rns=re.compile(r'[\r\n\s]+')

	def __init__(self, uri):
		self.uri = uri

	def getWebData(self, uri):
		response=urllib.request.urlopen(uri)
		return response.read().decode('UTF-8')

	def getTitle(self, data):
		m = re.search(self.p_title, data, re.M)
		if m:
			return m.group(1)

	def getCreateAt(self, data):
		m = re.search(self.p_create_at, data, re.M)
		if m:
			return m.group(1)

	def getNextPageUrl(self, data):
		m = re.search(self.p_next_page, data, re.M)
		if m:
			return m.group(1)

	def getContent(self, data):
		data=self.p_r_rns.sub(" ", data)
		m = re.search(self.p_content, data, re.M)
		if m:
			return m.group(1)

	def start(self):
		data = self.getWebData(self.uri)
		title=self.getTitle(data)
		createAt=self.getCreateAt(data)
		nextPageUrl=self.getNextPageUrl(data)
		print(f'{title}\t\t{createAt}')
		content=self.getContent(data)
		print(content)

		if nextPageUrl != None:
			self.uri=nextPageUrl
			# self.start()


if __name__ == '__main__':
	task=Script('http://www.dushiwudao.com/2019/07/09/%e5%8f%b8%e9%a9%ac%e5%85%89%e7%a0%b8%e7%bc%b8%ef%bc%9a%e6%bc%94%e5%91%98%e7%9a%84%e8%87%aa%e6%88%91%e4%bf%ae%e5%85%bb/');
	task.start()

			
	
	
		
