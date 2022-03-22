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
            # print(keyword)
            getResultId = "SELECT count(id) FROM spots WHERE name LIKE '%" + \
                keyword+"%'"
            mycursor.execute(getResultId)
            keyDataCount = mycursor.fetchall()[0][0]  # 有關鍵字的數量
            # print(resultId)
            # keyDataCount = len(resultId)
            print(keyDataCount)

            attractionsData = {}
            attractionsData["nextPage"] = pageRequest+1
            if keyDataCount <= (pageRequest+1)*12:  # 檢查是否有下一頁 沒有就取代
                attractionsData["nextPage"] = None
            print(attractionsData["nextPage"])

            attractionsData["data"] = []
            skipdata = str(pageRequest*12)
            print(skipdata)
            getAttractionssql = "SELECT * FROM spots WHERE name LIKE '%" + \
                keyword+"%' ORDER BY id limit 12 offset " + skipdata
            # print(getAttractionssql)

            mycursor.execute(getAttractionssql)
            AttractionData = mycursor.fetchall()
            # print(AttractionData)

            for i in range(0, len(AttractionData)):
                singleAttraction = {}
                singleAttraction["id"] = AttractionData[i][0]
                singleAttraction["name"] = AttractionData[i][1]
                singleAttraction["category"] = AttractionData[i][2]
                singleAttraction["description"] = AttractionData[i][3]
                singleAttraction["address"] = AttractionData[i][4]
                singleAttraction["transport"] = AttractionData[i][5]
                singleAttraction["mrt"] = AttractionData[i][6]
                singleAttraction["latitude"] = AttractionData[i][7]
                singleAttraction["longitude"] = AttractionData[i][8]
                # print(singleAttraction["id"])

                singleAttraction["images"] = []
                for j in range(9, len(AttractionData[i])+1):
                    if AttractionData[i][j] == None:
                        break
                    singleAttraction["images"].append(AttractionData[i][j])

                # print(singleAttraction["images"])
                attractionsData["data"].append(singleAttraction)
            # print(attractionsData)
            return jsonify(attractionsData)

        else:
            getResultId = "SELECT count(id) FROM spots"
            pageRequest = int(request.args.get("page", 0))  # 從前端取得頁數(數字)
            # pageRequest = 0
            # print(pageRequest)
            mycursor.execute(getResultId)
            DataCount = mycursor.fetchall()[0][0]

            attractionsData = {}
            attractionsData["nextPage"] = pageRequest+1  # 下一頁
            if DataCount <= (pageRequest+1)*12:  # 檢查是否有下一頁 沒有就取代
                attractionsData["nextPage"] = None
            print(attractionsData["nextPage"])

            attractionsData["data"] = []  # 景點資料
            skipdata = str(pageRequest*12)
            print(skipdata)
            getAttractionssql = "SELECT * FROM spots ORDER BY id limit 12 offset " + skipdata
            # print(getAttractionssql)

            mycursor.execute(getAttractionssql)
            AttractionData = mycursor.fetchall()
            # print(AttractionData)

            for i in range(0, len(AttractionData)):
                singleAttraction = {}
                singleAttraction["id"] = AttractionData[i][0]
                singleAttraction["name"] = AttractionData[i][1]
                singleAttraction["category"] = AttractionData[i][2]
                singleAttraction["description"] = AttractionData[i][3]
                singleAttraction["address"] = AttractionData[i][4]
                singleAttraction["transport"] = AttractionData[i][5]
                singleAttraction["mrt"] = AttractionData[i][6]
                singleAttraction["latitude"] = AttractionData[i][7]
                singleAttraction["longitude"] = AttractionData[i][8]
                # print(singleAttraction["id"])

                singleAttraction["images"] = []
                for j in range(9, len(AttractionData[i])):
                    if AttractionData[i][j] == None:
                        break
                    singleAttraction["images"].append(AttractionData[i][j])

                # print(singleAttraction["images"])
                attractionsData["data"].append(singleAttraction)
            # print(attractionsData)
            return jsonify(attractionsData)

    except:
        check = {}
        check["error"] = True
        check["massage"] = request.args.get("message", "伺服器內部錯誤")
        return jsonify(check)


@app.route("/api/attraction/<int:spot_id>")
def attractionsId(spot_id):
    try:
        getAttractionssql = "SELECT * FROM spots WHERE id=%s"
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
            for j in range(9, len(AttractionData[0])):
                if AttractionData[0][j] == None:
                    break
                singleAttraction["images"].append(AttractionData[0][j])
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


app.run(host='0.0.0.0', port=3000)
