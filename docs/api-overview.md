# API 草案

## 基础约定

- 风格：REST
- 数据格式：JSON
- 路径前缀：`/api/v1`
- 时间格式：ISO 8601
- 鉴权方式：`JWT + 匿名 session`

## 路由分组

### `GET /api/v1/health`

服务健康检查。

### `GET /api/v1/grammar/recommended`

返回首页推荐文法卡片。

### `GET /api/v1/search/grammar?q=...`

输入文法关键词后返回：

- `best_match`
- `similar_cards`
- `search_confidence`
- `should_offer_ai_generation`

同时支持标准化写法与标准化读音检索。

### `POST /api/v1/auth/login`

邮箱登录入口。可选提交邀请码，由系统判断是直接通过还是进入审核状态。

### `GET /api/v1/user/my-grammar`

返回用户相关文法聚合结果，默认按最近学习/浏览排序，包含创建与收藏内容。

### `POST /api/v1/creation/sessions`

创建会话并触发 AI 结构化生成。

### `POST /api/v1/creation/sessions/{session_id}/follow-up`

仅创建流程内可用，用追加提问调整结构化结果。

### `POST /api/v1/creation/sessions/{session_id}/complete`

创建结束，正式写入公共库。

### `POST /api/v1/practice/choice/submit`

提交选择题结果。

### `POST /api/v1/practice/sentence-feedback`

登录用户提交自由造句并获得 AI 点评。

### `GET /api/v1/user/recent`

返回最近浏览与练习记录。
