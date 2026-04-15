# 围棋 AI 大作业

## 项目结构

```
hw1/
├── docs/                  # 【文档】作业说明
│   └── homework.pdf       # 作业要求 PDF
│
├── dlgo/                  # 【已提供】围棋规则基础设施
│   ├── __init__.py        # 模块导出
│   ├── gotypes.py         # Player, Point 等基础类型
│   ├── goboard.py         # Board, GameState, Move 核心逻辑
│   ├── scoring.py         # 计分系统
│   └── zobrist.py         # Zobrist 哈希表
│
├── agents/                # 【学生实现】智能体算法
│   ├── __init__.py
│   ├── random_agent.py    # 第一小问：随机 AI
│   ├── mcts_agent.py      # 第二小问：MCTS AI
│   └── minimax_agent.py   # 第三小问：Minimax AI（选做）
│
├── report/                # 报告pdf及其md源文件
│   └── report.md		   # 报告源文件
│
├── example/                       # 对弈示例
│   ├── readme.md		 		   # 相关说明 后缀带1的是未进行优化的MCTS算法
│   ├── human_vs_mcts1.mp4		   # 人对蒙特卡洛搜索
│   ├── random_vs_mcts1.mp4		   # 随机对蒙特卡洛搜索
│   ├── mcts_vs_minimax1.mp4	   # 蒙特卡洛搜索对minimax搜索
│   ├── mcts_vs_mcts1.mp4		   # 蒙特卡洛搜索对蒙特卡洛搜索
│   ├── human_vs_random.mp4		   # 人对随机
│   ├── human_vs_mcts.mp4		   # 人对蒙特卡洛搜索
│   ├── human_vs_minimax.mp4	   # 人对minimax搜索
│   ├── random_vs_random.mp4	   # 随机对随机
│   ├── random_vs_mcts.mp4		   # 随机对蒙特卡洛搜索
│   ├── random_vs_minimax.mp4	   # 随机对minimax搜索
│   ├── mcts_vs_minimax.mp4		   # 蒙特卡洛搜索对minimax搜索
│   ├── mcts_vs_mcts.mp4		   # 蒙特卡洛搜索对蒙特卡洛搜索
│   └── minimax_vs_minimax.mp4     # minimax搜索对minimax搜索
│
├── gui_tk.py			   # 图形化界面程序
├── play.py                # 命令行对弈脚本
└── README.md              # 本文件
```

---
