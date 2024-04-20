import socket, argparse  # Import các module cần thiết

# Tạo một đối tượng ArgumentParser để xử lý các đối số dòng lệnh
parser = argparse.ArgumentParser()
parser.add_argument("--url")  # Thêm đối số --url để chứa URL của trang web
parser.add_argument("--remotefile")  # Thêm đối số --remotefile để chứa đường dẫn tệp từ xa
args = parser.parse_args()  # Phân tích các đối số dòng lệnh

# Tạo một socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Gán các giá trị từ đối số dòng lệnh vào các biến
url = args.url
filepath = args.remotefile
image_name = filepath.split("/")[-1]

# Khởi tạo biến get_url để chứa phần đầu URL (http:// hoặc https://)
get_url = ""
i = 8  # Khởi tạo i để xác định vị trí bắt đầu của phần đầu URL
if url[0:7] == "http://":  # Kiểm tra xem URL có bắt đầu bằng http:// không
    i = 7  # Nếu có, cập nhật i thành 7
get_url += url[i:(len(url)-1)]  # Lấy phần đầu URL bằng cách cắt chuỗi

# Kết nối đến máy chủ web thông qua socket
s.connect((get_url, 80))

# Tạo yêu cầu GET để tải tệp từ xa và gửi nó đến máy chủ
request = "GET " + filepath + " HTTP/1.1\r\nHost: " + get_url + "\r\n\r\n"
s.send(request.encode())

# Nhận phản hồi và đọc nó từ máy chủ
response =  b''
while True:
    respons = s.recv(2048)
    if not respons:
        break
    response += respons
s.close()

# Chuyển đổi phản hồi từ dạng byte sang chuỗi iso-8859-1
response = response.decode('iso-8859-1')

# Kiểm tra xem tệp đã được tải thành công hay không
if "HTTP/1.1 200 OK" in response:
    # Tính kích thước của tệp ảnh
    image_len = len(response.split('\r\n\r\n')[1].encode('iso-8859-1'))
    print("Kích thước tệp ảnh: " + str(image_len) + " bytes")

    # Lấy loại tệp ảnh
    image_type = response.split("\r\n\r\n")[-1]

    # Ghi tệp ảnh vào ổ đĩa
    image_url =  image_name
    open(image_url, "wb").write(image_type.encode('iso-8859-1'))
else:
    print("Không tồn tại tệp ảnh")
    exit(0)
