from gym.envs.registration import register

#### MARIO

register(
    id='Mario-v0',
    entry_point='envs.mario:MarioEnv',
    kwargs={'full_state': True}
)

register(
    id='MarioVisual-v0',
    entry_point='mario.mario:MarioEnv',
    kwargs={'full_state': False}
)

register(
    id='MarioMultiBin-v0',
    entry_point='mario:MarioMultiBinEnv',
    kwargs={'full_state': True}
)

register(
    id='MarioMultiBinVisual-v0',
    entry_point='mario:MarioMultiBinEnv',
    kwargs={'full_state': False}
)

register(
    id='Mario3D-v0',
    entry_point='mario:Mario3DEnv',
    kwargs={}
)

register(
    id='Mario3DMultiBin-v0',
    entry_point='mario:Mario3DMultiBinEnv',
    kwargs={}
)