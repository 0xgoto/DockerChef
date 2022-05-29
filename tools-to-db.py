#! /usr/bin/python3

from pymongo import MongoClient

client = MongoClient("mongodb://user_g0at:bs0dislit@cluster0-shard-00-00.xwp04.mongodb.net:27017,"
                     "cluster0-shard-00-01.xwp04.mongodb.net:27017,"
                     "cluster0-shard-00-02.xwp04.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas"
                     "-1009yy-shard-0&authSource=admin&retryWrites=true&w=majority")
db = client.dockerchef
tools = db["tools"]

# apt_list_file = open('apt-list.txt', 'r')
#
# apt_list_file_data = apt_list_file.read()
# apt_list = apt_list_file_data.replace('\n', ' ').split(" ")
#
# tools.insert_one({
#     'tools': apt_list
# })
#
# print("Tools list successfully added")

tools_list = tools.find()[0]["tools"]
print(tools_list[999])
