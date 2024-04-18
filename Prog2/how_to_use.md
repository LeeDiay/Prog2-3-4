# HOW TO RUN CODE IN LINUX

## Đối với "myid.cpp"
- Cài đặt g++ trên linux: `sudo apt install g++`
- Tải file về, hoặc copy code và tạo file mới: `nano myid.cpp`
- Cấp quyền thực thi cho file: `sudo chmod +x myid.cpp`
- Biên dịch file: `sudo g++ -o myid myid.cpp`
- Cuối cùng là run file: `./myid`

## Đối với "mypasswd.cpp"
- Cài đặt g++ trên linux: `sudo apt install g++`
- Tải file về, hoặc copy code và tạo file mới: `nano mypasswd.cpp`
- Cấp quyền thực thi cho file: `sudo chmod +x mypasswd.cpp`
- Biên dịch file: `sudo g++ -o mypassword mypasswd.cpp -lcrypt`
- Cuối cùng là run file: `sudo ./mypassword`