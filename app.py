#! /usr/bin/python3

from flask import Flask, jsonify, request, session, render_template, redirect, g, url_for
from pymongo import MongoClient
import bcrypt
import os
import docker
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "temp"
app.permanent_session_lifetime = timedelta(hours=2)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8001)
