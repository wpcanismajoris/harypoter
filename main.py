from fastapi import FastAPI
import mysql.connector
import time
import uvicorn
import os 
# import base64
app = FastAPI()

mydb = mysql.connector.connect(user="burak", password="webscraping123!", host="androidmysql.mysql.database.azure.com", port=3306, database="harrypoter", ssl_ca="cert.pem", ssl_disabled=False)
mycursor = mydb.cursor()


# checkTokenExpire fonksiyonu tokenin süresini kontrol eder.
def checkTokenExpire(token):
    if(int(token) < int(time.time())):
        return False
    else:
        return True

# anasayfaya geldiginde json olarak ekrana mesaj baslilir.
@app.get("/")
async def root():
    return {"message": "Welcome"}


# login islemi icin kullanilacak route burada tanimlanmistir. username ve password bilgileri ile login olunur.
# kullanici basarili bir sekilde giris yaptiginda tokeni olusturulur ve tokenin süresi 1 saat olarak belirlenir.
@app.get("/login")
async def login(username,password):
    try:
        mycursor = mydb.cursor()
        sql = f'SELECT id FROM users WHERE username="{username}" AND password="{password}"'
        mycursor.execute(sql)
        data = mycursor.fetchall()
        mydb.commit()
        if len(data) == 0:
            return {"message": "No User Found"}
        else:
            expireTime = int(time.time()) + 3600
            sql = f'UPDATE users SET token="{expireTime}" WHERE username="{username}" AND password="{password}"'
            mycursor.execute(sql)
            mydb.commit()
        return {"message": "Success"}
    except Exception as e:
        return {"message": str(e)}



# kullanici register olmak istediginde buradaki endpointi kullanarak register islemlerini tamamlar.
# post methodu ile username, password ve email bilgileri alinir.
# token olusturulur ve tokenin süresi 1 saat olarak belirlenir.
# kullanici bilgileri veritabanina kaydedilir.
@app.post("/register")
async def register(username,password,email):

    try:
        token = int(time.time()) + 3600
        mycursor = mydb.cursor()
        sql = "INSERT INTO users (username, password, token, email) VALUES (%s, %s, %s ,%s)"
        val = (username, password,token, email)
        mycursor.execute(sql, val)

        mydb.commit()
        return {"message": "Success", "token": token}
    except Exception as e:
        return {"message": str(e)}

# kullanici logout olmak istediginde buradaki endpointi kullanarak logout islemlerini tamamlar.
# post methodu ile username ve password bilgileri alinir.
@app.post("/reset-password")
async def resetPassword(username,password,newPassword):

    try:
        mycursor = mydb.cursor()
        sql = f'SELECT id FROM users WHERE username="{username}" AND password="{password}"'
        mycursor.execute(sql)
        data = mycursor.fetchall()
        mydb.commit()
        if len(data) == 0:
            return {"message": "No User Found"}
        else:
            sql = f'UPDATE users SET password="{newPassword}" WHERE username="{username}" AND password="{password}"'
            mycursor.execute(sql)
            mydb.commit()
        return {"message": "Success"}
    except Exception as e:
        return {"message": str(e)}


# kullanici kartlari goruntulemek istediginde buradaki endpointi kullanarak kartlari goruntuleme islemlerini tamamlar.
# kullanicinin kulanacagi kart bilgileri kullaniciya json olarak gonderilir.
@app.get("/get-cards")
async def resetPassword():
    try:
        mycursor = mydb.cursor()
        sql = f'SELECT * FROM cards'
        mycursor.execute(sql)
        data = mycursor.fetchall()
        mydb.commit()
        newData = {}
        for i in data:
            newData[i[0]] = {"id":i[0], "cardName": i[1], "point": i[2]}
        print(f'newData: {newData}')
        return {"message": "Success", "data": newData}
    except Exception as e:
        return {"message": str(e)}

# @app.get("/add-card")
# async def addCard():

#     cards = {

#         "Albus Dumbledore":"20",
#         "Rubeus Hagrid":"12",
#         "Minerva McGonagall":"13",
#         "Arthur Weasley":"10",
#         "Sirius Black":"18",
#         "Lily Potter":"12",
#         "Remus Lupin":"10",
#         "Peter Pettigrew":"5",
#         "Harry Potter":"10",
#         "Ron Weasley":"8",
#         "Hermione Granger":"10",

#         "Rowena Ravenclaw":"20",
#         "Luna Lovegood":"9",
#         "Gilderoy Lockhart":"13",
#         "Filius Flitwick":"10",
#         "Cho Chang":"11",
#         "Sybill Trelawney":"14",
#         "Marcus Belby":"10",
#         "Myrtle Warren":"5",
#         "Padma Patil":"10",
#         "Quirinus Quirrell":"15",
#         "Garrick Ollivander":"15",

#         "Tom Riddle":"20",
#         "Horace Slughorn":"12",
#         "Bellatrix Lestrange":"13",
#         "Narcissa Malfoy":"10",
#         "Andromeda Tonks":"16",
#         "Lucius Malfoy":"12",
#         "Evan Rosier":"10",
#         "Draco Malfoy":"5",
#         "Dolores Umbridge":"10",
#         "Severus Snape":"18",
#         "Leta Lestrange":"10",

#         "Helga Hufflepuff":"20",
#         "Cedric Diggory":"18",
#         "Nymphadora Tonks":"14",
#         "Pomona Sprout":"10",
#         "Newt Scamander":"18",
#         "Fat Friar":"12",
#         "Hannah Abbott":"10",
#         "Ernest Macmillan":"5",
#         "Leanne" :"10",
#         "Silvanus Kettleburn":"12",
#         "Ted Lupin":"10"
#     }


#     try:

#         for card in list(cards.keys()):
#             sql = "INSERT INTO cards (cardName, point) VALUES (%s, %s)"
#             val = (card, cards[card])
#             mycursor.execute(sql, val)
#             mydb.commit()
#         return {"message": "Success"}
#     except Exception as e:
#         return {"message": str(e)}


