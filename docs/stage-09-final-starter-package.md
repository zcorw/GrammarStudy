# Stage 9 阶段记录：最终 Starter Package

## 已确认选型

- 前端框架：`Vite + React + TypeScript`
- 单仓工具：`pnpm workspace`
- 后端数据层：`SQLAlchemy + Alembic`
- 管理员审核首版方式：先数据库手工改状态
- AI 接入首版策略：先接单一供应商，接口层保留薄抽象

## Starter Package 交付内容

- 根目录单仓脚本、`.env.example`、`docker-compose.yml`
- `apps/web`：Vite 前端骨架、页面路由、基础样式、Mock 数据
- `apps/api`：FastAPI 应用、分层模块、SQLAlchemy 基线、Alembic 初始迁移、PostgreSQL 文法仓储
- `ui-static`：已确认的 HTML 原型镜像版本

## 目录结构

```text
apps/
  api/
    app/
      api/routes/
      core/
      models/
      services/
    alembic/
    tests/
  web/
    src/
docs/
ui-static/
```

## 当前实现边界

- 前端已把首页、搜索、详情、练习、创建、登录、我的文法等页面转成 React 页面骨架
- 后端已按 `auth/search/grammar/creation/practice/user` 模块组织
- 数据库模型与首个迁移目前覆盖正式卡片、练习题、用户账号的 starter 级结构
- `recommended/search/detail` 已通过 PostgreSQL 仓储读取
- 应用启动时会在空库下自动写入最小 demo 文法数据
- 邀请码与审核规则先通过接口响应和数据模型预留，不在首版内建完整后台

## 后续建议顺序

1. 把 `ui-static` 的交互细节继续映射进 `apps/web`
2. 补第一版 Alembic 初始迁移
3. 用真实 PostgreSQL 查询替换 sample data
4. 接入真实 AI 供应商和结构化输出校验
5. 增加鉴权、中间件、审核流程与端到端测试
