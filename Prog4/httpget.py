import argparse
import socket
import ssl
import re
import urllib.parse

def send_request(host, port, request):
    # Tạo socket và kết nối đến host và port
    context = ssl.create_default_context()
    with socket.create_connection((host, port)) as sock:
        with context.wrap_socket(sock, server_hostname=host) as ssock:
            # Gửi yêu cầu đến máy chủ
            ssock.sendall(request.encode())
            # Nhận và trả về phản hồi từ máy chủ
            response = b""
            while True:
                data = ssock.recv(1024)
                if not data:
                    break
                response += data
    return response.decode()

def get_request(host, path, params=None):
    # Tạo yêu cầu GET
    if params:
        path += '?' + urllib.parse.urlencode(params)
    request = f"GET {path} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
    return request

def get_title(html_content):
    # Tìm và trích xuất title từ nội dung HTML
    match = re.search(r'<title>(.*?)</title>', html_content, re.IGNORECASE)
    if match:
        return match.group(1)
    else:
        return None

def httpget(url):
    # Phân tích URL để lấy host và path
    parsed_url = urllib.parse.urlparse(url)
    host, path = parsed_url.netloc, parsed_url.path

    # Gửi yêu cầu GET đến trang web
    request = get_request(host, path)
    response = send_request(host, 443, request)

    # Trích xuất và in ra title của trang
    title = get_title(response)
    if title:
        print("Tiêu đề của trang web:", title)
    else:
        print("Không tìm thấy tiêu đề!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HTTP GET request lấy tiêu đề của web.")
    parser.add_argument("--url", help="URL của trang web", required=True)
    args = parser.parse_args()

    httpget(args.url)
