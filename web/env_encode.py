import gym
from PIL import Image
import base64
import numpy as np
import cv2
from io import BytesIO

env = gym.make('Pong-v0')
env.reset()
env.step(0)
t = env.render(mode="rgb_array")

print(t)
img = Image.fromarray(t)
print(img)
im_file = BytesIO()
img.save(im_file, format="PNG")
im_bytes = im_file.getvalue()  # im_bytes: image in binary format.
im_b64 = base64.b64encode(im_bytes)
print(im_b64)