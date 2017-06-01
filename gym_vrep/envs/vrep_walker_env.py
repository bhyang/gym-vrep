from gym_vrep.envs.vrep_env import VrepEnv

class VrepWalkerEnv(VrepEnv):

	def __init__(self):
		super().__init__('walker.ttt', ['walker', 'leg1', 'leg2', 'leg3', 'leg4', 'leg5', 'leg6', 'foot1', 'foot2', 'foot3', 'foot4', 'foot5', 'foot6'])

	def _step(self, action):
		# action is a list/tupe of size 6, which corresponds to the velocities of the 6 legs
		print(action)
		self.setJointTargetVelocity('leg1', action[0])
		self.setJointTargetVelocity('leg2', action[1])
		self.setJointTargetVelocity('leg3', action[2])
		self.setJointTargetVelocity('leg4', action[3])
		self.setJointTargetVelocity('leg5', action[4])
		self.setJointTargetVelocity('leg6', action[5])
		VrepEnv._step(self, action)
		ob = self.getObjectPosition('walker'), self.getObjectVelocity('walker')
		return ob, 0, False, {}
