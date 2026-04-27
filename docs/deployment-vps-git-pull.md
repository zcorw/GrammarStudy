# VPS 部署方案 A：VPS 拉仓库构建

该方案由 GitHub Actions 负责检查和 SSH 登录，VPS 自己拉取仓库、构建镜像并重启服务。

## 适用场景

- VPS 性能够用，可以承担 Docker build
- 可以在 VPS 上保存源码
- 私有仓库已配置 deploy key 或访问 token
- 不想额外维护镜像仓库

## 生产行为

- 使用 `docker-compose.prod.yml`
- PostgreSQL 数据保存在 VPS 的 Docker volume `postgres_data`
- 只有 `nginx` 容器对宿主机 `127.0.0.1:${WEB_PORT:-80}` 开放端口
- `web` 和 `api` 容器不对宿主机开放端口，外部访问统一经过 `nginx`
- API 容器启动时执行 `alembic upgrade head`
- 生产环境固定 `SEED_DEMO_DATA=false`
- 首次启动只创建 `ADMIN_EMAIL / ADMIN_PASSWORD` 对应的管理员账号
- 不导入演示文法、演示邀请码 `DEMO-ACCESS` 或测试数据

## VPS 首次准备

1. 安装基础依赖：

```bash
sudo apt update
sudo apt install -y git ca-certificates curl
```

2. 安装 Docker Engine 和 Docker Compose Plugin。

确认安装：

```bash
docker --version
docker compose version
```

3. 创建部署目录并拉取仓库：

```bash
sudo mkdir -p /opt/grammar-study
sudo chown "$USER":"$USER" /opt/grammar-study
git clone <your-repository-url> /opt/grammar-study
cd /opt/grammar-study
```

私有仓库需要先在 VPS 配置只读 deploy key，或使用具备权限的 HTTPS token。

4. 准备生产环境变量：

```bash
cp .env.production.example .env.production
nano .env.production
```

必须替换：

```text
POSTGRES_PASSWORD
JWT_SECRET
ADMIN_EMAIL
ADMIN_PASSWORD
OPENAI_API_KEY
```

5. 首次手动启动并验证：

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml up -d --build
docker compose --env-file .env.production -f docker-compose.prod.yml ps
docker compose --env-file .env.production -f docker-compose.prod.yml logs -f api
```

访问：

```text
http://<vps-ip>/
http://<vps-ip>/api/v1/health
```

## GitHub Secrets

```text
VPS_HOST
VPS_USER
VPS_SSH_KEY
VPS_SSH_PORT
VPS_DEPLOY_PATH
PRODUCTION_ENV
```

说明：

- `VPS_DEPLOY_PATH`：仓库目录，例如 `/opt/grammar-study`
- `PRODUCTION_ENV`：完整 `.env.production` 文件内容
- `VPS_SSH_PORT`：可选，未配置时默认 22

`PRODUCTION_ENV` 示例：

```text
POSTGRES_DB=grammar_study
POSTGRES_USER=grammar_study
POSTGRES_PASSWORD=<strong-db-password>
JWT_SECRET=<long-random-secret>
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=<strong-admin-password>
APPROVAL_MODE=invite_or_review
MODEL_PROVIDER=openai
MODEL_NAME=gpt-5-mini
OPENAI_API_KEY=<openai-api-key>
VITE_API_BASE_URL=/api/v1
WEB_PORT=80
```

## VPS_SSH_KEY 生成方式

`VPS_SSH_KEY` 是 GitHub Actions 登录 VPS 使用的 SSH 私钥内容。对应的公钥需要提前放到 VPS 用户的 `~/.ssh/authorized_keys` 中。

在本地生成一组专用于部署的 SSH key：

```bash
ssh-keygen -t ed25519 -C "github-actions-grammar-study" -f ~/.ssh/grammar-study-deploy
```

生成后会得到：

```text
~/.ssh/grammar-study-deploy      私钥，填入 GitHub Secret: VPS_SSH_KEY
~/.ssh/grammar-study-deploy.pub  公钥，添加到 VPS
```

把公钥安装到 VPS。以下示例中的 `<vps-user>` 和 `<vps-host>` 分别对应 `VPS_USER` 和 `VPS_HOST`：

```bash
ssh-copy-id -i ~/.ssh/grammar-study-deploy.pub <vps-user>@<vps-host>
```

如果没有 `ssh-copy-id`，可手动在 VPS 上执行：

```bash
mkdir -p ~/.ssh
chmod 700 ~/.ssh
echo "<grammar-study-deploy.pub 文件内容>" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

GitHub Secret `VPS_SSH_KEY` 应填写私钥完整内容：

```text
-----BEGIN OPENSSH PRIVATE KEY-----
...
-----END OPENSSH PRIVATE KEY-----
```

不要把 `.pub` 公钥内容填到 `VPS_SSH_KEY`。

## 自动部署流程

如需使用本方案，需要将 `.github/workflows/deploy-vps.yml` 改为 SSH 后在 VPS 执行 `git fetch/reset` 和本机 Docker build 的流程：

1. GitHub Actions 拉取代码并执行检查
2. SSH 登录 VPS
3. 在 `VPS_DEPLOY_PATH` 执行 `git fetch`
4. `git reset --hard <commit sha>`
5. 写入 `.env.production`
6. 执行：

```bash
docker compose --env-file .env.production -f docker-compose.prod.yml up -d --build
```

## 常用运维命令

```bash
cd /opt/grammar-study
docker compose --env-file .env.production -f docker-compose.prod.yml ps
docker compose --env-file .env.production -f docker-compose.prod.yml logs -f api
docker compose --env-file .env.production -f docker-compose.prod.yml logs -f web
docker compose --env-file .env.production -f docker-compose.prod.yml down
```

不要在生产环境执行会删除 volume 的命令，除非确认要清空数据库。
