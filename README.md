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
$ curl localhost:8888/prometheus
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 348.0
python_gc_objects_collected_total{generation="1"} 38.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 58.0
python_gc_collections_total{generation="1"} 5.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="9",patchlevel="0",version="3.9.0"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 2.9483008e+07
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 2.5448448e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.60578523369e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 1.68
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 10.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.048576e+06
# HELP request_latency_seconds Tornado latency
# TYPE request_latency_seconds summary
request_latency_seconds_count{method="GET",path="/urls"} 400.0
request_latency_seconds_sum{method="GET",path="/urls"} 0.023884184000081632
request_latency_seconds_sample{method="GET",path="/urls",period="60.0"} 300.0
request_latency_seconds{method="GET",path="/urls",period="60.0",quantile="0.99"} 0.0002545179999628999
request_latency_seconds{method="GET",path="/urls",period="60.0",quantile="0.999"} 0.0005088450000130251
# HELP request_latency_seconds_created Tornado latency
# TYPE request_latency_seconds_created gauge
request_latency_seconds_created{method="GET",path="/urls"} 1.605785234351844e+09
```
