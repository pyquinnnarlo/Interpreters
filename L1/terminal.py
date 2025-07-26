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
    tokens = re.findall(r"\b\w+\b", expr)
    for token in tokens:
        if token in variables and f"#{token}" not in expr:
            raise ValueError(f"[Line {line_number}] Error: Variable '{token}' used without '#'. Use '#{token}'.")

    def replacer(match):
        var_name = match.group(1)
        if var_name not in variables:
            raise ValueError(f"[Line {line_number}] Error: Undefined variable '#{var_name}'.")
        value = variables[var_name]
        return f'"{value}"' if isinstance(value, str) else str(value)

    return re.sub(r"#(\w+)", replacer, expr)

def evaluate_expression(expr, expected_type, line_number):
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
    value = substitute_variables(value, variables, line_number)
    result = evaluate_expression(value, expected_type="number", line_number=line_number)
    if not isinstance(result, (int, float)):
        raise ValueError(f"[Line {line_number}] Error: Value must be numeric.")
    return int(result)

def handle_var(var_name, operator_token, value, variables, line_number):
    if not var_name.isidentifier():
        raise ValueError(f"[Line {line_number}] Error: Invalid variable name '{var_name}'")
    if operator_token != "=":
        raise ValueError(f"[Line {line_number}] Error: Expected '=' after variable name.")
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    value = substitute_variables(value, variables, line_number)
    result = evaluate_expression(value, expected_type="string", line_number=line_number)
    if not isinstance(result, str):
        raise ValueError(f"[Line {line_number}] Error: Value must be string.")
    return result

def repl():
    print("CustomLang REPL (type 'exit' to quit)")
    variables = {}
    line_number = 0

    while True:
        try:
            line = input(">>> ").strip()
            if line.lower() == "exit":
                print("Bye!")
                break
            if not line:
                continue

            line_number += 1
            tokens = line.split(maxsplit=3)
            if len(tokens) != 4:
                print(f"[Line {line_number}] Error: Use format <type> <name> = <value>")
                continue

            keyword, var_name, operator_token, value = tokens
            if keyword not in ("var", "int"):
                print(f"[Line {line_number}] Error: Unknown keyword '{keyword}'")
                continue

            if var_name in variables:
                print(f"[Line {line_number}] Error: Variable '{var_name}' already declared.")
                continue

            if keyword == "int":
                result = handle_integer(var_name, operator_token, value, variables, line_number)
            else:
                result = handle_var(var_name, operator_token, value, variables, line_number)

            variables[var_name] = result
            print(f"[OK] {var_name} = {result}")

        except Exception as e:
            print(e)

repl()
