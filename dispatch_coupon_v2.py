#encoding:UTF-8
# __author__ ='cc'

import pymysql
import urllib
import urllib.request
import ssl
import time

ssl._create_default_https_context=ssl._create_unverified_context

class Script(object):
	"""根据电话号码发放优惠券"""
	dbHost='192.168.100.70'
	dbPort=3306
	dbUser='root'
	dbPassword='mysqlHolder'
	dbName='qxh_island'
	dbCharset='utf8'

	# serviceAddr=r'https://zhuancan.holderzone.cn';
	# serviceAddr=r'https://zhuancan-sit.holderzone.cn'
	serviceAddr='http://192.168.102.235:8080';

	batchItemMax=10
	actualDispatchedNum=0

	def __init__(self, phoneFilePath, platformId, couponPackageId):
		self.logFile=open('log', 'w',encoding="utf-8");
		with open(phoneFilePath,"r",encoding="utf-8") as f:
			phones=f.read().splitlines()
			self.log(f'init dispatch coupon package {couponPackageId} at platform {platformId}, total: {len(phones)}')
			self.groupPhones=self.groupData(phones, self.batchItemMax)
		self.platformId=platformId
		self.couponPackageId=couponPackageId
		self.conn=pymysql.connect(host=self.dbHost, port=self.dbPort, user=self.dbUser, password=self.dbPassword, db=self.dbName, charset=self.dbCharset)
		self.cursor=self.conn.cursor()

	def groupData(self,data,n):
	    result=[]
	    for i in range(0, len(data), n):
	        b=data[i:i+n]
	        result.append(b)
	    return result

	def log(self, msg):
		print(msg)
		self.logFile.write(msg + '\n')

	def queryUserIds(self, phones):
		tv=",".join(phones)
		self.log(f'query userId by phones:[{tv}]')
		self.cursor.execute(f'select group_concat(id),group_concat(phone) from island_user where phone in ({tv}) and platform_id={self.platformId}')		
		result=self.cursor.fetchone()
		if result[0]==None:
			self.log(f"\tuser {set(phones)} does not exist.")
		elif len(result[0]) != len(phones):
			t=result[1].split(",")
			self.log(f"\tuser {set(phones).difference(set(t))} does not exist.")
		return result[0]

	def sendDispatchRequest(self,userIdsStr):
		self.actualDispatchedNum = self.actualDispatchedNum + len(userIdsStr.split(','));
		url=f'{self.serviceAddr}/island/api/designated_coupon_package'
		data=f'cpPackageId={self.couponPackageId}&platFormId={self.platformId}&userIds={userIdsStr}'
		data=bytes(data, encoding='utf-8')
		response=urllib.request.urlopen(url,data);
		rsp=response.read().decode('utf-8')
		self.log(f'\tdispatch result: {rsp}')

	def beginDipatch(self):
		for phones in self.groupPhones:
			userIds=self.queryUserIds(phones)
			if userIds!=None:
				self.log(f'\tbegin dispatch coupon to user: {userIds}')
				self.sendDispatchRequest("".join(userIds))
				time.sleep(3)
		self.end()

	def end(self):
		self.log(f'dispatch coupon package[{self.couponPackageId}] over, actual dispatched num is {self.actualDispatchedNum}')
		self.logFile.close()
		self.conn.close()

if __name__ == '__main__':
	task=Script('phone.txt', 142, 927);
	task.beginDipatch()

			
	
	
		
