# --- Momentum Interpreter in Python (Version 1.0.2) ---

import sys
import time
import math
import asyncio
import traceback

# --- Numba JIT Compilation Module ---
try:
    import numba
    NUMBA_ENABLED = True
except ImportError:
    NUMBA_ENABLED = False

# --- Graphics Module (using tkinter) ---
try:
    import tkinter
    GFX_ENABLED = True
except ImportError:
    GFX_ENABLED = False

# --- Global State for Graphics ---
GFX_GLOBALS = {"window": None, "canvas": None, "color": "black"}


def gfx_init(width=640, height=480, title="Momentum Graphics"):
    """Initializes the graphics window."""
    if not GFX_ENABLED:
        raise Exception("โมดูลกราฟิกต้องการ tkinter ซึ่งไม่พบ")
    if GFX_GLOBALS["window"]:
        GFX_GLOBALS["window"].destroy()

    window = tkinter.Tk()
    window.title(title)
    canvas = tkinter.Canvas(window, width=width, height=height, bg="white")
    canvas.pack()
    window.update()
    GFX_GLOBALS["window"], GFX_GLOBALS["canvas"] = window, canvas
    return 1


def gfx_set_color(r, g, b):
    """Sets the drawing color using RGB values."""
    if not GFX_GLOBALS["canvas"]:
        raise Exception("กราฟิกยังไม่ได้เริ่มต้น เรียกใช้ gfx_init() ก่อน")
    GFX_GLOBALS["color"] = f'#{int(r):02x}{int(g):02x}{int(b):02x}'
    return GFX_GLOBALS["color"]


def gfx_draw_line(x1, y1, x2, y2):
    """Draws a line."""
    if not GFX_GLOBALS["canvas"]:
        raise Exception("กราฟิกยังไม่ได้เริ่มต้น เรียกใช้ gfx_init() ก่อน")
    GFX_GLOBALS["canvas"].create_line(x1, y1, x2, y2, fill=GFX_GLOBALS["color"])


def gfx_draw_rect(x, y, width, height, fill=0):
    """Draws a rectangle."""
    if not GFX_GLOBALS["canvas"]:
        raise Exception("กราฟิกยังไม่ได้เริ่มต้น เรียกใช้ gfx_init() ก่อน")
    fill_color = GFX_GLOBALS["color"] if fill else ""
    GFX_GLOBALS["canvas"].create_rectangle(
        x, y, x + width, y + height, fill=fill_color, outline=GFX_GLOBALS["color"]
    )


def gfx_draw_circle(x, y, radius, fill=0):
    """Draws a circle."""
    if not GFX_GLOBALS["canvas"]:
        raise Exception("กราฟิกยังไม่ได้เริ่มต้น เรียกใช้ gfx_init() ก่อน")
    fill_color = GFX_GLOBALS["color"] if fill else ""
    GFX_GLOBALS["canvas"].create_oval(
        x - radius, y - radius, x + radius, y + radius, fill=fill_color, outline=GFX_GLOBALS["color"]
    )


def gfx_update():
    """Updates the graphics window to show drawings."""
    if GFX_GLOBALS["window"]:
        GFX_GLOBALS["window"].update()


def gfx_wait():
    """Waits for the user to close the graphics window."""
    if not GFX_GLOBALS["window"]:
        return
    try:
        GFX_GLOBALS["window"].mainloop()
    except (tkinter.TclError, KeyboardInterrupt):
        GFX_GLOBALS["window"], GFX_GLOBALS["canvas"] = None, None


# --- Custom Errors ---
class MomentumError(Exception):
    """Base class for errors in Momentum."""
    pass


class ParserError(MomentumError):
    """Error during the parsing phase."""
    def __init__(self, message, token):
        super().__init__(f"[บรรทัดที่ {token.line}] ข้อผิดพลาดทางไวยากรณ์: {message}")
        self.token = token


class InterpreterError(MomentumError):
    """Error during the interpretation (runtime) phase."""
    def __init__(self, message, node):
        line = '?'
        if hasattr(node, 'token') and hasattr(node.token, 'line'):
            line = node.token.line
        super().__init__(f"[บรรทัดที่ {line}] ข้อผิดพลาดขณะทำงาน: {message}")
        self.node = node


# --- 1. Token Definitions ---
class Token:
    """Represents a token from the source code."""
    def __init__(self, type, value, line):
        self.type, self.value, self.line = type, value, line

    def __repr__(self):
        return f'Token({self.type}, {repr(self.value)}, L{self.line})'


