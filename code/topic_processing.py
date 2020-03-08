import json
import mysql.connector
cnx = mysql.connector.connect(user='root', password='12345678',
                              host='127.0.0.1',auth_plugin='mysql_native_password')
mycursor = cnx.cursor()
mycursor.execute("use project")
data = [json.loads(line) for line in open('../business/business_a', 'r')]
for d in data:
    name = d['name'].replace('\\', '\\\\')
    name = name.replace('"', '\\"')
    mycursor.execute("insert into topic values(\""+d['business_id']+"\",\""+name+"\",\"None\");")
cnx.commit()
print("completed!")