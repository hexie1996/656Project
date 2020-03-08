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
    mycursor.execute("select * from user where userID=\""+id+"\"")
    results=get_results(mycursor)
    return jsonify(results)

@app.route('/friends_post', methods=['GET'])
def friends_post():
    if 'user_id' in request.args:
        id = str(request.args['user_id'])
    else:
        return "Error: Cannot find the user id."
    mycursor.execute("select * from "
                     "(select * from post where userID in "
                     "(select followingID from friendsTable "
                     "where followerID = \'"+id+"\')"
                     " and postID not in "
                     "(select postID from statusTable where userID="
                     "\'"+id+"\' and seen=true)) as A "
                     "inner join user on A.userID=user.userID;")
    results=get_results(mycursor)
    mark_seen(id,results,mycursor)
    return jsonify(results)

@app.route('/topic_post', methods=['GET'])
def topic_post():
    if 'user_id' in request.args:
        id = str(request.args['user_id'])
    else:
        return "Error: Cannot find the user id."
    mycursor.execute("select * from post where postID in "
                     "(select postID from postTopicTable "
                     "where topicID in (select topicID "
                     "from userTopicTable where userID"
                     " = \'"+id+"\')) and postID not in "
                     "(select postID from statusTable where userID="
                     "\'"+id+"\' and seen=true)")
    results = get_results(mycursor)
    mark_seen(id, results, mycursor)
    return jsonify(results)
@app.route('/group_post', methods=['GET'])
def group_post():
    if 'user_id' in request.args:
        id = str(request.args['user_id'])
    else:
        return "Error: Cannot find the user id."
    mycursor.execute("select * from post where userID in "
                     "(select userID from userGroupTable "
                     "where groupID in (select groupID "
                     "from userGroupTable where userID"
                     " = \'" + id + "\')) and postID not in "
                                    "(select postID from statusTable where userID="
                                    "\'" + id + "\' and seen=true)")
    results = get_results(mycursor)
    mark_seen(id, results, mycursor)
    return jsonify(results)

@app.route('/all_topic', methods=['GET'])
def all_topic():
    if 'topic_id' in request.args:
        id = str(request.args['topic_id'])
    else:
        return "Error: Cannot find the topic id."
    mycursor.execute("select nickname,post_time,content"
                     " from (select * from post where postID in "
                     "(select postID from postTopicTable where topicID=\""+id+"\"))"
                     " as A inner join user on A.userID=user.userID;")
    results = get_results(mycursor)
    return jsonify(results)

@app.route('/all_person',methods=['GET'])
def all_person():
    if 'user_id' in request.args:
        id = str(request.args['user_id'])
    else:
        return "Error: Cannot find the user id."
    mycursor.execute("select * from post where userID=\""+id+"\";")
    results = get_results(mycursor)
    return jsonify(results)

@app.route('/friend_list',methods=['GET'])
def friend_list():
    if 'user_id' in request.args:
        id = str(request.args['user_id'])
    else:
        return "Error: Cannot find the user id."
    mycursor.execute("select userID,nickname from user where userID in (select followingID from friendsTable where followerID=\'" + id + "\');")
    results = get_results(mycursor)
    return jsonify(results)

@app.route('/all_group',methods=['GET'])
def all_group():
    mycursor.execute("select * from peopleGroup;")
    results = get_results(mycursor)
    return jsonify(results)

def mark_seen(id,results,mycursor):
    for r in results:
        mycursor.execute("select * from statusTable where userID=\""+id+"\" and postID=\""+r['postID']+"\";")
        t=mycursor.fetchall()
        if t == []:
            mycursor.execute("insert into statusTable values (\""+id+"\",\""+r['postID']+"\",NULL,NULL,true,\""+str(datetime.datetime.now())+"\")")
        else:
            mycursor.execute("update statusTable set seen=true, seenTime=\""+str(datetime.datetime.now())+"\" where userID=\""+id+"\" and postID=\""+r['postID']+"\";")

def get_results(db_cursor):
    desc = [d[0] for d in db_cursor.description]
    results = [dotdict(dict(zip(desc, res))) for res in db_cursor.fetchall()]
    return results

class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

app.run()