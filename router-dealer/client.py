import zmq
import time
import logging
import sys
import threading

# Logger configuration
logging.basicConfig(
     level=logging.DEBUG,
     format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s :\n %(message)s',
     datefmt='%Y-%m-%d %H:%M:%S'
)

class RouterDealerClient():
    """ In a ZeroMQ client-server architecture, a single server
        communicates with multiple clients.

        A client creates a ZeroMQ DEALER socket and connects it
        to a specified ROUTER.
        The DEALER socket sends messages to the server.
        Clients can also receive messages from the server,
        but they don't need to specify the recipient since messages
        are routed automatically by the server.
    """

    def __init__(self, host_ip, port) -> None:
        self.host = f"tcp://{host_ip}"
        self.port = port
        self.socket = self.initialise_socket()

    def initialise_socket(self):
        # Initialise a zeromq context
        self.zcontext = zmq.Context()
        socket = self.zcontext.socket(zmq.DEALER)
        socket.setsockopt(zmq.LINGER, 0)
        return socket

    def create_client(self):
        # Bind socket to host and port
        endpoint = f"{self.host}:{self.port}"
        self.socket.connect(endpoint)  # Connect to server

    def interact_with_server(self):
        print("interacting with server")
        self.create_client()
        # Send messages to the server
        for i in range(5):
            message = f"Message from {i} client"
            self.socket.send(message.encode())
            print(f"Sent message to server: {message}")

            # Wait for and decode response from the server
            response = self.socket.recv().decode()
            print(f"Received response from server: {response}")
        self.destroy()

    def destroy(self):
        self.zcontext.destroy()
        self.socket.close()

if __name__ == "__main__":
    host_ip = sys.argv[1]
    port = sys.argv[2]
    print(f"IP: {host_ip}, Port: {port}")

    if(host_ip and port):
        client = RouterDealerClient(host_ip, port)
        client_thread = threading.Thread(target=client.interact_with_server)
        client_thread.start()
    else:
        print("Please supply both the Host IP and Port Number as command line argument")
        