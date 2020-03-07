import json
import string
import mysql.connector
cnx = mysql.connector.connect(user='root', password='12345678',
                              host='127.0.0.1',auth_plugin='mysql_native_password')
mycursor = cnx.cursor()
letters=string.ascii_lowercase
userID=set()
count=0
for l in letters:
    try:
        data = [json.loads(line) for line in open('../user/user_'+l, 'r')]
    except:
        break
    for d in data:
        mycursor.execute(
            "insert into user values (\"" + d['user_id'] + "\",\"" + d['name'] + "\",'un','None','None','None');")
        userID.add(d['user_id'])
        count+=1
        if count%50000 == 0:
            cnx.commit()
            print(str(count)+" completed")
count=0
for l in letters:
    try:
        data = [json.loads(line) for line in open('../user/user_'+l, 'r')]
    except:
        break
    for d in data:
        if d['friends'] != 'None':
            friendList = d['friends'].split(', ')
        else:
            friendList = []
        for f in friendList:
            if f in userID:
                mycursor.execute("insert into friendsTable values(\"" + d['user_id'] + "\",\"" + f + "\",'None');")
                mycursor.execute("insert into friendsTable values(\"" + f + "\",\"" + d['user_id'] + "\",'None');")
                count += 1
                if count % 50000 == 0:
                    cnx.commit()
                    print(str(count) + " completed")


