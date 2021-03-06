#! /usr/bin/python3

import os
from datetime import timedelta
import random
import bcrypt
import docker
from flask import Flask, request, session, render_template, redirect, url_for
from pymongo import MongoClient

import classes

app = Flask(__name__)
app.secret_key = "temp"
app.permanent_session_lifetime = timedelta(hours=2)

client = MongoClient("mongodb://user_g0at:bs0dislit@cluster0-shard-00-00.xwp04.mongodb.net:27017,"
                     "cluster0-shard-00-01.xwp04.mongodb.net:27017,"
                     "cluster0-shard-00-02.xwp04.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas"
                     "-1009yy-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.dockerchef
users = db["Users"]
tools = db["tools"]
tools_list = tools.find()[0]["tools"]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('uname')
    password = request.form.get('pswd')
    if classes.verifyPw(username, password):
        session.permanent = True
        session["user"] = username
        # return classes.retJson(200, "Logged in successfully")
        return redirect(url_for("user"), code=307)
    else:
        # return classes.retJson(302, "Invalid Username/Password")
        return render_template("index.html")


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form.get('uname')
    email = request.form.get('email')
    password = request.form.get('pswd')

    if classes.UserExist(username):
        return render_template('index.html', data="User already exist!")

    hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    users.insert_one({
        "Username": username,
        "Email": email,
        "Password": hashed_pw,
        "tools_used": [],
        "Docker_history": []
    })
    os.system("mkdir results/" + username)
    session.permanent = True
    session["user"] = username

    return redirect(url_for("user"), code=307)


@app.route('/user', methods=['POST', 'GET'])
def user():
    return render_template('user.html', user=session["user"], tools=tools_list)
    # return "<h1> Welcome {}! </h1>".format(session["user"])


@app.route('/build', methods=['POST'])
def build():
    lst = request.form.getlist('list')
    image_name = request.form.get('name')
    username = session["user"]
    apt_cmd = ""
    if lst != "":
        apt_cmd = "FROM ubuntu:18.04\nRUN apt-get update && apt-get install -y openssh-server \\\n\t"
        for tool in lst:
            apt_cmd += tool + " \\ \n\t"
        apt_cmd += "&& rm -rf /var/lib/apt/lists/*\n"

    apt_cmd += "RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 " + username + "\n"
    apt_cmd += "RUN echo '" + username + ":" + username + "' | chpasswd\n"
    apt_cmd += "RUN service ssh start\n"
    apt_cmd += "EXPOSE 22\n"
    apt_cmd += "CMD [\"/usr/sbin/sshd\",\"-D\"]"
    dest_file = "results/" + username + "/Dockerfile"
    dest_path = "results/" + username + "/"
    dockerfile = open(dest_file, "w")
    dockerfile.write(apt_cmd)
    dockerfile.close()

    docker_client = docker.from_env()
    print(docker_client.login("nukkunda", "whatiswr0ng", "lefef79626@ztymm.com"))
    print(docker_client.images.build(path="results/" + username, dockerfile="Dockerfile",
                                     tag="nukkunda/" + username + ":" + image_name, rm=True))
    print(docker_client.images.push(repository="nukkunda/" + username))
    return render_template('build.html', image="nukkunda/" + username + ":" + image_name)


@app.route('/deploy', methods=['POST', 'GET'])
def deploy():
    image = request.form.get('image')

    ssh_port = random.randint(2002, 2062)
    shell_port = random.randint(4002, 4062)
    # os.system("sudo docker run -d -p 22:"+str(ssh_port)+" "+image)
    # os.system("shellinaboxd --disable-ssl --port "+str(shell_port)+" -s /:SSH:172.31.13.227:"+str(ssh_port)+"&")
    return redirect("http://43.204.116.161:4226")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8001)
