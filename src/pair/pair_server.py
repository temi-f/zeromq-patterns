import zmq
import time
import sys
import threading
from src.zeromq_server import ZeroMQServer

class PairPatternServer(ZeroMQServer):
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

    def __init__(self, host_ip:str, port:int) -> None:
        super().__init__(zmq.PAIR, host_ip, port)

    def create_server(self):
        # Bind socket to host and port
        endpoint = f"{self.host}:{self.port}"
        self.socket.bind(endpoint)

    def interact_with_client(self):
        self.create_server()
        while True:
            # send message to client
            self.socket.send_string("Message from server")
            # Receive a message from client
            msg = self.socket.recv()
            print(msg)
            time.sleep(1)


if __name__ == "__main__":
    host_ip = sys.argv[1]
    port = sys.argv[2]
    print(f"IP: {host_ip}, Port: {port}")

    if(host_ip and port):
        server = PairPatternServer(host_ip, port)
        server_thread = threading.Thread(target=server.interact_with_client)
        server_thread.start()
    else:
        print("Please supply both the Host IP and Port Number as command line argument")

