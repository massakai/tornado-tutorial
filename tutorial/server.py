import json

import tornado.ioloop
import tornado.web
from prometheus_client import start_http_server, Histogram

# bucketに含まれるリクエスト数がカウントされる(percentileは取得できない)
LATENCY_HISTOGRAM = Histogram(name='request_latency_seconds', documentation='Description of histogram',
                              labelnames=('method', 'path'))


class UrlsHandler(tornado.web.RequestHandler):

    @LATENCY_HISTOGRAM.labels('GET', '/urls').rate()
    def get(self):
        js = json.dumps([
            {
                "name": "Tornado Tutorial API",
                "url": "https://raw.githubusercontent.com/massakai/tornado-tutorial/master/openapi.yaml",
            }
        ])
        self.set_header("Content-Type", "application/json")
        self.write(js + "\n")


def make_app():
    return tornado.web.Application([
        (r"/urls", UrlsHandler),
    ])


def main():
    # prometheus
    start_http_server(8000)

    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
