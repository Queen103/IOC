import pymysql as db
import credentials as cr
from telegram import Update
from telegram.ext import ContextTypes 
import note as nt
import getdata as gd
import time
import train
import Recognize as rc
import requests
import admin as ad
import sound as sd

#Check người dùng
def check_user(id):
    try:
        connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
        curs = connection.cursor()
        data = id
        sql = "select * from `securitysystem`.`user` where `userid` = %s and `active` = '0'"
        if curs.execute(sql,data):
            return True
        else:
            return False 
    except:
        print("Lỗi check user")
    finally:
        connection.close()
#check allow register 
def check_register(userid):
    try:
        connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
        curs = connection.cursor()
        data = userid
        sql = "select * from `securitysystem`.`registerrequest` where `userid` = %s and `cf` = 1"
        if curs.execute(sql,data):
            return True
        else:
            return False 
    except:
        print("Lỗi check register")
    finally:
        connection.close()
#đăng ký người dùng fomat /dangky - fullname - phone - room 
async def register(update:Update,context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
        curs=connection.cursor()
        data = update.message
        infor = data.text.split("-")
        if check_register(data.chat.id):
            sql = "INSERT INTO `securitysystem`.`user` (`userid`, `fullname`, `username`, `phonenumber`, `room`) VALUES (%s,%s,%s,%s,%s);"
            value = (str(data.chat.id),infor[1].strip(),data.from_user.username,infor[2].strip(),infor[3].strip())
            print(value)
            curs.execute(sql,value)
            sql1 = "DELETE FROM `securitysystem`.`registerrequest` WHERE (`userid` = %s);"
            curs.execute(sql1,data.chat.id)
            await update.message.reply_text("Dưa mặt lại gần camera")
            sql2 = "select id from `securitysystem`.`user` where `userid` = %s"
            curs.execute(sql2,data.chat.id)
            id = curs.fetchone()
            print(id[0])
            sd.playsound(cr.movecame)
            gd.getdataface(id[0])
            train.training()
            await update.message.reply_text("Bạn đã đăng lý thành công")
        else:
            await update.message.reply_text(nt.SP)
    except:
        await update.message.reply_text(nt.CHECKSYNTAX)
    finally:
        connection.commit()
        connection.close()

#load data theo số điện toại lệnh /find - số điện thoại
async def getData(update:Update,context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if ad.check_admin:
            connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            curs=connection.cursor()
            sql = "select * from `securitysystem`.`user` where `phonenumber` = %s"
            valuein = update.message
            value = valuein.text.split("-")
            phone = value[1].strip()
            curs.execute(sql,phone)
            print("ok")
            data = curs.fetchone()
            if data:
                print(data)
            else: 
                return await update.message.reply_text("Người dùng không tồn tại\nVui lòng kiểm tra lại")
            out = f"Thông tin người dùng: \n-ID: {data[1]}\nName: {data[2]}\nUsername: {data[3]} \nPhone: {data[4]} \nRoom: {data[5]}\nActive: {data[6]}\n"
            await update.message.reply_text(out)
        else:
            await update.message.reply_text("Vui lòng kiểm tra lại")
    except:
        await update.message.reply_text(nt.CHECKSYNTAX)
    finally:
        connection.close()

#Lấy thông tin tất cả người dùng /getall 
async def getAllData(update:Update,context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if ad.check_admin:
            connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
            curs=connection.cursor()
            sql = "select * from `securitysystem`.`user`"
            curs.execute(sql)
            datas = curs.fetchall()
            value="Danh sách người dùng: \n"
            for data in datas:
                value += f"-ID: {data[1]}\nName: {data[2]}\nUsername: {data[3]} \nPhone: {data[4]} \nRoom: {data[5]}\nActive: {data[6]}\n"
            await update.message.reply_text(value)
        else:
            await update.message.reply_text("Vui lòng xem lại")
    except:
        await update.message.reply_text(nt.CHECKSYNTAX)
    finally:
        connection.close()

# xác nhận người đến thăm /open - id
async def open(update:Update,context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
        curs = connection.cursor()
        data = update.message
        id = data.chat.id
        if ad.check_admin(id) :
            door()
            await update.message.reply_text("Đã mở cửa")
        text = data.text.split("-")
        cusid = text[1].strip()
        sql = "select id from `securitysystem`.`visit` where `cusid` = %s"
        curs.execute(sql,cusid)
        idvs = curs.fetchall()
        if check_user(id) and idvs:
            save,date = rc.visit(id)
            value = (save,date,cusid)
            print(value)
            sql = "UPDATE `securitysystem`.`visit` SET `pic` =%s, `date` = %s,`open`= 1 where (cusid = %s and `open` = 0);"
            if curs.execute(sql,value):
                print("Done")
                door()
                await update.message.reply_text("Đã mở cửa")
            else:
                await update.message.reply_text("Kiểm tra lại")
    except:
        await update.message.reply_text(nt.CHECKSYNTAX)
    finally:
        connection.commit()
        connection.close()

def door():
    sd.playsound(cr.well)
    data = {"data":"1"}
    url = f"http://{cr.url}/api"
    response = requests.post(url, data=data)
    print(response.text)


        
        