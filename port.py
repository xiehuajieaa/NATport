import socket

def start_server(port, host=None):
    """
    启动一个支持 IPv4 和 IPv6 的服务器。
    
    :param port: 要监听的端口号
    :param host: 绑定的地址，默认为 None，表示监听所有接口 (IPv4 和 IPv6)
    """
    try:
        # 创建支持 IPv6 的 socket
        server_socket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # 绑定到指定的主机和端口
        server_socket.bind((host if host else "::", port))
        server_socket.listen(5)

        print(f"Server is running on port {port} ({'IPv6' if ':' in (host or '') else 'IPv4'})")
        print("Waiting for connections...")

        while True:
            # 接收连接
            client_socket, client_address = server_socket.accept()
            print(f"Connection received from {client_address}")

            # 接收和响应数据
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                print(f"Received: {data}")
                client_socket.sendall("Hello, Client!".encode('utf-8'))
            
            client_socket.close()

    except Exception as e:
        print(f"Error: {e}")

    finally:
        server_socket.close()

if __name__ == "__main__":
    # 设置端口号
    port = 52011
    # 设置主机，默认为监听所有接口 (IPv4 和 IPv6)
    host = None  # "::" 表示 IPv6，"0.0.0.0" 表示 IPv4

    start_server(port, host)
