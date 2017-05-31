try:
	from gym_vrep.envs import vrep
except:
	print ('--------------------------------------------------------------')
	print ('"vrep.py" could not be imported. This means very probably that')
	print ('either "vrep.py" or the remoteApi library could not be found.')
	print ('Make sure both are in the same folder as this file,')
	print ('or appropriately adjust the file "vrep.py"')
	print ('--------------------------------------------------------------')
	print ('')

class VrepEnv:
	def __init__(self, model, names):
		vrep.simxFinish(-1)	# Closes existing unclosed connections
		print('Attempting to connect to local V-REP instance...')
		self.clientID = vrep.simxStart('127.0.0.1',19997,True,True,5000,5)
		assert self.clientID != -1, 'Unable to conect to V-REP, make sure an instance of V-REP is running'
		print('Successfully connected to V-REP')

		# Loading scene with specified path (for now has to be in working directory)
		print('Loading scene...')
		errorCode = vrep.simxLoadScene(self.clientID, model, 1, vrep.simx_opmode_blocking)
		assert errorCode in (0, 1), 'Could not find model, returned error code ' + str(errorCode)
		print('Successfully loaded scene')

		# Retrieving handles
		print('Loading handles...')
		self.handles = {}
		for name in names:
			errorCode, handle = vrep.simxGetObjectHandle(self.clientID, name, vrep.simx_opmode_blocking)
			if errorCode in (0, 1):
				self.handles[name] = handle
			else:
				print('WARNING: Could not find object named "' + name + '"')

		# Simulation has to be synchronous (as in tick-by-tick) so that data transfer can be synchronized with the actions of the agent
		print('Toggling synchronization...')
		assert vrep.simxSynchronous(self.clientID, True) in (0, 1), 'Failed to make simulation, synchronous'

		print('Starting simulation...')
		assert vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_oneshot)
		print('V-REP environment initialized')

		self.firstAPICall = True	# Ensures that streaming for remote API function calls is enabled the first time and that buffering is used for other calls

	def close(self):
		vrep.simxGetPingTime(self.clientID)
		vrep.simxFinish(self.clientID)
		print('Successfully disconnected from V-REP')

	def start(self):
		assert vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_oneshot) in (0, 1), 'Error starting simulation'
		print('Simulation started')

	def stop(self):
		assert vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_oneshot) in (0, 1), 'Error stopping simulation'
		print('Simulation stopped')

	def step(self):
		assert vrep.simxSynchronousTrigger(self.clientID) in (0, 1), 'Error stepping simulation'

	def getObjectPosition(self, name, reference=-1):
		if name in self.handles:
			errorCode, position = vrep.simxGetObjectPosition(self.clientID, self.handles[name], reference, (self.firstAPICall and vrep.simx_opmode_streaming) or vrep.simx_opmode_buffer)
			if errorCode in (0, 1):
				if self.firstAPICall:
					self.firstAPICall = False
				return position
			else:
				print('Could not get position of ' + name + ', returned error code ' + errorCode)
		else:
			print(name + ' handle not found')

	def getObjectVelocity(self, name, angular=False):
		if name in self.handles:
			errorCode, velocity, angular_velocity = vrep.simxGetObjectVelocity(self.clientID, self.handles[name], (self.firstAPICall and vrep.simx_opmode_streaming) or vrep.simx_opmode_buffer)
			if errorCode in (0, 1):
				if self.firstAPICall:
					self.firstAPICall = False
				return (angular and angular_velocity) or velocity
			else:
				print('Could not get velocity of ' + name + ', returned error code ' + errorCode)
		else:
			print(name + ' handle not found')