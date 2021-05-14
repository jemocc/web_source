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
	"""涨涨涨"""

	def __init__(self, url):
		self.currentUrl=url

	def buildNewUrl(self,nowUrl,href):
		if href.startswith('../'):
			p=re.compile('^../')
			href=p.sub('',href)
			p=re.compile('/[^/]*$')
			nowUrl=p.sub('',nowUrl)
			return self.buildNewUrl(nowUrl,href)
		else:
			p=re.compile('/[^/]*$')
			nowUrl=p.sub('/',nowUrl)
			return nowUrl+href

	def begin(self):
		# response=urllib.request.urlopen(self.currentUrl);
		# print(response.read().decode('utf-8'))
		nu=self.buildNewUrl(self.currentUrl,'../disclosure/szmb.html')
		print(nu)

if __name__ == '__main__':
	task=Script('https://www.bbvisi.com/cninfo/information/companyinfo.html')
	# task=Script('https://www.bbvisi.com/cninfo/disclosure/districtmarket.html')
	task.begin()

			
	
	
		
