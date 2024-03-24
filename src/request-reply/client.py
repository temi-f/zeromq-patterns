import zmq
import time
import sys
import threading
from src.zeromq_client import ZeroMQClient

class RequestReplyClient(ZeroMQClient):
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

    def __init__(self, host_ip:str, port:int) -> None:
        super().__init__(zmq.REQ, host_ip, port)

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


if __name__ == "__main__":
    host_ip = sys.argv[1]
    port = sys.argv[2]
    print(f"IP: {host_ip}, Port: {port}")

    if(host_ip and port):
        client = RequestReplyClient(host_ip, port)
        client_thread = threading.Thread(target=client.interact_with_server)
        client_thread.start()
    else:
        print("Please supply both the Host IP and Port Number as command line argument")
