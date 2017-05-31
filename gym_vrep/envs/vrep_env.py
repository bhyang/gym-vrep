import gym
from gym import error, spaces, utils
from gym.utils import seeding

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

# Base class for V-REP environments, doesn't actually do anything on its own
class VrepEnv(gym.Env):
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

		# Starting simulation
		self.start()
		print('V-REP environment initialized')

	def closeConnection(self):
		vrep.simxGetPingTime(self.clientID)
		vrep.simxFinish(self.clientID)
		print('Successfully disconnected from V-REP')

	def start(self):
		assert vrep.simxSynchronous(self.clientID, 1) in (0, 1), 'Failed to make simulation synchronous'
		assert vrep.simxStartSimulation(self.clientID, vrep.simx_opmode_oneshot_wait) in (0, 1), 'Error starting simulation'
		print('Simulation started')
		# self.step()

	def stop(self):
		assert vrep.simxStopSimulation(self.clientID, vrep.simx_opmode_blocking) in (0, 1), 'Error stopping simulation'
		vrep.simxGetPingTime(self.clientID)
		vrep.simxClearFloatSignal(self.clientID, '', vrep.simx_opmode_blocking)
		vrep.simxClearIntegerSignal(self.clientID, '', vrep.simx_opmode_blocking)
		print('Simulation stopped')

	# Wrappers for remote API functions
	def getObjectPosition(self, name, reference=-1):
		if name in self.handles:
			errorCode, position = vrep.simxGetObjectPosition(self.clientID, self.handles[name], reference, vrep.simx_opmode_streaming)
			if errorCode in (0, 1):
				return position
			else:
				print('Could not get position of ' + name + ', returned error code ' + str(errorCode))
		else:
			print(name + ' handle not found')

	def getObjectVelocity(self, name, angular=False):
		if name in self.handles:
			errorCode, velocity, angular_velocity = vrep.simxGetObjectVelocity(self.clientID, self.handles[name], vrep.simx_opmode_streaming)
			if errorCode in (0, 1):
				return (angular and angular_velocity) or velocity
			else:
				print('Could not get velocity of ' + name + ', returned error code ' + errorCode)
		else:
			print(name + ' handle not found')

	def setJointTargetVelocity(self, name, velocity):
		if name in self.handles:
			errorCode = vrep.simxSetJointTargetVelocity(self.clientID, self.handles[name], velocity, vrep.simx_opmode_streaming)
		else:
			print(name + 'handle not found')

	# Overriden methods from gym
	def _step(self, action):
		errorCode = vrep.simxSynchronousTrigger(self.clientID)
		assert errorCode in (0, 1), 'Error stepping simulation'

	def _reset(self):
		self.stop()
		self.start()

	def _render(self, mode, close=False):
		if close:
			self.stop()
			self.closeConnection()

		# this doesn't really do anything until temporary remote API is incorporated