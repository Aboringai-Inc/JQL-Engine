
# JQL - JSON Query Language

**JQL (JSON Query Language)** is a lightweight and extensible scripting language that allows querying and manipulating JSON datasets with a SQL-like syntax, enhanced by the power of Python.

## Key Features

1. **SQL-Like Commands**:
   - `Select`: Query JSON datasets with filters and retrieve specific columns.
     ```plaintext
     Select name, age All age > 25 From example:;
     ```
   - `Set`: Define variables and datasets.
     ```plaintext
     Set example '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 20}]':;
     ```
   - `Print`: Output messages with support for f-string-style expressions.
     ```plaintext
     Print "Hello, ${example[0].name}":;
     ```

2. **Python Integration**:
   - **Python Functions**: Define and execute Python functions.
     ```plaintext
     Define add(a, b): return a + b:;
     Print "Sum: $(add(5, 3))":;
     ```
   - **Modules**: Import Python libraries for advanced computations.
     ```plaintext
     Import math:;
     Print "Square root of 16: $(math.sqrt(16))":;
     ```
   - **Built-in Python Features**: Use operators (`==`, `>`, `%`, etc.) and constructs (`if-else`, expressions).

3. **Flexible Syntax**:
   - Combines SQL-inspired commands with Python expressions, offering simplicity for JSON querying and the flexibility of Python for advanced operations.

4. **Safe Execution**:
   - Variables, functions, and modules are scoped within the JQL runtime to prevent unexpected behavior or conflicts.

## Example Script

```plaintext
Import math:;
Define add(a, b): return a + b:; 
Set example '[{"name": "Alice", "age": 30}, {"name": "Bob", "age": 20}]':;
Set result '$(add(10, 20))':;
Print "Sum is $(result)":;
Select name, age All age > 25 From example:;
End
```

**Output**:
```plaintext
Sum is 30
[{'name': 'Alice', 'age': 30}]
Query execution completed.
```

## Why Use JQL?

- Ideal for querying and manipulating JSON data in a structured and readable format.
- Lightweight and easy to learn for both developers and non-technical users.
- Leverages Python's power for extensibility, making it a hybrid tool for querying and computation.

## How to Contribute

Contributions are welcome! Fork the repository, make your improvements, and submit a pull request.
