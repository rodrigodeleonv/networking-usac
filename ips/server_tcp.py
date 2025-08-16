"""TCP Server implementation using asyncio"""

import asyncio
import logging
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handler_client(
    reader: asyncio.StreamReader, writer: asyncio.StreamWriter
) -> None:
    """Echo back any data received from a single client connection.

    Responsibilities:
    - Read line-oriented input from the client.
    - Echo back exactly what was received.
    - Handle graceful shutdown and logging per connection.
    """
    peer: Any = writer.get_extra_info("peername")
    logger.info("[CLIENT] Connected: %s", peer)
    try:
        while True:
            data = await reader.readline()
            if not data:
                # Client closed the write side
                logger.info("[CLIENT] Disconnected: %s", peer)
                break

            client_host, client_port = (
                (peer[0], peer[1]) if isinstance(peer, tuple) else (str(peer), "?")
            )

            msg = data.decode(errors="replace").rstrip("\r\n")
            logger.info("(%s:%s): %s", client_host, client_port, msg)

            # Echo back
            writer.write(data)
            await writer.drain()
    except asyncio.CancelledError:
        # Task cancelled during server shutdown
        logger.debug("[CLIENT] Cancelled: %s", peer)
        raise
    except Exception as exc:
        logger.exception("[CLIENT] Error with %s: %s", peer, exc)
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        finally:
            logger.debug("[CLIENT] Writer closed: %s", peer)


async def run_server(host: str, port: int) -> None:
    """Main function"""
    logger.info("Starting TCP server on %s:%s", host, port)

    # Create TCP server async
    server: asyncio.AbstractServer = await asyncio.start_server(
        handler_client, host, port=port
    )
    logger.info("Server started")
    logger.info("accept client connections forever")

    try:
        await server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server shutdown: signal received")
    finally:
        server.close()
        await server.wait_closed()
        logger.info("Server stopped")


if __name__ == "__main__":
    server: str = "0.0.0.0"
    port: int = 8888
    try:
        asyncio.run(run_server(server, port))
    except KeyboardInterrupt:
        # Suppress traceback on Ctrl+C during shutdown
        logger.info("exit")
