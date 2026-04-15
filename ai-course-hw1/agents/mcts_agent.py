"""
MCTS (蒙特卡洛树搜索) 智能体模板。

学生作业：完成 MCTS 算法的核心实现。
参考：《深度学习与围棋》第 4 章
"""

import math
import random
from dlgo.gotypes import Player, Point
from dlgo.goboard import GameState, Move

__all__ = ["MCTSAgent"]



class MCTSNode:
    """
    MCTS 树节点。


    属性：
        game_state: 当前局面
        parent: 父节点（None 表示根节点）
        children: 子节点列表
        visit_count: 访问次数
        value_sum: 累积价值（胜场数）
        prior: 先验概率（来自策略网络，可选）
    """

    def __init__(self, game_state, parent=None, move=None, prior=1.0):
        self.game_state = game_state
        self.parent = parent
        self.children = []
        self.visit_count = 0
        self.value_sum = 0
        self.prior = prior
        # TODO: 初始化其他必要属性
        self.unvisited_moves = [m for m in game_state.legal_moves() if not m.is_resign]
        self.move = move

    @property
    def value(self):
        """计算平均价值 = value_sum / visit_count，防止除零。"""
        # TODO: 实现价值计算
        if self.visit_count == 0:
            return 0
        return self.value_sum / self.visit_count

    def is_leaf(self):
        """是否为叶节点（未展开）。"""
        return len(self.children) == 0

    def is_terminal(self):
        """是否为终局节点。"""
        return self.game_state.is_over()
    
    def is_fully_expanded(self):
        """所有合法动作是否都已展开。"""
        return len(self.unvisited_moves) == 0

    def best_child(self, c=1.414):
        """
        选择最佳子节点（UCT 算法）。

        UCT = value + c * sqrt(ln(parent_visits) / visits)

        Args:
            c: 探索常数（默认 sqrt(2)）

        Returns:
            最佳子节点
        """
        # TODO: 实现 UCT 选择
        best_score = float('-inf')
        best_node = None
        for child in self.children:
            if child.visit_count == 0:
                # 赋予未访问节点极高的分数，鼓励探索
                score = float('inf') 
            else:
                # 探索
                exploration = c * math.sqrt(math.log(self.visit_count) / child.visit_count)
                # 胜率
                score = child.value + exploration
                
            if score > best_score:
                best_score = score
                best_node = child
                
        return best_node

    def expand(self):
        """
        展开节点：为所有合法棋步创建子节点。

        Returns:
            新创建的子节点（用于后续模拟）
        """
        # TODO: 实现节点展开

        idx = random.randrange(len(self.unvisited_moves))
        move = self.unvisited_moves.pop(idx)
        
        next_state = self.game_state.apply_move(move)
        
        child_node = MCTSNode(next_state, parent=self, move=move)
        self.children.append(child_node)
        return child_node

    def backup(self, value):
        """
        反向传播：更新从当前节点到根节点的统计。

        Args:
            value: 从当前局面模拟得到的结果（1=胜，0=负，0.5=和）
        """
        # TODO: 实现反向传播
        self.visit_count += 1
        self.value_sum += value
        if self.parent is not None:
            self.parent.backup(1.0 - value)


class MCTSAgent:
    """
    MCTS 智能体。

    属性：
        num_rounds: 每次决策的模拟轮数
        temperature: 温度参数（控制探索程度）
    """

    def __init__(self, num_rounds=1000, temperature=1.0):
        self.num_rounds = num_rounds
        self.temperature = temperature

    def select_move(self, game_state: GameState) -> Move:
        """
        为当前局面选择最佳棋步。

        流程：
            1. 创建根节点
            2. 进行 num_rounds 轮模拟：
               a. Selection: 用 UCT 选择路径到叶节点
               b. Expansion: 展开叶节点
               c. Simulation: 随机模拟至终局
               d. Backup: 反向传播结果
            3. 选择访问次数最多的棋步

        Args:
            game_state: 当前游戏状态

        Returns:
            选定的棋步
        """
        # TODO: 实现 MCTS 主循环
        root = MCTSNode(game_state)
        for _ in range(self.num_rounds):
            # Selection
            node = root
            while not node.is_leaf() and not node.is_terminal():
                node = node.best_child(c=self.temperature)

            # Expansion
            if not node.is_terminal():
                node = node.expand()

            # Simulation
            value = self._simulate(node.game_state)

            # Backup
            node.backup(value)

        return self._select_best_move(root)

    def _simulate(self, game_state):
        """
        快速模拟（Rollout）：随机走子至终局。

        【第二小问要求】
        标准 MCTS 使用完全随机走子，但需要实现至少两种优化方法：
        1. 启发式走子策略（如：优先选有气、不自杀、提子的走法）
        2. 限制模拟深度（如：最多走 20-30 步后停止评估）
        3. 其他：快速走子评估（RAVE）、池势启发等

        Args:
            game_state: 起始局面

        Returns:
            从当前玩家视角的结果（1=胜, 0=负, 0.5=和）
        """
        # TODO: 实现快速模拟（含两种优化策略）
        current_state = game_state
        rollout_player = game_state.next_player
        max_depth = 50
        depth = 0

        while not current_state.is_over() and depth < max_depth:
            legal_moves = [m for m in current_state.legal_moves() if not m.is_resign]
            if not legal_moves:
                move = Move.pass_turn()
            else:                # 启发式走子：优先选有气、不自杀、提子的走法
                play_moves = [m for m in legal_moves if m.is_play]
                if play_moves:
                    scored = []
                    for m in play_moves:
                        point = m.point
                        score = 0
                        for nb in point.neighbors():
                            if not current_state.board.is_on_grid(nb):
                                continue
                            s = current_state.board.get_go_string(nb)
                            if s is None:
                                continue
                            if s.color != current_state.next_player:
                                if s.num_liberties == 1:
                                    score += 1000   # 提子优先
                                elif s.num_liberties == 2:
                                    score += 80     # 打吃倾向
                            else:
                                if s.num_liberties == 1:
                                    score += 300    # 救己方打吃
                                else:
                                    score += 10
                            scored.append((score, m))

                    scored.sort(key=lambda x: x[0], reverse=True)

                    # 80% 选最优，20% 在前3里随机，保留探索倾向
                    if random.random() < 0.8:
                        move = scored[0][1]
                    else:
                        top_k = min(3, len(scored))
                        move = random.choice([m for _, m in scored[:top_k]])
                else:
                    move = random.choice(legal_moves)
            current_state = current_state.apply_move(move)
            depth += 1
            
        if current_state.is_over():
            winner = current_state.winner()
            if winner is None:
                return 0.5
            return 1.0 if winner == rollout_player else 0.0

        return 0.5

    def _select_best_move(self, root):
        """
        根据访问次数选择最佳棋步。

        Args:
            root: MCTS 树根节点

        Returns:
            最佳棋步
        """
        # TODO: 根据访问次数或价值选择
        best_move = None
        best_visit_count = -1
        for child in root.children:
            if child.visit_count > best_visit_count:
                best_visit_count = child.visit_count
                best_move = child.move
        if best_move is None:
            return Move.pass_turn()
        return best_move
