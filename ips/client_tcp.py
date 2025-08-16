"""Client for TCP server.

Implementation using socket and blocking I/O
"""

import logging
import socket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(host: str, port: int):
    try:
        with socket.create_connection((host, port)) as s:
            logger.info(
                "[CLIENT] Connected to %s:%s. Type text, 'quit' to exit.", host, port
            )
            local_ip, local_port = s.getsockname()[:2]
            while True:
                try:
                    line = input("> ")
                except (EOFError, KeyboardInterrupt):
                    break
                s.sendall((line + "\n").encode())
                data = s.recv(4096)
                if not data:
                    logger.info("[CLIENT] Server closed connection")
                    break
                msg = data.decode().rstrip()
                logger.info("(%s:%s): %s", local_ip, local_port, msg)
                if line.strip().lower() in ("quit", "exit"):
                    break
    except KeyboardInterrupt:
        pass
    finally:
        logger.info("[CLIENT] Bye")


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8888
    main(host, port)
