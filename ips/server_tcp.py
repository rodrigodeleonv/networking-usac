"""TCP Server implementation using asyncio

https://superfastpython.com/asyncio-server/
"""

import asyncio
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST = "127.0.0.1"
PORT = 8888


async def handler(reader, writer):
    """Echo back any data received from a single client connection.

    Responsibilities:
    - Read line-oriented input from the client.
    - Echo back exactly what was received.
    - Handle graceful shutdown and logging per connection.
    """
    peer = writer.get_extra_info("peername")
    logger.info(f"[CLIENT] Connected: {peer}")
    try:
        while True:
            data = await reader.readline()
            if not data:
                # Client closed the write side
                logger.info(f"[CLIENT] Disconnected: {peer}")
                break

            client_host, client_port = (
                (peer[0], peer[1]) if isinstance(peer, tuple) else (str(peer), "?")
            )

            msg = data.decode(errors="replace").rstrip("\r\n")
            logger.info(f"({client_host}:{client_port}): {msg}")

            # Echo back
            writer.write(data)
            await writer.drain()
    except asyncio.CancelledError:
        # Task cancelled during server shutdown
        logger.debug(f"[CLIENT] Cancelled: {peer}")
        raise
    except Exception as exc:
        logger.exception(f"[CLIENT] Error with {peer}: {exc}")
    finally:
        try:
            writer.close()
            await writer.wait_closed()
        finally:
            logger.debug(f"[CLIENT] Writer closed: {peer}")


async def main():
    """Main function"""
    logger.info(f"Starting server on {HOST}:{PORT}")
    # Create TCP server async
    server = await asyncio.start_server(handler, HOST, port=PORT)
    logger.info(server)
    # accept client connections forever (kill via control-c)
    try:
        await server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Close signal received")
    finally:
        server.close()
        await server.wait_closed()
        logger.info("[SERVER] Stopped")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        # Suppress traceback on Ctrl+C during shutdown
        print("[SERVER] exit")
