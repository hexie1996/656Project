import json
import string
import mysql.connector
import mysql.connector
cnx = mysql.connector.connect(user='root', password='12345678',
                              host='127.0.0.1',auth_plugin='mysql_native_password')
mycursor = cnx.cursor()
mycursor.execute("use project")
letters=string.ascii_lowercase
count=0
for i in letters:
    for j in letters:
        try:
            data = [json.loads(line) for line in open('../review/review_' + i + j, 'r')]
        except:
            break
        for d in data:
            mycursor.execute(
                "insert into post (postID,userID,content,url,imageUrl,post_time) values (\"" + d['review_id'] + "\",\"" + d['user_id'] + "\",\""+d['text']+"\",\"None\",\"None\",\""+d['date']+"\");")
            count+=1
            if count % 100000 == 0:
                cnx.commit()
                print(str(count) + " completed")
cnx.commit()