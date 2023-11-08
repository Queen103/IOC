import pymysql as db
import credentials as cr
from telegram import Update, Bot
from telegram.ext import ContextTypes 
import note as nt

bot = Bot(nt.TOKEN)

#check admin 
def check_admin(id):
    try:
        connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
        curs = connection.cursor()
        data = id
        sql = "select * from `securitysystem`.`admin` where `idadmin` = %s"
        if curs.execute(sql,data):
            return True
        else:
            return False
    except:
        print("Lỗi check admin")
    finally:
        connection.close()

#cf customer to register /cf - customerid 
async def cf_register(update:Update,context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
        curs = connection.cursor()
        data = update.message
        id = data.chat.id
        text = data.text.split("-")
        userid = text[1].strip()
        sql1 = "select * from `securitysystem`.`registerrequest` where `userid` = %s"
        sql2 = "UPDATE `securitysystem`.`registerrequest` SET `adminid` = %s, `cf` = '1' WHERE (`userid` = %s)"
        if check_admin(id):
            data2 = (id,userid)
            if curs.execute(sql1,userid):
                curs.execute(sql2,data2)
                await update.message.reply_text(nt.SUCCESSCF)
                print("ok2")
                await bot.sendMessage(chat_id = userid,text = nt.REGISTER)
            else:
                await update.message.reply_text(text = nt.NOTEXITUSER)
    except:
        await update.message.reply_text(nt.CHECKSYNTAX)
    finally:
        connection.commit()
        connection.close()

#đăng ký admin
async def adminregis(update:Update,context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
        crus = connection.cursor()
        data = update.message
        sql = "INSERT INTO `securitysystem`.`admin` (`idadmin`,`username`) VALUES (%s,%s)"
        value = (data.chat.id,data.from_user.username)
        crus.execute(sql,value)
    except:
        await update.message.reply_text(nt.CHECKSYNTAX)
    finally:
        connection.commit()
        connection.close()

    
#block user /block - id
async def block(update:Update,context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
        crus = connection.cursor()
        data = update.message
        id = data.chat.id
        text = data.text.split("-")
        userid = text[1].strip()
        sql = "UPDATE `securitysystem`.`user` SET `active` = '1' WHERE (`userid` = %s);"
        if check_admin(id):
            crus.execute(sql,userid)
            await update.message.reply_text(f"Đã Block người dùng {userid}")
    except:
        await update.message.reply_text(nt.CHECKSYNTAX)
    finally:
        connection.commit()
        connection.close()

#unblock user /unblock - id
async def block(update:Update,context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
        crus = connection.cursor()
        data = update.message
        id = data.chat.id
        text = data.text.split("-")
        userid = text[1].strip()
        sql = "UPDATE `securitysystem`.`user` SET `active` = '0' WHERE (`userid` = %s);"
        if check_admin(id):
            crus.execute(sql,userid)
            await update.message.reply_text(f"Đã UnBlock người dùng {userid}")
    except:
        await update.message.reply_text(nt.CHECKSYNTAX)
    finally:
        connection.commit()
        connection.close()
# /history - id 
async def getHistory(update:Update,context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
        crus = connection.cursor()
        data = update.message
        id = data.chat.id
        text = data.text.split("-")
        userid = text[1].strip()
        sql = "SELECT * FROM `securitysystem`.`history` where (`userid` = %s) ORDER BY `hisid` DESC LIMIT 5;"
        if check_admin(id):
            crus.execute(sql,userid)
            historys = crus.fetchall()
            print(historys)
            if historys:
                value = f"Lịch sử ra vào của {userid}: \n"
                count = 1
                for his in historys:
                    value+= f"-{count}.pic: {his[2]}\nDate: {his[3]}\n"
            else:
                value = "Không có lịch sử"
            await update.message.reply_text(value)
    except:
        await update.message.reply_text(nt.CHECKSYNTAX)
    finally:
        connection.commit()
        connection.close()