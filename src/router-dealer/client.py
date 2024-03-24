import zmq
import sys
import threading
from src.zeromq_client import ZeroMQClient

class RouterDealerClient(ZeroMQClient):
    """ In a ZeroMQ client-server architecture, a single server
        communicates with multiple clients.

        A client creates a ZeroMQ DEALER socket and connects it
        to a specified ROUTER.
        The DEALER socket sends messages to the server.
        Clients can also receive messages from the server,
        but they don't need to specify the recipient since messages
        are routed automatically by the server.
    """
    def __init__(self, host_ip:str, port:int) -> None:
        super().__init__(zmq.DEALER, host_ip, port)

    def create_client(self):
        # Bind socket to host and port
        endpoint = f"{self.host}:{self.port}"
        self.socket.connect(endpoint)  # Connect to server

    def interact_with_server(self):
        print("interacting with server")
        self.create_client()
        # Send messages to the server
        for i in range(1, 6):
            message = f"Message {i} from client"
            self.socket.send(message.encode())
            print(f"Sent message to server: {message}")

            # Wait for and decode response from the server
            response = self.socket.recv().decode()
            print(f"Received response from server: {response}")
        self.destroy()


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
