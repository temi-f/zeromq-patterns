import zmq
import time
import logging
import sys
import threading
from src.zeromq_server import ZeroMQServer

class RouterDealerServer(ZeroMQServer):
    """ In a ZeroMQ client-server architecture, a single server
        communicates with multiple clients. The ROUTER socket is
        capable of handling multiple connections and can send messages
        to specific DEALER sockets based on their unique identities.
        It allows bidirectional communication between the server (ROUTER)
        and multiple clients (DEALERs) without strict request-reply sequencing.
        The ROUTER socket is typically paired with one or more DEALER
        sockets on the client side.

        IMPLEMENTATION: Server (a.k.a. Router) creates a ZeroMQ ROUTER
        socket and binds it to a specific address. It then listens for
        incoming connections from multiple clients.
        Each client connection is identified by a unique identity.
    """

    def __init__(self, host_ip:str, port:int) -> None:
        super().__init__(zmq.ROUTER, host_ip, port)

    def create_server(self):
        # Bind socket to host and port
        endpoint = f"{self.host}:{self.port}"
        self.socket.bind(endpoint)

    def interact_with_client(self):
        print("starting server thread")
        self.create_server()
        while True:
            # Wait for messages from clients
            identity, message = self.socket.recv_multipart()
            try:
                # Attempt to decode message as UTF-8
                decoded_message = message.decode('utf-8')
                decoded_identity = identity.decode('utf-8')
            except UnicodeDecodeError:
                # Handle the case where decoding fails (e.g., binary data)
                decoded_message = f"<Binary data: {message}>"
                decoded_identity = f"<Binary data: {identity}>"

            print(f"Received message from Client '{decoded_identity}': {decoded_message}")

            # Send message back to the client
            response = f"Echo: {decoded_message}"
            self.socket.send_multipart([identity, response.encode()])
            time.sleep(1)

if __name__ == "__main__":
    host_ip = sys.argv[1]
    port = sys.argv[2]
    print(f"IP: {host_ip}, Port: {port}")

    if(host_ip and port):
        server = RouterDealerServer(host_ip, port)
        server_thread = threading.Thread(target=server.interact_with_client)
        server_thread.start()
    else:
        print("Please supply both the Host IP and Port Number as command line argument")
        