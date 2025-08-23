"""UDP Server implementation using socket and blocking I/O"""

import logging
import socket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start_udp_server(host: str, port: int) -> None:
    """Create and start a UDP server."""
    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    server_address = (host, port)
    sock.bind(server_address)
    logger.info("Starting UDP Server on %s port %s", *server_address)

    while True:
        logger.info("UDP Server: Waiting for message")
        data, address = sock.recvfrom(4096)
        logger.info("Received %s bytes from %s", len(data), address)
        logger.info(data)
        if data:
            sent = sock.sendto(data, address)
            logger.info("Sent %s bytes back to %s", sent, address)


if __name__ == "__main__":
    start_udp_server("0.0.0.0", 8888)
