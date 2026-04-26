# Stage 7 阶段记录：API 与数据约定

## 已确认事实

- API 风格为 `REST`
- 数据格式为 `JSON`
- 鉴权方式为 `JWT + 匿名 session`
- 时间格式为 `ISO 8601`
- 正式卡片有稳定 `id`
- 会话草稿与正式卡片分离建模
- 标签以受控枚举为主，辅以少量自由标签

## API 分组

- `auth`
- `search`
- `grammar`
- `creation`
- `practice`
- `user`

## 创建流程接口顺序

1. 前端先调用检索接口
2. 用户确认需要创建后，再调用 AI 生成接口
3. 创建流程内可调用追加提问接口调整结构化数据
4. 创建完成后，调用完成创建/入库接口

## 数据建模约定

- 正式卡片与会话草稿不混用
- 标签采用结构化字段为主
- 正式卡片保留标准化写法与标准化读音字段
- 检索结果至少返回 `best_match`、`similar_cards`、`search_confidence`、`should_offer_ai_generation`

## 检索相关字段建议

- `title_raw`
- `title_normalized`
- `title_reading_kana`
- `aliases`
- `aliases_reading_kana`

## 假设

- 首版接口版本前缀沿用现有草案，例如 `/api/v1`
- JSON 响应会包含足够的状态字段用于前端区分推荐复用、继续创建与失败态

## 风险

- 匿名 session 与登录态并存时，状态合并和迁移逻辑容易出错
- 标签若过早自由化，会削弱检索排序与聚合能力
- 注音统一质量会直接影响搜索体验

## 缺失信息

- 错误码规范
- 分页与排序响应格式
- JWT 生命周期与刷新策略
