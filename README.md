# gym-vrep
OpenAI gym environment for V-REP. This environment should provide a serviceable baseline for any reinforcement learning ventures involving robots in V-REP. But you'll probably still have to configure the environment to your own needs, and potentially extend the base environment to encompass more V-REP functionality.

This is far from a finished product, so keep that in mind if you try to follow along.

## Installation
You'll need to install [V-REP](http://www.coppeliarobotics.com/downloads.html). Also the included scenes/models are pretty rudimentary so if you have a specific robot in mind you should have that already built in V-REP.
```
git clone https://github.com/bhyang/gym-vrep.git
cd gym-vrep
pip install -e .
```
If you're running Linux, then you're done with installation. Otherwise, you need to navigate to your V-REP folder and go to `programming/remoteAPIBindings/lib/lib/`, 32-bit or 64-bit depending on your system, and copy and paste that file into the repo at `/gym_vrep/envs/`. You should also delete `remoteApi.so`.

## Usage
There are a few caveats when it comes to running this. For one thing, you need to have V-REP open already whenever you execute a script. You also have to have the scene files you plan on using in the same directory as your script (if you want to use the sample scenes, you can either move them or run your script in `gym_vrep/scenes/`. If you've been using V-REP for some time, you may have changed the remote API port, in which case you should modify `vrep_env.py` to reflect that change.
```
import gym, gym_vrep
env = gym.make('vrep-pioneer-v0[or whatever your custom environment is]')
for _ in range(1000):
    if _ != 0:
        env.reset()
    action = (0, 0)
    ob, reward, done, diagnostic = env.step(action)
    # [insert revolutionary machine learning magic here]
    # No need to render since V-REP should already be open    
```
As of now the `vrep_env.py` base class only supports getting velocity and position data, as well as setting the velocity of a target joint. Once I have time I'll probably extend the API, but if you'd like extending it should be super easy (the remote API functions for Python are well-documented [here](http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsPython.htm)). As it stands, new classes also need to have all handles given upon initialization.
![Walker example](http://imgur.com/a/XqBbp)
