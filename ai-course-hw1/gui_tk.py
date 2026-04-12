import tkinter as tk
from tkinter import messagebox
import threading

from dlgo.goboard import GameState, Move
from dlgo.gotypes import Point, Player
from agents.random_agent import RandomAgent
from agents.mcts_agent import MCTSAgent
from agents.minimax_agent import MinimaxAgent

BOARD_SIZE = 5
GRID = 40
MARGIN = 30
STONE_R = 16

HUMAN = "Human"
RANDOM = "Random"
MCTS = "MCTS"
MINIMAX = "Minimax"
PLAYER_TYPES = [HUMAN, RANDOM, MCTS, MINIMAX]


class GoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Go (Tkinter)")

        self.black_type = tk.StringVar(value=HUMAN)
        self.white_type = tk.StringVar(value=MINIMAX)
        self.ai_running = False
        self.state_serial = 0
        self.game_state = GameState.new_game(BOARD_SIZE)

        self._build_controls()
        self._build_board()
        self.draw()
        self._maybe_run_ai()

    def _build_controls(self):
        top = tk.Frame(self.root)
        top.pack(pady=6)

        tk.Label(top, text="Black").pack(side=tk.LEFT)
        tk.OptionMenu(top, self.black_type, *PLAYER_TYPES).pack(side=tk.LEFT, padx=4)
        tk.Label(top, text="White").pack(side=tk.LEFT)
        tk.OptionMenu(top, self.white_type, *PLAYER_TYPES).pack(side=tk.LEFT, padx=4)

        tk.Button(top, text="New Game", command=self.new_game).pack(side=tk.LEFT, padx=6)
        tk.Button(top, text="Pass", command=self.human_pass).pack(side=tk.LEFT, padx=2)
        tk.Button(top, text="Resign", command=self.human_resign).pack(side=tk.LEFT, padx=2)

        self.info = tk.Label(self.root, text="")
        self.info.pack()

    def _build_board(self):
        w = MARGIN * 2 + GRID * (BOARD_SIZE - 1)
        h = MARGIN * 2 + GRID * (BOARD_SIZE - 1)
        self.canvas = tk.Canvas(self.root, width=w, height=h, bg="#DDBB77")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

    def new_game(self):
        self.ai_running = False
        self.state_serial += 1
        self.game_state = GameState.new_game(BOARD_SIZE)
        self.draw()
        self._maybe_run_ai()

    def _current_player_type(self):
        if self.game_state.next_player == Player.black:
            return self.black_type.get()
        return self.white_type.get()

    def _is_human_turn(self):
        return self._current_player_type() == HUMAN

    def _get_agent(self, player_type):
        if player_type == RANDOM:
            return RandomAgent()
        if player_type == MCTS:
            return MCTSAgent(num_rounds=200)
        if player_type == MINIMAX:
            return MinimaxAgent(max_depth=3)
        return None

    def _apply_move(self, move):
        if not self.game_state.is_valid_move(move):
            return False
        self.game_state = self.game_state.apply_move(move)
        self.state_serial += 1
        self.draw()
        return True

    def _run_one_ai_move_async(self):
        if self.game_state.is_over() or self._is_human_turn() or self.ai_running:
            return

        self.ai_running = True
        state_snapshot = self.game_state
        serial_snapshot = self.state_serial
        player_type = self._current_player_type()
        self.info.config(text=f"{self.game_state.next_player.name} thinking... ({player_type})")

        def worker():
            try:
                agent = self._get_agent(player_type)
                move = agent.select_move(state_snapshot)
                self.root.after(0, lambda: self._on_ai_move_ready(serial_snapshot, move, None))
            except Exception as exc:  # noqa: BLE001
                self.root.after(0, lambda: self._on_ai_move_ready(serial_snapshot, None, exc))

        threading.Thread(target=worker, daemon=True).start()

    def _on_ai_move_ready(self, serial_snapshot, move, error):
        if serial_snapshot != self.state_serial:
            self.ai_running = False
            return

        if error is not None:
            self.ai_running = False
            messagebox.showerror("AI 错误", str(error))
            self.draw()
            return

        self._apply_move(move)
        self.ai_running = False
        self._maybe_run_ai()

    def _maybe_run_ai(self):
        if self.game_state.is_over() or self._is_human_turn() or self.ai_running:
            return
        self.root.after(10, self._run_one_ai_move_async)

    def draw(self):
        self.canvas.delete("all")
        for i in range(BOARD_SIZE):
            x = MARGIN + i * GRID
            self.canvas.create_line(MARGIN, x, MARGIN + GRID * (BOARD_SIZE - 1), x)
            self.canvas.create_line(x, MARGIN, x, MARGIN + GRID * (BOARD_SIZE - 1))

        board = self.game_state.board
        for r in range(1, BOARD_SIZE + 1):
            for c in range(1, BOARD_SIZE + 1):
                point = Point(r, c)
                stone = board.get(point)
                if stone is None:
                    continue
                x = MARGIN + (c - 1) * GRID
                y = MARGIN + (r - 1) * GRID
                color = "black" if stone == Player.black else "white"
                self.canvas.create_oval(
                    x - STONE_R,
                    y - STONE_R,
                    x + STONE_R,
                    y + STONE_R,
                    fill=color,
                    outline="black",
                )

        if self.game_state.is_over():
            winner = self.game_state.winner()
            if winner is None:
                self.info.config(text="Game Over. Draw")
            else:
                self.info.config(text=f"Game Over. Winner: {winner.name}")
        else:
            side = self.game_state.next_player.name
            role = self._current_player_type()
            self.info.config(text=f"{side} to move ({role})")

    def on_click(self, event):
        if self.game_state.is_over() or not self._is_human_turn():
            return

        col = round((event.x - MARGIN) / GRID) + 1
        row = round((event.y - MARGIN) / GRID) + 1
        if not (1 <= row <= BOARD_SIZE and 1 <= col <= BOARD_SIZE):
            return

        move = Move.play(Point(row, col))
        if not self._apply_move(move):
            messagebox.showwarning("非法落子", "这个位置不能下。")
            return
        self._maybe_run_ai()

    def human_pass(self):
        if self.game_state.is_over() or not self._is_human_turn():
            return
        self._apply_move(Move.pass_turn())
        self._maybe_run_ai()

    def human_resign(self):
        if self.game_state.is_over() or not self._is_human_turn():
            return
        self._apply_move(Move.resign())
        self._maybe_run_ai()


if __name__ == "__main__":
    root = tk.Tk()
    GoGUI(root)
    root.mainloop()
