"""TCP Server implementation using socket and blocking I/O"""

import logging
import socket

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def start_tcp_server(host: str, port: int) -> None:
    """Create and start a TCP server.

    This server implementation only accept one client connection at a time.
    For multiple clients, you need to create a new process or thread for each client.
    """
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    server_address = (host, port)
    sock.bind(server_address)
    logger.info("Starting TCP Server on %s port %s", *server_address)

    # Listen for incoming connections with a maximum backlog connections
    sock.listen(5)

    while True:
        # Wait for a connection
        logger.info("TCP Server: Waiting for a connection...")
        connection, client_address = sock.accept()

        try:
            logger.info("Connection from %s", client_address)

            # Receive the data in small chunks and retransmit it
            while True:
                # Receive data from the connection
                data = connection.recv(1024)
                if data:
                    logger.info("Received: %r", data)
                    logger.info("Sending data back to the client")

                    # Send data back
                    connection.sendall(data)
                else:
                    logger.info("No more data from %s", client_address)
                    break
        except Exception as e:
            logger.exception("Exception: %s", e)
        finally:
            # 6. Close the connection
            logger.info("Closing current connection")
            connection.close()


if __name__ == "__main__":
    start_tcp_server("0.0.0.0", 8888)
