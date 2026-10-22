import socket

HOST = "127.0.0.1"
PORT = 8000

def make_response(status, body):
    parts = [
        f"HTTP/1.1 {status}",
        "Content-Type: text/html; charset=utf-8",
        f"Content-Length: {len(body.encode())}",
        "",
        body
    ]

    return "\r\n".join(parts).encode()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen()

routes = {
    "/": "Hello",
    "/about": "About page"
}

while True:
    conn, addr = s.accept()
    data = conn.recv(4096)
    if data == b'':
        conn.close()
        continue

    lines = data.decode().split('\r\n')
    method, path, version = lines[0].split()

    print(method, path)

    if path in routes:
        response = make_response("200 OK", routes[path])
    else:
        response = make_response("404 Not Found", "Not Found")
    conn.sendall(response)
    conn.close()
s.close()