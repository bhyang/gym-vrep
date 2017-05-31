from gym_vrep.envs.vrep_env import VrepEnv

class VrepPioneerEnv(VrepEnv):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		super().__init__('pioneer.ttt', ['pioneer', 'leftMotor', 'rightMotor'])

	def _step(self, action):
		self.setJointTargetVelocity('leftMotor', action[0])
		self.setJointTargetVelocity('rightMotor', action[1])
		VrepEnv._step(self, action)
		ob = self.getObjectPosition('pioneer'), self.getObjectVelocity('pioneer')
		return ob, 0, False, {}

	# def _reset(self):
	# 	print('_reset called from pioneer class')
	# 	# VrepEnv._reset(self)

	# def _render(self, mode='human', close=False):
	# 	print('_render called from pioneer class')
	# 	# VrepEnv._render(self, mode, close)