# 部署

## Docker

```bash
docker build -t agentdesk .
docker run -p 8500:8500 agentdesk
```

## docker-compose

```bash
docker-compose up -d
```

## Kubernetes / Helm

```bash
helm install agentdesk ./helm/agentdesk
# 或
kubectl apply -f k8s/
```

## 监控

`monitoring/` 提供 Prometheus 抓取配置、Grafana 仪表盘与告警规则。
