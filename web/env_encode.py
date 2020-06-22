import gym
from PIL import Image
import base64

env = gym.make('Pong-v0')
env.reset()
env.step(0)
t = env.render(mode="rgb_array")
print(t)
img = Image.fromarray(t)
coded = base64.b64encode(img)
print(coded)