import flask
from flask import request, jsonify
import string
import datetime
import mysql.connector
import random
cnx = mysql.connector.connect(user='root', password='12345678',
                              host='127.0.0.1',auth_plugin='mysql_native_password')
mycursor = cnx.cursor()
mycursor.execute("use project")

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET']) #home
def home():
    return "<h1>ECE656 project</h1><p>20848700</p>"

@app.route('/user', methods=['GET']) #get the user's information
def user_detailed_information():
    if 'user_id' in request.args:
        id = str(request.args['user_id'])
        #127.0.0.1:5000/user?user_id=__
    else:
        return "Error: No id field provided. Please specify an id."
    mycursor.execute("select * from user where userID=\""+id+"\"")
    results=get_results(mycursor)
    return jsonify(results)

@app.route('/friends_post', methods=['GET']) #get the unseen posts from all the friends of the user
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

@app.route('/topic_post', methods=['GET']) #get all the unseen topic's post
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
@app.route('/group_post', methods=['GET']) #get the the post of groups that the user follows
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

@app.route('/all_topic', methods=['GET']) #get all the posts in this topic
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

@app.route('/all_person',methods=['GET']) #get all the posts of an user
def all_person():
    if 'user_id' in request.args:
        id = str(request.args['user_id'])
    else:
        return "Error: Cannot find the user id."
    mycursor.execute("select * from post where userID=\""+id+"\";")
    results = get_results(mycursor)
    return jsonify(results)

@app.route('/friend_list',methods=['GET']) #get the friend list of an user
def friend_list():
    if 'user_id' in request.args:
        id = str(request.args['user_id'])
    else:
        return "Error: Cannot find the user id."
    mycursor.execute("select userID,nickname from user where userID in (select followingID from friendsTable where followerID=\'" + id + "\');")
    results = get_results(mycursor)
    return jsonify(results)

@app.route('/all_group',methods=['GET']) #get all the group's information
def all_group():
    mycursor.execute("select * from peopleGroup;")
    results = get_results(mycursor)
    return jsonify(results)
#post methods

@app.route('/send_post',methods=['POST']) #send one post
def send_post():
    data = request.get_json()
    this_post_id=random_string()
    mycursor.execute("insert into post values(\""+this_post_id+"\",\""+data['userID']+"\",\""+data['content']+",'None','None',\""+str(datetime.datetime.now())+"\");")
    if(data['topicID']!='None'):
        mycursor.execute("select * from topic where topicID=\""+data['topicID']+"\"")
        t=mycursor.fetchall()
        if t!=[]:
            mycursor.execute("insert into postTopicTable values(\""+data['topicID']+"\",\""+this_post_id+"\");")
        else:
            return "Error: topic id does not exist."
    mycursor.commit()
    return "Completed!"

@app.route('/follow_person',methods=['POST']) #follow a person
def follow_person():
    data = request.get_json()
    mycursor.execute("select * from user where userID=\"" + data['userID'] + "\"")
    t = mycursor.fetchall()
    if t!=[]:
        try:
            mycursor.execute("insert into friendsTable values(\""+data['followerID']+"\",\""+data['followingID']+"\",\""+str(datetime.datetime.now())+"\");")
        except:
            return "Error: you have followed this person already."
    else:
        return "Error: user id does not exist"
    mycursor.commit()
    return "Completed!"

@app.route('/follow_topic',methods=['POST']) #follow a topic
def follow_topic():
    data = request.get_json()
    mycursor.execute("select * from topic where topicID=\"" + data['topicID'] + "\"")
    t = mycursor.fetchall()
    if t!=[]:
        try:
            mycursor.execute("insert into userTopicTable values(\""+data['topicID']+"\",\""+data['userID']+"\");")
        except:
            return "Error: you have followed this topic already"
    else:
        return "Error: topic id does not exist."
    mycursor.commit()
    return "Completed!"

