"""UDP Server implementation using asyncio"""

import asyncio
import logging
from typing import Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EchoUDPProtocol(asyncio.DatagramProtocol):
    """Echo protocol for UDP.

    Keeps a reference to the underlying DatagramTransport and echoes back
    any datagram received.
    """

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        self.transport = transport  # type: asyncio.DatagramTransport

    def datagram_received(self, data: bytes, addr: Tuple[str, int]) -> None:
        message = data.decode(errors="replace")
        logger.info("Message from %s: %s", addr, message)
        # Echoing back the received message
        self.transport.sendto(data, addr)


async def run_server(host: str, port: int) -> None:
    logger.info("Starting UDP server on %s:%s", host, port)
    loop = asyncio.get_running_loop()
    transport, _ = await loop.create_datagram_endpoint(
        lambda: EchoUDPProtocol(), local_addr=(host, port)
    )
    transport = transport  # type: asyncio.DatagramTransport

    try:
        # Run indefinitely until cancelled (Ctrl+C)
        stop = asyncio.Event()
        await stop.wait()
    except asyncio.CancelledError:
        # Graceful shutdown on Ctrl+C (task cancellation)
        logger.info("Server shutdown: signal received")
    finally:
        transport.close()


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 8888
    try:
        asyncio.run(run_server(host, port))
    except KeyboardInterrupt:
        # Suppress traceback on Ctrl+C during shutdown
        logger.info("exit")
