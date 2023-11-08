import pygame
import credentials as cr

def playsound(mp3):
    # Khởi tạo pygame
    pygame.init()
    # Tên tệp MP3 bạn muốn phát
    mp3_file = f"voice/{mp3}"
    # Phát tệp MP3
    pygame.mixer.music.load(mp3_file)
    pygame.mixer.music.play()
    # Dừng để cho âm thanh phát đủ lâu
    pygame.time.delay(3000)
    # Dừng âm thanh
    pygame.mixer.music.stop()
    # Đóng pygame
    pygame.quit()
