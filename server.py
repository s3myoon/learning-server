import socket
import threading

HOST = "127.0.0.1"
PORT = 8000
ROUTES = {
    "/": "Hello",
    "/about": "About page"
}


def make_response(status: str, body: str) -> bytes:
    parts = [
        f"HTTP/1.1 {status}",
        "Content-Type: text/html; charset=utf-8",
        f"Content-Length: {len(body.encode())}",
        "",
        body
    ]

    return "\r\n".join(parts).encode()


def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:
    try:
        with conn:
            data = conn.recv(4096)
            if not data:
                return

            lines = data.decode().split("\r\n")
            try:
                method, path, version = lines[0].split()
            except ValueError:
                response = make_response("400 Bad Request", "Bad Request")
                conn.sendall(response)
                print(f"Client: {addr} 400 Bad Request {lines[0]!r} Thread: {threading.current_thread().name}")
                return

            print(addr, method, path, threading.current_thread().name)

            if path in ROUTES:
                response = make_response("200 OK", ROUTES[path])
            else:
                response = make_response("404 Not Found", "Not Found")
            conn.sendall(response)
    except Exception as err:
        print(f"Client: {addr} {err!r} Thread: {threading.current_thread().name}")


def main() -> None:
    with socket.socket() as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        while True:
            conn, addr = server_socket.accept()
            conn.settimeout(5)
            print(f"Connected: {addr}")
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
