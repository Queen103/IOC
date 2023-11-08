import logging
from telegram import Update
from telegram.ext import Application, CommandHandler
import note as nt
import tele_system as sys
import user 
import customer as cs
import admin as ad

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

TOKEN = nt.TOKEN
def main() -> None:
    print("------ Bot đang hoạt động ------")
    # tạo application với token bot
    app = Application.builder().token(TOKEN).build()

    #Tạo lệnh 
    app.add_handler(CommandHandler("start",sys.start))
    app.add_handler(CommandHandler("help",sys.help))
    app.add_handler(CommandHandler("register",user.register))
    app.add_handler(CommandHandler("getall",user.getAllData))
    app.add_handler(CommandHandler("find",user.getData))
    app.add_handler(CommandHandler("getid",cs.get_id))
    app.add_handler(CommandHandler("join",cs.send_register))
    app.add_handler(CommandHandler("cf",ad.cf_register))
    app.add_handler(CommandHandler("admin",ad.adminregis))
    app.add_handler(CommandHandler("visit",cs.visit))
    app.add_handler(CommandHandler("open",user.open))
    app.add_handler(CommandHandler("block",ad.block))
    app.add_handler(CommandHandler("unblock",ad.block))
    app.add_handler(CommandHandler("history",ad.getHistory))

    #chạy bot 
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__=="__main__":
    main()

