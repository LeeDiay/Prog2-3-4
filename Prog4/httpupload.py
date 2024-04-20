import socket, html, argparse  # Import các module cần thiết

# Tạo một đối tượng ArgumentParser để xử lý các đối số dòng lệnh
parser = argparse.ArgumentParser()
parser.add_argument("--url")  # Thêm đối số --url để chứa URL của trang web
parser.add_argument("--user")  # Thêm đối số --user để chứa tên người dùng
parser.add_argument("--password")  # Thêm đối số --password để chứa mật khẩu
parser.add_argument("--localfile")  # Thêm đối số --localfile để chứa đường dẫn tệp cục bộ
args = parser.parse_args()  # Phân tích các đối số dòng lệnh

# Tạo một socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Gán các giá trị từ đối số dòng lệnh vào các biến
url = args.url
user = args.user
password = args.password
filepath = args.localfile

# Tạo dữ liệu yêu cầu POST để đăng nhập
request_body = "log=" + user + "&pwd=" + password + "&wp-submit=Log+In"

# Khởi tạo biến get_url để chứa phần đầu URL (http:// hoặc https://)
get_url = ""
i = 8  # Khởi tạo i để xác định vị trí bắt đầu của phần đầu URL
if url[0:7] == "http://":  # Kiểm tra xem URL có bắt đầu bằng http:// không
    i = 7  # Nếu có, cập nhật i thành 7
get_url += url[i:(len(url)-1)]  # Lấy phần đầu URL bằng cách cắt chuỗi

# Kết nối đến máy chủ web thông qua socket
s.connect((get_url, 80))

# Tạo yêu cầu POST để đăng nhập và gửi nó đến máy chủ
request = "POST /wp-login.php HTTP/1.1\r\nHost: " + get_url + "\r\n"
request += "Content-Length: " + str(len(request_body)) + "\r\n"
request += "Content-Type: application/x-www-form-urlencoded\r\n"
request += "\r\n" + request_body
s.send(request.encode())

# Nhận và đọc phản hồi từ máy chủ
response = s.recv(2048)
s.close()

# Chuyển đổi phản hồi từ dạng byte sang chuỗi UTF-8
response = response.decode("utf8")

# Kiểm tra xem đăng nhập có thành công hay không
if "HTTP/1.1 302 Found" not in response and "login_error" in response:
    print("Upload failed")
    exit(0)

# Lấy cookie từ phản hồi
cookie = ""
for i in response.split("\r\n"):
    if "Set-Cookie:" in i:
        cookie += " " + i.split(" ")[1]

# Tạo yêu cầu GET để tải trang media mới và gửi nó đến máy chủ
request_cookie = "GET /wp-admin/media-new.php HTTP/1.1\r\nHost: " + get_url + "\r\n" + "Cookie:" + cookie + "\r\n\r\n"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((get_url, 80))
s.send(request_cookie.encode())

# Nhận phản hồi và đọc nó từ máy chủ
response_cookie =  b''
while True:
    respons = s.recv(2048)
    if not respons:
        break
    response_cookie += respons
s.close()

# Chuyển đổi phản hồi từ dạng byte sang chuỗi UTF-8
response_cookie = response_cookie.decode("utf8")

# Tìm nonce trong phản hồi để sử dụng cho việc tải tệp
response_cookie_index = response_cookie.find("\"_wpnonce\":\"")
res = response_cookie[response_cookie_index+ 12:response_cookie_index + 22]

# Lấy tên tệp, loại tệp và nội dung tệp
filename = filepath.split("/")[-1]
filetype = filename.split(".")[-1]
file_img = open(filepath, 'rb').read()   

# Tạo yêu cầu POST để tải tệp và gửi nó đến máy chủ
request_file = "------WebKitFormBoundary"+"\r\n" + \
    "Content-Disposition: form-data; name=\"name\"" + "\r\n\r\n"+filename+"\r\n"+"------WebKitFormBoundary"+"\r\n" + \
    "Content-Disposition: form-data; name=\"action\"" + "\r\n\r\n" + "upload-attachment"+"\r\n" + "------WebKitFormBoundary" + "\r\n" + \
    "Content-Disposition: form-data; name=\"_wpnonce\""+"\r\n\r\n"+res+"\r\n"+"------WebKitFormBoundary" + "\r\n" + \
    "Content-Disposition: form-data; name=\"async-upload\"; filename=\"" + filename + "\""+"\r\n" + \
    "Content-Type: image/"+filetype+"\r\n\r\n"
request_file = request_file.encode() + file_img + b"\r\n" + b"------WebKitFormBoundary--\r\n"
request = "POST /wp-admin/async-upload.php HTTP/1.1\r\n"+"Host: " + get_url + "\r\n" 
request += 'Cookie:' + cookie + '\r\n'
request += "Content-Length: " + str(len(request_file)) + "\r\n"
request += "Content-Type: multipart/form-data; boundary=----WebKitFormBoundary\r\n"
request += 'Connection: close\r\n'
request = request.encode() + request_file   
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((get_url, 80))
s.send(request)

# Nhận phản hồi và đọc nó từ máy chủ
response_upfile =  b''
while True:
    respon = s.recv(2048)
    if not respon:
        break
    response_upfile += respon
s.close()

# Chuyển đổi phản hồi từ dạng byte sang chuỗi
response_upfile = response_upfile.decode()

# Kiểm tra xem tệp đã được tải thành công hay không
if "HTTP/1.1 200 OK" in response_upfile:
    print("Upload success\r\nFile upload url: ")
    response_upfile_start = response_upfile.find("\"url\":\"") 
    url_upload = ""
    for j in range(response_upfile_start + 7, len(response_upfile)):
        if(response_upfile[j] == "\""):
            break
        url_upload += response_upfile[j]
        url_upload.replace("\\", "")
    print(url_upload)
else:
    print("Upload failed")
    exit(0)
