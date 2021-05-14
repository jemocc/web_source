#encoding:UTF-8

import urllib
import urllib.request
import html
import re
import time

def fun(url, nextPage, f, si, mi, type):
	r=getContent(url+nextPage, type)
	si=si+1
	if (nextPage != None) & (mi != si):
		time.sleep(2)
		fun(url, r['nextPage'], f, si, mi, r['type'])

def getText(url):
	data = urllib.request.urlopen(url).read()
	record = data.decode('GBK')
	return html.unescape(record)

def getContent(url, type):
	text=getText(url)
	# print(text)
	p = re.compile('[\r\n]')
	s = re.compile('^\s*')
	
	if type == 1:
		m = re.search(r'<h1 class="nr_title" id="nr_title">([^<]*)</h1>', text, re.M)
		if m:
			title = s.sub('',p.sub('', m.group(1)))
		else:
			title = "None"
		print(title)
		print('\t'+url+'\n')
		f.write(title+'\n')
		f.write('\t'+url+'\n\n')
	ms = re.findall(r'>([^<]*)<br />', text, re.M)
	for mi in ms:
		ts='\t' + s.sub('',p.sub('', mi));
		print(ts)
		f.write(ts+'\n')

	m = re.search(r'href="([^"]*)">下一页', text, re.M)
	if m:
		nextPage=m.group(1).replace('/book_12396','')
		return {'type': 0, 'nextPage': nextPage}
	m = re.search(r'href="([^"]*)">下一章', text, re.M)
	if m:
		nextPage=m.group(1).replace('/book_12396','')
		return {'type': 1, 'nextPage': nextPage}
	return None;

if __name__ == '__main__':
	url = 'https://m.630shu.net/book_12396/'
	path='D:/t4.txt'
	with open(path,"w",encoding="utf-8") as f:
		fun(url,'/4566689.html',f,0,200,1)
	