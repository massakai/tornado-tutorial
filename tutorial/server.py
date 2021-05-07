import asyncio
import json
import logging
import random
import signal
from datetime import timedelta

import tornado.ioloop
import tornado.web
from prometheus_client.metrics import Counter, Histogram
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


class LogLevelCountFilter(logging.Filter):
    counter = Counter(
        name='log_events',
        documentation='Number of error level events that made it to the logs',
        labelnames=('level',))

    def filter(self, record: logging.LogRecord) -> bool:
        LogLevelCountFilter.counter.labels(
            level=record.levelname
        ).inc()
        return True


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
        self.set_status(random.choice([200, 400, 500]))

    def on_finish(self) -> None:
        if self.get_status() == 200:
            logging.info(
                f'{self.request.method} {self.request.uri} {self.get_status()}')
        elif self.get_status() == 400:
            logging.warning(
                f'{self.request.method} {self.request.uri} {self.get_status()}')
        elif self.get_status() == 500:
            logging.error(
                f'{self.request.method} {self.request.uri} {self.get_status()}')


async def shutdown():
    # リクエストを受けないようにする

    # すべてのリクエストが完了するまで待つ
    await asyncio.sleep(1)

    # リソースの解放などの終了処理を実行する

    tornado.ioloop.IOLoop.current().stop()


def shutdown_handler(sig, frame):
    tornado.ioloop.IOLoop.instance().add_callback_from_signal(shutdown)


def main():
    signal.signal(signal.SIGTERM, shutdown_handler)
    signal.signal(signal.SIGINT, shutdown_handler)

    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addFilter(LogLevelCountFilter())

    app = tornado.web.Application([
        (r'/test', TestHandler),
        (r'/metrics', MetricsHandler),
    ])
    app.listen(8080)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()
