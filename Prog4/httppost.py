import socket, html, argparse  # Import các module cần thiết

# Tạo một đối tượng ArgumentParser để xử lý các đối số dòng lệnh
parser = argparse.ArgumentParser()
parser.add_argument("--url")  # Thêm đối số --url để chứa URL của trang web
parser.add_argument("--user")  # Thêm đối số --user để chứa tên người dùng
parser.add_argument("--password")  # Thêm đối số --password để chứa mật khẩu
args = parser.parse_args()  # Phân tích các đối số dòng lệnh

# Tạo một socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Gán các giá trị từ đối số dòng lệnh vào các biến
url = args.url
user = args.user
password = args.password

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

# Tạo yêu cầu POST để đăng nhập
request = "POST /wp-login.php HTTP/1.1\r\nHost: " + get_url + "\r\n"
request += "Content-Length: " + str(len(request_body)) + "\r\n"
request += "Content-Type: application/x-www-form-urlencoded\r\n"
request += "\r\n" + request_body

# Gửi yêu cầu POST đến máy chủ
s.send(request.encode())

# Nhận và đọc phản hồi từ máy chủ
response = s.recv(2048)

# Đóng kết nối
s.close()

# Chuyển đổi phản hồi từ dạng byte sang chuỗi UTF-8
response = response.decode("utf8")

# Kiểm tra xem đăng nhập thành công hay không và in ra thông báo tương ứng
if "HTTP/1.1 302 Found" in response and "login_error" not in response:
	print("User " + user + " đăng nhập thành công")
else:
	print("User " + user + " đăng nhập thất bại")
