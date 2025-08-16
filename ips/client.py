"""Client for asyncio server"""

import socket


def main(host: str, port: int):
    try:
        with socket.create_connection((host, port)) as s:
            print(f"[CLIENT] Connected to {host}:{port}. Type text, 'quit' to exit.")
            local_ip, local_port = s.getsockname()[:2]
            while True:
                try:
                    line = input("> ")
                except (EOFError, KeyboardInterrupt):
                    break
                s.sendall((line + "\n").encode())
                data = s.recv(4096)
                if not data:
                    print("[CLIENT] Server closed connection")
                    break
                msg = data.decode().rstrip()
                print(f"({local_ip}:{local_port}): {msg}")
                if line.strip().lower() in ("quit", "exit"):
                    break
    except KeyboardInterrupt:
        pass
    finally:
        print("[CLIENT] Bye")


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8888
    main(host, port)
