import requests

while True:
    # Gọi API hoặc kiểm tra trạng thái của API
    response = requests.get('http://127.0.0.1:5000/check_loop')
    
    if response.status_code == 200 and response.json().get('should_stop'):
        break  # Dừng vòng lặp nếu API trả về trạng thái 'should_stop' là True
    else:
        # Thực hiện công việc khác khi API không yêu cầu dừng
        print("Tiếp tục thực hiện công việc")

print("Vòng lặp đã dừng bằng yêu cầu của API")