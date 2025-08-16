import socket
import threading
import time
from contextlib import closing

HOST = "0.0.0.0"  # Escucha en todas las interfaces
PORT = 8080  # Puerto del servidor


class TCPServer:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.clients = {}  # Diccionario para almacenar clientes conectados
        self.running = False

    def start(self):
        """Inicia el servidor TCP"""
        self.running = True

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # Permite reutilizar la dirección
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

            # Bind y listen
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)

            print(f"[SERVIDOR] Escuchando en {self.host}:{self.port}")

            try:
                while self.running:
                    # Acepta conexiones entrantes
                    client_socket, client_address = server_socket.accept()
                    print(f"[SERVIDOR] Nueva conexión desde {client_address}")

                    # Crea un hilo para manejar cada cliente
                    client_thread = threading.Thread(
                        target=self.handle_client, args=(client_socket, client_address)
                    )
                    client_thread.daemon = True
                    client_thread.start()

            except KeyboardInterrupt:
                print("\n[SERVIDOR] Cerrando servidor...")
                self.stop()

    def handle_client(self, client_socket, client_address):
        """Maneja la comunicación con un cliente específico"""
        client_id = f"{client_address[0]}:{client_address[1]}"
        self.clients[client_id] = {
            "socket": client_socket,
            "address": client_address,
            "connected_at": time.time(),
        }

        try:
            with closing(client_socket):
                while self.running:
                    # Recibe datos del cliente
                    data = client_socket.recv(1024)

                    if not data:
                        break

                    # Decodifica el mensaje
                    message = data.decode("utf-8").strip()
                    print(f"[CLIENTE {client_id}] {message}")

                    # Procesa el mensaje
                    response = self.process_message(message, client_id)

                    # Envía respuesta
                    if response:
                        client_socket.send(response.encode("utf-8"))

        except ConnectionResetError:
            print(f"[SERVIDOR] Cliente {client_id} desconectado abruptamente")
        except Exception as e:
            print(f"[SERVIDOR] Error con cliente {client_id}: {e}")
        finally:
            # Limpia el cliente de la lista
            if client_id in self.clients:
                del self.clients[client_id]
            print(f"[SERVIDOR] Cliente {client_id} desconectado")

    def process_message(self, message, client_id):
        """Procesa mensajes del cliente y genera respuestas"""
        if message.lower() == "ping":
            return "pong\n"
        elif message.lower() == "time":
            return f"Hora del servidor: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        elif message.lower() == "clients":
            return f"Clientes conectados: {len(self.clients)}\n"
        elif message.lower() == "help":
            return (
                "Comandos disponibles:\n"
                "- ping: responde con pong\n"
                "- time: muestra la hora del servidor\n"
                "- clients: número de clientes conectados\n"
                "- help: muestra esta ayuda\n"
                "- quit: desconecta del servidor\n"
            )
        elif message.lower() == "quit":
            return "Adiós!\n"
        else:
            return f"Echo: {message}\n"

    def broadcast(self, message):
        """Envía un mensaje a todos los clientes conectados"""
        disconnected_clients = []

        for client_id, client_info in self.clients.items():
            try:
                client_info["socket"].send(message.encode("utf-8"))
            except Exception:
                disconnected_clients.append(client_id)

        # Limpia clientes desconectados
        for client_id in disconnected_clients:
            del self.clients[client_id]

    def stop(self):
        """Detiene el servidor"""
        self.running = False
        print("[SERVIDOR] Servidor detenido")


def main():
    """Función principal"""
    server = TCPServer()

    try:
        server.start()
    except Exception as e:
        print(f"[ERROR] {e}")


if __name__ == "__main__":
    main()
