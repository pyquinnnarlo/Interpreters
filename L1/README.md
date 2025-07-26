# L1 Interpreter and Programming Language

A simple, educational programming language interpreter written in Python. L1 supports basic variable declarations, arithmetic operations, and string manipulation with a clean, minimal syntax.

## Features

- **Two Data Types**: `int` for integers and `var` for strings
- **Variable References**: Use `#variable_name` to reference previously declared variables
- **Arithmetic Operations**: Support for `+`, `-`, `*`, `/`, `%`, and `^` (power)
- **String Concatenation**: Use `+` to concatenate strings
- **Error Handling**: Clear error messages with line numbers
- **REPL Mode**: Interactive command-line interface
- **File Execution**: Run L1 programs from `.q` files

## Installation

No installation required! Just make sure you have Python 3.6+ installed.

```bash
# Clone the repository
git clone <repository-url>
cd L1
```

## Usage

### Running L1 Programs

Execute L1 programs from `.q` files:

```bash
python main.py
```

This will read and execute the `main.q` file in the current directory.

### Interactive REPL Mode

Start the interactive REPL (Read-Eval-Print Loop):

```bash
python terminal.py
```

Type `exit` to quit the REPL.

## Syntax

### Variable Declarations

L1 uses a simple declaration syntax:

```
<type> <variable_name> = <value>
```

Where:
- `<type>` is either `int` or `var`
- `<variable_name>` is a valid identifier
- `<value>` is the initial value or expression

### Data Types

#### Integer (`int`)
```q
int age = 25
int result = 10 + 5
int power = 2 ^ 3
```

#### String (`var`)
```q
var name = "Alice"
var greeting = "Hello, " + "World!"
var message = "Age: " + #age
```

### Variable References

Use `#` prefix to reference previously declared variables:

```q
int x = 10
int y = #x + 5        # y = 15
var message = "x is " + #x  # message = "x is 10"
```

### Supported Operations

#### Arithmetic Operations
- Addition: `+`
- Subtraction: `-`
- Multiplication: `*`
- Division: `/`
- Modulo: `%`
- Power: `^`

#### String Operations
- Concatenation: `+`

## Examples

### Basic Variable Declarations

```q
int age = 25
var name = "John"
int score = 100
var message = "Hello, " + #name
```

**Output:**
```
25
John
100
Hello, John
```

### Arithmetic Operations

```q
int a = 10
int b = 5
int sum = #a + #b
int product = #a * #b
int power = #a ^ 2
```

**Output:**
```
10
5
15
50
100
```

### String Manipulation

```q
var first = "Hello"
var second = "World"
var greeting = #first + ", " + #second + "!"
int year = 2024
var message = "Welcome to " + #year
```

**Output:**
```
Hello
World
Hello, World!
2024
Welcome to 2024
```

### Complex Example

```q
int base = 10
int height = 5
int area = #base * #height / 2
var shape = "triangle"
var result = "Area of " + #shape + " is " + #area
```

**Output:**
```
10
5
25
triangle
Area of triangle is 25
```

## Error Handling

L1 provides clear error messages for common issues:

### Undefined Variable
```q
int x = #undefined_var
```
**Error:** `[Line 1] Error: Undefined variable 'undefined_var' used in expression.`

### Missing # Prefix
```q
int x = 10
int y = x + 5
```
**Error:** `[Line 2] Error: Variable 'x' used without '#'. Use '#x' to reference it.`

### Invalid Variable Name
```q
int 123invalid = 10
```
**Error:** `[Line 1] Error: Invalid variable name '123invalid'`

### Type Mismatch
```q
var text = "Hello"
int result = #text + 5
```
**Error:** `[Line 2] Error: Mixed types in numeric expression.`

## File Structure

- `main.py` - Main interpreter for executing `.q` files
- `terminal.py` - Interactive REPL implementation
- `main.q` - Example L1 program file
- `README.md` - This documentation

## Contributing

This is an educational project. Feel free to:
- Add new language features
- Improve error handling
- Add more examples
- Enhance documentation

## License

[Add your license information here]