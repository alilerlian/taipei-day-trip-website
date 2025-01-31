from ast import Try
from flask import *
import json
import mysql.connector
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

mydb = mysql.connector.connect(  # 連線資料庫
    host='localhost',
    port='3306',
    user='root',
    password='12345678',
    database='spots',
    charset='utf8',
)
mycursor = mydb.cursor()

# Pages


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/attraction/<id>")
def attraction(id):
    return render_template("attraction.html")


@app.route("/booking")
def booking():
    return render_template("booking.html")


@app.route("/thankyou")
def thankyou():
    return render_template("thankyou.html")


@app.route("/api/attractions")
def attractions():
    try:
        keyword = request.args.get("keyword")
        if keyword != None:
            pageRequest = int(request.args.get("page", 0))

            getResultId = "SELECT id FROM spots WHERE stitle LIKE '%"+keyword+"%'"
            mycursor.execute(getResultId)
            resultId = mycursor.fetchall()

            keyDataCount = len(resultId)  # 有關鍵字的數量

            getAttractionssql = "SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude FROM spots WHERE id=%s"

            attractionsData = {}
            attractionsData["nextPage"] = pageRequest+1
            if keyDataCount <= (pageRequest+1)*12:  # 檢查是否有下一頁 沒有就取代
                attractionsData["nextPage"] = None

            attractionsData["data"] = []
            for keyId in resultId:
                mycursor.execute(getAttractionssql, keyId)
                AttractionData = mycursor.fetchall()
                if AttractionData == []:  # 沒抓到資料就跳出
                    break

                singleAttraction = {}
                singleAttraction["id"] = AttractionData[0][0]
                singleAttraction["name"] = AttractionData[0][1]
                singleAttraction["category"] = AttractionData[0][2]
                singleAttraction["description"] = AttractionData[0][3]
                singleAttraction["address"] = AttractionData[0][4]
                singleAttraction["transport"] = AttractionData[0][5]
                singleAttraction["mrt"] = AttractionData[0][6]
                singleAttraction["latitude"] = AttractionData[0][7]
                singleAttraction["longitude"] = AttractionData[0][8]

                singleAttraction["images"] = []
                mycursor.execute(
                    "SELECT count(*) FROM information_schema.columns WHERE table_name ='spots'")
                totalColumn = mycursor.fetchone()[0]
                for j in range(0, totalColumn-21):
                    selectFile = "SELECT file_" + \
                        str(j+1)+" FROM spots WHERE id="+str(keyId[0])
                    mycursor.execute(selectFile)
                    fileData = mycursor.fetchall()
                    if fileData == [(None,)]:
                        break
                    singleAttraction["images"].append(fileData[0][0])

                attractionsData["data"].append(singleAttraction)

            return jsonify(attractionsData)

        else:
            getAttractionssql = "SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude FROM spots WHERE id=%s"

            pageRequest = int(request.args.get("page", 0))  # 從前端取得頁數(數字)

            attractionsData = {}

            attractionsData["nextPage"] = pageRequest+1  # 檢查是否有下一頁 沒有就取代

            mycursor.execute(getAttractionssql, (str((pageRequest+1)*12+1),))
            checkPage = mycursor.fetchall()

            if checkPage == []:
                attractionsData["nextPage"] = None

            attractionsData["data"] = []
            for i in range(pageRequest*12, (pageRequest+1)*12):
                mycursor.execute(getAttractionssql, (i+1,))
                AttractionData = mycursor.fetchall()
                if AttractionData == []:  # 沒抓到資料就跳出
                    break

                singleAttraction = {}
                singleAttraction["id"] = AttractionData[0][0]
                singleAttraction["name"] = AttractionData[0][1]
                singleAttraction["category"] = AttractionData[0][2]
                singleAttraction["description"] = AttractionData[0][3]
                singleAttraction["address"] = AttractionData[0][4]
                singleAttraction["transport"] = AttractionData[0][5]
                singleAttraction["mrt"] = AttractionData[0][6]
                singleAttraction["latitude"] = AttractionData[0][7]
                singleAttraction["longitude"] = AttractionData[0][8]

                singleAttraction["images"] = []
                mycursor.execute(
                    "SELECT count(*) FROM information_schema.columns WHERE table_name ='spots'")
                totalColumn = mycursor.fetchone()[0]
                for j in range(0, totalColumn-21):
                    selectFile = "SELECT file_" + \
                        str(j+1)+" FROM spots WHERE id="+str(i+1)
                    mycursor.execute(selectFile)
                    fileData = mycursor.fetchall()
                    if fileData == [(None,)]:
                        break
                    singleAttraction["images"].append(fileData[0][0])

                attractionsData["data"].append(singleAttraction)

            return jsonify(attractionsData)

    except:
        check = {}
        check["error"] = True
        check["massage"] = request.args.get("message", "伺服器內部錯誤")
        return jsonify(check)


@app.route("/api/attraction/<int:spot_id>")
def attractionsId(spot_id):
    try:
        getAttractionssql = "SELECT id,stitle,CAT2,xbody,address,info,MRT,latitude,longitude FROM spots WHERE id=%s"
        attractionsData = {}

        mycursor.execute(getAttractionssql, (spot_id,))
        AttractionData = mycursor.fetchall()
        if AttractionData != []:
            singleAttraction = {}
            singleAttraction["id"] = AttractionData[0][0]
            singleAttraction["name"] = AttractionData[0][1]
            singleAttraction["category"] = AttractionData[0][2]
            singleAttraction["description"] = AttractionData[0][3]
            singleAttraction["address"] = AttractionData[0][4]
            singleAttraction["transport"] = AttractionData[0][5]
            singleAttraction["mrt"] = AttractionData[0][6]
            singleAttraction["latitude"] = AttractionData[0][7]
            singleAttraction["longitude"] = AttractionData[0][8]

            singleAttraction["images"] = []
            mycursor.execute(
                "SELECT count(*) FROM information_schema.columns WHERE table_name ='spots'")
            totalColumn = mycursor.fetchone()[0]
            for j in range(0, totalColumn-21):
                selectFile = "SELECT file_" + \
                    str(j+1)+" FROM spots WHERE id="+str(spot_id)
                mycursor.execute(selectFile)
                fileData = mycursor.fetchall()
                if fileData == [(None,)]:
                    break
                singleAttraction["images"].append(fileData[0][0])
            attractionsData["data"] = singleAttraction

            return jsonify(attractionsData)
        else:
            checknumber = {}
            checknumber["error"] = True
            checknumber["massage"] = request.args.get("message", "景點編號不正確")
            return jsonify(checknumber)
    except:
        check = {}
        check["error"] = True
        check["massage"] = request.args.get("message", "伺服器內部錯誤")
        return jsonify(check)


app.run(port=3000)
