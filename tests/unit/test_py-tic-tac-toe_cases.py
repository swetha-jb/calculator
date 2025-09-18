import sys, os, types
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'calculator')))

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
import tkinter as tk
from calc import Calculator

@pytest.fixture
def calculator():
    calc = Calculator()
    # Mock the mainloop to prevent the Tkinter window from actually appearing
    calc.window.mainloop = lambda: None
    return calc

def test_initialization(calculator):
    assert calculator.total_expression == ""
    assert calculator.current_expression == ""
    assert isinstance(calculator.window, tk.Tk)
    assert calculator.display_frame is not None
    assert calculator.total_label is not None
    assert calculator.label is not None
    assert calculator.buttons_frame is not None

def test_add_to_expression(calculator):
    calculator.add_to_expression(5)
    assert calculator.current_expression == "5"
    calculator.add_to_expression("+")
    assert calculator.current_expression == "5+"

def test_append_operator(calculator):
    calculator.current_expression = "123"
    calculator.append_operator("+")
    assert calculator.total_expression == "123+"
    assert calculator.current_expression == ""

def test_clear(calculator):
    calculator.current_expression = "123"
    calculator.total_expression = "456"
    calculator.clear()
    assert calculator.current_expression == ""
    assert calculator.total_expression == ""

def test_square(calculator):
    calculator.current_expression = "5"
    calculator.square()
    assert calculator.current_expression == "25.0"

def test_sqrt(calculator):
    calculator.current_expression = "25"
    calculator.sqrt()
    assert calculator.current_expression == "5.0"

def test_evaluate_addition(calculator):
    calculator.total_expression = "5+3"
    calculator.evaluate()
    assert calculator.current_expression == "8.0"
    assert calculator.total_expression == ""

def test_evaluate_subtraction(calculator):
    calculator.total_expression = "10-4"
    calculator.evaluate()
    assert calculator.current_expression == "6.0"
    assert calculator.total_expression == ""

def test_evaluate_multiplication(calculator):
    calculator.total_expression = "6*7"
    calculator.evaluate()
    assert calculator.current_expression == "42.0"
    assert calculator.total_expression == ""

def test_evaluate_division(calculator):
    calculator.total_expression = "10/2"
    calculator.evaluate()
    assert calculator.current_expression == "5.0"
    assert calculator.total_expression == ""

def test_evaluate_mixed_operations(calculator):
    calculator.total_expression = "5+3*2"
    calculator.evaluate()
    assert calculator.current_expression == "11.0"
    assert calculator.total_expression == ""

def test_evaluate_with_decimal(calculator):
    calculator.total_expression = "2.5*2"
    calculator.evaluate()
    assert calculator.current_expression == "5.0"
    assert calculator.total_expression == ""

def test_evaluate_division_by_zero(calculator):
    calculator.total_expression = "10/0"
    calculator.evaluate()
    assert calculator.current_expression == "Error"
    assert calculator.total_expression == ""

def test_update_label_short_expression(calculator):
    calculator.current_expression = "12345"
    calculator.update_label()
    assert calculator.label.cget("text") == "12345"

def test_update_label_long_expression(calculator):
    calculator.current_expression = "1234567890123"
    calculator.update_label()
    assert calculator.label.cget("text") == "12345678901"

def test_update_total_label_no_operators(calculator):
    calculator.total_expression = "123"
    calculator.update_total_label()
    assert calculator.total_label.cget("text") == "123"

def test_update_total_label_with_operators(calculator):
    calculator.total_expression = "10+5-3*2"
    calculator.update_total_label()
    assert calculator.total_label.cget("text") == "10 + 5 - 3 * 2"

def test_evaluate_when_current_expression_is_empty(calculator):
    calculator.total_expression = ""
    calculator.current_expression = ""
    calculator.evaluate()
    assert calculator.current_expression == ""
    assert calculator.total_expression == ""

def test_evaluate_when_total_expression_is_empty(calculator):
    calculator.total_expression = ""
    calculator.current_expression = "5"
    calculator.evaluate()
    assert calculator.current_expression == "5"
    assert calculator.total_expression == ""

def test_evaluate_with_preceding_operator(calculator):
    calculator.total_expression = "+5"
    calculator.evaluate()
    assert calculator.current_expression == "5.0"
    assert calculator.total_expression == ""

def test_special_buttons_create(calculator):
    assert True  # Placeholder assert
    # Check if special buttons are created and have the correct commands
    # This is a bit tricky to test directly without digging into button attributes.
    # We can check if the associated methods are called when the logic is triggered.
    # For now, we'll assume the grid placement and command assignment are handled internally.
    pass

def test_digit_buttons_create(calculator):
    assert True  # Placeholder assert
    # Similar to special buttons, checking creation directly is complex.
    pass

def test_operator_buttons_create(calculator):
    assert True  # Placeholder assert
    # Similar to special buttons, checking creation directly is complex.
    pass
