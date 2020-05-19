import numpy as np

def transistionMatix(url):
	print('realTime_________________________________________________')
	senStaSet = np.loadtxt(url + 'sensorStateSet.txt', dtype = int)
	group = np.loadtxt(url + 'GroupState.txt', dtype = int)
	index = np.loadtxt(url + 'Index.txt', dtype = int)
	n = len(group)
	G2G = np.zeros((n, n)) #G2G matrix
	for x in range(len(group)):
		arr = np.where(index == x) #find group[x] in senStaSet
		# find times that G1...Gn after Gx
		for y in arr[0]:
			if y < (len(index) - 1):
				numGro = index[y + 1] #get element next of Gx
				G2G[x, numGro] += 1
		for z in range(len(group)):
			G2G[x, z] = round((G2G[x, z]/len(arr[0]))*100, 2)
			print(G2G[x, z])
	np.savetxt(url + 'G2G.txt',G2G, delimiter=',', fmt='%0.2f')
	a = len(senStaSet)
	dataTest = (int)(a*(0.1))
	false = 0 #count false
	#print(index[15725])
	for i in range(a - dataTest, a):
		MainGroup = 0
		print(i)
		ind = index[i -1]
		for y in range(len(group)):
			arr = (senStaSet[i] == group[y])
			# if sensorStateSet as MainGroup
			if (len(arr[np.where(arr == False)]) == 0):
				MainGroup +=1
				print(ind)
				if(G2G[ind, y] == 0):
					false +=1
					index[i] = ind
				else:
					index[i] = y
				break
			#elif (len(arr[np.where(arr == False)]) == 1):
		if(MainGroup == 0):
			false +=1
			index[i] = ind
	print(false, dataTest)
	for x in senStaSet:
		print(x)
	return
