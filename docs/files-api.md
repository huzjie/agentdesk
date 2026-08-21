# Files API（文件产物）

对标 Anthropic Files API：数字员工产出的成品文件，统一在工作区管理、追踪、打包交付。

## 工作区（Workspace）

- 根目录隔离：`resolve()` 强制路径留在工作区内，杜绝路径逃逸。
- 文本/二进制写入：`write` / `write_bytes`。

## 产物（Artifact）

```python
art = artifacts.create(employee_id, "report.md", mime="text/markdown")
# art.size / art.sha256 / art.created_at 自动填充
```

## 交付（Delivery）

```python
delivery.bundle(["report.md", "data.csv"], "handoff.zip")
```
