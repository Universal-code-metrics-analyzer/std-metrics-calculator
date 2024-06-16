# UCMA | Std Proxy Metrics Calculator Plugin

Metrics plugin, which can be used to calculate source code tree metrics with external programs or plugins using `stdin`, `stdout` and `stderr` streams.

**Install**

``` bash
poetry add git+https://github.com/Universal-code-metrics-analyzer/std-proxy-metrics-calculator.git@v0.1.1
```

**Runner configuration**

``` yaml
# config.yml

metrics_calculator:
  plugin: std_proxy_metrics_calculator
  config:
    cmd: "cmd to execute"
    # try to coerce stdout json keys to snake case
    preprocess_keys: True
```
