from telegram import Update
from telegram.ext import ContextTypes 
import note as nt
import pymysql as db
import credentials as cr

async def start(update:Update,context: ContextTypes.DEFAULT_TYPE) -> None:
    data = update.message.from_user
    print("start from "+str(data.id))
    await update.message.reply_text(nt.HELLO)

async def help(update:Update,context: ContextTypes.DEFAULT_TYPE) -> None:
    data = update.message.from_user
    print("Help from "+str(data.id))
    connection = db.connect(host=cr.host, user=cr.username, password=cr.password, database=cr.database)
    curs = connection.cursor()
    sql1 = "select * from `securitysystem`.`admin` where `idadmin` = %s"
    sql2 = "select * from `securitysystem`.`user` where `userid` = %s"
    if (curs.execute(sql1,data.id)):
        await update.message.reply_text(nt.HELPADMIN)
    elif (curs.execute(sql2,data.id)):
        await update.message.reply_text(nt.HELPUSER)
    else:
        await update.message.reply_text(nt.HELP)