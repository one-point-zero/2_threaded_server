import socket
import threading

def handle_client(client_socket, address):
    print(f"[+] Подключен клиент {address}")
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"[{address}] Получено: {data.decode()}")
            client_socket.sendall(data)
        except ConnectionResetError:
            break
    print(f"[-] Клиент {address} отключился")
    client_socket.close()

def start_server(host='127.0.0.1', port=9090):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"[*] Сервер запущен на {host}:{port}")
    try:
        while True:
            client_socket, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.start()
            print(f"[=] Активных подключений: {threading.active_count() - 1}")
    except KeyboardInterrupt:
        print("\n[!] Сервер остановлен") # Сервер остановится только при нажатии CTRL+C
    finally:
        server.close()

if __name__ == "__main__":
    start_server()