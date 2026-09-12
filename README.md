# 软设备考 · 软件设计师互动学习站

[![Tests](https://github.com/techdou/ruankao-software-designer/actions/workflows/tests.yml/badge.svg)](https://github.com/techdou/ruankao-software-designer/actions/workflows/tests.yml)
[![Deploy Pages](https://github.com/techdou/ruankao-software-designer/actions/workflows/deploy.yml/badge.svg)](https://github.com/techdou/ruankao-software-designer/actions/workflows/deploy.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

面向软考中级「软件设计师」的单机互动学习站：**讲义精读 · 分章刷题 · 真题套卷 · 限时模考 · 案例题专项 · 错题间隔复习**。零后端、零登录，数据全部保存在本机浏览器，支持 JSON 存档跨设备迁移。

**在线使用**：<https://techdou.github.io/ruankao-software-designer/>

## 功能

| 模块 | 说明 |
|---|---|
| 📖 讲义中心 | 14 章考点精讲，按官方考纲知识域组织，含考情分析、例题演算、易错警示、考前速记表；KaTeX 公式渲染 |
| ✎ 刷题练习 | 按章节/作答状态筛选，顺序或随机，选项点击即判分并展示解析 |
| ▤ 真题套卷 | 2020—2022 五套上午卷整卷作答，答题卡导航，交卷统一判分出报告 |
| ⏱ 模拟考试 | 全题库随机抽 75 题，限时 150 分钟，倒计时，模拟机考节奏 |
| 📝 案例题专项 | 下午卷五大固定题型（数据流图/数据库/UML/算法/设计模式），先答后评 |
| ✂ 错题本 | SRS 间隔复习（1/2/4/7/15/30 天，连对 6 轮毕业），答错自动入队 |
| ◔ 统计 | 章节正确率、近 30 天刷题曲线、复习队列分布、薄弱章节提醒 |
| ⛁ 存档 | 进度自动持久化（IndexedDB），一键导出/导入 JSON 迁移 |

## 题库规模

| 类型 | 数量 | 来源 |
|---|---|---|
| 上午真题 | 261 题 | 2020 下—2022 下五套真题程序化提取，解析逐题撰写 |
| 分章练习 | 168 题 | 原创，覆盖高频考点与计算题型 |
| 案例套题 | 5 套 × 4 问 | 原创，按下午卷固定题型 |

## 本地运行

```bash
git clone https://github.com/techdou/ruankao-software-designer.git
cd ruankao-software-designer/app
npm install
npm run dev        # http://localhost:5173
```

生产构建与预览：

```bash
npm run build      # 类型检查 + 构建到 dist/
npm run preview    # http://localhost:4173
```

## 测试

```bash
# 题库结构校验（id 唯一、答案合法、解析齐备）
python scripts/validate_bank.py

# 交互冒烟测试（需先 npm run preview）
python scripts/smoke.py
```

GitHub Actions 每次推送自动执行：题库校验 → 类型检查 → 构建 → Playwright 冒烟测试，全部通过后自动部署 Pages。

## 技术栈

Vue 3 + TypeScript + Pinia + Vue Router (hash) + Vite · marked + KaTeX · IndexedDB · Python (题库 ETL 与测试)

## 内容声明

- 真题题干提取自考后公开的历年试卷；答案与解析为逐题独立撰写，个别依赖原图的图题已标注「原卷含图，建议对照原卷复核」。
- 讲义、解析、自编题均为原创学习内容，仅供个人备考使用，禁止商业转载；详见 [LICENSE](LICENSE)。
- 本项目与任何考试机构无关。

## 致谢

- 练习模式设计参考 [ruankao-architect-practice](https://github.com/Zhang-986/ruankao-architect-practice)
- 真题 PDF 源：[xiaomabenten/software_designer](https://github.com/xiaomabenten/software_designer)
