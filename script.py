import re

def statis():
	with open('D:/phone.txt', 'r') as f:
		lines = f.readlines()
		for line in lines:
			print(line)

statis()