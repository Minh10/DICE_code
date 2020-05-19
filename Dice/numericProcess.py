def formula1(S, m, o):

def formula2(S1, S2)

def formula3():

def numeric(url):
	data = pd.read_table(url + 'houseA.txt')
	sensor = pd.unique(data['sensor'])
	date = data['date'].values
	time = data['time'].values
	#stateS = [0, 0,..., 0] save state current
	stateS = np.zeros(len(sensor))
	for i in range(len(date)):
		s = data.at[i,'state'] #get value at (j,state)
		if 
