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

class RequestReplyClient():
    """ In a ZeroMQ request-reply pattern, a REP(LY) socket
        is created which represents the server. It receives
        requests from clients and sends replies back to those clients.
        Each request from a client must be followed by a reply from
        the server (REP socket), and vice versa.
        The REP socket is typically paired with a zmq.REQ (Request)
        socket on the client side.

        This pattern is used when where synchronous communication
        with strict sequencing and reliability requirements is
        needed e.g. in a RPC style communication.

        IMPLEMENTATION:
        The client sends a request to a server using a zmq.REQ socket
        connected to the server's address.
        The client then waits for the response from the server
        and prints it out.
    """

    def __init__(self, host_ip, port) -> None:
        self.host = f"tcp://{host_ip}"
        self.port = port
        self.socket = self.initialise_socket()

    def initialise_socket(self):
        # Initialise a zeromq context
        self.zcontext = zmq.Context()
        socket = self.zcontext.socket(zmq.REQ)
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
        for i in range(1, 5):
            request = f"{i}: Hello from client"
            print("Sending request: ", request)
            self.socket.send_string(request)

            # Wait for the response from the server
            response = self.socket.recv_string()
            print("Received response:", response)
        self.destroy()

    def destroy(self):
        self.zcontext.destroy()
        self.socket.close()


if __name__ == "__main__":
    host_ip = sys.argv[1]
    port = sys.argv[2]
    print(f"IP: {host_ip}, Port: {port}")

    if(host_ip and port):
        server = RequestReplyClient(host_ip, port)
        server_thread = threading.Thread(target=server.interact_with_server)
        server_thread.start()
    else:
        print("Please supply both the Host IP and Port Number as command line argument")
