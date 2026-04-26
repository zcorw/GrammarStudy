# Grammar Study Starter Package

当前基线：

- 前端：`Vite + React + TypeScript`
- 后端：`FastAPI + SQLAlchemy + Alembic`
- 数据库：`PostgreSQL`
- 单仓：`pnpm workspace`
- 部署：`Docker Compose`

## 目录结构

```text
apps/
  api/     FastAPI API
  web/     Vite React PWA shell
docs/      架构、阶段记录、开发约束、TODO
ui-static/ 已确认 HTML 原型
```

## 已完成

- 推荐、搜索、详情、练习、自由造句点评、我的文法、登录、创建流程的 React 页面骨架
- 前端真实接入推荐、搜索、详情、练习、登录、我的文法、创建流程等 API
- PostgreSQL + Alembic 初始迁移、创建会话迁移、用户进度与鉴权迁移
- 邮箱密码注册、邮箱密码登录、邀请码通过、待审核状态、JWT 签发与校验
- 已接入 OpenAI Responses API，用于结构化文法卡片生成和自由造句点评
- 创建流程真实持久化：`创建 -> 追问 -> 完成入库`
- 收藏、最近浏览、练习记录、我的文法真实入库
- 统一错误响应结构：`error.code / error.message / error.details`
- 前端 `eslint`、后端 `ruff`、统一检查脚本

## 本地开发

环境变量：

```bash
copy .env.example .env
```

安装前端依赖：

```bash
pnpm install
```

安装后端依赖：

```bash
cd apps/api
..\..\.venv\Scripts\python -m pip install -e .[dev]
```

启动前端：

```bash
pnpm dev:web
```

启动后端：

```bash
pnpm dev:api
```

执行数据库迁移：

```bash
cd apps/api
..\..\.venv\Scripts\python -m alembic -c alembic.ini upgrade head
```

统一检查：

```bash
pnpm check
```

AI 配置：

```bash
OPENAI_API_KEY=your-real-openai-api-key
MODEL_PROVIDER=openai
MODEL_NAME=gpt-5-mini
```

说明：

- 后端通过 OpenAI `Responses API` + `Structured Outputs` 生成结构化文法卡片与句子点评
- 测试环境默认强制 `MODEL_PROVIDER=stub`，避免单测依赖真实外部网络
- 当 `MODEL_PROVIDER=openai` 但未设置 `OPENAI_API_KEY` 时，AI 相关接口会返回 `502`

## Docker

启动：

```bash
docker compose up --build
```

停止：

```bash
docker compose down
```

默认端口：

- Web: `http://localhost:8080`
- API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`

## 演示准入

- 演示邀请码：`DEMO-ACCESS`
- 管理员账号来自 `.env` 中的 `ADMIN_EMAIL / ADMIN_PASSWORD`
- 普通用户先注册账号，再用邮箱和密码登录
- 不填邀请码时，账号会进入 `pending_review`
- 受保护接口要求 Bearer Token，创建流程和“我的文法”需要已通过准入
- AI 相关接口需要容器内也能拿到 `OPENAI_API_KEY`

## 当前仍未完成

见 [docs/TODO.md](</d:/Workspace/money/新建文件夹/docs/TODO.md>)。
