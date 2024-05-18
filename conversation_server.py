from typing import Iterator

from concurrent.futures import ThreadPoolExecutor
import grpc
from transformers import Pipeline

import conversation_pb2
import conversation_pb2_grpc

from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer

from ai import setup_ai
from ai import run_ai

import threading


class Conversation(conversation_pb2_grpc.ConversationServicer):
    def __init__(self, pipe: Pipeline):
        self.pipe = pipe

    def AnalyzeAudio(
            self,
            request_iterator: Iterator[conversation_pb2.ConversationRequest],
            context: grpc.ServicerContext,
    ) -> Iterator[conversation_pb2.ConversationReply]:
        print("Start bidi streaming")

        for request in request_iterator:
            text = run_ai(self.pipe, request.file)

            yield conversation_pb2.ConversationReply(text=text)

        print("Stop bidi streaming")


class HttpGetHandler(BaseHTTPRequestHandler):
    """Обработчик с реализованным методом do_GET."""

    def do_GET(self):
        self.send_response(200)
        self.end_headers()


def run_health_check_server(server_class=HTTPServer, handler_class=HttpGetHandler):
    server_address = ('', 5001)
    print(f"Start health check handler on address {server_address}")
    httpd = server_class(server_address, handler_class)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()


def serve(address: str) -> None:
    pipe = setup_ai()
    conservation_service = Conversation(pipe)

    server = grpc.server(ThreadPoolExecutor())
    conversation_pb2_grpc.add_ConversationServicer_to_server(conservation_service, server)

    server.add_insecure_port(address)
    server.start()
    print(f"Server serving at {address}")

    health_check_thread = threading.Thread(target=run_health_check_server)
    health_check_thread.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve("[::]:5000")
