
import mysql.connector
import json

mydb = mysql.connector.connect(  # 連線資料庫
    host='localhost',
    port='3306',
    user='root',
    password='12345678',
    database='spots',
    charset='utf8',
)

mycursor = mydb.cursor()

with open('taipei-attractions.json', encoding="utf-8") as jsonData:
    data = json.load(jsonData)

resultList = data["result"]["results"]  # 取出景點部分

for i in range(0, len(resultList)):  # 把網址分好放回去 取得景點的list 各景點為dict
    photo_split = resultList[i]["file"].split("https://")

    photoList = []
    for j in range(1, len(photo_split)):
        photo = "https://"+photo_split[j]
        filelast3 = photo[-3:]
        if (filelast3 == "jpg" or filelast3 == "JPG" or filelast3 == "png" or filelast3 == "PNG"):
            photoList.append(photo)
    resultList[i]["file"] = photoList

for i in range(0, len(resultList)):
    spot = resultList[i]

    id = i+1
    name = spot["stitle"]
    category = spot["CAT2"]
    description = spot["xbody"]
    address = spot["address"]
    transport = spot["info"]
    mrt = spot["MRT"]
    latitude = spot["latitude"]
    longitude = spot["longitude"]

    insertData = (id, name, category, description, address,
                  transport, mrt, latitude, longitude)
    insertsql = "INSERT INTO spots (id,name,category,description,address,transport,mrt,latitude,longitude) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    mycursor.execute(insertsql, insertData)
    mydb.commit()

    files = spot["file"]

    mycursor.execute(
        "SELECT count(*) FROM information_schema.columns WHERE table_name ='spots'")
    totalColumn = mycursor.fetchone()[0]  # 初始欄位總數 47
    if totalColumn-47 > len(files):
        for k in range(0, len(files)):
            fileNum = k+1
            updateFileSql = "UPDATE spots SET "+"file_" + \
                str(fileNum)+"=%s WHERE id="+str(id)
            mycursor.execute(updateFileSql, (files[k],))
            mydb.commit()

    elif totalColumn-47 == 0:
        for k in range(0, len(files)):
            fileNum = k+1
            addCloumnSql = "ALTER TABLE spots ADD " + \
                "file_"+str(fileNum)+" VARCHAR(255)"
            updateFileSql = "UPDATE spots SET "+"file_" + \
                str(fileNum)+"=%s WHERE id="+str(id)
            mycursor.execute(addCloumnSql)
            mycursor.execute(updateFileSql, (files[k],))
            mydb.commit()

    elif totalColumn-47 < len(files):
        for k in range(0, totalColumn-47):
            fileNum = k+1
            updateFileSql = "UPDATE spots SET "+"file_" + \
                str(fileNum)+"=%s WHERE id="+str(id)
            mycursor.execute(updateFileSql, (files[k],))
            mydb.commit()
        for l in range(totalColumn-47, len(files)):
            fileNum = l+1
            addCloumnSql = "ALTER TABLE spots ADD " + \
                "file_"+str(fileNum)+" VARCHAR(255)"
            updateFileSql = "UPDATE spots SET "+"file_" + \
                str(fileNum)+"=%s WHERE id="+str(id)
            mycursor.execute(addCloumnSql)
            mycursor.execute(updateFileSql, (files[l],))
            mydb.commit()
