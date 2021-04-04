import json
from datetime import timedelta

import tornado.ioloop
import tornado.web
from prometheus_client.metrics import Histogram
from prometheus_client.registry import REGISTRY
from prometheus_client.exposition import choose_encoder

from tutorial.metrics import SummaryWithQuantile

# bucketに含まれるリクエスト数がカウントされる(percentileは取得できない)
LATENCY_SUMMARY = SummaryWithQuantile(
    name='request_latency_seconds', documentation='Tornado latency', labelnames=('method', 'path'),
    quantiles=(0.99, 0.999), period=timedelta(minutes=1))

histogram = Histogram(name='http_server_requests_seconds',
                      documentation='Latency',
                      labelnames=('method', 'uri', 'status'))


class MetricsHandler(tornado.web.RequestHandler):
    def get(self):
        encoder, content_type = choose_encoder(
            self.request.headers.get('Accept'))
        self.set_header('Content-Type', content_type)
        self.write(encoder(REGISTRY))


class UrlsHandler(tornado.web.RequestHandler):

    @LATENCY_SUMMARY.labels('GET', '/urls').time()
    def get(self):
        js = json.dumps([
            {
                'name': 'Tornado Tutorial API',
                'url': 'https://raw.githubusercontent.com/massakai/tornado-tutorial/master/openapi.yaml',
            }
        ])
        self.set_header('Content-Type', 'application/json')
        self.write(js + '\n')


class TestHandler(tornado.web.RequestHandler):
    def get(self) -> None:
        self.write('OK')

    def on_finish(self) -> None:
        histogram.labels(
            method=self.request.method,
            uri=self.request.path,
            status=int(self.get_status())
        ).observe(self.request.request_time())


def main():
    app = tornado.web.Application([
        (r'/test', TestHandler),
        (r'/metrics', MetricsHandler),
    ])
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
