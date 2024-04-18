#include <iostream>
#include <fstream>
#include <unistd.h>
#include <shadow.h>
#include <cstring>

using namespace std;

int main() {
    char user[100];
    cout << "Nhap Username muon thay doi: ";
    cin >> user;

    struct spwd *spwd = getspnam(user);
    if (spwd == NULL) {
        cerr << "Khong tim thay nguoi dung!!" << endl;
        return 1;
    }

    char *password = getpass("Nhap mat khau cu: ");
    char *encrypted = crypt(password, spwd->sp_pwdp);

    if (strcmp(encrypted, spwd->sp_pwdp) != 0) {
        cerr << "Mat khau cu khong dung!" << endl;
        return 1;
    }

    password = getpass("Nhap mat khau moi: ");
    encrypted = crypt(password, spwd->sp_pwdp);
    spwd->sp_pwdp = encrypted;

    FILE *file = fopen("/etc/shadow", "r");
    FILE *fileTemp = fopen("/tmp/replace.tmp", "w");

    if (!file || !fileTemp) {
        cerr << "Khong the mo file!" << endl;
        return 1;
    }

    // Đọc từng dòng trong /etc/shadow và cập nhật mật khẩu mới nếu là dòng của người dùng
    char *line = nullptr;
    size_t len = 0;
    while (getline(&line, &len, file) != -1) {
        if (strstr(line, user) != NULL) {
            putspent(spwd, fileTemp); // Ghi thông tin người dùng với mật khẩu mới vào file tạm
        } else {
            fputs(line, fileTemp); // Ghi lại các dòng khác mà không thay đổi
        }
    }

    fclose(file);
    fclose(fileTemp);

    // Sau khi ghi vào file tạm, chúng ta cần thay thế file /etc/shadow bằng file tạm đã ghi
    remove("/etc/shadow");
    rename("/tmp/replace.tmp", "/etc/shadow");

    cout << "Cap nhat mat khau thanh cong!" << endl;

    return 0;
}
