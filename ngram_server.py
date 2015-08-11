from SimpleXMLRPCServer import SimpleXMLRPCServer
from utils import get_working_model
from predictor import Predictor

server = SimpleXMLRPCServer(("localhost", 9999), allow_none=True)
server.register_introspection_functions()
server.register_instance(Predictor(*get_working_model(7)))
server.serve_forever()
