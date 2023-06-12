import paramiko

# Thiết lập thông tin kết nối SSH tới máy B
hostname = '0.tcp.ap.ngrok.io'
port = 10928
username = 'tkien'
password = '2608'

# Số lần chạy GAMA headless
num_runs = 3

# Tạo đối tượng SSHClient
client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Thiết lập chính sách xác thực
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # Kết nối tới máy B
    client.connect(hostname=hostname, port=port, username=username, password=password)

    # Đường dẫn tới tệp cần gửi từ máy A
    localpath = "predatorPrey.gaml"

    # Đường dẫn đến thư mục trên máy B để lưu tệp
    remotepath = "/home/tkien/Downloads/opt/gama-platform/headless/samples/predatorPrey/predatorPrey.gaml"

    # Sử dụng kết nối SFTP
    sftp = client.open_sftp()

    # Gửi tệp từ máy A sang máy B
    sftp.put(localpath, remotepath, confirm=False)

    # Thực thi lệnh chạy tạo file xml từ gaml
    gama_command_initial = 'cd /home/tkien/Downloads/opt/gama-platform/headless/ && bash ./gama-headless.sh -xml prey_predator ./samples/predatorPrey/predatorPrey.gaml ./samples/predatorPrey.xml'
    stdin, stdout, stderr = client.exec_command(gama_command_initial)

    # Xử lý lỗi nếu có
    error_initial = stderr.read().decode()
    if error_initial:
        print("Lỗi khi tạo file xml:")
        print(error_initial)

    # Sửa xml : Số ảnh cần chụp trong 1 lần mô phỏng
    final_value = 200
    xml_cmd = f"cd /home/tkien/Downloads/opt/gama-platform/headless/samples/ && sed -i 's/\\(finalStep=\"\\)[^\"]*\"/\\1{final_value}\"/' predatorPrey.xml"

    # Thực thi lệnh xml
    stdin, stdout, stderr = client.exec_command(xml_cmd)

    # Đóng kết nối SFTP
    sftp.close()

    # Thực thi lệnh chạy tạo file output
    output_command = 'mkdir /home/tkien/Downloads/opt/gama-platform/headless/output'
    stdin, stdout, stderr = client.exec_command(output_command)

    # Thực thi lệnh chạy GAMA headless nhiều lần
    for i in range(num_runs):
        output_folder = f"output-folder-{i + 1}"

        # Lệnh thay đổi thư mục làm việc và chạy GAMA headless
        gama_command = f'cd /home/tkien/Downloads/opt/gama-platform/headless/ && bash ./gama-headless.sh ./samples/predatorPrey.xml ./output/{output_folder}'

        # Thực thi lệnh chạy GAMA headless
        stdin, stdout, stderr = client.exec_command(gama_command)

        # Đọc và in kết quả từ GAMA
        output = stdout.read().decode()
        print(f"Kết quả chạy lần thứ {i + 1}:")
        print(output)

        # Xử lý lỗi nếu có
        error = stderr.read().decode()
        if error:
            print(f"Lỗi khi chạy lần thứ {i + 1}:")
            print(error)

        #Sửa xml
        seed_value = float(i + 5.0)
        xml_cmd = f"cd /home/tkien/Downloads/opt/gama-platform/headless/samples/ && sed -i 's/\\(seed=\"\\)[^\"]*\"/\\1{seed_value}\"/' predatorPrey.xml"

        # Thực thi lệnh xml
        stdin, stdout, stderr = client.exec_command(xml_cmd)
        output = stdout.read().decode()
        error = stderr.read().decode()
        print(output)
        print(error)


    # Lệnh nén
    tar_command = 'tar -czvf output2.tar.gz --directory=/home/tkien/Downloads/opt/gama-platform/headless output'

    # Thực thi lệnh nén
    stdin, stdout, stderr = client.exec_command(tar_command)

    # Đường dẫn tới tệp cần gửi từ máy A
    localpath = "output2.tar.gz"

    # Đường dẫn đến thư mục trên máy B để lưu tệp
    remotepath = "/home/tkien/output2.tar.gz"

    # Sử dụng kết nối SFTP
    sftp = client.open_sftp()

    # Gửi tệp từ máy B sang máy A
    sftp.get(remotepath, localpath)

    # Đóng kết nối SFTP
    sftp.close()

finally:
    # Đóng kết nối SSH trên máy B
    client.close()

