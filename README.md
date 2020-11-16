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

## Prometheus

```bash
$ curl localhost:8000/
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 41.0
python_gc_objects_collected_total{generation="1"} 349.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 55.0
python_gc_collections_total{generation="1"} 5.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="9",patchlevel="0",version="3.9.0"} 1.0
# HELP request_latency_seconds Description of histogram
# TYPE request_latency_seconds histogram
request_latency_seconds_bucket{le="0.5"} 400.0
request_latency_seconds_bucket{le="0.99"} 400.0
request_latency_seconds_bucket{le="0.999"} 400.0
request_latency_seconds_bucket{le="+Inf"} 400.0
request_latency_seconds_count 400.0
request_latency_seconds_sum 0.015222323000045002
# HELP request_latency_seconds_created Description of histogram
# TYPE request_latency_seconds_created gauge
request_latency_seconds_created 1.605425430907378e+09
```
