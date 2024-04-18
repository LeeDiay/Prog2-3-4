#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <pwd.h>
#include <grp.h>

int main() {
    char username[100];
    printf("Nhap username: ");
    fgets(username, sizeof(username), stdin);
    username[strcspn(username, "\n")] = 0; // Xóa ký tự xuống dòng từ fgets

    struct passwd *pwd;
    pwd = getpwnam(username); // Lấy thông tin người dùng từ /etc/passwd

    if (pwd == NULL) {
        printf("Khong tim thay User.\n");
        return 1;
    }
    
    printf("------------------\n");
    printf("Thong tin nguoi dung\n");
    printf("------------------\n");
    printf("ID: %d\n", pwd->pw_uid);
    printf("Username: %s\n", pwd->pw_name);
    printf("Thu muc home: %s\n", pwd->pw_dir);

    // Lấy danh sách các nhóm của người dùng
    struct group *grp;
    printf("Nhom: ");
    while ((grp = getgrent()) != NULL) {
        char **member;
        for (member = grp->gr_mem; *member != NULL; member++) {
            if (strcmp(*member, username) == 0) {
                printf("%s ", grp->gr_name);
            }
        }
    }
    printf("\n");

    endgrent(); // Kết thúc việc đọc file /etc/group
    return 0;
}

