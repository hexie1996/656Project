import json
import string
import mysql.connector
cnx = mysql.connector.connect(user='root', password='12345678',
                              host='127.0.0.1',auth_plugin='mysql_native_password')
mycursor = cnx.cursor()
mycursor.execute("use project")
letters=string.ascii_lowercase
for l in letters:
    try:
        data = [json.loads(line) for line in open('../yelp-dataset/user/user_'+l, 'r')]
    except:
        break
        """
    for d in data:
        mycursor.execute("select userID from user where userID=\"" + d['user_id'] + "\";")
        myresult = mycursor.fetchall()
        if myresult == []:
            mycursor.execute("insert into user values (\"" + d['user_id'] + "\",\""+d['name']+"\",'un','None','None','None');")
            cnx.commit()
        """
    for d in data:
        if d['friends']!='None':
            friendList=d['friends'].split(', ')
            print(friendList)
            for f in friendList:
                try:
                    mycursor.execute("insert into friendsTable values(\"" + d['user_id'] + "\",\"" + f + "\",'None');")
                except:
                    print("userID doesn't exist.")
                try:
                    mycursor.execute("insert into friendsTable values(\"" + f + "\",\"" + d['user_id'] + "\",'None');")
                except:
                    print("userID doesn't exist.")
                cnx.commit()

