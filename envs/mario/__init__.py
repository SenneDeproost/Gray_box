from gym.envs.registration import register

#### MARIO

register(
    id='Mario-v0',
    entry_point='mario.envs:UnaryMarioAction',
    kwargs={'full_state': True}
)

register(
    id='MarioVisual-v0',
    entry_point='mario.envs:MarioEnv',
    kwargs={'full_state': False}
)

register(
    id='MarioMultiBin-v0',
    entry_point='mario.envs:MarioMultiBinEnv',
    kwargs={'full_state': True}
)

register(
    id='MarioMultiBinVisual-v0',
    entry_point='mario.envs:MarioMultiBinEnv',
    kwargs={'full_state': False}
)

register(
    id='Mario3D-v0',
    entry_point='mario.envs:Mario3DEnv',
    kwargs={}
)

register(
    id='Mario3DMultiBin-v0',
    entry_point='mario.envs:Mario3DMultiBinEnv',
    kwargs={}
)