import time
import BaseHTTPServer
from srilm import vocab
from urlparse import urlparse
import linecache
import re
from cgi import escape
from utils import grouper
import os
from predictor import read_table


HOST_NAME = "localhost"
PORT_NUMBER = 4567

vocab = vocab.Vocab()
vocab.read(os.environ["CORPUS_PATH"] + "/vocabulario.txt")


def palabra(w):
    return escape(vocab[w] or vocab[0])


class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def serve_html(self, html):
        self.wfile.write(html)

    def serve_file(self, filename):
        # TODO: serve header accordingly..
        self.wfile.write(open("template" + filename).read())

    def do_GET(self):
        self.do_HEAD()
        request = urlparse(self.path)
        path = request.path
        if path == "/":
            path = "/texto_1"
        if path == "/texto_1":
            self.serve_html(self.generar_codigo(1))
        elif path == "/predicciones":
            if not re.match(r'^\d+,\d+,\d+$', request.query):
                self.wfile.write("epa...")
            else:
                order, textnum, indice_faltante = map(int, request.query.split(","))
                self.serve_html(self.get_predicciones(order, textnum, indice_faltante))
        else:
            self.serve_file(path)

    def get_predicciones(self, order, textnum, indice_faltante):
        linea = linecache.getline("%s/%d-grams/texto_%d.txt" % (os.environ["PREDICTIONS_PATH"], order, textnum), indice_faltante + 1)
        return "<table><tr><td>" + \
            "</td></tr><tr><td>".join((logp+"</td><td>"+palabra(int(ind_palabra)) for logp, ind_palabra in grouper(linea.split(" "), 2))) + "</tr></table>"

    def generar_codigo(self, num_texto):
        assert(num_texto in (1, 2, 3, 4, 5, 7, 8))
        tabla = read_table(num_texto)
        s = """<html>
            <head>
                <title>Texto %d</title>
                <script src="js/jquery-2.1.4.min.js"></script>
                <script src="js/main.js"></script>
                <link rel="stylesheet" type="text/css" href="css/style.css" />
            </head>
            <body onclick="clickOutside();"><div id="content">""" % num_texto
        indice_faltante = 0
        for row in tabla:
            if row['palabras'][0].isupper() and row['CM_catsimple'] != 'n':
                s += "<br>"
            else:
                s += " "
            if row['palabrascompletadas']:
                s += "<u onclick=\"display('%s', this, 7, %d, %d); event.cancelBubble=true;\">%s</u>" % \
                    (row['palabrascompletadas'], num_texto, indice_faltante, row['palabras'])
                indice_faltante += 1
            else:
                s += "<span>%s</span>" % row['palabras']
        s += """
                </div>
                <div id="popup">
                </div>
            </body>
        </html>"""
        return s


if __name__ == '__main__':
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print time.asctime(), "Server Starts - http://%s:%s" % (HOST_NAME, PORT_NUMBER)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
