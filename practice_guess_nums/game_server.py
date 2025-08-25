"""Guessing game server."""

import asyncio
import logging
import random

logger = logging.getLogger(__name__)


class Game:
    """Encapsulates the logic and state of the guessing game."""

    def __init__(self):
        self.secret_number = random.randint(1, 100)
        self._game_over_event = asyncio.Event()
        logger.info("New game started. The secret number is %d", self.secret_number)

    def guess(self, number: int) -> str:
        """Check a guess and return the result."""
        if number < self.secret_number:
            return "Too low"
        if number > self.secret_number:
            return "Too high"
        return "Correct"

    def is_over(self) -> bool:
        """Check if the game is over."""
        return self._game_over_event.is_set()

    def set_over(self) -> None:
        """Signal that the game is over."""
        self._game_over_event.set()

    async def wait_for_game_over(self) -> None:
        """Wait until the game is over."""
        await self._game_over_event.wait()


class ClientHandler:
    """Handles a single client connection for the guessing game."""

    def __init__(
        self, game: Game, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        self.game = game
        self.reader = reader
        self.writer = writer
        self.peer: tuple[str, int] = writer.get_extra_info("peername")

    async def start(self) -> None:
        """The main loop for handling a client."""
        logger.info("[CLIENT] Connected: %s", self.peer)
        self.writer.write(
            b"Welcome to the Guessing Game!\nGuess a number between 1 and 100\n"
        )
        await self.writer.drain()

        is_winner = False
        try:
            while not self.game.is_over():
                try:
                    data = await asyncio.wait_for(self.reader.readline(), timeout=1.0)
                except asyncio.TimeoutError:
                    continue

                if not data:
                    logger.info("[CLIENT] Disconnected: %s", self.peer)
                    break

                try:
                    guess = int(data.decode().strip())
                except ValueError:
                    self.writer.write(b"Invalid input. Please send a number.\n")
                    await self.writer.drain()
                    continue

                result = self.game.guess(guess)

                if result == "Correct":
                    logger.info("Player %s guessed the number correctly!", self.peer)
                    self.writer.write(b"You win!\n")
                    self.game.set_over()
                    is_winner = True
                    break

                logger.info("Player %s guessed %s", self.peer, result.lower())
                self.writer.write(f"{result}\n".encode())
                await self.writer.drain()

            if self.game.is_over() and not is_winner:
                logger.info("Game over. Notifying non-winner %s", self.peer)
                self.writer.write(b"Game over! Another player won.\n")
                await self.writer.drain()

        except asyncio.CancelledError:
            logger.debug("[CLIENT] Task cancelled for %s", self.peer)
        except Exception as exc:
            logger.exception("[CLIENT] Error with %s: %s", self.peer, exc)
        finally:
            self.writer.close()
            await self.writer.wait_closed()
            logger.debug("[CLIENT] Connection closed for %s", self.peer)


class GameServer:
    """Manages the game server lifecycle and client connections."""

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.game = Game()

    async def _handle_connection(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        """Callback for new client connections."""
        handler = ClientHandler(self.game, reader, writer)
        await handler.start()

    async def start(self):
        """Start the game server."""
        logger.info("Starting Guessing Game server on %s:%s", self.host, self.port)
        server = await asyncio.start_server(
            self._handle_connection,
            self.host,
            self.port,
        )

        async with server:
            await self.game.wait_for_game_over()

        logger.info("Game over. Server is shutting down.")


def main():
    """Main function to run the server."""
    logging.basicConfig(level=logging.INFO)
    server = GameServer("0.0.0.0", 49235)
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\nServer shut down by user.")


if __name__ == "__main__":
    main()
