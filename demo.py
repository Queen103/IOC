import telegram
from telegram import InputFile
import note as nt
# import tracemalloc

# tracemalloc.start()
async def demo():
    

    # Thay thế 'YOUR_BOT_TOKEN' bằng API Token của bot của bạn
    bot_token = nt.TOKEN

    # Thay thế 'USER_CHAT_ID' bằng chat ID của người dùng bạn muốn gửi ảnh
    user_chat_id = '6400965471'

    # Tạo một đối tượng bot
    bot = telegram.Bot(token=bot_token)

    # Đường dẫn tới tệp ảnh trên máy tính
    image_path = 'visitdata/6400965471.20231108155514.jpg'

    # Sử dụng InputFile để gửi tệp ảnh
    photo = InputFile(image_path)

    # Gửi ảnh đến người dùng
    await bot.send_message(user_chat_id,"hihi")
    await bot.send_photo(chat_id=user_chat_id, photo=photo)

demo()
