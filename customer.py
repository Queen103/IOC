import pymysql as db
import credentials as cr
from telegram import Update, Bot
from telegram.ext import ContextTypes 
import note as nt
bot = Bot(nt.TOKEN) 
#Lấy id bản thân /getid
async def get_id(update:Update,context:ContextTypes.DEFAULT_TYPE) -> None:
    try: 
        id = update.message.chat.id
        out = f"Mã ID của bạn là: {id}"
        await update.message.reply_text(out)
    except:
        await update.message.reply_text("Kiểm tra lại cú pháp")

#gửi yêu cầu đăng ký đến admin cú pháp /join
async def send_register(update: Update,context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        id = update.message.chat.id
        out = f"Có yêu cầu đăng ký từ người dùng {id}"
        connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
        curs = connection.cursor()
        sql1 = "INSERT INTO `securitysystem`.`registerrequest` (`userid`) VALUES (%s);"
        sql2 = "select idadmin from `securitysystem`.`admin`"
        print(id)
        curs.execute(sql1,id)
        curs.execute(sql2)
        admins = curs.fetchall()
        print(admins)
        for admin in admins:
            print(admin)
            await bot.sendMessage(chat_id=admin[0],text = out)
        await update.message.reply_text("Đã gửi yêu cầu vui lòng đợi")
    except:
        await update.message.reply_text(nt.CHECKSYNTAX)
    finally:
        connection.commit()
        connection.close()

# gửi yêu cầu ghé thăm đến user /visit - số điện thoại
async def visit(update: Update,context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
        curs = connection.cursor()
        data = update.message
        cusid = data.chat.id
        text = data.text.split("-")
        phonenumber = text[1].strip()
        sql1 = "select `userid` from `securitysystem`.`user` where `phonenumber` = %s"
        sql2 = "INSERT INTO `securitysystem`.`visit` (`userid`, `cusid`) VALUES (%s, %s);"
        curs.execute(sql1,phonenumber)
        userid = curs.fetchone()
        userid = int(userid[0])
        if(userid):
            value = (userid,cusid)
            curs.execute(sql2,value)
            text = f"Bạn đang có {cusid} đến thăm\nSử dụng lệnh /open - id để mở cửa"
            await bot.sendMessage(chat_id=userid,text=text)
            await update.message.reply_text("Đã gửi yêu cầu")
        else:
            await update.message.reply_text("Kiểm tra lại người bạn đến thăm")
    except:
        await update.message.reply_text(nt.CHECKSYNTAX)
    finally:
        connection.commit()
        connection.close()
    