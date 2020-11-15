import json

import tornado.ioloop
import tornado.web


class UrlsHandler(tornado.web.RequestHandler):
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
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
