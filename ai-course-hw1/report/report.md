<center><h1>项目1 实验报告</h1></center>

### 一、源代码

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
│   ├── report.md		   # 报告源文件
│   └── report.pdf		   # 报告pdf文件
│
├── gui_tk.py			   # 图形化界面程序
├── play.py                # 命令行对弈脚本
└── README.md              # 作业GitHub项目的readme文件
```

---

提交的压缩包中，AI模型处于agent文件夹中，图形化界面运行gui_tk.py即可。

![image-20260415172257692](report.assets/image-20260415172257692.png)

如图所示，可在Black/White后更换执黑棋/白棋的搜索模型/人，使用New Game开启下一局，Pass选项跳过一步棋，Resign选项认输，Undo选项悔棋。棋盘上方显示黑/白方下，并显示相应的执棋者。在棋局结束后，会显示游戏结束与获胜方，Move后显示下子回合数，Captures后显示每方提子数量。在鼠标点击规则不允许的落子处时，会提示如下所示的非法落子提示。

![image-20260415163811533](report.assets/image-20260415163811533.png)