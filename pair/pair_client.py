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

class PairPatternClient():
    """ Pair pattern is a socket communication pattern where two sockets
        connect to each other in a bidirectional, peer-to-peer manner.
        One socket acts as the "server" by binding to an endpoint and
        the other acts as the "client" by connect to the bound endpoint
        forming a direct one-to-one (point-to-point) communication between
        the two endpoints.

        Once the connection is established, both sockets can send and receive
        messages to and from each other asynchronously. There is no guarantee of
        message ordering or delivery.
    """

    def __init__(self, host_ip, port) -> None:
        self.host = f"tcp://{host_ip}"
        self.port = port
        self.socket = self.initialise_socket()

    def initialise_socket(self):
        # Initialise a zeromq context
        self.zcontext = zmq.Context()
        socket = self.zcontext.socket(zmq.PAIR)
        socket.setsockopt(zmq.LINGER, 0)
        return socket

    def create_client(self):
        # Bind socket to host and port
        endpoint = f"{self.host}:{self.port}"
        self.socket.connect(endpoint)

    def destroy(self):
        self.zcontext.destroy()
        self.socket.close()

    def interact_with_server(self):
        print("interacting with server")
        self.create_client()
        count = 0
        while count < 10:
            server_message = self.socket.recv()
            print(server_message)
            self.socket.send_string("Message from client")
            self.socket.send_string("Another message from client")
            print("Counter: ", count)
            count += 1
            time.sleep(1)
        self.destroy()

if __name__ == "__main__":
    host_ip = sys.argv[1]
    port = sys.argv[2]
    print(f"IP: {host_ip}, Port: {port}")

    client = PairPatternClient(host_ip, port)
    # client.interact_with_server()
    client_thread = threading.Thread(target=client.interact_with_server)
    client_thread.start()
