import zmq
import logging

class ZeroMQServer:
    def __init__(self, socket_type, host_ip:str, port:int):
        self.zmq_context = zmq.Context()
        self.socket = self.zmq_context.socket(socket_type)
        self.socket.setsockopt(zmq.LINGER, 0)
        self.host = f"tcp://{host_ip}"
        self.port = port

        # Logger configuration
        logging.basicConfig(
            level=logging.DEBUG,
            format= '[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s :\n %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def create_server(self):
        # Bind socket to host and port
        endpoint = f"{self.host}:{self.port}"
        self.socket.bind(endpoint)

    def close(self):
        self.socket.close()