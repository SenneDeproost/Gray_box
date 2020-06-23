import gym
from PIL import Image
import base64
import numpy as np
import cv2
from io import BytesIO
import json

env = None


# Load in new session
def load_session(profile, distillate, algorithm, environment):
    global env
    env = gym.make(environment)
    env.reset()
    #env.render()
    rgb = env.render(mode='rgb_array')
    game_b64 = to_b64(rgb)
    data = {}
    data['game'] = game_b64.decode("utf-8")
    return data


# Convert RGB array to base 64.
def to_b64(array):
    img = Image.fromarray(array)
    im_file = BytesIO()
    img.save(im_file, format="PNG")
    im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
    im_b64 = base64.b64encode(im_bytes)
    return im_b64
