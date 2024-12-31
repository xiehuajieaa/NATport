import socket
import threading

# 配置
IPV6_HOST = "::"  # IPv6地址
IPV6_PORT = 52011  # 要监听的IPv6端口

IPV4_HOST = "10.10.1.22"  # 转发到的IPv4地址
IPV4_PORT = 2302  # 转发到的IPv4端口

# TCP 转发
def tcp_forward():
    with socket.socket(socket.AF_INET6, socket.SOCK_STREAM) as ipv6_server:
        ipv6_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ipv6_server.bind((IPV6_HOST, IPV6_PORT))
        ipv6_server.listen(5)
        print(f"TCP: Listening on [{IPV6_HOST}]:{IPV6_PORT}")

        while True:
            client_socket, client_address = ipv6_server.accept()
            print(f"TCP: Connection from {client_address}")

            threading.Thread(
                target=handle_tcp_connection, args=(client_socket,)
            ).start()

def handle_tcp_connection(client_socket):
    with client_socket, socket.socket(socket.AF_INET, socket.SOCK_STREAM) as ipv4_socket:
        ipv4_socket.connect((IPV4_HOST, IPV4_PORT))
        print(f"TCP: Forwarding to {IPV4_HOST}:{IPV4_PORT}")

        threading.Thread(target=forward_data, args=(client_socket, ipv4_socket)).start()
        forward_data(ipv4_socket, client_socket)

def forward_data(src_socket, dest_socket):
    try:
        while True:
            data = src_socket.recv(4096)
            if not data:
                break
            dest_socket.sendall(data)
    except Exception as e:
        print(f"Forwarding error: {e}")

# UDP 转发
def udp_forward():
    with socket.socket(socket.AF_INET6, socket.SOCK_DGRAM) as ipv6_socket, \
         socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as ipv4_socket:
        ipv6_socket.bind((IPV6_HOST, IPV6_PORT))
        print(f"UDP: Listening on [{IPV6_HOST}]:{IPV6_PORT}")

        while True:
            data, client_address = ipv6_socket.recvfrom(4096)
            print(f"UDP: Received data from {client_address}")
            ipv4_socket.sendto(data, (IPV4_HOST, IPV4_PORT))

            # Optionally send a response back
            response, server_address = ipv4_socket.recvfrom(4096)
            ipv6_socket.sendto(response, client_address)

# 主线程启动
if __name__ == "__main__":
    threading.Thread(target=tcp_forward, daemon=True).start()
    threading.Thread(target=udp_forward, daemon=True).start()

    print("IPv6 to IPv4 forwarding service running...")
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("Shutting down...")
