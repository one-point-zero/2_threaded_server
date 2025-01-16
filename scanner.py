import socket
import threading
from queue import Queue
from tqdm import tqdm # pip install tqdm

# Функция для сканирования одного порта
def scan_port(host, port, open_ports, progress_bar):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)  # Таймаут на соединение
            if s.connect_ex((host, port)) == 0:
                open_ports.append(port)  # Порт открыт
    except Exception:
        pass
    finally:
        progress_bar.update(1)

# Функция для работы потоков
def worker(host, queue, open_ports, progress_bar):
    while not queue.empty():
        port = queue.get()
        scan_port(host, port, open_ports, progress_bar)
        queue.task_done()

# Основная функция
def main():
    # Ввод данных пользователя
    host = input("Введите имя хоста или IP-адрес: ").strip()
    try:
        socket.gethostbyname(host)  # Проверяем, что хост доступен
    except socket.gaierror:
        print("[!] Хост недоступен")
        return

    start_port = 1
    end_port = 65535

    # Очередь для портов
    port_queue = Queue()
    for port in range(start_port, end_port + 1):
        port_queue.put(port)

    open_ports = []
    threads = []
    num_threads = 100  # Количество потоков

    print(f"Сканирование портов на хосте {host}...")
    with tqdm(total=port_queue.qsize(), desc="Прогресс") as progress_bar:
        # Создаем потоки
        for _ in range(num_threads):
            thread = threading.Thread(target=worker, args=(host, port_queue, open_ports, progress_bar))
            threads.append(thread)
            thread.start()

        # Ждем завершения всех потоков
        for thread in threads:
            thread.join()

    # Вывод результатов
    open_ports.sort()
    if open_ports:
        print("\nОткрытые порты:")
        for port in open_ports:
            print(f"Порт {port} открыт")
    else:
        print("\nНет открытых портов")

if __name__ == "__main__":
    main()