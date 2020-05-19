import pandas as pd
import numpy as np
from datetime import datetime

def correlationExtraction(url):
	print('correlationExtraction________________________________________________________________________________')
	#read data.csv 
	data = pd.read_table(url + 'ann.txt')
	#read sensor is array
	sensor = pd.unique(data['sensor'])
	date = data['date'].values
	time = data['time'].values
	#stateS = [0, 0,..., 0] save state current
	stateS = np.zeros(len(sensor), dtype = '<U6')
	#sensor state set
	SSS = np.zeros((len(sensor)), dtype = '<U6') #use to save 1 state set
	#get data with duration=1m 
	from datetime import timedelta
	d = timedelta(minutes = 1)
	#read state
	i = -1 
	x = datetime.strptime(date[0] + time[0], "%Y-%m-%d%H:%M:%S.%f") #cat mat.%f
	t = x # time window
	n = len(time)
	senStaSet = np.zeros(len(sensor), dtype = '<U6') #use to save state sets
	checkSensor = np.zeros((len(sensor)), dtype = 'i')
	n = 10000
	while (i < n-1):
		'''if(i +1 < n):
			x2 =datetime.strptime(date[i+1] + time[i+1], "%Y-%m-%d%H:%M:%S.%f")#cat mat.%f
			if(x2 - t >2*d):
				h = (x2 - t)//(d - 1)
				t += h*d
				#print(h)
			else:
				t += d
		else:'''
		t += d
		# save itialization dict
		dictN = {}
		checkN = 0
		while((x < t) and (i <n)):
			i += 1
			if(i == n):
				continue
			x = datetime.strptime(date[i] + time[i], "%Y-%m-%d%H:%M:%S.%f")
			s = data.at[i,'state'] #get value at (j,state)

			name = data.at[i,'sensor'] #get value name of sensor at (j,state)
			index = np.where(sensor == name)
			
			#motion sensor
			if s == 'ON':
				s = '1'
			elif s == 'OFF':
				s = '0'
			#items sensor
			elif s == 'ABSENT':
				s = '0'
			elif s == 'PRESENT':
				s = '1'
			# door sensor
			elif s == 'CLOSE':
				s = '0'
			elif s == 'OPEN':
				s = '1'
			else:
				s = float(s)
				# dictionary chua numeric sensor va value
				if dictN.get(name, 'no') == 'no':
					arr = np.array([s], dtype = float)
					dictTemp = {name:arr} 
					dictN.update(dictTemp)
				else:
					arr2 = np.append(dictN[name], s)
					dictN[name] = arr2
				checkN = 1
				checkSensor[index] = 1
				
			print(checkSensor[index])
				
			'''stateS[index] = s #save state current	M
			if(SSS[index] == 1 or s == 1):
				SSS[index] = 1'''
			#houseA,BC
			if (checkSensor[index] == 0) and (SSS[index] != '1'):	#sensor binary
				SSS[index] = s
				print('s=', s, index[0][0])
					#handing numeric
				#handing numeric
		if checkN == 1:
			key = dictN.keys()
			print(key)
			for k in key:
				value = dictN[k]
				print(value, type(value))
				stateN = ''
				df = data
				#mean value
				#arr = value.astype(float)
				mean = float(np.sum(value)/value.size)
				#Standard deviation
				arr2 = (value - mean)**2
				o = float(np.sum(arr2)/(value.size))
				arr3 = (value - mean)**3
				skewness = float(np.sum(arr3))
				if(skewness >= 0):
					stateN = '1'
				else:
					stateN = '0'
				#formula2
				if value[len(value) -1] - value[0] >= 0:
					stateN += '1'
				else:
					stateN += '0'
				#formula 3
				sumN = np.sum(value)
				if sumN >= mean:
					stateN += '1'
				else:
					stateN += '0'
				index = np.where(sensor == k)
				SSS[index] = stateN		
		senStaSet = np.vstack((senStaSet, SSS)) #add SSS in senStaSet
		#SSS = stateS.copy()	M
		#houseA,BC
		SSS = np.zeros((len(sensor)), dtype = '<U6')
		print(i)

	#np.savetxt('test.txt', senStaSet, delimiter=',', fmt='%d')
	#senStaSet = np.delete(senStaSet, 0, 0)
	senStaSet[senStaSet == ''] = '0'
	senStaSet[senStaSet == '0.0'] = '0'
	for x in range(len(senStaSet)):
		print(senStaSet[x][1])
	n = int(len(sensor) + 2*(np.sum(checkSensor)))
	senStaSet2 = np.zeros((len(senStaSet), n), dtype = '<U6')
	for x in range(len(senStaSet)):
		i=0
		for j in range(len(sensor)):
			if checkSensor[j] == 0:
				senStaSet2[x][i] = senStaSet[x][j]
				i +=1

			else:
				st =  (senStaSet[x][j])
				if st == '0':
					i+=3
				else:	
					senStaSet2[x][i] = (st[0])
					i +=1
					senStaSet2[x][i] = (st[1])
					i+=1
					senStaSet2[x][i] = (st[2])
					i+=1
	senStaSet2[senStaSet2 == ''] = '0'
	print(senStaSet2)
	senStaSet2 = senStaSet2.astype(int)
	np.savetxt(url + 'sensorStateSet.txt', senStaSet2, fmt='%i')
	return

# Group Set
def groupSet(url):
	print('groupSet_________________________________________________________________')
	senStaSet = np.loadtxt(url + 'sensorStateSet.txt', dtype = int)
	length = len(senStaSet)
	dataTest = (int)(length*(0.1))
	print(dataTest)
	group = senStaSet[0].copy()
	group = np.vstack((group, senStaSet[1]))
	index = np.zeros((len(senStaSet))) # save index group of sensorStateSet
	for x in range(1, len(senStaSet) - dataTest):
		n = 1
		for y in range(len(group)):
			arr = (senStaSet[x] == group[y])
			if len(arr[np.where(arr == False)]) == 0:
				index[x] = y
				n = 0
				break
		if n == 1:
			index[x] = len(group)
			group = np.vstack((group, senStaSet[x]))
		print(x)
	np.savetxt(url + 'GroupState.txt', group)
	np.savetxt(url + 'Index.txt', index)
	print(len(group), len(senStaSet), dataTest)
	return