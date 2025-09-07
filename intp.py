# --- Momentum Interpreter in Python (Version 1.0.1) ---

import sys
import time

# --- 1. Token Definitions ---
# Represents a single token from the source code.
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    def __str__(self):
        return f'Token({self.type}, {repr(self.value)})'
    def __repr__(self):
        return self.__str__()

# --- 2. Lexer ---
# Breaks the source code into a stream of tokens.
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[0] if self.text else None
        self.keywords = {
            'LET': Token('LET', 'LET'),
            'PRINT': Token('PRINT', 'PRINT'),
            'INPUT': Token('INPUT', 'INPUT'),
            'IF': Token('IF', 'IF'),
            'THEN': Token('THEN', 'THEN'),
            'ELSE': Token('ELSE', 'ELSE'),
            'WHILE': Token('WHILE', 'WHILE'),
            'WEND': Token('WEND', 'WEND'),
            'FOR': Token('FOR', 'FOR'),
            'TO': Token('TO', 'TO'),
            'STEP': Token('STEP', 'STEP'),
            'NEXT': Token('NEXT', 'NEXT'),
            'FUNCTION': Token('FUNCTION', 'FUNCTION'),
            'RETURN': Token('RETURN', 'RETURN'),
            'DIM': Token('DIM', 'DIM'),
            'DATA': Token('DATA', 'DATA'),
            'READ': Token('READ', 'READ'),
            'RESTORE': Token('RESTORE', 'RESTORE'),
        }

    def advance(self):
        """Move the 'pos' pointer and set 'current_char'."""
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None
    
    def skip_whitespace_and_comments(self):
        """Combines skipping whitespace and comments for efficiency."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
                continue
            if self.current_char == '/' and self.peek() == '/':
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
                self.advance()
                continue
            break

    def peek(self):
        """Look at the next character without consuming the current one."""
        peek_pos = self.pos + 1
        return self.text[peek_pos] if peek_pos < len(self.text) else None
    
    def number(self):
        """Parse an integer or float number."""
        result = ''
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            result += self.current_char
            self.advance()
        if '.' in result:
            return Token('FLOAT', float(result))
        else:
            return Token('INTEGER', int(result))

    def string(self):
        """Parse a string literal enclosed in double quotes."""
        result = ''
        self.advance() # Skip the opening quote
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance() # Skip the closing quote
        return Token('STRING', result)
    
    def identifier(self):
        """Parse an identifier (variable name, keyword, or function name)."""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        
        token_value = result.upper()
        # Handle compound keywords like 'END IF'
        if token_value == 'END':
            peeked_word = self.peek_word().upper()
            if peeked_word == 'IF':
                self.advance_word('IF')
                return Token('ENDIF', 'ENDIF')
            if peeked_word == 'FUNCTION':
                self.advance_word('FUNCTION')
                return Token('ENDFUNCTION', 'ENDFUNCTION')
        
        # Check if it's a reserved keyword or just an ID
        return self.keywords.get(token_value, Token('ID', result))

    def peek_word(self):
        """Look ahead to see the next word for compound keywords."""
        start_pos = self.pos
        while start_pos < len(self.text) and self.text[start_pos].isspace():
            start_pos += 1
        end_pos = start_pos
        while end_pos < len(self.text) and self.text[end_pos].isalnum():
            end_pos += 1
        return self.text[start_pos:end_pos]

    def advance_word(self, word):
        """Consume whitespace and the specified word."""
        while self.current_char is not None and self.current_char.isspace():
            self.advance()
        for _ in range(len(word)):
            self.advance()
    
    def get_next_token(self):
        """The main method of the lexer which returns the next token."""
        self.skip_whitespace_and_comments()
        
        if self.current_char is None:
            return Token('EOF', None)

        if self.current_char.isdigit():
            return self.number()
        
        if self.current_char.isalpha():
            return self.identifier()
        
        if self.current_char == '"':
            return self.string()
        
        # Handle multi-character operators first
        if self.current_char == '=' and self.peek() == '=': self.advance(); self.advance(); return Token('EQ', '==')
        if self.current_char == '!' and self.peek() == '=': self.advance(); self.advance(); return Token('NEQ', '!=')
        if self.current_char == '>' and self.peek() == '=': self.advance(); self.advance(); return Token('GTE', '>=')
        if self.current_char == '<' and self.peek() == '=': self.advance(); self.advance(); return Token('LTE', '<=')

        # Handle single-character operators and delimiters
        op_map = {
            '=': ('ASSIGN', '='), '+': ('PLUS', '+'), '-': ('MINUS', '-'),
            '*': ('MUL', '*'), '/': ('DIV', '/'), '(': ('LPAREN', '('),
            ')': ('RPAREN', ')'), ',': ('COMMA', ','), '>': ('GT', '>'), '<': ('LT', '<'),
        }
        if self.current_char in op_map:
            char = self.current_char
            self.advance()
            return Token(*op_map[char])

        raise Exception(f"Lexer error: Invalid character '{self.current_char}'")

    def tokenize_all(self):
        """Creates a list of all tokens from the source code."""
        tokens = []
        while True:
            token = self.get_next_token()
            tokens.append(token)
            if token.type == 'EOF':
                break
        return tokens

# --- 3. Parser & AST ---
# Builds an Abstract Syntax Tree (AST) from the token stream.

class AST: pass
class BinOp(AST):
    def __init__(self, left, op, right): self.left, self.op, self.right = left, op, right
class UnaryOp(AST):
    def __init__(self, op, expr): self.op, self.expr = op, expr
class Num(AST):
    def __init__(self, token): self.token, self.value = token, token.value
class String(AST):
    def __init__(self, token): self.token, self.value = token, token.value
class Var(AST):
    def __init__(self, token): self.token, self.value = token, token.value
class Assign(AST):
    def __init__(self, left, op, right): self.left, self.op, self.right = left, op, right
class Print(AST):
    def __init__(self, expr): self.expr = expr
class Input(AST):
    def __init__(self, var, prompt): self.var, self.prompt = var, prompt
class If(AST):
    def __init__(self, condition, if_block, else_block): self.condition, self.if_block, self.else_block = condition, if_block, else_block
class While(AST):
    def __init__(self, condition, block): self.condition, self.block = condition, block
class For(AST):
    def __init__(self, var, start, end, step, block): self.var, self.start, self.end, self.step, self.block = var, start, end, step, block
class FuncDef(AST):
    def __init__(self, name, params, block): self.name, self.params, self.block = name, params, block
class FuncCall(AST):
    def __init__(self, name, args): self.name, self.args = name, args
class Return(AST):
    def __init__(self, expr): self.expr = expr
class Program(AST):
    def __init__(self, statements): self.statements = statements
class NoOp(AST):
    pass
class Dim(AST):
    def __init__(self, var, size): self.var, self.size = var, size
class ArrayAccess(AST):
    def __init__(self, name_token, index_expr): self.name_token, self.index_expr = name_token, index_expr
class Data(AST):
    def __init__(self, values): self.values = values
class Read(AST):
    def __init__(self, variables): self.variables = variables
class Restore(AST):
    pass


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[0]

    def eat(self, token_type):
        """Consume the current token if it matches the expected type."""
        if self.current_token.type == token_type:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.current_token = self.tokens[self.pos]
        else:
            raise Exception(f"Parser error: Expected {token_type}, but found {self.current_token.type} at position {self.pos}")

    def factor(self):
        """Parse numbers, strings, variables, function/array calls, and expressions in parentheses."""
        token = self.current_token
        if token.type in ('INTEGER', 'FLOAT'):
            self.eat(token.type)
            return Num(token)
        if token.type == 'STRING':
            self.eat('STRING')
            return String(token)
        if token.type == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node
        if token.type == 'ID':
            return self.variable() # Use the new general variable parser

        raise Exception(f"Parser error: Invalid factor '{token}'")

    def unary(self):
        """Parse unary plus and minus operators."""
        token = self.current_token
        if token.type in ('PLUS', 'MINUS'):
            self.eat(token.type)
            return UnaryOp(op=token, expr=self.unary())
        return self.factor()

    def term(self):
        """Parse multiplication and division."""
        node = self.unary()
        while self.current_token.type in ('MUL', 'DIV'):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.unary())
        return node
        
    def expr(self):
        """Parse addition, subtraction, and comparisons."""
        node = self.term()
        while self.current_token.type in ('PLUS', 'MINUS', 'EQ', 'NEQ', 'LT', 'LTE', 'GT', 'GTE'):
            token = self.current_token
            self.eat(token.type)
            node = BinOp(left=node, op=token, right=self.term())
        return node

    def variable(self):
        """Parses a simple variable (x) or an array/function access (x(i))."""
        name_token = self.current_token
        self.eat('ID')
        
        if self.current_token.type == 'LPAREN':
            self.eat('LPAREN')
            args = []
            if self.current_token.type != 'RPAREN':
                args.append(self.expr())
                while self.current_token.type == 'COMMA':
                    self.eat('COMMA')
                    args.append(self.expr())
            self.eat('RPAREN')
            
            # The interpreter will decide if it's an ArrayAccess or FuncCall at runtime
            if len(args) == 1:
                return ArrayAccess(name_token, args[0])
            return FuncCall(name_token.value, args)
        else:
            return Var(name_token)

    def statement_list(self, end_tokens):
        """Parse a list of statements until an end token is found."""
        statements = []
        while self.current_token.type not in end_tokens and self.current_token.type != 'EOF':
            statements.append(self.statement())
        if not statements:
            return [NoOp()]
        return statements

    def statement(self):
        """Parse a single statement."""
        token_type = self.current_token.type
        if token_type == 'LET': return self.assignment_statement()
        if token_type == 'PRINT': return self.print_statement()
        if token_type == 'INPUT': return self.input_statement()
        if token_type == 'IF': return self.if_statement()
        if token_type == 'WHILE': return self.while_statement()
        if token_type == 'FOR': return self.for_statement()
        if token_type == 'FUNCTION': return self.func_definition()
        if token_type == 'RETURN': return self.return_statement()
        if token_type == 'DIM': return self.dim_statement()
        if token_type == 'DATA': return self.data_statement()
        if token_type == 'READ': return self.read_statement()
        if token_type == 'RESTORE': return self.restore_statement()
        
        self.eat(self.current_token.type)
        return NoOp()
        
    def assignment_statement(self):
        self.eat('LET')
        left = self.variable()
        if not isinstance(left, (Var, ArrayAccess)):
            raise Exception("Parser error: Invalid target for assignment.")
        op = self.current_token
        self.eat('ASSIGN')
        right = self.expr()
        return Assign(left, op, right)

    def print_statement(self):
        self.eat('PRINT')
        return Print(self.expr())

    def input_statement(self):
        self.eat('INPUT')
        var = self.variable() # Can now be an array element
        prompt = None
        if self.current_token.type == 'COMMA':
            self.eat('COMMA')
            prompt = self.expr()
        return Input(var, prompt)

    def if_statement(self):
        self.eat('IF')
        condition = self.expr()
        self.eat('THEN')
        if_block = self.statement_list(['ELSE', 'ENDIF'])
        else_block = None
        if self.current_token.type == 'ELSE':
            self.eat('ELSE')
            else_block = self.statement_list(['ENDIF'])
        self.eat('ENDIF')
        return If(condition, if_block, else_block)

    def while_statement(self):
        self.eat('WHILE')
        condition = self.expr()
        block = self.statement_list(['WEND'])
        self.eat('WEND')
        return While(condition, block)

    def for_statement(self):
        self.eat('FOR')
        var = self.variable() # FOR loop variable must be a simple var
        if not isinstance(var, Var):
             raise Exception("Parser error: FOR loop counter must be a simple variable.")
        self.eat('ASSIGN')
        start_expr = self.expr()
        self.eat('TO')
        end_expr = self.expr()
        step_expr = Num(Token('INTEGER', 1))
        if self.current_token.type == 'STEP':
            self.eat('STEP')
            step_expr = self.expr()
        block = self.statement_list(['NEXT'])
        self.eat('NEXT')
        if self.current_token.value.lower() != var.value.lower():
            raise Exception(f"Parser error: Mismatched FOR/NEXT variable. Expected '{var.value}', found '{self.current_token.value}'")
        self.eat('ID')
        return For(var, start_expr, end_expr, step_expr, block)
    
    def func_definition(self):
        self.eat('FUNCTION')
        func_name = self.current_token.value
        self.eat('ID')
        self.eat('LPAREN')
        params = []
        if self.current_token.type != 'RPAREN':
            params.append(Var(self.current_token))
            self.eat('ID')
            while self.current_token.type == 'COMMA':
                self.eat('COMMA')
                params.append(Var(self.current_token))
                self.eat('ID')
        self.eat('RPAREN')
        block = self.statement_list(['ENDFUNCTION'])
        self.eat('ENDFUNCTION')
        return FuncDef(func_name, params, block)

    def return_statement(self):
        self.eat('RETURN')
        return Return(self.expr())

    def dim_statement(self):
        self.eat('DIM')
        var_token = self.current_token
        self.eat('ID')
        self.eat('LPAREN')
        size_expr = self.expr()
        self.eat('RPAREN')
        return Dim(Var(var_token), size_expr)

    def data_statement(self):
        self.eat('DATA')
        values = []
        # Loop until the end of the line or a non-data token
        while self.current_token.type not in ('EOF', 'LET', 'PRINT', 'IF', 'FOR', 'WHILE', 'FUNCTION', 'DIM', 'READ', 'RESTORE', 'NEXT', 'WEND', 'ENDIF', 'ENDFUNCTION'):
            values.append(self.expr())
            if self.current_token.type == 'COMMA':
                self.eat('COMMA')
            else:
                break
        return Data(values)
        
    def read_statement(self):
        self.eat('READ')
        variables = [self.variable()] # Can now parse array elements
        while self.current_token.type == 'COMMA':
            self.eat('COMMA')
            variables.append(self.variable()) # Can now parse array elements
        return Read(variables)

    def restore_statement(self):
        self.eat('RESTORE')
        return Restore()
        
    def parse(self):
        """Parse the entire program and return the AST."""
        statements = self.statement_list(['EOF'])
        if self.current_token.type != 'EOF':
            raise Exception("Parser error: Unexpected tokens at end of file.")
        return Program(statements)

# --- 4. Interpreter ---
# Executes the program by walking the AST.

class ReturnSignal(Exception):
    """
    Custom exception used to signal a return from a function.
    This allows breaking out of nested control structures.
    """
    def __init__(self, value):
        self.value = value

class CallStack:
    """Manages the stack of activation records for function calls."""
    def __init__(self): self.records = []
    def push(self, ar): self.records.append(ar)
    def pop(self): return self.records.pop()
    def peek(self): return self.records[-1] if self.records else None

class ActivationRecord:
    """Represents the memory space for a single function call (or the global scope)."""
    def __init__(self, name, type, nesting_level):
        self.name = name
        self.type = type
        self.nesting_level = nesting_level
        self.members = {} # Variable storage

class Interpreter:
    def __init__(self, tree):
        self.tree = tree
        self.call_stack = CallStack()
        global_ar = ActivationRecord(name='global', type='program', nesting_level=1)
        self.call_stack.push(global_ar)
        self.data_store = []
        self.data_pointer = 0

    def visit(self, node):
        """Dynamically dispatch to the correct visit method based on the node's type."""
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception(f'Interpreter error: No visit_{type(node).__name__} method')

    def visit_Program(self, node):
        # First pass: find all function and data definitions and store them globally
        for statement in node.statements:
            if isinstance(statement, FuncDef):
                self.visit(statement)
            elif isinstance(statement, Data):
                self.visit(statement)

        # Second pass: execute all other statements
        for statement in node.statements:
            if not isinstance(statement, (FuncDef, Data)):
                self.visit(statement)

    def visit_NoOp(self, node):
        """Handles empty nodes, does nothing."""
        pass

    def visit_Num(self, node): return node.value
    def visit_String(self, node): return node.value

    def visit_UnaryOp(self, node):
        value = self.visit(node.expr)
        if node.op.type == 'MINUS':
            return -value
        elif node.op.type == 'PLUS':
            return +value
        return value

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op_type = node.op.type
        # Arithmetic
        if op_type == 'PLUS': return left + right
        if op_type == 'MINUS': return left - right
        if op_type == 'MUL': return left * right
        if op_type == 'DIV': return left / right
        # Comparison
        if op_type == 'EQ': return left == right
        if op_type == 'NEQ': return left != right
        if op_type == 'LT': return left < right
        if op_type == 'LTE': return left <= right
        if op_type == 'GT': return left > right
        if op_type == 'GTE': return left >= right

    def visit_Assign(self, node):
        ar = self.call_stack.peek()
        value = self.visit(node.right)

        if isinstance(node.left, Var):
            var_name = node.left.value.lower()
            ar.members[var_name] = value
        elif isinstance(node.left, ArrayAccess):
            array_name = node.left.name_token.value.lower()
            array = ar.members.get(array_name)
            if not isinstance(array, list):
                raise TypeError(f"'{array_name}' is not an array.")
            
            index = self.visit(node.left.index_expr)
            if not isinstance(index, int) or not (0 <= index < len(array)):
                 raise IndexError(f"Array index out of bounds for '{array_name}'.")
            
            array[index] = value
        else:
            raise Exception("Interpreter error: Invalid assignment target.")

    def visit_Var(self, node):
        var_name = node.value.lower()
        ar = self.call_stack.peek()
        val = ar.members.get(var_name)
        if val is None: # If not in local scope, check global scope
            global_ar = self.call_stack.records[0]
            val = global_ar.members.get(var_name)
            if val is None:
                raise NameError(f"Variable '{node.value}' is not defined.")
        return val

    def visit_Print(self, node):
        value = self.visit(node.expr)
        print(str(value))
    
    def visit_Input(self, node):
        ar = self.call_stack.peek()
        prompt = str(self.visit(node.prompt)) if node.prompt else ""
        user_input = input(prompt)
        
        try:
            val = float(user_input)
            if val.is_integer(): val = int(val)
        except ValueError:
            val = user_input
        
        # Handle assignment to simple var or array element
        if isinstance(node.var, Var):
            var_name = node.var.value.lower()
            ar.members[var_name] = val
        elif isinstance(node.var, ArrayAccess):
            array_name = node.var.name_token.value.lower()
            array = ar.members.get(array_name)
            if not isinstance(array, list):
                raise TypeError(f"'{array_name}' is not an array.")
            index = self.visit(node.var.index_expr)
            if not isinstance(index, int) or not (0 <= index < len(array)):
                raise IndexError(f"Array index out of bounds for '{array_name}'.")
            array[index] = val
    
    def visit_If(self, node):
        if self.visit(node.condition):
            for statement in node.if_block: self.visit(statement)
        elif node.else_block:
            for statement in node.else_block: self.visit(statement)

    def visit_While(self, node):
        while self.visit(node.condition):
            for statement in node.block: self.visit(statement)
    
    def visit_For(self, node):
        var_name = node.var.value.lower()
        ar = self.call_stack.peek()
        start_val = self.visit(node.start)
        end_val = self.visit(node.end)
        step_val = self.visit(node.step)
        
        current_val = start_val
        ar.members[var_name] = current_val
        
        while (step_val > 0 and current_val <= end_val) or \
              (step_val < 0 and current_val >= end_val):
            for statement in node.block:
                self.visit(statement)
            current_val += step_val
            ar.members[var_name] = current_val

    def visit_FuncDef(self, node):
        # Store the function definition (the AST node itself) in the global scope
        self.call_stack.records[0].members[node.name.lower()] = node

    def visit_FuncCall(self, node):
        func_name = node.name.lower()
        func_def = self.call_stack.records[0].members.get(func_name)
        
        if isinstance(func_def, FuncDef):
            ar = ActivationRecord(name=func_name, type='function', nesting_level=self.call_stack.peek().nesting_level + 1)
            
            if len(node.args) != len(func_def.params):
                raise Exception(f"Function '{node.name}' expected {len(func_def.params)} arguments, but got {len(node.args)}")
            
            for param_node, arg_node in zip(func_def.params, node.args):
                ar.members[param_node.value.lower()] = self.visit(arg_node)

            self.call_stack.push(ar)
            
            return_value = None # Default return value if no return statement is hit
            try:
                # Execute the function block
                for statement in func_def.block:
                    self.visit(statement)
            except ReturnSignal as rs:
                # Catch the return signal and get the value
                return_value = rs.value
            finally:
                # Always pop the activation record
                self.call_stack.pop()
            
            return return_value

        if func_name in BUILTIN_FUNCTIONS:
            args = [self.visit(arg) for arg in node.args]
            return BUILTIN_FUNCTIONS[func_name](*args)
        
        raise Exception(f"'{node.name}' is not a function.")

    def visit_Return(self, node):
        """Instead of returning a value, raise an exception to unwind the stack."""
        value = self.visit(node.expr)
        raise ReturnSignal(value)

    def visit_Dim(self, node):
        ar = self.call_stack.peek()
        var_name = node.var.value.lower()
        if var_name in ar.members:
            raise Exception(f"Cannot redimension array '{var_name}'.")

        size = self.visit(node.size)
        if not isinstance(size, int) or size <= 0:
            raise ValueError("Array size must be a positive integer.")
        
        ar.members[var_name] = [None] * size

    def visit_ArrayAccess(self, node):
        ar = self.call_stack.peek()
        name_val = node.name_token.value.lower()
        
        # Check current scope first
        target = ar.members.get(name_val)
        if target is None: # Then check global scope
             target = self.call_stack.records[0].members.get(name_val)

        # If it's an array (list in Python), access it
        if isinstance(target, list):
            index = self.visit(node.index_expr)
            if not isinstance(index, int) or not (0 <= index < len(target)):
                 raise IndexError(f"Array index {index} out of bounds for '{name_val}' with size {len(target)}.")
            value = target[index]
            return 0 if value is None else value
        
        # If it's not an array, it must be a function call with one argument
        func_call_node = FuncCall(node.name_token.value, [node.index_expr])
        return self.visit(func_call_node)

    def visit_Data(self, node):
        # This is a pre-processing step.
        for value_node in node.values:
            self.data_store.append(self.visit(value_node))

    def visit_Read(self, node):
        ar = self.call_stack.peek()
        for var_node in node.variables:
            if self.data_pointer >= len(self.data_store):
                raise Exception("Out of DATA to read.")
            
            value = self.data_store[self.data_pointer]
            
            # Handle assignment to simple var or array element
            if isinstance(var_node, Var):
                var_name = var_node.value.lower()
                ar.members[var_name] = value
            elif isinstance(var_node, ArrayAccess):
                array_name = var_node.name_token.value.lower()
                array = ar.members.get(array_name)
                if not isinstance(array, list):
                    raise TypeError(f"'{array_name}' is not an array.")
                index = self.visit(var_node.index_expr)
                if not isinstance(index, int) or not (0 <= index < len(array)):
                    raise IndexError(f"Array index out of bounds for '{array_name}'.")
                array[index] = value

            self.data_pointer += 1
            
    def visit_Restore(self, node):
        self.data_pointer = 0

    def interpret(self):
        """Start the interpretation process."""
        tree = self.tree
        if tree is None: return ''
        return self.visit(tree)
        
