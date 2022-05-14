#! /usr/bin/python3

from flask import Flask, jsonify, request
from pymongo import MongoClient
import bcrypt
import os
import docker
import requests
from pymongo.server_api import ServerApi

client = MongoClient("mongodb://user_g0at:bs0dislit@cluster0-shard-00-00.xwp04.mongodb.net:27017,"
                     "cluster0-shard-00-01.xwp04.mongodb.net:27017,"
                     "cluster0-shard-00-02.xwp04.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas"
                     "-1009yy-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.dockerchef
users = db["Users"]


def UserExist(username):
    if users.count_documents({"username":username}) == 0:
        return False
    else:
        return True


def verifyPw(username, password):
    if not UserExist(username):
        return False

    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False
