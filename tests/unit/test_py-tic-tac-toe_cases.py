import sys, os, types
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'py-tic-tac-toe')))

# Auto-mock tkinter for headless environments
try:
    import tkinter as tk
except ImportError:
    import sys, types
    class _WidgetMock:
        def __init__(self, *a, **k): self._text = ""
        def config(self, **kwargs): 
            if "text" in kwargs: self._text = kwargs["text"]
        def cget(self, key): return self._text if key == "text" else None
        def get(self): return self._text
        def grid(self, *a, **k): return []
        def pack(self, *a, **k): return []
        def place(self, *a, **k): return []
        def destroy(self): return None
        def __getattr__(self, item): return lambda *a, **k: None
    tk = types.ModuleType("tkinter")
    for widget in ["Tk","Label","Button","Entry","Frame","Canvas","Text","Scrollbar","Checkbutton",
                "Radiobutton","Spinbox","Menu","Toplevel","Listbox"]:
        setattr(tk, widget, _WidgetMock)
    for const in ["N","S","E","W","NE","NW","SE","SW","CENTER","NS","EW","NSEW"]:
        setattr(tk, const, const)
    sys.modules["tkinter"] = tk

import pytest
from unittest.mock import patch
import io

# Assuming the source code is saved as Main.py
from Main import TicTacToe

@pytest.fixture
def game():
    game = TicTacToe()
    game.create_board()
    return game

def test_create_board(game):
    game.create_board()
    assert game.board == [['-', '-', '-'], ['-', '-', '-'], ['-', '-', '-']]

def test_fix_spot(game):
    game.fix_spot(0, 0, 'X')
    assert game.board[0][0] == 'X'

def test_has_player_won_row(game):
    game.fix_spot(0, 0, 'X')
    game.fix_spot(0, 1, 'X')
    game.fix_spot(0, 2, 'X')
    assert game.has_player_won('X') == True

def test_has_player_won_column(game):
    game.fix_spot(0, 0, 'O')
    game.fix_spot(1, 0, 'O')
    game.fix_spot(2, 0, 'O')
    assert game.has_player_won('O') == True

def test_has_player_won_diagonal_main(game):
    game.fix_spot(0, 0, 'X')
    game.fix_spot(1, 1, 'X')
    game.fix_spot(2, 2, 'X')
    assert game.has_player_won('X') == True

def test_has_player_won_diagonal_anti(game):
    game.fix_spot(0, 2, 'O')
    game.fix_spot(1, 1, 'O')
    game.fix_spot(2, 0, 'O')
    assert game.has_player_won('O') == True

def test_has_player_won_no_win(game):
    game.fix_spot(0, 0, 'X')
    game.fix_spot(0, 1, 'O')
    game.fix_spot(0, 2, '-')
    assert game.has_player_won('X') == False
    assert game.has_player_won('O') == False

def test_is_board_filled_true(game):
    for r in range(3):
        for c in range(3):
            game.fix_spot(r, c, 'X')
    assert game.is_board_filled() == True

def test_is_board_filled_false(game):
    game.fix_spot(0, 0, 'X')
    assert game.is_board_filled() == False

def test_swap_player_turn_x_to_o(game):
    assert game.swap_player_turn('X') == 'O'

def test_swap_player_turn_o_to_x(game):
    assert game.swap_player_turn('O') == 'X'

@patch('builtins.input', side_effect=['1 1', '2 2', '3 3', '1 2', '1 3', '2 1', '2 3', '3 1', '3 2'])
@patch('sys.stdout', new_callable=io.StringIO)
def test_start_player_x_wins(mock_stdout, mock_input):
    game = TicTacToe()
    # Simulate player X winning
    with patch.object(game, 'get_random_first_player', return_value=1): # X starts
        game.start()
    output = mock_stdout.getvalue()
    assert "Player X wins the game!" in output
    assert "Player X turn" in output

@patch('builtins.input', side_effect=['1 1', '2 2', '3 3', '1 2', '1 3', '2 1', '2 3', '3 2', '3 1'])
@patch('sys.stdout', new_callable=io.StringIO)
def test_start_player_o_wins(mock_stdout, mock_input):
    game = TicTacToe()
    # Simulate player O winning
    with patch.object(game, 'get_random_first_player', return_value=0): # O starts
        game.start()
    output = mock_stdout.getvalue()
    assert "Player O wins the game!" in output
    assert "Player O turn" in output

@patch('builtins.input', side_effect=['1 1', '2 2', '1 2', '2 1', '1 3', '3 1', '2 3', '3 2', '3 3'])
@patch('sys.stdout', new_callable=io.StringIO)
def test_start_draw(mock_stdout, mock_input):
    game = TicTacToe()
    # Simulate a draw
    with patch.object(game, 'get_random_first_player', return_value=0): # O starts
        game.start()
    output = mock_stdout.getvalue()
    assert "Match Draw!" in output

@patch('builtins.input', side_effect=['0 0', '1 1', '2 2']) # Invalid input test
@patch('sys.stdout', new_callable=io.StringIO)
def test_start_invalid_input_handled(mock_stdout, mock_input):
    game = TicTacToe()
    with patch.object(game, 'get_random_first_player', return_value=1): # X starts
        game.start()
    output = mock_stdout.getvalue()
    assert "Invalid spot. Try again!" in output
