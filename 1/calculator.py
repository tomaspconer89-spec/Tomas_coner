class Calculator:
    """
    A simple calculator that supports basic arithmetic operations,
    keeps history of calculations, and tracks unique operations used.
    """

    def __init__(self):
        # Stores calculation history as tuples:
        # (operator, operand1, operand2, result)
        self.history = []
        self.operations_used = set()

    def add(self, a: float, b: float) -> float:
        result = a + b
        self.history.append(("+", a, b, result))
        self.operations_used.add("+")
        return result

    def subtract(self, a: float, b: float) -> float:
        result = a - b
        self.history.append(("-", a, b, result))
        self.operations_used.add("-")
        return result

    def multiply(self, a: float, b: float) -> float:
        result = a * b
        self.history.append(("*", a, b, result))
        self.operations_used.add("*")
        return result

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not allowed.")
        result = a / b
        self.history.append(("/", a, b, result))
        self.operations_used.add("/")
        return result

    def get_history(self):
        """Return calculation history."""
        return self.history

    def clear_history(self):
        """Clear calculation history."""
        self.history.clear()

    def get_operations_used(self):
        """Return unique operations used."""
        return self.operations_used

    def get_last_result(self):
        """Return last calculation result or None."""
        if not self.history:
            return None
        return self.history[-1][3]