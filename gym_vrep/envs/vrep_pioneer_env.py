import gym
from gym import error, spaces, utils
from gym.utils import seeding

from gym_vrep.envs.vrep_env import VrepEnv

class VrepPioneerEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		self.vrep = VrepEnv('pioneer.ttt', ['pioneer', 'leftMotor', 'rightMotor'])

	def _step(self, action):
		self.vrep.step()
		ob = self.vrep.getObjectPosition('pioneer'), self.vrep.getObjectVelocity('pioneer')
		return ob, 0, False, {}

	def _reset(self):
		self.vrep.stop()
		self.vrep.start()

	def _render(self, mode='human', close=False):
		if close:
			self.vrep.stop()
			self.vrep.close()
		
