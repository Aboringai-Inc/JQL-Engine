import re
import sys

class JQL:
    def __init__(self):
        self.variables = {}  # Store variables
        self.functions = {}  # Store user-defined functions
        self.modules = {}  # Store imported modules

    def execute_command(self, command: str):
        command = command.strip()
        if command.startswith("Set "):
            self._set_variable(command)
        elif command.startswith("Print "):
            return self._print_variable(command)
        elif command.startswith("If "):
            return self._handle_condition(command)
        elif command.startswith("Define "):
            self._define_function(command)
        elif command.startswith("Import "):
            self._import_module(command)
        elif command.startswith("Select "):
            return self._select_from_dataset(command)
        elif command == "End":
            return "Query execution completed."
        else:
            raise ValueError(f"Unknown command: {command}")

    def _evaluate_expressions(self, text: str) -> str:
        """Evaluate expressions enclosed in $(...) within the string."""
        while "$(" in text:
            start = text.index("$(")
            depth = 1
            end = start + 2
            while depth > 0 and end < len(text):
                if text[end] == "(":
                    depth += 1
                elif text[end] == ")":
                    depth -= 1
                end += 1
            if depth > 0:
                raise ValueError("Unmatched parentheses in expression.")
            expression = text[start + 2 : end - 1]
            try:
                result = eval(expression, {**self.variables, **self.functions}, self.modules)
                text = text[:start] + str(result) + text[end:]
            except Exception as e:
                raise ValueError(f"Error in evaluating expression '{expression}': {e}")
        return text

    def _set_variable(self, command: str):
        # Parse the Set command
        match = re.match(r"Set (\w+)\s+'(.*)':;", command)
        if not match:
            raise ValueError("Invalid Set syntax.")
        name, value = match.groups()
        # Evaluate expressions in the value
        value = self._evaluate_expressions(value)
        self.variables[name] = eval(value)

    def _print_variable(self, command: str):
        # Parse the Print command
        match = re.match(r'Print "(.*)":;', command)
        if not match:
            raise ValueError("Invalid Print syntax.")
        message = match.group(1)
        # Evaluate expressions in the message
        message = self._evaluate_expressions(message)
        return message

    def _handle_condition(self, command: str):
        # Parse the If-Else condition
        match = re.match(r"If (.+?) Then Print \"(.*?)\":; Else Print \"(.*?)\":;", command)
        if not match:
            raise ValueError("Invalid If-Else syntax.")
        condition, true_message, false_message = match.groups()
        # Evaluate the condition
        try:
            if eval(condition, {**self.variables, **self.functions}, self.modules):
                return self._evaluate_expressions(true_message)
            else:
                return self._evaluate_expressions(false_message)
        except Exception as e:
            raise ValueError(f"Error in evaluating condition: {e}")

    def _define_function(self, command: str):
        # Parse the Define command
        match = re.match(r"Define (\w+)\((.*?)\):\s*(return .+?):;", command)
        if not match:
            raise ValueError("Invalid Define syntax.")
        func_name, args, body = match.groups()
        # Dynamically create a function
        exec(
            f"def {func_name}({args}): {body}",
            self.variables,
            self.functions,
        )

    def _import_module(self, command: str):
        # Parse the Import command
        match = re.match(r"Import (\w+):;", command)
        if not match:
            raise ValueError("Invalid Import syntax.")
        module_name = match.group(1)
        # Dynamically import the module
        try:
            self.modules[module_name] = __import__(module_name)
        except ImportError:
            raise ValueError(f"Module '{module_name}' could not be imported.")

    def _select_from_dataset(self, command: str):
        # Parse the Select command
        match = re.match(r"Select (.+) All (.+) From (\w+):;", command)
        if not match:
            raise ValueError("Invalid Select syntax.")
        columns, condition, dataset_name = match.groups()

        if dataset_name not in self.variables:
            raise ValueError(f"Dataset '{dataset_name}' not found.")

        dataset = self.variables[dataset_name]
        if not isinstance(dataset, list):
            raise ValueError(f"Dataset '{dataset_name}' must be a list of dictionaries.")

        columns = [col.strip() for col in columns.split(",")]
        try:
            filtered_data = filter(
                lambda item: eval(condition, {**self.variables, **item}, self.modules), dataset
            )
            result = [
                {col: row.get(col, None) for col in columns} for row in filtered_data
            ]
            return result
        except Exception as e:
            raise ValueError(f"Error in evaluating Select condition: {e}")

# Example JQL script loaded with sys.argv
with open(sys.argv[1], "r") as bro:
    data = bro.read()
script = str(data)

# Execute the JQL script
jql_engine = JQL()
results = []
for command in script.splitlines():
    command = command.strip()
    if command:  # Skip empty lines
        output = jql_engine.execute_command(command)
        if output is not None:  # Capture output for Print, Select, etc.
            results.append(output)

print(results)
