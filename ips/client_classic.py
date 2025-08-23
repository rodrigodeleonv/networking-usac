"""Simple client for UDP and TCP server. Implementation using socket and blocking I/O"""

import logging
import socket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_udp_client(host: str, port: int) -> None:
    """Create a UDP client."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, port)

    try:
        message = "Hello, world UDP"
        logger.info("Sending: %s", message)
        sent = sock.sendto(message.encode(), server_address)
        logger.info("Sent %s bytes back to %s", sent, server_address)
    finally:
        sock.close()


def create_tcp_client(host: str, port: int) -> None:
    """Create a TCP client."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)

    try:
        # Connect the socket to the port where the server is listening
        logger.info("Connecting to %s port %s", *server_address)
        sock.connect(server_address)

        # Send data
        message = "Hello, world TCP"
        logger.info("Sending: %s", message)
        sock.sendall(message.encode())

        # Look for the response
        data = sock.recv(1024)
        logger.info("Received: %r", data)

    finally:
        logger.info("Closing socket")
        sock.close()


if __name__ == "__main__":
    create_udp_client("127.0.0.1", 8888)
    create_tcp_client("127.0.0.1", 8888)
