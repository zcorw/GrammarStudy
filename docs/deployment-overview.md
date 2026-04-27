# 部署方案总览

当前保留两种 VPS 部署方式。默认自动部署采用方案 B。

## 方案 A：VPS 拉仓库构建

文档：[deployment-vps-git-pull.md](deployment-vps-git-pull.md)

流程：

1. GitHub Actions 执行检查
2. SSH 登录 VPS
3. VPS 拉取仓库指定 commit
4. VPS 执行 Docker build
5. `docker compose up -d --build`

优点：

- 实现简单
- 不需要镜像仓库

代价：

- VPS 需要保存源码
- VPS 需要仓库访问权限
- 构建消耗 VPS CPU/内存/磁盘

## 方案 B：Actions 构建镜像，VPS 拉镜像运行

文档：[deployment-vps-image-pull.md](deployment-vps-image-pull.md)

当前 `.github/workflows/deploy-vps.yml` 已按本方案实现。

流程：

1. GitHub Actions 执行检查
2. GitHub Actions 构建 api/web 镜像
3. 推送镜像到 GHCR 或 Docker Hub
4. SSH 登录 VPS
5. VPS 只拉取镜像并重启服务

优点：

- VPS 不需要保存源码
- VPS 不承担 Docker build
- 更接近标准生产发布流程

代价：

- 需要配置镜像仓库权限
- compose 文件必须使用镜像地址

## 共同生产规则

两种方案都必须满足：

- API 启动执行 Alembic 迁移
- `SEED_DEMO_DATA=false`
- 只有 `nginx` 容器对宿主机 `127.0.0.1` 开放端口，`web` 和 `api` 均只在 Docker 网络内访问
- 首次启动只创建管理员账号
- 不导入演示文法、演示邀请码或测试数据
- 生产密钥只放在 VPS `.env.production` 或 GitHub Secrets 中
