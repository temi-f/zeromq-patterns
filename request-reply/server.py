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

class RequestReplyServer():
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

        IMPLEMENTATION: The Server listens for incoming requests
        using a zmq.REP socket bound to a specified port.
        When a request is received, the server processes it
        and sends a reply.
        The client sends a request to the server using a zmq.REQ socket
        connected to the server's address.
        The client then waits for the response from the server
        and prints it out.
    """

    def __init__(self, host_ip:str, port:int) -> None:
        self.host = f"tcp://{host_ip}"
        self.port = port
        self.socket = self.initialise_socket()

    def initialise_socket(self):
        # Initialise a zeromq context
        zcontext = zmq.Context()
        socket = zcontext.socket(zmq.REP)
        socket.setsockopt(zmq.LINGER, 0)
        return socket

    def create_server(self):
        # Bind socket to host and port
        endpoint = f"{self.host}:{self.port}"
        self.socket.bind(endpoint)

    def interact_with_client(self):
        self.create_server()
        print("Server started, waiting for requests...")

        while True:
            # Wait for a request from the client
            request = self.socket.recv_string()
            print("Received request:", request)

            # Process the request
            response = "Reply to: " + request

            # Send the response back to the client
            self.socket.send_string(response)


if __name__ == "__main__":
    print("***** REQUEST REPLY Pattern *****")

    host_ip = sys.argv[1]
    port = sys.argv[2]
    print(f"IP: {host_ip}, Port: {port}")

    if(host_ip and port):
        server = RequestReplyServer(host_ip, port)
        server_thread = threading.Thread(target=server.interact_with_client)
        server_thread.start()
    else:
        print("Please supply both the Host IP and Port Number as command line argument")
