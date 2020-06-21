import signal
import socket
import struct
import subprocess
from time import sleep

import numpy as np

from gym import Env, spaces, logger


class MarioEnv(Env):
    IP = "127.0.0.1"
    PORT = 7934
    METADATA_SIZE = 19
    CELL_CATEGORIES = 24
    # Retrieved from ch.idsia.benchmark.mario.engine.GeneralizerLevelScene.java and
    # ch.idsia.benchmark.mario.engine.GeneralizerEnemies.java

    # TODO transform to enum class?
    CELL_MEANING = {
        0: 'NULL',
        1: 'COIN_YELLOW',
        2: 'COIN_BLUE',
        3: 'COIN_GREEN',
        4: 'COIN_RED',
        5: 'CANON_MUZZLE',
        6: 'CANON_TRUNK',
        7: 'BREAKABLE_BRICK',
        8: 'UNBREAKABLE_BRICK',
        9: 'BRICK',
        10: 'FLOWER_POT',
        11: 'BORDER_CANNOT_PASS_THROUGH',
        12: 'BORDER_HILL',
        13: 'FLOWER_POT_OR_CANON',
        14: 'LADDER',
        15: 'TOP_OF_LADDER',
        16: 'MARIO',
        17: 'PRINCESS',
        18: 'BLOCK',
        # 19 seems to be omitted
        20: 'FLOWER',
        21: 'MUSHROOM',
        22: 'FIREBALL',
        23: 'GOOMBA',
        24: 'SPIKY'}
    # Normalized RGB values
    CELL_COLORS = {
        0: (0, 0, 0),  # BLACK
        1: (1, 1, 0),  # YELLOW
        2: (0, 0, 1),  # BLUE
        3: (0, 1, 0),  # GREEN
        4: (1, 0, 0),  # RED
        5: (0.592, 0.584, 0.627),
        6: (0.321, 0.317, 0.329),
        7: (1, 0.682, 0.349),
        8: (1, 0.514, 0),
        9: (1, 0.416, 0),
        10: (0.215, 0.529, 0.294),
        11: (0.286, 0.176, 0),
        12: (0.459, 0.286, 0.008),
        13: (0, 1, 0.482),
        14: (0.431, 0, 1),
        15: (0.208, 0.055, 0.408),
        16: (0, 1, 1),
        17: (1, 0, 1),
        18: (0, 0, 0),  # TODO
        20: (0.318, 0.388, 0.110),
        21: (1, 0.462, 0.266),
        22: (1, 0.263, 0),
        23: (0.933, 1, 0),
        24: (0, 0, 0)}  # TODO

    metadata = {'render.modes': ['human'], 'video.frames_per_second': 50}

    def __init__(self, full_state=True, vis='on', fps=24):
        # Saving attributes
        self._full_state = full_state
        self.emul_vis = vis
        self.emul_fps = fps

        # Starting Java emulator
        self._emul = self._start_java_emul_popen()

        # Connecting to socket
        logger.info(f'Connecting to {MarioEnv.IP}:{MarioEnv.PORT}...')
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        print(MarioEnv.IP)
        print(MarioEnv.PORT)
        self._socket.connect((MarioEnv.IP, MarioEnv.PORT))
        logger.info('Connected')

        # Wait for the first observation, it contains information about the environment
        self._state = None
        self._last_reward = 0.0
        self._timestep = 0

        self._get_observation()

        # Configure Gym
        self._set_action_space()
        self._set_observation_space()

        # Rendering
        self.viewer = None

    def _start_java_emul_popen(self):
        # TODO try to elevate emulator classpath to a class argument
        from pathlib import Path
        classpath = 'marioai' / 'src'
        #classpath = Path().absolute()
        #classpath = "../../Mario-AI-Framework/src"
        scenario = 'ch.idsia.scenarios.Play'
        agent = 'ch.idsia.agents.controllers.TCPAgent'
        vis = self.emul_vis
        fps = self.emul_fps
        cmd = f'java -cp {classpath} {scenario} -z on -rfw 10 -rfh 10 -ag {agent} -vis {vis} -fps {fps}'
        print(cmd)
        import shlex
        cmd_shlex = ' '.join(shlex.quote(i) for i in cmd.split())
        logger.info('Starting Mario Java Emulator...')
        logger.info(cmd_shlex)
        p = subprocess.Popen(cmd_shlex, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # Give the emulator some time to boot
        sleep(5)
        return p

    def _set_observation_space(self):
        self.observation_space = spaces.Box(low=0.0, high=MarioEnv.CELL_CATEGORIES, shape=self._state.shape,
                                            dtype=self._state.dtype)

    def _set_action_space(self):
        self.action_space = spaces.Discrete(2 ** (self._num_keys - 1))

    def _get_observation(self):
        # Read metadata about the observation
        self._read_observation_metadata()
        # Read the map of the world
        self._read_state_observation()

    def _read_state_observation(self):
        if self._state is None:
            self._prepare_state()

        buffer = self._receive_buffer(self._field_width * self._field_height)
        self._process_state_buffer(buffer)

    def _process_state_buffer(self, buffer):
        for i in range(len(buffer)):
            self._state[i] = float(buffer[i])

        if self._full_state:
            self._state[-2] = 1.0 if self._on_ground else 0.0
            self._state[-1] = 1.0 if self._can_jump else 0.0

    def _receive_buffer(self, size):
        return self._socket.recv(size, socket.MSG_WAITALL)

    def _prepare_state(self):
        size = self._field_width * self._field_height
        shape = (size + 2,) if self._full_state else (size,)
        self._state = np.zeros(shape, dtype=np.float32)

    def _read_observation_metadata(self):
        buffer = self._receive_buffer(MarioEnv.METADATA_SIZE)
        contents = struct.unpack('>?fiii??', buffer)
        self._just_reset, reward, self._num_keys, self._field_width, self._field_height, self._on_ground, \
            self._can_jump = contents
        self._reward = reward - self._last_reward
        self._last_reward = reward

    def step(self, action):
        self._send_action(action)
        self._get_observation()
        self._timestep += 1

        return self._state, 0.0 if self._just_reset else self._reward, self._just_reset, {}

    def _send_action(self, action):
        # Write the action to the socket
        action = int(action)
        for i in range(self._num_keys):
            self._socket.sendall(b'\x00' if action & 1 == 0 else b'\x01')
            action //= 2

    def reset(self):
        self._timestep = 0
        self._last_reward = 0
        return self._state

    def render(self, mode='human'):
        if self._state is None:
            return None

        if self.viewer is None:
            self._prepare_rendering()

        self._render(mode)

    def _render(self, mode):
        # Edit the polygon colors
        for cell, value in zip(self.drawing_cell, self._state[:100]):
            cell.set_color(*MarioEnv.CELL_COLORS[value])

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def _prepare_rendering(self):
        from gym.envs.classic_control import rendering
        screen_width = screen_height = 400
        cell_width = screen_width / self._field_width
        self.drawing_cell = []
        self.viewer = rendering.Viewer(screen_height, screen_width)
        # Fill the viewer with polygons
        for y in range(self._field_height, -1, -1):
            for x in range(self._field_width):
                l, r, t, b = x * cell_width, (x + 1) * cell_width, y * cell_width, (y - 1) * cell_width
                cell = rendering.FilledPolygon([(l, b), (l, t), (r, t), (r, b)])
                cell.set_color(0, 0, 0)
                self.viewer.add_geom(cell)
                self.drawing_cell.append(cell)

    def close(self):
        logger.info('Terminating MarioAI emulator...')
        self._emul.terminate()
        # Give your OS some to do some process management (as in effectively terminating the emulator process)
        return_code = self._emul.wait()

        if return_code == 128 + signal.SIGTERM:
            logger.info('Terminated')
        else:
            logger.warn('Something went wrong while terminating the MarioAI emulator.')
            logger.warn(f'Subprocess returned exit code {return_code}')

        if self.viewer:
            self.viewer.close()


class MarioMultiBinEnv(MarioEnv):

    def __init__(self, full_state):
        super(MarioMultiBinEnv, self).__init__(full_state=full_state)

    def _set_action_space(self):
        self.action_space = spaces.MultiBinary(self._num_keys - 1)  # Last key of Java simulator is unused

    def _send_action(self, action):
        # Write the action to the socket
        for i in action:
            self._socket.sendall(b'\x00' if int(i) & 1 == 0 else b'\x01')
        # Final button (up) is unused in Java simulator
        self._socket.sendall(b'\x00')


class Mario3DEnv(MarioEnv):

    def __init__(self):
        # Zero One-hot Encoder (0 = all zeros)
        self._enc = np.eye(MarioEnv.CELL_CATEGORIES + 1, MarioEnv.CELL_CATEGORIES, k=-1, dtype=np.float32)
        super(Mario3DEnv, self).__init__(full_state=False)

    def _prepare_state(self):
        # Due to Pytorch, we have CHW tensor order
        shape = (MarioEnv.CELL_CATEGORIES, self._field_height, self._field_width)
        self._statebuffer = np.zeros(shape, dtype=np.float32)

    def _process_state_buffer(self, buffer):
        self._state = self._enc[list(map(int, buffer))].reshape(self._field_height, self._field_width, -1).transpose(2,
                                                                                                                     0,
                                                                                                                     1)

    def _set_observation_space(self):
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=self._state.shape, dtype=self._state.dtype)

    def _render(self, mode='human'):
        # Edit the polygon colors
        dec = [np.where(np.all(self._enc == i, axis=1))[0][0] for i in self._state.transpose(1, 2, 0).reshape(
            (self._field_height * self._field_width, MarioEnv.CELL_CATEGORIES))]
        for cell, value in zip(self.drawing_cell, dec):
            cell.set_color(*MarioEnv.CELL_COLORS[value])

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')


class Mario3DMultiBinEnv(Mario3DEnv, MarioMultiBinEnv):
    def __init__(self):
        Mario3DEnv.__init__(self)

class UnaryMarioAction():
    r"""Reducing the action space of a MarioEnv to 6 discrete actions."""
    def __init__(self, env):
        assert isinstance(env, MarioEnv)
        assert isinstance(env.action_space, spaces.Discrete)
        super(UnaryMarioAction, self).__init__(env)

        self.action_space = spaces.Discrete(6)
        self._old_actions= [0] + [2**(x-1) for x in range(1,6)]

    def action(self, action):
        return self._old_actions[action]



# !!! USE env = UnaryMarioAction(env)