@app.route('/create_group',methods=['POST']) #create a group
def create_group():
    data = request.get_json()
    group_id=random_string()
    mycursor.execute("select * from peopleGroup where groupID=\"" + group_id + "\"")
    t = mycursor.fetchall()
    if t==[]:
        mycursor.execute("insert into peopleGroup values(\""+group_id+"\",\""+data['groupName']+"\",0);")
    else:
        group_id = random_string()
        mycursor.execute("insert into peopleGroup values(\"" + group_id + "\",\"" + data['groupName'] + "\",0);")
    mycursor.commit()
    return "Completed!"

@app.route('/follow_group',methods=['POST']) #
def follow_group():
    data = request.get_json()
    mycursor.execute("select * from peopleGroup where groupID=\"" + data['groupID'] + "\"")
    t = mycursor.fetchall()
    if t!=[]:
        try:
            mycursor.execute("insert into userGroupTable values(\"" + data['groupID'] + "\",\"" + data['userID'] + "\")")
            mycursor.execute("update peopleGroup set peopleNum=peopleNum+1 where groupID=\"" + data['groupID'] + "\";")
        except:
            return "Error: you have followed this group already."
    else:
        return "Error: group id does not exist."
    mycursor.commit()
    return "Completed!"

@app.route('/create_user',methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = random_string()
    mycursor.execute("select * from user where userID=\"" + user_id + "\"")
    t = mycursor.fetchall()
    if t == []:
        mycursor.execute("insert into user values(\"" + user_id + "\",\"" + data['nickname'] + "\",\"" + data['gender'] + "\",\"" + data['birthday'] + "\",\"" + data['bio'] + "\",\"" + data['religion'] + "\");")
    else:
        user_id = random_string()
        mycursor.execute(
            "insert into user values(\"" + user_id + "\",\"" + data['nickname'] + "\",\"" + data['gender'] + "\",\"" +
            data['birthday'] + "\",\"" + data['bio'] + "\",\"" + data['religion'] + "\");")
    mycursor.commit()
    return "Completed!"

@app.route('/like',methods=['POST'])
def like():
    data = request.get_json()
    mycursor.execute("select * from statusTable where userID=\"" + data['userID'] + "\" and postID=\"" + data['postID'] + "\";")
    t = mycursor.fetchall()
    if t == []:
        mycursor.execute("insert into statusTable values (\""+data['userID']+"\",\""+data['postID']+"\","+data['likeType']+",\""+str(datetime.datetime.now())+"\",true,\""+str(datetime.datetime.now())+"\")")
    else:
        mycursor.execute("update statusTable set likeType="+data['likeType']+", likeTime=\""+str(datetime.datetime.now())+"\" where userID=\""+data['userID']+"\" and postID=\""+data['postID']+"\";")
    mycursor.commit()

@app.route('/create_topic',methods=['POST'])
def create_topic():
    data = request.get_json()
    topic_id = random_string()
    mycursor.execute("select * from topic where topicID=\"" + topic_id + "\"")
    t = mycursor.fetchall()
    if t == []:
        mycursor.execute(
            "insert into topic values(\""+topic_id+"\",\""+data['topicName']+"\",'None')")
    else:
        topic_id = random_string()
        mycursor.execute(
            "insert into topic values(\"" + topic_id + "\",\"" + data['topicName'] + "\",'None')")
    mycursor.commit()
    return "Completed!"

###########################################
def mark_seen(id,results,mycursor):
    for r in results:
        mycursor.execute("select * from statusTable where userID=\""+id+"\" and postID=\""+r['postID']+"\";")
        t=mycursor.fetchall()
        if t == []:
            mycursor.execute("insert into statusTable values (\""+id+"\",\""+r['postID']+"\",NULL,NULL,true,\""+str(datetime.datetime.now())+"\")")
        else:
            mycursor.execute("update statusTable set seen=true, seenTime=\""+str(datetime.datetime.now())+"\" where userID=\""+id+"\" and postID=\""+r['postID']+"\";")
    mycursor.commit()

def get_results(db_cursor):
    desc = [d[0] for d in db_cursor.description]
    results = [dotdict(dict(zip(desc, res))) for res in db_cursor.fetchall()]
    return results
def random_string():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(40))
class dotdict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

app.run()