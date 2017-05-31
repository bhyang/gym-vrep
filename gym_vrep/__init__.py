from gym.envs.registration import register

register(
	id='vrep-walker-v0',
	entry_point='gym_vrep.envs:VrepWalkerEnv',
)

register(
	id='vrep-pioneer-v0',
	entry_point='gym_vrep.envs:VrepPioneerEnv',
)
