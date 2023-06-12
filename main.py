import multiprocessing

def run_file(file_path):
    # Chạy tệp Python được chỉ định bởi file_path
    with open(file_path, encoding='utf-8') as file:
        code = file.read()
    exec(code)

if __name__ == '__main__':
    # Đường dẫn của hai tệp Python cần chạy
    file_paths = ['main1.py', 'main2.py']

    # Tạo danh sách các tiến trình
    processes = []

    # Tạo và bắt đầu tiến trình cho mỗi tệp Python
    for file_path in file_paths:
        process = multiprocessing.Process(target=run_file, args=(file_path,))
        process.start()
        processes.append(process)

    # Chờ cho tất cả các tiến trình hoàn thành
    for process in processes:
        process.join()
