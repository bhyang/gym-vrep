import gym
from gym import error, spaces, utils
from gym.utils import seeding

class VrepWalkerEnv(gym.Env):
	metadata = {'render.modes': ['human']}

	def __init__(self):
		print('__init__')

	def _step(self, action):
		print('_step')
		return None

	def _reset(self):
		print('_reset')

	def _render(self, mode='human', close=False):
		print('_render')