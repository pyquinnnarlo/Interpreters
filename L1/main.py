import re
import ast
import operator

safe_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

def substitute_variables(expr, variables, line_number):
    """Replace #varname with actual value, and detect unprefixed variable misuse"""

    # 1. Detect misuse of known variable names without #
    tokens = re.findall(r"\b\w+\b", expr)
    for token in tokens:
        if token in variables and f"#{token}" not in expr:
            raise ValueError(f"[Line {line_number}] Error: Variable '{token}' used without '#'. Use '#{token}' to reference it.")

    # 2. Substitute all #varname with actual value
    def replacer(match):
        var_name = match.group(1)
        if var_name not in variables:
            raise ValueError(f"[Line {line_number}] Error: Undefined variable '{var_name}' used in expression.")
        value = variables[var_name]
        if isinstance(value, str):
            return f'"{value}"'
        return str(value)

    return re.sub(r"#(\w+)", replacer, expr)


def evaluate_expression(expr, expected_type, line_number):
    """Safely evaluate arithmetic or string expressions with type checking"""
    try:
        node = ast.parse(expr, mode='eval')

        def eval_node(n):
            if isinstance(n, ast.Expression):
                return eval_node(n.body)
            elif isinstance(n, ast.BinOp):
                left = eval_node(n.left)
                right = eval_node(n.right)
                op_type = type(n.op)

                if expected_type == "number" and not all(isinstance(x, (int, float)) for x in (left, right)):
                    raise ValueError(f"[Line {line_number}] Error: Mixed types in numeric expression.")

                if expected_type == "string" and not all(isinstance(x, str) for x in (left, right)):
                    raise ValueError(f"[Line {line_number}] Error: Mixed types in string expression.")

                if op_type in safe_operators:
                    return safe_operators[op_type](left, right)
                elif expected_type == "string" and isinstance(n.op, ast.Add):
                    return left + right
                else:
                    raise ValueError("Unsupported operator")
            elif isinstance(n, ast.Constant):
                return n.value
            else:
                raise ValueError("Unsupported expression")

        return eval_node(node)
    except Exception as e:
        raise ValueError(f"[Line {line_number}] Error: {e}")

def handle_integer(var_name, operator_token, value, variables, line_number):
    if not var_name.isidentifier():
        raise ValueError(f"[Line {line_number}] Error: Invalid variable name '{var_name}'")

    if operator_token != "=":
        raise ValueError(f"[Line {line_number}] Error: Expected '=' after variable name.")

    # Substitute #variables in expression
    value = substitute_variables(value, variables, line_number)
    result = evaluate_expression(value, expected_type="number", line_number=line_number)

    if not isinstance(result, (int, float)):
        raise ValueError(f"[Line {line_number}] Error: Expression does not evaluate to a number.")

    return int(result)

def handle_var(var_name, operator_token, value, variables, line_number):
    if not var_name.isidentifier():
        raise ValueError(f"[Line {line_number}] Error: Invalid variable name '{var_name}'")

    if operator_token != "=":
        raise ValueError(f"[Line {line_number}] Error: Expected '=' after variable name.")

    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]

    # Substitute #variables in expression
    value = substitute_variables(value, variables, line_number)
    result = evaluate_expression(value, expected_type="string", line_number=line_number)

    if not isinstance(result, str):
        raise ValueError(f"[Line {line_number}] Error: Expression does not evaluate to a string.")

    return result

def main():
    variables = {}

    with open("./main.q", "r") as file:
        lines = file.readlines()

    for line_number, line in enumerate(lines, start=1):
        line = line.strip()
        if not line:
            continue

        tokens = line.split(maxsplit=3)
        if len(tokens) != 4:
            print(f"[Line {line_number}] Error: Invalid syntax. Format must be: <type> <name> = <value>")
            return

        keyword, var_name, operator_token, value = tokens

        if keyword not in ("var", "int"):
            print(f"[Line {line_number}] Error: Unsupported declaration keyword '{keyword}'. Expected 'var' or 'int'.")
            return

        try:
            if keyword == "int":
                final_value = handle_integer(var_name, operator_token, value, variables, line_number)
            elif keyword == "var":
                final_value = handle_var(var_name, operator_token, value, variables, line_number)

            if var_name in variables:
                print(f"[Line {line_number}] Error: Variable '{var_name}' already declared.")
                return

            variables[var_name] = final_value
        except ValueError as e:
            print(e)
            return

    for _, val in variables.items():
        print(f"{val}")

main()
