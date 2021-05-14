import re

status = ['RUNNABLE', 'TIMED_WAITING (sleeping)', 'TIMED_WAITING (on object monitor)', 'WAITING (on object monitor)', 'TIMED_WAITING (parking)', 'WAITING (parking)', 'BLOCKED (on object monitor)', 'total']
status2 = ['RUNNABLE', 'TIMED_WAITING', 'TIMED_WAITING', 'WAITING', 'TIMED_WAITING', 'WAITING', 'BLOCKED', 'total']
status3 = ['', 'sleeping', 'on object monitor', 'on object monitor', 'parking', 'parking', 'on object monitor', '']

def statis():
	with open('D:/sys.txt', 'r') as f:
		lines = f.readlines()
		tf = False
		threadName = ''
		dict = {}
		for line in lines:
			match = re.match('^"([^"]*)".*$', line)
			if match:
				tf = True
				threadName = match.group(1)
				if threadName == 'VM Thread':
					break
			elif tf:
				tf = False
				match2 = re.match('^   java.lang.Thread.State: (.*)$', line)
				if match2:
					group = re.match('^([^ ]*).*$', threadName).group(1)
					state = match2.group(1)
					if group not in dict:
						dict[group] = [0, 0, 0, 0, 0, 0, 0, 0]
					dict[group][status.index(state)] = dict[group][status.index(state)] + 1
					dict[group][7] = dict[group][7] + 1						
					# print('线程名称：%40s\t所属服务：%10s\t线程状态：%s' % (threadName, group, state))

		print('=========================================================================================================================================================================================================')
		print('%40s' % ('service'), end=' ')
		for x in status2:
			print('|%18s' % (x), end=' ')
		print()
		print('%40s' % (''), end=' ')
		for x in status3:
			print('|%18s' % (x), end=' ')
		print()
		
		print('=========================================================================================================================================================================================================')
		for k,v in dict.items():
			print('%40s' % (k), end=' ')
			for va in v:
				print('|%18s' % (va if va != 0 else ''), end=' ')
			print()

statis()