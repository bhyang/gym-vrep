from gym_vrep.envs.vrep_env import VrepEnv

class VrepPioneerEnv(VrepEnv):

	def __init__(self):
		super().__init__('pioneer.ttt', ['pioneer', 'leftMotor', 'rightMotor'])

	def _step(self, action):
		# action is a list/tuple of size 2, which corresponds to the velocities of left and right motors
		self.setJointTargetVelocity('leftMotor', action[0])
		self.setJointTargetVelocity('rightMotor', action[1])
		VrepEnv._step(self, action)
		ob = self.getObjectPosition('pioneer'), self.getObjectVelocity('pioneer')
		return ob, 0, False, {}