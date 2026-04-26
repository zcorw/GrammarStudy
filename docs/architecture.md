# 架构说明

## 当前协作约定

- 交互语言：中文
- 文档语言：中文
- 代码注释语言：英文
- 汇报风格：详细

> 说明：以下内容为已有架构草案，后续阶段会按最新确认结果持续校准。

## 当前平台基线

- 产品方向：文法卡片检索、AI 辅助创建、练习点评
- 首发平台：`PWA`
- 前端基线：`React + TypeScript`
- 后端基线：`Python + FastAPI`
- 数据库基线：`PostgreSQL`
- 仓库基线：`Monorepo`
- 部署基线：`Docker`
- 当前目标：易维护的上线版

## 目标

站点围绕以下链路设计：

1. 用户浏览热门/推荐文法
2. 用户按文法关键词或句型检索
3. 系统优先复用公共库已有卡片
4. 登录用户可发起创建流程
5. AI 生成结构化卡片、标签与选择题
6. 用户在创建流程内追加提问，调整结构化结果
7. 创建完成后进入公共库

## 模块边界

### 前端 `apps/web`

- `src/view/`：页面、布局、组件
- `src/application/`：前端 usecase 与 ports
- `src/domain/`：文法领域对象与纯业务结构
- `src/infrastructure/`：仓储实现、容器装配
- `src/styles.css`：当前前端样式基线

### 后端 `apps/api`

- `presentation/api/routes/`：路由、协议映射、请求响应模型
- `application/usecases/`：用例编排
- `domain/entities/`：领域对象
- `infrastructure/repositories/`：仓储实现
- `infrastructure/persistence/models/`：SQLAlchemy 模型
- `infrastructure/config/`：配置

## 检索机制

首版建议：

- 标准化写法检索
- 注音统一检索
- `pg_trgm` 模糊匹配
- 标签与结构字段辅助排序
- 用户输入汉字时，同时走注音统一检索路径

搜索结果返回：

- `best_match`
- `similar_cards`
- `search_confidence`
- `should_offer_ai_generation`

## 领域对象

- `GrammarEntry`：公共库中的正式文法卡片
- `CreationSession`：创建流程中的临时会话
- `PracticeQuestion`：选择题
- `SentenceFeedback`：自由造句点评结果
- `UserProgress`：最近浏览、练习记录、收藏

## 关键业务规则

- 游客可查看文法卡片和做选择题
- 游客不能创建文法，也不能自由造句
- 创建流程中的结构化版本历史只保留在客户端本地
- 创建完成后卡片进入公共库
- 创建结束后不允许继续追加提问
- 自由造句点评不反向修改公共卡片
- 登录采用邮箱登录，可选邀请码；无邀请码时进入管理员审核
