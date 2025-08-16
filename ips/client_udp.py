"""Client for UDP server.

Implementation using socket and blocking I/O
"""

import logging
import socket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main(host: str, port: int) -> None:
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Optional: connect to fix default remote address (allows send/recv)
            s.connect((host, port))
            local_ip, local_port = s.getsockname()[:2]
            logger.info(
                "[CLIENT-UDP] Ready on %s:%s -> %s:%s. Type text, 'quit' to exit.",
                local_ip,
                local_port,
                host,
                port,
            )
            while True:
                try:
                    line = input("> ")
                except (EOFError, KeyboardInterrupt):
                    break

                data = (line + "\n").encode()
                try:
                    s.send(data)
                    # Receive echo from server
                    buf = s.recv(4096)
                except KeyboardInterrupt:
                    break
                except OSError as e:
                    logger.error("[CLIENT-UDP] Socket error: %s", e)
                    break

                if not buf:
                    logger.info("[CLIENT-UDP] No response (server may be unreachable)")
                    continue

                msg = buf.decode(errors="replace").rstrip()
                logger.info("(%s:%s): %s", local_ip, local_port, msg)

                if line.strip().lower() in ("quit", "exit"):
                    break
    finally:
        logger.info("[CLIENT-UDP] Bye")


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8888
    main(host, port)
