import socket

def start_client(host='127.0.0.1', port=9090):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        print(f"[*] Подключено к серверу {host}:{port}")
        while True:
            message = input("Введите сообщение (или 'exit' для выхода): ")
            if message.lower() == 'exit':
                break
            client.sendall(message.encode())
            response = client.recv(1024)
            print(f"[Сервер]: {response.decode()}")
    except ConnectionRefusedError:
        print("[!] Невозможно подключиться к серверу")
    finally:
        client.close()
        print("[*] Клиент завершил работу")

if __name__ == "__main__":
    start_client()