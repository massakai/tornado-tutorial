# tornado-tutorial

## Docker

```bash
# ビルド
$ docker image build -t tornado-tutorial .

# 起動
$ docker run -p 8888:8888 --name tornado-tutorial -d tornado-tutorial

# 確認
$ curl localhost:8888/urls
```
