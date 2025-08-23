import socket
import sys


def main(host: str, port: int):
    """Run the simple socket client."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
        except ConnectionRefusedError:
            print("Connection refused. Is the server running?", file=sys.stderr)
            sys.exit(1)

        # The server sends a multi-line welcome message. Read until it's all received.
        welcome_message = s.recv(1024).decode()
        print(f"Server:\n{welcome_message.strip()}\n")

        while True:
            try:
                user_input = input("Enter your guess: ")
                if not user_input:
                    continue

                s.sendall(user_input.encode() + b"\n")

                response = s.recv(1024).decode()
                if not response:
                    print("Server closed the connection.")
                    break

                print(f"Server: {response.strip()}")

                if "You win!" in response or "Someone else won" in response:
                    break

            except (EOFError, KeyboardInterrupt):
                print("\nClosing connection.")
                break

    print("Game over.")


if __name__ == "__main__":
    main("127.0.0.1", 49235)
