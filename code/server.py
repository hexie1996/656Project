import flask
from flask import request, jsonify
import datetime
import mysql.connector
cnx = mysql.connector.connect(user='root', password='12345678',
                              host='127.0.0.1',auth_plugin='mysql_native_password')
mycursor = cnx.cursor()
mycursor.execute("use project")

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return "<h1>ECE656 project</h1><p>20848700</p>"

@app.route('/user', methods=['GET'])
def user_detailed_information():
    if 'user_id' in request.args:
        id = str(request.args['user_id'])
        #127.0.0.1:5000/user?user_id=__
    else:
        return "Error: No id field provided. Please specify an id."
    results = []
    mycursor.execute("select * from user where userID=\""+id+"\"")
    results = mycursor.fetchall()
    return jsonify(results)

@app.route('/friends', methods=['GET'])
def friends_post():
    if 'user_id' in request.args:
        id = str(request.args['user_id'])
    else:
        return "Error: Cannot find the user id."
    results=[]
    mycursor.execute("select nickname,postID,post_time,content from "
                     "(select * from post where userID in "
                     "(select followingID from friendsTable "
                     "where followerID = \'"+id+"\')"
                     " and postID not in "
                     "(select postID from statusTable where userID="
                     "\'"+id+"\' and seen=true)) as A "
                     "inner join user on A.userID=user.userID;")
    results=mycursor.fetchall()
    for r in results:
        mycursor.execute("select * from statusTable where userID=\""+id+"\" and postID=\""+r[1]+"\";")
        t=mycursor.fetchall()
        if t == []:
            mycursor.execute("insert into statusTable values (\""+id+"\",\""+r[1]+"\",NULL,NULL,true,\""+str(datetime.datetime.now())+"\")")
        else:
            mycursor.execute("update statusTable set seen=true, seenTime=\""+str(datetime.datetime.now())+"\" where userID=\""+id+"\" and postID=\""+r[1]+"\";")
    return jsonify(results)
app.run()