import zmq
import logging


class ZeroMQClient:
    def __init__(self, socket_type, host_ip, port):
        self.zmq_context = zmq.Context()
        self.socket = self.zmq_context.socket(socket_type)
        # self.zmq_context.setsockopt(zmq.LINGER, 0)
        self.host = f"tcp://{host_ip}"
        self.port = port


        # Logger configuration
        logging.basicConfig(
            level=logging.DEBUG,
            format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s :\n %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def create_client(self):
        # Bind socket to host and port
        endpoint = f"{self.host}:{self.port}"
        self.socket.connect(endpoint)  # Connect to server

    def destroy(self):
        self.zmq_context.destroy()
        self.socket.close()