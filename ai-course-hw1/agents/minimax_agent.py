"""
第三小问（选做）：Minimax 智能体

实现 Minimax + Alpha-Beta 剪枝算法，与 MCTS 对比效果。
可选实现，用于对比不同搜索算法的差异。

参考：《深度学习与围棋》第 3 章
"""
import random
from dlgo.gotypes import Player, Point
from dlgo.goboard import GameState, Move

__all__ = ["MinimaxAgent"]



class MinimaxAgent:
    """
    Minimax 智能体（带 Alpha-Beta 剪枝）。

    属性：
        max_depth: 搜索最大深度
        evaluator: 局面评估函数
    """

    def __init__(self, max_depth=3, evaluator=None):
        self.max_depth = max_depth
        # 默认评估函数（TODO：学生可替换为神经网络）
        self.evaluator = evaluator or self._default_evaluator
        self.root_player = None  # 搜索根节点的玩家

    def select_move(self, game_state: GameState) -> Move:
        """
        为当前局面选择最佳棋步。

        Args:
            game_state: 当前游戏状态

        Returns:
            选定的棋步
        """
        # TODO: 实现 Minimax 搜索，调用 minimax 或 alphabeta
        best_moves = []
        best_score = -float('inf')
        alpha = -float('inf')
        beta = float('inf')

        self.root_player = game_state.next_player

        for move in self._get_ordered_moves(game_state):
            next_state = game_state.apply_move(move)
            
            # 对手回合，所以 maximizing_player=False
            score = self.alphabeta(next_state, self.max_depth - 1, alpha, beta, False)

            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score:
                best_moves.append(move)

            # 更新根节点的 alpha
            alpha = max(alpha, best_score)

        if not best_moves:
            return Move.pass_turn()
            
        return best_moves[0]  # 如果有多个同分的最佳棋步，选择第一个

    def minimax(self, game_state, depth, maximizing_player):
        """
        基础 Minimax 算法。

        Args:
            game_state: 当前局面
            depth: 剩余搜索深度
            maximizing_player: 是否在当前层最大化（True=我方）

        Returns:
            该局面的评估值
        """
        # TODO: 实现 Minimax
        # 提示：
        # 1. 终局或 depth=0 时返回评估值
        if depth == 0 or game_state.is_over():
            return self.evaluator(game_state)
        # 2. 如果是最大化方：取所有子节点最大值
        if maximizing_player:
            max_eval = -float('inf')
            for move in self._get_ordered_moves(game_state):
                next_state = game_state.apply_move(move)
                eval = self.minimax(next_state, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        
        # 3. 如果是最小化方：取所有子节点最小值
        else:
            min_eval = float('inf')
            for move in self._get_ordered_moves(game_state):
                next_state = game_state.apply_move(move)
                eval = self.minimax(next_state, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def alphabeta(self, game_state, depth, alpha, beta, maximizing_player):
        """
        Alpha-Beta 剪枝优化版 Minimax。

        Args:
            game_state: 当前局面
            depth: 剩余搜索深度
            alpha: 当前最大下界
            beta: 当前最小上界
            maximizing_player: 是否在当前层最大化

        Returns:
            该局面的评估值
        """
        # TODO: 实现 Alpha-Beta 剪枝
        # 提示：在 minimax 基础上添加剪枝逻辑
        # - 最大化方：如果 value >= beta 则剪枝
        # - 最小化方：如果 value <= alpha 则剪枝
        if depth == 0 or game_state.is_over():
            return self.evaluator(game_state)
        if maximizing_player:
            max_eval = -float('inf')
            for move in self._get_ordered_moves(game_state):
                next_state = game_state.apply_move(move)
                eval_val = self.alphabeta(next_state, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval_val)
                alpha = max(alpha, eval_val)
                if beta <= alpha:
                    break  # Beta 剪枝
            return max_eval
        else:
            min_eval = float('inf')
            for move in self._get_ordered_moves(game_state):
                next_state = game_state.apply_move(move)
                eval_val = self.alphabeta(next_state, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval_val)
                beta = min(beta, eval_val)
                if beta <= alpha:
                    break  # Alpha 剪枝
            return min_eval

    def _default_evaluator(self, game_state):
        """
        默认局面评估函数（简单版本）。

        学生作业：替换为更复杂的评估函数，如：
            - 气数统计
            - 眼位识别
            - 神经网络评估

        Args:
            game_state: 游戏状态

        Returns:
            评估值（正数对我方有利）
        """
        # TODO: 实现简单的启发式评估
        # 示例：子数差 + 气数差
        # 如果局面已结束，返回极大/极小值
        if game_state.is_over():
            winner = game_state.winner()
            if winner == self.root_player:
                return 100000
            elif winner is None:
                return 0
            else:
                return -100000
        
        my_player = self.root_player
        opponent = my_player.other
        my_stones = 0
        opponent_stones = 0
        my_liberties = 0
        opponent_liberties = 0

        processed_strings = set()
        
        board = game_state.board

        for r in range(1, board.num_rows + 1):
            for c in range(1, board.num_cols + 1):
                p = Point(r, c)
                stone = board.get(p)
                
                # 如果是空点，跳过
                if stone is None:
                    continue
                
                # 统计子数
                if stone == my_player:
                    my_stones += 1
                else:
                    opponent_stones += 1
                
                # 获取该位置的完整棋串
                go_string = board.get_go_string(p)
                
                # 如果这个棋串还没统计过气，就加气数
                string_key = go_string.stones  
                if string_key not in processed_strings:
                    processed_strings.add(string_key)
                
                    if go_string.color == my_player:
                        my_liberties += go_string.num_liberties 
                    else:
                        opponent_liberties += go_string.num_liberties

        return (my_stones - opponent_stones)  + (my_liberties - opponent_liberties )*3 # 气数权重更大
        

    def _get_ordered_moves(self, game_state):
        """
        获取排序后的候选棋步（用于优化剪枝效率）。

        好的排序能让 Alpha-Beta 剪掉更多分支。

        Args:
            game_state: 游戏状态

        Returns:
            按启发式排序的棋步列表
        """
        # TODO: 实现棋步排序
        # 提示：优先检查吃子、提子、连络等好棋
        
        moves = game_state.legal_moves()
        # 落子
        play_moves = [m for m in moves if m.is_play]
        # 停手和认输
        other_moves = [m for m in moves if not m.is_play]

        play_moves.sort(key=lambda m: self._move_score(game_state, m), reverse=True)

        return play_moves + other_moves   
    

    def _move_score(self, game_state, move):
        """
        快速计算单个落子动作的启发式得分，用于移动排序。
        """
        if not move.is_play:
            return 0
        
        score = 0
        point = move.point
        board = game_state.board
        
        # 简单的启发式规则：
        for neighbor in point.neighbors():
            if not board.is_on_grid(neighbor):
                continue
            
            neighbor_string = board.get_go_string(neighbor)
            if neighbor_string is not None:
                if neighbor_string.color != game_state.next_player:
                    # 进攻/提子倾向
                    if neighbor_string.num_liberties == 1:
                        score += 1000  
                    else:
                        score += 10
                else:
                    # 防守/长气倾向
                    if neighbor_string.num_liberties == 1:
                        score += 500
                    else:
                        score += 5
                        
        return score


class GameResultCache:
    """
    局面缓存（Transposition Table）。

    用 Zobrist 哈希缓存已评估的局面，避免重复计算。
    """

    def __init__(self):
        self.cache = {}

    def get(self, zobrist_hash):
        """获取缓存的评估值。"""
        return self.cache.get(zobrist_hash)

    def put(self, zobrist_hash, depth, value, flag='exact'):
        """
        缓存评估结果。

        Args:
            zobrist_hash: 局面哈希
            depth: 搜索深度
            value: 评估值
            flag: 'exact'/'lower'/'upper'（精确值/下界/上界）
        """
        # TODO: 实现缓存逻辑（考虑深度优先替换策略）
        if zobrist_hash in self.cache:
            cached_depth, _, _ = self.cache[zobrist_hash]
            # 深度优先：如果当前搜索深度比缓存的浅，说明信息含金量低，不覆盖
            if depth < cached_depth:
                return
                
        # 写入或覆盖缓存
        self.cache[zobrist_hash] = (depth, value, flag)