# --- 2. Lexer ---
class Lexer:
    """Breaks the source code into a stream of tokens."""
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.line = 1
        self.current_char = self.text[self.pos] if self.text else None
        self.keywords = {
            'LET': 'LET', 'PRINT': 'PRINT', 'INPUT': 'INPUT', 'IF': 'IF', 'THEN': 'THEN',
            'ELSE': 'ELSE', 'WHILE': 'WHILE', 'WEND': 'WEND', 'FOR': 'FOR', 'TO': 'TO',
            'STEP': 'STEP', 'NEXT': 'NEXT', 'FUNCTION': 'FUNCTION', 'RETURN': 'RETURN',
            'DIM': 'DIM', 'DATA': 'DATA', 'READ': 'READ', 'RESTORE': 'RESTORE', 'AND': 'AND',
            'OR': 'OR', 'NOT': 'NOT', 'AWAIT': 'AWAIT', 'ENDIF': 'ENDIF', 'ELSEIF': 'ELSEIF',
            'ENDFUNCTION': 'ENDFUNCTION', 'JIT_FUNCTION': 'JIT_FUNCTION',
            'ASYNC_FUNCTION': 'ASYNC_FUNCTION', 'RUN_ASYNC': 'RUN_ASYNC'
        }

    def advance(self):
        """Move the pointer to the next character."""
        if self.current_char == '\n':
            self.line += 1
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace_and_comments(self):
        """Skips over whitespace and single-line comments."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.advance()
            elif self.current_char == '/' and self.text[self.pos+1:self.pos+2] == '/':
                while self.current_char is not None and self.current_char != '\n':
                    self.advance()
            else:
                break

    def number(self):
        """Handles integer and float literals."""
        result = ''
        start_line = self.line
        has_dot = False
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if has_dot: break
                has_dot = True
            result += self.current_char
            self.advance()
        if has_dot:
            return Token('FLOAT', float(result), start_line)
        return Token('INTEGER', int(result), start_line)

    def string(self):
        """Handles string literals with escape characters."""
        result = ''
        start_line = self.line
        self.advance()
        while self.current_char is not None and self.current_char != '"':
            if self.current_char == '\\':
                self.advance()
                if self.current_char == 'n': result += '\n'
                elif self.current_char == 't': result += '\t'
                elif self.current_char == '"': result += '"'
                elif self.current_char == '\\': result += '\\'
                else: result += '\\' + self.current_char
            else:
                result += self.current_char
            self.advance()
        self.advance()
        return Token('STRING', result, start_line)

    def identifier(self):
        """Handles identifiers and multi-word keywords."""
        result = ''
        start_line = self.line
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()

        result_upper = result.upper()

        if result_upper in ('END', 'ELSE', 'JIT', 'ASYNC', 'RUN'):
            saved_pos, saved_line, saved_char = self.pos, self.line, self.current_char
            self.skip_whitespace_and_comments()
            
            next_word = ''
            peek_pos = self.pos
            while peek_pos < len(self.text) and self.text[peek_pos].isalnum():
                next_word += self.text[peek_pos]
                peek_pos += 1
            next_word_upper = next_word.upper()

            combo = f"{result_upper}_{next_word_upper}"
            remap = {
                'END_IF': 'ENDIF', 'END_FUNCTION': 'ENDFUNCTION', 'ELSE_IF': 'ELSEIF',
                'JIT_FUNCTION': 'JIT_FUNCTION', 'ASYNC_FUNCTION': 'ASYNC_FUNCTION', 'RUN_ASYNC': 'RUN_ASYNC'
            }

            if remap.get(combo):
                for _ in range(len(next_word)):
                    self.advance()
                token_type = remap[combo]
                return Token(token_type, token_type, start_line)
            else:
                self.pos, self.line, self.current_char = saved_pos, saved_line, saved_char

        token_type = self.keywords.get(result_upper)
        if token_type:
            return Token(token_type, result_upper, start_line)
        return Token('ID', result, start_line)

    def get_next_token(self):
        """Get the next token from the input."""
        while self.current_char is not None:
            self.skip_whitespace_and_comments()

            if self.current_char is None:
                continue

            if self.current_char.isalpha(): return self.identifier()
            if self.current_char.isdigit(): return self.number()
            if self.current_char == '"': return self.string()
            
            op2 = self.text[self.pos:self.pos+2]
            if op2 == '==': self.advance(); self.advance(); return Token('EQ', '==', self.line)
            if op2 == '!=': self.advance(); self.advance(); return Token('NEQ', '!=', self.line)
            if op2 == '>=': self.advance(); self.advance(); return Token('GTE', '>=', self.line)
            if op2 == '<=': self.advance(); self.advance(); return Token('LTE', '<=', self.line)

            op1_map = {'=':'ASSIGN', '+':'PLUS', '-':'MINUS', '*':'MUL', '/':'DIV', '(': 'LPAREN', ')':'RPAREN', ',':'COMMA', '>':'GT', '<':'LT'}
            if self.current_char in op1_map:
                char, line = self.current_char, self.line
                self.advance()
                return Token(op1_map[char], char, line)

            raise MomentumError(f"[บรรทัดที่ {self.line}] ข้อผิดพลาด Lexer: พบอักขระที่ไม่ถูกต้อง '{self.current_char}'")
        
        return Token('EOF', None, self.line)

    def tokenize_all(self):
        tokens = []
        while True:
            tok = self.get_next_token()
            tokens.append(tok)
            if tok.type == 'EOF': break
        return tokens

# --- 3. AST Nodes ---
class AST: pass
class BinOp(AST):
    def __init__(self, left, op, right): self.left, self.op, self.right, self.token = left, op, right, op
class UnaryOp(AST):
    def __init__(self, op, expr): self.op, self.expr, self.token = op, expr, op
class Num(AST):
    def __init__(self, token): self.token, self.value = token, token.value
class String(AST):
    def __init__(self, token): self.token, self.value = token, token.value
class Var(AST):
    def __init__(self, token): self.token, self.value = token, token.value
class Assign(AST):
    def __init__(self, left, op, right): self.left, self.op, self.right, self.token = left, op, right, op
class Print(AST):
    def __init__(self, expr, token): self.expr, self.token = expr, token
class Input(AST):
    def __init__(self, var, prompt, token): self.var, self.prompt, self.token = var, prompt, token
class If(AST):
    def __init__(self, cases, else_case, token): self.cases, self.else_case, self.token = cases, else_case, token
class While(AST):
    def __init__(self, condition, block, token): self.condition, self.block, self.token = condition, block, token
class For(AST):
    def __init__(self, var, start, end, step, block, token): self.var, self.start, self.end, self.step, self.block, self.token = var, start, end, step, block, token
class FuncDef(AST):
    def __init__(self, name, params, block, token, is_async=False, is_jit=False):
        self.name, self.params, self.block, self.token = name, params, block, token
        self.is_async, self.is_jit = is_async, is_jit
class FuncCall(AST):
    def __init__(self, name_token, args): self.name_token, self.args, self.token = name_token, args, name_token
    @property
    def name(self): return self.name_token.value
class Return(AST):
    def __init__(self, expr, token): self.expr, self.token = expr, token
class Program(AST):
    def __init__(self, statements): self.statements = statements
class NoOp(AST): pass
class Dim(AST):
    def __init__(self, var_token, size_exprs, token): self.var_token, self.size_exprs, self.token = var_token, size_exprs, token
class ArrayAccess(AST):
    def __init__(self, name_token, index_exprs): self.name_token, self.index_exprs, self.token = name_token, index_exprs, name_token
class Data(AST):
    def __init__(self, values, token): self.values, self.token = values, token
class Read(AST):
    def __init__(self, variables, token): self.variables, self.token = variables, token
class Restore(AST):
    def __init__(self, token): self.token = token
class Await(AST):
    def __init__(self, expr, token): self.expr, self.token = expr, token
class RunAsync(AST):
    def __init__(self, tasks, token): self.tasks, self.token = tasks, token

# --- 4. Parser ---
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens; self.pos = 0; self.current_token = tokens[0]

    def error(self, message):
        raise ParserError(message, self.current_token)

    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.pos += 1
            self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        else:
            found = self.current_token.type if self.current_token else "None"
            self.error(f"คาดหวังโทเค็น {token_type}, แต่พบ {found}")

    def factor(self):
        token = self.current_token
        if token.type in ('INTEGER', 'FLOAT'): self.eat(token.type); return Num(token)
        if token.type == 'STRING': self.eat('STRING'); return String(token)
        if token.type == 'LPAREN': self.eat('LPAREN'); node = self.expr(); self.eat('RPAREN'); return node
        if token.type == 'ID': return self.variable_or_func_call()
        if token.type == 'AWAIT': return self.await_expression()
        self.error(f"ไวยากรณ์ไม่ถูกต้องสำหรับ factor, พบโทเค็น {token}")
    
    def unary(self):
        token = self.current_token
        if token.type in ('PLUS', 'MINUS', 'NOT'): self.eat(token.type); return UnaryOp(op=token, expr=self.unary())
        return self.factor()

    def term(self):
        node = self.unary()
        while self.current_token and self.current_token.type in ('MUL', 'DIV'):
            token = self.current_token; self.eat(token.type); node = BinOp(left=node, op=token, right=self.unary())
        return node

    def arith_expr(self):
        node = self.term()
        while self.current_token and self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token; self.eat(token.type); node = BinOp(left=node, op=token, right=self.term())
        return node

    def comparison_expr(self):
        node = self.arith_expr()
        op_types = ('EQ','NEQ','LT','LTE','GT','GTE')
        while self.current_token and self.current_token.type in op_types:
            token = self.current_token; self.eat(token.type); node = BinOp(left=node, op=token, right=self.arith_expr())
        return node

    def logic_and_expr(self):
        node = self.comparison_expr()
        while self.current_token and self.current_token.type == 'AND':
            token = self.current_token; self.eat('AND'); node = BinOp(left=node, op=token, right=self.comparison_expr())
        return node

    def logic_or_expr(self):
        node = self.logic_and_expr()
        while self.current_token and self.current_token.type == 'OR':
            token = self.current_token; self.eat('OR'); node = BinOp(left=node, op=token, right=self.logic_and_expr())
        return node

    def expr(self): return self.logic_or_expr()

    def variable_or_func_call(self):
        name_token = self.current_token; self.eat('ID')
        if self.current_token and self.current_token.type == 'LPAREN':
            self.eat('LPAREN'); args = []
            if self.current_token.type != 'RPAREN':
                args.append(self.expr())
                while self.current_token.type == 'COMMA': self.eat('COMMA'); args.append(self.expr())
            self.eat('RPAREN'); return ArrayAccess(name_token, args)
        return Var(name_token)
    
    def await_expression(self):
        token = self.current_token; self.eat('AWAIT'); return Await(self.expr(), token)

    def statement_list(self, end_tokens):
        statements = []
        while self.current_token and self.current_token.type not in end_tokens:
            statements.append(self.statement())
        return statements or [NoOp()]

    def statement(self):
        if not self.current_token or self.current_token.type == 'EOF': self.error("พบจุดสิ้นสุดของไฟล์ที่ไม่คาดคิด")
        tok_type = self.current_token.type
        
        dispatch = {
            'LET': self.assignment_statement, 'PRINT': self.print_statement,
            'INPUT': self.input_statement, 'IF': self.if_statement,
            'WHILE': self.while_statement, 'FOR': self.for_statement,
            'FUNCTION': self.func_definition, 'ASYNC_FUNCTION': self.func_definition,
            'JIT_FUNCTION': self.func_definition, 'RETURN': self.return_statement,
            'DIM': self.dim_statement, 'DATA': self.data_statement,
            'READ': self.read_statement, 'RESTORE': self.restore_statement,
            'RUN_ASYNC': self.run_async_statement, 'AWAIT': self.await_expression
        }
        if tok_type in dispatch: return dispatch[tok_type]()

        if tok_type == 'ID':
            node = self.variable_or_func_call()
            if isinstance(node, ArrayAccess): 
                return node
            self.error(f"คำสั่งไม่ถูกต้อง เริ่มต้นด้วย '{node.token.value}' หากต้องการกำหนดค่า ให้ใช้ LET")

        self.error(f"โทเค็นที่ไม่คาดคิด '{self.current_token.value}'")

    def assignment_statement(self):
        self.eat('LET'); left = self.variable_or_func_call()
        if not isinstance(left, (Var, ArrayAccess)): self.error("เป้าหมายการกำหนดค่าไม่ถูกต้อง")
        op = self.current_token; self.eat('ASSIGN'); right = self.expr()
        return Assign(left, op, right)

    def print_statement(self):
        token = self.current_token; self.eat('PRINT'); return Print(self.expr(), token)

    def input_statement(self):
        token = self.current_token; self.eat('INPUT'); var = self.variable_or_func_call(); prompt = None
        if self.current_token and self.current_token.type == 'COMMA':
            self.eat('COMMA'); prompt = self.expr()
        return Input(var, prompt, token)

    def if_statement(self):
        token = self.current_token; self.eat('IF'); condition = self.expr(); self.eat('THEN')
        if_block = self.statement_list(['ELSEIF', 'ELSE', 'ENDIF']); cases = [(condition, if_block)]
        while self.current_token and self.current_token.type == 'ELSEIF':
            self.eat('ELSEIF'); condition = self.expr(); self.eat('THEN')
            cases.append((condition, self.statement_list(['ELSEIF', 'ELSE', 'ENDIF'])))
        else_case = None
        if self.current_token and self.current_token.type == 'ELSE':
            self.eat('ELSE'); else_case = self.statement_list(['ENDIF'])
        self.eat('ENDIF'); return If(cases, else_case, token)

    def while_statement(self):
        token = self.current_token; self.eat('WHILE'); condition = self.expr()
        block = self.statement_list(['WEND']); self.eat('WEND'); return While(condition, block, token)

    def for_statement(self):
        token = self.current_token; self.eat('FOR'); var = self.variable_or_func_call()
        if not isinstance(var, Var): self.error("ตัวนับใน FOR loop ต้องเป็นตัวแปรธรรมดา")
        self.eat('ASSIGN'); start_expr = self.expr(); self.eat('TO'); end_expr = self.expr()
        step_expr = Num(Token('INTEGER', 1, token.line))
        if self.current_token and self.current_token.type == 'STEP':
            self.eat('STEP'); step_expr = self.expr()
        block = self.statement_list(['NEXT']); self.eat('NEXT')
        if not self.current_token or self.current_token.type != 'ID' or self.current_token.value.lower() != var.value.lower():
            found = self.current_token.value if self.current_token and self.current_token.type != 'EOF' else "None"
            self.error(f"ตัวแปร FOR/NEXT ไม่ตรงกัน คาดหวัง '{var.value}', แต่พบ '{found}'")
        self.eat('ID'); return For(var, start_expr, end_expr, step_expr, block, token)

    def func_definition(self):
        token = self.current_token; is_async = token.type == 'ASYNC_FUNCTION'; is_jit = token.type == 'JIT_FUNCTION'
        self.eat(token.type); func_name = self.current_token.value; self.eat('ID'); self.eat('LPAREN'); params = []
        if self.current_token and self.current_token.type == 'ID':
            params.append(Var(self.current_token)); self.eat('ID')
            while self.current_token and self.current_token.type == 'COMMA':
                self.eat('COMMA'); params.append(Var(self.current_token)); self.eat('ID')
        self.eat('RPAREN'); block = self.statement_list(['ENDFUNCTION']); self.eat('ENDFUNCTION')
        return FuncDef(func_name, params, block, token, is_async, is_jit)

    def return_statement(self):
        token = self.current_token; self.eat('RETURN'); return Return(self.expr(), token)

    def dim_statement(self):
        token = self.current_token; self.eat('DIM'); var_token = self.current_token; self.eat('ID'); self.eat('LPAREN')
        size_exprs = [self.expr()]
        while self.current_token and self.current_token.type == 'COMMA':
            self.eat('COMMA'); size_exprs.append(self.expr())
        self.eat('RPAREN'); return Dim(var_token, size_exprs, token)

    def data_statement(self):
        token = self.current_token; self.eat('DATA'); values = []
        stop_tokens = {
            'LET', 'PRINT', 'INPUT', 'IF', 'WHILE', 'FOR', 'FUNCTION',
            'ASYNC_FUNCTION', 'JIT_FUNCTION', 'RETURN', 'DIM', 'DATA', 'READ',
            'RESTORE', 'RUN_ASYNC', 'AWAIT', 'ID', 'EOF', 'ELSE', 'ELSEIF',
            'WEND', 'NEXT', 'ENDFUNCTION'
        }
        while self.current_token and self.current_token.type not in stop_tokens:
            values.append(self.expr())
            if self.current_token and self.current_token.type == 'COMMA':
                self.eat('COMMA')
            else: break
        return Data(values, token)
        
    def read_statement(self):
        token = self.current_token; self.eat('READ'); variables = [self.variable_or_func_call()]
        while self.current_token and self.current_token.type == 'COMMA':
            self.eat('COMMA'); variables.append(self.variable_or_func_call())
        return Read(variables, token)

    def restore_statement(self):
        token = self.current_token; self.eat('RESTORE'); return Restore(token)

    def run_async_statement(self):
        token = self.current_token; self.eat('RUN_ASYNC'); tasks = [self.expr()]
        while self.current_token and self.current_token.type == 'COMMA':
            self.eat('COMMA'); tasks.append(self.expr())
        return RunAsync(tasks, token)

    def parse(self):
        statements = self.statement_list(['EOF'])
        if self.current_token and self.current_token.type != 'EOF':
            self.error("พบโทเค็นที่ไม่คาดคิดท้ายไฟล์")
        return Program(statements)

# --- 5. Transpiler (Momentum AST to Python Code for Numba) ---
class MomentumToPythonTranspiler:
    def transpile(self, func_node):
        self.indent_level = 1
        param_names = {p.value for p in func_node.params}
        local_vars = self._find_local_vars(func_node.block, param_names)
        init_code = ""
        for var in local_vars:
            init_code += f"{self.indent()}{var} = 0.0\n"
        body_code = "".join(self._visit(stmt) for stmt in func_node.block)
        return init_code + body_code
    def _find_local_vars(self, block, param_names):
        locals_found = set()
        for stmt in block:
            if isinstance(stmt, Assign) and isinstance(stmt.left, Var):
                if stmt.left.value not in param_names: locals_found.add(stmt.left.value)
            elif isinstance(stmt, For):
                if stmt.var.value not in param_names: locals_found.add(stmt.var.value)
        return locals_found
    def indent(self): return "    " * self.indent_level
    def _visit(self, node):
        method_name = f'_visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)
    def generic_visit(self, node): 
        raise InterpreterError(f"คำสั่งประเภท '{type(node).__name__}' ไม่รองรับภายใน JIT_FUNCTION", node)
    def _visit_BinOp(self, node):
        op_map = {'PLUS':'+', 'MINUS':'-', 'MUL':'*', 'DIV':'/', 'EQ':'==', 'NEQ':'!=', 'LT':'<', 'LTE':'<=', 'GT':'>', 'GTE':'>=', 'AND':'and', 'OR':'or'}
        return f"({self._visit(node.left)} {op_map[node.op.type]} {self._visit(node.right)})"
    def _visit_UnaryOp(self, node):
        if node.op.type == 'MINUS': return f"(-{self._visit(node.expr)})"
        if node.op.type == 'NOT': return f"(not {self._visit(node.expr)})"
        return self._visit(node.expr)
    def _visit_Num(self, node): return str(node.value)
    def _visit_Var(self, node): return node.value
    def _visit_Assign(self, node): return f"{self.indent()}{self._visit(node.left)} = {self._visit(node.right)}\n"
    def _visit_If(self, node):
        code = ""; cond, block = node.cases[0]
        code += f"{self.indent()}if {self._visit(cond)}:\n"
        self.indent_level += 1; code += "".join(self._visit(stmt) for stmt in block); self.indent_level -= 1
        for cond, block in node.cases[1:]:
            code += f"{self.indent()}elif {self._visit(cond)}:\n"
            self.indent_level += 1; code += "".join(self._visit(stmt) for stmt in block); self.indent_level -= 1
        if node.else_case:
            code += f"{self.indent()}else:\n"
            self.indent_level += 1; code += "".join(self._visit(stmt) for stmt in node.else_case); self.indent_level -= 1
        return code
    def _visit_For(self, node):
        var, start, end, step = self._visit(node.var), self._visit(node.start), self._visit(node.end), self._visit(node.step)
        end_adj = f"int({end}) + (1 if {step} > 0 else -1)"
        code = f"{self.indent()}for {var} in numba.prange(int({start}), {end_adj}, int({step})):\n"
        self.indent_level += 1; code += "".join(self._visit(stmt) for stmt in node.block); self.indent_level -= 1
        return code
    def _visit_FuncCall(self, node): return f"{node.name}({', '.join(self._visit(arg) for arg in node.args)})"
    def _visit_Return(self, node): return f"{self.indent()}return {self._visit(node.expr)}\n"
    def _visit_NoOp(self, node): return ""

# --- 6. Interpreter ---
class ReturnSignal(Exception):
    def __init__(self, value): self.value = value
class CallStack:
    def __init__(self): self.records = []
    def push(self, ar): self.records.append(ar)
    def pop(self): return self.records.pop()
    def peek(self): return self.records[-1] if self.records else None
class ActivationRecord:
    def __init__(self, name, type, nesting_level): self.name, self.type, self.nesting_level, self.members = name, type, nesting_level, {}
class Interpreter:
    def __init__(self, tree):
        self.tree = tree; self.call_stack = CallStack()
        self.call_stack.push(ActivationRecord(name='global', type='program', nesting_level=1))
        self.data_store = []; self.data_pointer = 0
        self.transpiler = MomentumToPythonTranspiler(); self.jit_functions = {}
    def error(self, message, node): raise InterpreterError(message, node)
    
    def _get_type_name(self, value):
        if isinstance(value, bool): return "BOOLEAN"
        if isinstance(value, int): return "INTEGER"
        if isinstance(value, float): return "FLOAT"
        if isinstance(value, str): return "STRING"
        if isinstance(value, list): return "ARRAY"
        return "UNKNOWN"

    def _check_numeric_operands(self, node, left, right):
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            left_type = self._get_type_name(left)
            right_type = self._get_type_name(right)
            self.error(f"ไม่สามารถใช้ตัวดำเนินการ '{node.op.value}' กับ {left_type} และ {right_type} ได้", node)

    def _check_unary_numeric(self, node, val):
        if not isinstance(val, (int, float)):
            val_type = self._get_type_name(val)
            self.error(f"ไม่สามารถใช้ตัวดำเนินการ '{node.op.value}' กับ {val_type} ได้", node)

    async def visit(self, node):
        method_name = f'visit_{type(node).__name__}'; visitor = getattr(self, method_name)
        return await visitor(node)
    async def visit_Program(self, node):
        for stmt in node.statements:
            if isinstance(stmt, FuncDef): await self.visit(stmt)
            elif isinstance(stmt, Data): await self.visit(stmt)
        for stmt in node.statements:
            if not isinstance(stmt, (FuncDef, Data)): await self.visit(stmt)
    async def visit_NoOp(self, node): pass
    async def visit_Num(self, node): return node.value
    async def visit_String(self, node): return node.value
    
    async def visit_UnaryOp(self, node):
        val = await self.visit(node.expr)
        op_type = node.op.type
        if op_type in ('MINUS', 'PLUS'):
            self._check_unary_numeric(node, val)
            return -val if op_type == 'MINUS' else +val
        if op_type == 'NOT':
            return 1 if not val else 0
    
    async def visit_BinOp(self, node):
        left = await self.visit(node.left)
        if node.op.type == 'OR': return 1 if left else (1 if await self.visit(node.right) else 0)
        if node.op.type == 'AND': return 0 if not left else (1 if await self.visit(node.right) else 0)
        
        right = await self.visit(node.right)
        op_type = node.op.type

        if op_type == 'PLUS' and (isinstance(left, str) or isinstance(right, str)):
            return str(left) + str(right)
        
        self._check_numeric_operands(node, left, right)

        if op_type == 'PLUS': return left + right
        if op_type == 'MINUS': return left - right
        if op_type == 'MUL': return left * right
        if op_type == 'DIV':
            if right == 0: self.error("หารด้วยศูนย์", node)
            return left / right
        if op_type == 'EQ': return 1 if left == right else 0
        if op_type == 'NEQ': return 1 if left != right else 0
        if op_type == 'LT': return 1 if left < right else 0
        if op_type == 'LTE': return 1 if left <= right else 0
        if op_type == 'GT': return 1 if left > right else 0
        if op_type == 'GTE': return 1 if left >= right else 0
        
    def set_variable(self, name, value, ar): ar.members[name.lower()] = value
    def get_variable(self, name, node):
        var_name = name.lower(); ar = self.call_stack.peek()
        if ar and var_name in ar.members: return ar.members[var_name]
        if ar and ar.type == 'function' and var_name in self.call_stack.records[0].members:
            return self.call_stack.records[0].members[var_name]
        self.error(f"ไม่พบตัวแปร '{name}'", node)
    def set_array_element(self, array, indices, value, node):
        target = array
        for index in indices[:-1]:
            if not (isinstance(index, int) and 0 <= index < len(target)): self.error(f"ดัชนีอาร์เรย์อยู่นอกขอบเขต", node)
            target = target[index]
        last_index = indices[-1]
        if not (isinstance(last_index, int) and 0 <= last_index < len(target)): self.error(f"ดัชนีอาร์เรย์อยู่นอกขอบเขต", node)
        target[last_index] = value
    async def get_array_element(self, array, indices, node):
        target = array
        for index in indices:
            if not isinstance(index, int): self.error(f"ดัชนีอาร์เรย์ต้องเป็น INTEGER", node)
            if not (0 <= index < len(target)): self.error(f"ดัชนีอาร์เรย์ {index} อยู่นอกขอบเขต", node)
            target = target[index]
        return 0 if target is None else target
    async def visit_Assign(self, node):
        value = await self.visit(node.right)
        if isinstance(node.left, Var): self.set_variable(node.left.value, value, self.call_stack.peek())
        elif isinstance(node.left, ArrayAccess):
            array = self.get_variable(node.left.name_token.value, node.left)
            if not isinstance(array, list): self.error(f"ตัวแปร '{node.left.name_token.value}' ไม่ใช่อาร์เรย์", node.left)
            indices = [await self.visit(idx) for idx in node.left.index_exprs]
            self.set_array_element(array, indices, value, node.left)
    async def visit_Var(self, node): return self.get_variable(node.value, node)
    async def visit_Print(self, node): print(str(await self.visit(node.expr)))
    async def visit_Input(self, node):
        prompt = str(await self.visit(node.prompt)) if node.prompt else ""
        user_input = await asyncio.to_thread(input, prompt)
        try: 
            val = float(user_input)
            val = int(val) if val.is_integer() else val
        except (ValueError, TypeError): 
            val = user_input
        
        if isinstance(node.var, Var):
            self.set_variable(node.var.value, val, self.call_stack.peek())
        elif isinstance(node.var, ArrayAccess):
            array = self.get_variable(node.var.name_token.value, node.var)
            if not isinstance(array, list): self.error(f"ตัวแปร '{node.var.name_token.value}' ไม่ใช่อาร์เรย์", node.var)
            indices = [await self.visit(idx) for idx in node.var.index_exprs]
            self.set_array_element(array, indices, val, node.var)
    async def visit_If(self, node):
        for condition, block in node.cases:
            if await self.visit(condition):
                for statement in block: await self.visit(statement)
                return
        if node.else_case:
            for statement in node.else_case: await self.visit(statement)
    async def visit_While(self, node):
        while await self.visit(node.condition):
            for statement in node.block: await self.visit(statement)
    async def visit_For(self, node):
        var_name = node.var.value; ar = self.call_stack.peek()
        start, end, step = await self.visit(node.start), await self.visit(node.end), await self.visit(node.step)
        
        if not all(isinstance(v, (int, float)) for v in [start, end, step]):
            self.error("ค่า START, END, และ STEP ของ FOR loop ต้องเป็นตัวเลข", node)

        current = start; self.set_variable(var_name, current, ar)
        while (step > 0 and current <= end) or (step < 0 and current >= end):
            for statement in node.block: await self.visit(statement)
            current += step; self.set_variable(var_name, current, ar)
    async def visit_FuncDef(self, node):
        func_name = node.name.lower()
        if node.is_jit:
            if not NUMBA_ENABLED: self.error("Numba is not installed. JIT_FUNCTION is unavailable.", node)
            py_code = self.transpiler.transpile(node); params_str = ", ".join(p.value for p in node.params)
            full_src = f"def {func_name}_impl({params_str}):\n{py_code or '    pass'}"
            try:
                ns = {'numba': numba}; exec(full_src, globals(), ns); py_func = ns[f"{func_name}_impl"]
                self.jit_functions[func_name] = numba.jit(nopython=True, parallel=True)(py_func)
            except Exception as e: self.error(f"Numba compilation failed for '{node.name}': {e}\nGenerated code:\n{full_src}", node)
        else: self.call_stack.records[0].members[func_name] = node
    
    async def visit_FuncCall(self, node):
        func_name = node.name.lower(); args = [await self.visit(arg) for arg in node.args]
        if func_name in self.jit_functions: return self.jit_functions[func_name](*args)
        if func_name in BUILTIN_FUNCTIONS: return BUILTIN_FUNCTIONS[func_name](*args)
        if func_name in ASYNC_BUILTIN_FUNCTIONS: self.error(f"ฟังก์ชัน Async '{node.name}' ต้องถูกเรียกด้วย AWAIT", node)
        
        func_def = self.get_variable(node.name, node)

        if isinstance(func_def, FuncDef):
            if func_def.is_async: self.error(f"ฟังก์ชัน Async '{node.name}' ต้องถูกเรียกด้วย AWAIT", node)
            ar = ActivationRecord(name=func_name, type='function', nesting_level=self.call_stack.peek().nesting_level + 1)
            if len(args) != len(func_def.params): self.error(f"ฟังก์ชัน '{node.name}' คาดหวัง {len(func_def.params)} อาร์กิวเมนต์ แต่ได้รับ {len(args)}", node)
            for param_node, arg_val in zip(func_def.params, args): ar.members[param_node.value.lower()] = arg_val
            self.call_stack.push(ar); return_value = None
            try:
                for statement in func_def.block: await self.visit(statement)
            except ReturnSignal as rs: return_value = rs.value
            finally: self.call_stack.pop()
            return return_value
        self.error(f"'{node.name}' ไม่ใช่ฟังก์ชันที่ถูกกำหนดไว้", node)
    
    async def visit_Return(self, node):
        current_ar = self.call_stack.peek()
        if not current_ar or current_ar.type != 'function':
            self.error("คำสั่ง RETURN สามารถใช้ได้ภายในฟังก์ชันเท่านั้น", node)
        raise ReturnSignal(await self.visit(node.expr))

    async def visit_Dim(self, node):
        ar = self.call_stack.peek(); var_name = node.var_token.value.lower()
        if var_name in ar.members or var_name in self.call_stack.records[0].members: self.error(f"ไม่สามารถประกาศขนาดอาร์เรย์ซ้ำ '{var_name}'", node)
        dims = [await self.visit(s) for s in node.size_exprs]
        for d in dims:
            if not isinstance(d, int) or d <= 0: self.error("ขนาดมิติของอาร์เรย์ต้องเป็นจำนวนเต็มบวก", node)
        def create_nested_list(dimensions):
            if not dimensions: return 0
            return [create_nested_list(dimensions[1:]) for _ in range(dimensions[0])]
        ar.members[var_name] = create_nested_list(dims)

    async def visit_ArrayAccess(self, node):
        name = node.name_token.value
        try:
            target = self.get_variable(name, node)
        except InterpreterError:
            target = None
        
        if isinstance(target, list):
            indices = [await self.visit(idx) for idx in node.index_exprs]
            return await self.get_array_element(target, indices, node)
        
        func_call_node = FuncCall(node.name_token, node.index_exprs)
        return await self.visit_FuncCall(func_call_node)

    async def visit_Data(self, node):
        for value_node in node.values: self.data_store.append(await self.visit(value_node))
    async def visit_Read(self, node):
        for var_node in node.variables:
            if self.data_pointer >= len(self.data_store): self.error("ข้อมูลใน DATA หมดแล้ว", node)
            value = self.data_store[self.data_pointer]
            temp_value_node = Num(Token("VALUE", value, var_node.token.line))
            assign_node = Assign(left=var_node, op=None, right=temp_value_node)
            await self.visit(assign_node); self.data_pointer += 1
    async def visit_Restore(self, node): self.data_pointer = 0

    async def _create_async_coroutine(self, func_call_node):
        """Helper to create a coroutine from a function call node."""
        func_name = func_call_node.name.lower()
        args = [await self.visit(arg) for arg in func_call_node.args]

        if func_name in ASYNC_BUILTIN_FUNCTIONS:
            return ASYNC_BUILTIN_FUNCTIONS[func_name](*args)
        
        func_def = self.get_variable(func_name, func_call_node)

        if isinstance(func_def, FuncDef) and func_def.is_async:
            # This is the logic to execute a user-defined async function
            async def coroutine_wrapper():
                ar = ActivationRecord(name=func_name, type='function', nesting_level=self.call_stack.peek().nesting_level + 1)
                if len(args) != len(func_def.params): self.error(f"ฟังก์ชัน '{func_name}' คาดหวัง {len(func_def.params)} อาร์กิวเมนต์ แต่ได้รับ {len(args)}", func_call_node)
                for param_node, arg_val in zip(func_def.params, args): ar.members[param_node.value.lower()] = arg_val
                self.call_stack.push(ar)
                return_value = None
                try:
                    for statement in func_def.block: await self.visit(statement)
                except ReturnSignal as rs: return_value = rs.value
                finally: self.call_stack.pop()
                return return_value
            return coroutine_wrapper()

        self.error(f"ฟังก์ชัน '{func_name}' ไม่ใช่ฟังก์ชัน async ที่สามารถใช้กับ AWAIT หรือ RUN ASYNC ได้", func_call_node)

    async def visit_Await(self, node):
        if not isinstance(node.expr, ArrayAccess): self.error("AWAIT สามารถใช้ได้กับการเรียกฟังก์ชัน async เท่านั้น", node)
        func_call_node = FuncCall(node.expr.name_token, node.expr.index_exprs)
        coro = await self._create_async_coroutine(func_call_node)
        return await coro
    
    # --- START OF BUG FIX for RUN ASYNC ---
    async def visit_RunAsync(self, node):
        tasks = []
        for task_call_node in node.tasks:
            if not isinstance(task_call_node, ArrayAccess):
                self.error("RUN ASYNC สามารถใช้ได้กับการเรียกฟังก์ชัน async เท่านั้น", task_call_node)
            
            # Convert ArrayAccess to FuncCall to properly evaluate
            func_call = FuncCall(task_call_node.name_token, task_call_node.index_exprs)
            
            # Create the coroutine using our helper
            coro = await self._create_async_coroutine(func_call)
            
            # Create a task from the coroutine
            tasks.append(asyncio.create_task(coro))
        
        if tasks:
            await asyncio.gather(*tasks)
    # --- END OF BUG FIX for RUN ASYNC ---

    async def interpret(self):
        if self.tree is None: return
        await self.visit(self.tree)
        
# --- 7. Built-in Functions ---
def builtin_type(value):
    if isinstance(value, int): return "INTEGER"
    if isinstance(value, float): return "FLOAT"
    if isinstance(value, str): return "STRING"
    if isinstance(value, list): return "ARRAY"
    return "UNKNOWN"
async def builtin_sleep(seconds): await asyncio.sleep(float(seconds))
BUILTIN_FUNCTIONS = {
    'time': time.time, 'str': str, 'int': int, 'float': float, 'len': len, 'abs': abs, 
    'round': round, 'type': builtin_type, 'sqrt': math.sqrt, 'gfx_init': gfx_init, 
    'gfx_set_color': gfx_set_color, 'gfx_draw_line': gfx_draw_line, 
    'gfx_draw_rect': gfx_draw_rect, 'gfx_draw_circle': gfx_draw_circle, 
    'gfx_update': gfx_update, 'gfx_wait': gfx_wait
}
ASYNC_BUILTIN_FUNCTIONS = {'sleep': builtin_sleep}

# --- 8. Main Execution Block ---
def run_momentum(code):
    """Lexes, parses, and interprets the given Momentum code."""
    if not code.strip(): return
    try:
        lexer = Lexer(code); tokens = lexer.tokenize_all()
        parser = Parser(tokens); tree = parser.parse()
        interpreter = Interpreter(tree)
        asyncio.run(interpreter.interpret())
    except MomentumError as e:
        print(f"\nข้อผิดพลาด Momentum: {e}", file=sys.stderr)
    except Exception as e:
        print(f"\nข้อผิดพลาดร้ายแรงของตัวแปลภาษา: {e}", file=sys.stderr)
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, 'r', encoding="utf-8-sig") as f:
                source_code = f.read()
        except FileNotFoundError:
            print(f"ข้อผิดพลาด: ไม่พบไฟล์ '{filename}'", file=sys.stderr)
            sys.exit(1)
    else:
        print("การใช้งาน: python intp.py your_program.mn")
        source_code = ""
    
    if source_code:
        print("--- กำลังรันโค้ด Momentum ---")
        run_momentum(source_code)
        print("---------------------------")