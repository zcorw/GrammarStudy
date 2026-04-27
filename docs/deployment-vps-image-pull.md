# VPS 部署方案 B：Actions 构建镜像，VPS 拉镜像运行

该方案由 GitHub Actions 构建 `api` 和 `web` Docker 镜像并推送到镜像仓库，VPS 不拉取源码，只拉取镜像并重启服务。

## 适用场景

- 不希望 VPS 保存源码
- 不希望 VPS 承担 Docker build
- 可以使用 GHCR 或 Docker Hub 等镜像仓库
- 希望部署更接近标准生产发布流程

## 生产行为

- 使用 `docker-compose.image.prod.yml`
- PostgreSQL 数据保存在 VPS 的 Docker volume `postgres_data`
- 只有 `nginx` 容器对宿主机 `127.0.0.1:${WEB_PORT:-80}` 开放端口
- `web` 和 `api` 容器不对宿主机开放端口，外部访问统一经过 `nginx`
- API 镜像启动时执行 `alembic upgrade head`
- 生产环境固定 `SEED_DEMO_DATA=false`
- 首次启动只创建 `ADMIN_EMAIL / ADMIN_PASSWORD` 对应的管理员账号
- 不导入演示文法、演示邀请码 `DEMO-ACCESS` 或测试数据

## VPS 首次准备

1. 安装基础依赖：

```bash
sudo apt update
sudo apt install -y ca-certificates curl
```

2. 安装 Docker Engine 和 Docker Compose Plugin。

确认安装：

```bash
docker --version
docker compose version
```

3. 创建部署目录：

```bash
sudo mkdir -p /opt/grammar-study
sudo chown "$USER":"$USER" /opt/grammar-study
cd /opt/grammar-study
```

4. 放置生产 compose 和 Nginx 配置文件。

从仓库复制 `docker-compose.image.prod.yml` 和 `deploy/nginx.prod.conf` 到 VPS：

```bash
nano docker-compose.image.prod.yml
mkdir -p deploy
nano deploy/nginx.prod.conf
```

内容应与仓库中的同名文件保持一致。

当前 GitHub Actions 自动部署时也会把这两个文件复制到 `VPS_DEPLOY_PATH`。

5. 准备 `.env.production`：

```bash
nano .env.production
```

示例：

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
WEB_PORT=80
API_IMAGE=ghcr.io/<owner>/<repo>-api:latest
WEB_IMAGE=ghcr.io/<owner>/<repo>-web:latest
```

`WEB_PORT` 是 VPS 宿主机本地监听端口，会绑定到 `127.0.0.1` 并映射到 `nginx` 容器的 80 端口。公网入口应由宿主机上的 Nginx/Caddy 或其他网关再转发到 `127.0.0.1:${WEB_PORT}`。

6. 登录镜像仓库。

GHCR 示例：

```bash
echo "<github-token>" | docker login ghcr.io -u "<github-username>" --password-stdin
```

token 至少需要读取 package 的权限。

7. 首次手动启动并验证：

```bash
docker compose --env-file .env.production -f docker-compose.image.prod.yml pull
docker compose --env-file .env.production -f docker-compose.image.prod.yml up -d
docker compose --env-file .env.production -f docker-compose.image.prod.yml ps
docker compose --env-file .env.production -f docker-compose.image.prod.yml logs -f api
```

访问：

```text
http://<vps-ip>/
http://<vps-ip>/api/v1/health
```

## GitHub Actions 参考流程

当前 `.github/workflows/deploy-vps.yml` 已按本方案实现。如果需要自行重建，参考如下：

```yaml
name: Deploy VPS Images

on:
  push:
    branches:
      - master
      - main
  workflow_dispatch:

permissions:
  contents: read
  packages: write

jobs:
  check-build-push-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: "22"

      - uses: pnpm/action-setup@v4
        with:
          version: 10.33.1

      - run: pnpm install --frozen-lockfile

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - run: python -m pip install -e "apps/api[dev]"

      - run: |
          pnpm --dir apps/web lint
          pnpm --dir apps/web typecheck
          python -m ruff check apps/api/app apps/api/tests
          MODEL_PROVIDER=stub python -m pytest apps/api/tests -q

      - uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push api image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: apps/api/Dockerfile
          push: true
          tags: |
            ghcr.io/${{ github.repository }}-api:${{ github.sha }}
            ghcr.io/${{ github.repository }}-api:latest

      - name: Build and push web image
        uses: docker/build-push-action@v6
        with:
          context: .
          file: apps/web/Dockerfile
          push: true
          build-args: |
            VITE_API_BASE_URL=/api/v1
          tags: |
            ghcr.io/${{ github.repository }}-web:${{ github.sha }}
            ghcr.io/${{ github.repository }}-web:latest

      - name: Deploy on VPS
        uses: appleboy/ssh-action@v1.2.0
        with:
          host: ${{ secrets.VPS_HOST }}
          username: ${{ secrets.VPS_USER }}
          key: ${{ secrets.VPS_SSH_KEY }}
          port: ${{ secrets.VPS_SSH_PORT || 22 }}
          script_stop: true
          script: |
            mkdir -p "${{ secrets.VPS_DEPLOY_PATH }}"
            cd "${{ secrets.VPS_DEPLOY_PATH }}"
            cat > .env.production <<'EOF'
            ${{ secrets.PRODUCTION_ENV }}
            API_IMAGE=ghcr.io/${{ github.repository }}-api:${{ github.sha }}
            WEB_IMAGE=ghcr.io/${{ github.repository }}-web:${{ github.sha }}
            EOF
            docker compose --env-file .env.production -f docker-compose.image.prod.yml pull
            docker compose --env-file .env.production -f docker-compose.image.prod.yml up -d
            docker image prune -f
```

## GitHub Secrets

```text
VPS_HOST
VPS_USER
VPS_SSH_KEY
VPS_SSH_PORT
VPS_DEPLOY_PATH
PRODUCTION_ENV
GHCR_USERNAME
GHCR_READ_TOKEN
```

`PRODUCTION_ENV` 不需要包含 `API_IMAGE` / `WEB_IMAGE`，workflow 可以在部署时按 commit sha 追加。

`GHCR_USERNAME` / `GHCR_READ_TOKEN` 仅在 GHCR package 是私有时需要。当前 workflow 会在这两个 secret 都存在时，在 VPS 上执行 `docker login ghcr.io`。

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

## 常用运维命令

```bash
cd /opt/grammar-study
docker compose --env-file .env.production -f docker-compose.image.prod.yml ps
docker compose --env-file .env.production -f docker-compose.image.prod.yml logs -f api
docker compose --env-file .env.production -f docker-compose.image.prod.yml logs -f web
docker compose --env-file .env.production -f docker-compose.image.prod.yml pull
docker compose --env-file .env.production -f docker-compose.image.prod.yml up -d
```

不要在生产环境执行会删除 volume 的命令，除非确认要清空数据库。
