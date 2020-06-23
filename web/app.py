from flask import Flask, render_template, redirect, jsonify, request
import sys
import os
sys.path.append('../')
import webutils, webrun
os.chdir('../')
app = Flask(__name__)


@app.route('/')
def redir():
   return redirect('/index.html')


@app.route('/index.html')
def home():
   return render_template('index.html')


@app.route('/api/list_profiles', methods=['GET'])
def list_profiles():
    return jsonify(webutils.list_profiles())


@app.route('/api/list_distillates', methods=['GET'])
def list_distillates():
    profile = request.args.get('profile')
    return jsonify(webutils.list_distillates(profile))


@app.route('/api/list_algorithms', methods=['GET'])
def list_algorithms():
    return jsonify(webutils.list_algorithms())


@app.route('/api/list_environments', methods=['GET'])
def list_environments():
    return jsonify(webutils.list_environments())


@app.route('/api/load_session', methods=['GET'])
def load_session():
    profile = request.args.get('profile')
    distillate = request.args.get('distillate')
    environment = request.args.get('environment')
    algorithm = request.args.get('algorithm')

    game_img = webrun.load_session(profile, distillate, algorithm, environment)
    return jsonify(game_img)





if __name__ == '__main__':
   app.run()