# --- 5. Built-in Functions ---
# Define some built-in functions that can be called from Momentum code
BUILTIN_FUNCTIONS = {
    'time': time.time,
    'str': str,
    'int': int,
    'float': float,
}

# --- 6. Main Execution Block ---
def run_momentum(code):
    """A helper function to run the whole process: lexer -> parser -> interpreter."""
    if not code.strip(): # Check for empty source code
        return # Do nothing if the file is empty
    try:
        lexer = Lexer(code)
        tokens = lexer.tokenize_all()
        
        parser = Parser(tokens)
        tree = parser.parse()
        
        interpreter = Interpreter(tree)
        interpreter.interpret()
    except Exception as e:
        # Print a more user-friendly error message
        import traceback
        print(f"\nMomentum Runtime Error: {e}")
        # Uncomment the line below for a full Python traceback for debugging
        # traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if not filename.endswith('.mn'):
            print(f"Warning: Momentum files should typically have a '.mn' extension.")
        try:
            with open(filename, 'r', encoding="utf-8") as f:
                source_code = f.read()
        except FileNotFoundError:
            print(f"Error: File not found '{filename}'")
            sys.exit(1)
    else:
        # Default example code if no file is provided
        print("No input file. Running default demo program.\n"
              "Usage: python intp.py my_program.mn")
        source_code = """
        // Momentum Version 1.0.1 Demo
        // Now correctly handles nested RETURN statements.
        
        function get_sign(num)
            if num > 0 then
                return "Positive"
            else if num < 0 then
                return "Negative"
            else
                return "Zero"
            end if
        end function

        print("The sign of 10 is: " + get_sign(10))
        print("The sign of -5 is: " + get_sign(-5))
        print("The sign of 0 is: " + get_sign(0))
        """

    print("--- Running Momentum Code ---")
    run_momentum(source_code)
    print("---------------------------")