import sys
import time
import math
import os
import asyncio
import traceback
import operator
import random
import itertools
import re
import locale
import json
from enum import Enum, auto
from pathlib import Path
from collections import Counter, namedtuple

try:
    import numba
    NUMBA_ENABLED = True
except ImportError:
    NUMBA_ENABLED = False

try:
    import tkinter
    GFX_ENABLED = True
except ImportError:
    GFX_ENABLED = False
    
import numpy as np

try:
    import colorama
    from colorama import Fore, Style, init
    colorama_enabled = True
    init(autoreset=True)
except ImportError:
    colorama_enabled = False

def detect_language():
    try:
        lang_code, _ = locale.getdefaultlocale()
        if lang_code and lang_code.lower().startswith('th'): return 'th'
    except Exception: pass
    return 'en'

LANG = detect_language()

MESSAGES = {
    'en': {
        'error_syntax': "Syntax Error", 'error_runtime': "Runtime Error", 'error_unhandled_vm': "Unhandled Internal VM Error",
        'error_file_not_found': "Error: File not found '{filename}'", 'error_import_failed': "Cannot import module: File not found '{path}'",
        'error_out_of_data': "Out of DATA", 'error_jit_failed': "JIT pre-compilation failed: {e}",
        'usage_message': "Usage: python {script_name} [your_program.mn]", 'repl_welcome': "Momentum Language. Type 'exit()' to quit.",
        'running_header': "--- Running Momentum Language from '{filename}' ---", 'run_success': "--- Execution successful ---",
        'run_finished_divider': "---------------------------------------------------------",
        'p_err_unexpected_eof': "Unexpected end of file", 'p_err_unexpected_token': "Unexpected token '{value}'",
        'p_err_expected_token': "Expected token {expected}, but found {found}", 'p_err_invalid_factor': "Invalid syntax for factor, found token {token}",
        'p_err_pipe_rhs_not_func': "Right-hand side of Pipe Operator (|>) must be a function",
        'p_err_invalid_stmt_start': "Invalid statement starting with '{value}'. To assign a value, use LET or to call a function, use its name directly.",
        'p_err_import_expects_string': "Expected a filename (in quotes) after IMPORT", 'p_err_invalid_assign_target': "Invalid assignment target",
        'p_err_for_counter_not_var': "Counter in FOR loop must be a simple variable",
        'p_err_for_next_mismatch': "FOR/NEXT variable mismatch. Expected '{expected}', but found '{found}'",
        'p_err_data_expects_number': "Expected a number after minus sign in DATA",
        'p_err_data_literal_only': "DATA statement can only contain literal numbers and strings",
        'p_err_var_already_declared': "Variable '{name}' already declared in this scope", 'p_err_break_outside_loop': "'BREAK' can only be used inside a loop",
        'p_err_continue_outside_loop': "'CONTINUE' can only be used inside a loop", 'p_err_dict_key_must_be_string': "Dictionary keys must be strings",
        'p_err_unmatched_brace_in_fstring': "Unmatched '{{' or '}}' in f-string",
        'p_err_empty_expr_in_fstring': "Empty expression within {} in f-string",
        'p_err_switch_expects_var': "SWITCH statement requires a variable or expression to check against",
        'p_err_case_after_default': "'CASE' statement cannot appear after 'DEFAULT'",
        'rt_err_tkinter_not_found': "Graphics module requires tkinter, which was not found", 'rt_err_gfx_not_init': "Graphics not initialized. Call gfx_init() first",
        'rt_err_var_not_found': "Variable '{name}' not found",
        'rt_err_type_error_op': "TypeError: Cannot perform '{op}' on a {type_a} and a {type_b}",
        'rt_err_unsupported_op_matrix': "Operator {op_name} is not supported for matrices",
        'rt_err_func_arity_mismatch': "Function '{name}' expected {expected} arguments but received {received}",
        'rt_err_cannot_call_async': "Cannot call async function '{name}' directly. Use 'await'",
        'rt_err_cannot_call_type': "Cannot call or access data of type '{type_name}'", 'rt_err_unknown_builtin': "Unknown built-in function: {name}",
        'rt_err_mat_inverse_failed': "Cannot compute inverse: {e}", 'rt_err_mat_solve_failed': "Cannot solve equation system: {e}",
        'rt_err_not_subscriptable': "Type '{type_name}' is not subscriptable (cannot use [] or () on it)",
        'rt_err_invalid_key_type': "Invalid key type for {container_type}: {key_type}", 'rt_err_assertion_failed': "Assertion failed: {message}",
        'hint_concat_header': "Hint: To combine text with other data types, you must first convert them", 'hint_concat_body': "      to a STRING using the `str()` function.",
        'hint_concat_example': "      Example: `print(f\"Value is {my_number}\")`",
        'hint_var_undefined_header': "Hint: The variable '{name}' is not defined in the current scope.",
        'hint_var_undefined_body': "      Make sure it's declared with `LET` before use and check for typos.",
        'hint_index_oob_header': "Hint: You are trying to access an array element that does not exist.",
        'hint_index_oob_body': "      Check your loop bounds and array indices. Remember that array indexing starts at 0.",
        'traceback_header': "Traceback (most recent call last):",
    },
    'th': {
        'error_syntax': "ข้อผิดพลาดทางไวยากรณ์", 'error_runtime': "ข้อผิดพลาดขณะทำงาน", 'error_unhandled_vm': "ข้อผิดพลาดภายใน VM ที่ไม่รู้จัก",
        'error_file_not_found': "ข้อผิดพลาด: ไม่พบไฟล์ '{filename}'", 'error_import_failed': "ไม่สามารถ import โมดูลได้: ไม่พบไฟล์ '{path}'",
        'error_out_of_data': "ข้อมูลหมดแล้ว (Out of DATA)", 'error_jit_failed': "การคอมพายล์ JIT ล่วงหน้าล้มเหลว: {e}",
        'usage_message': "การใช้งาน: python {script_name} [your_program.mn]", 'repl_welcome': "Momentum Language. พิมพ์ 'exit()' เพื่อออก",
        'running_header': "--- กำลังรันโค้ด Momentum Language จาก '{filename}' ---", 'run_success': "--- การรันโปรแกรมสำเร็จ ---",
        'run_finished_divider': "---------------------------------------------------------",
        'p_err_unexpected_eof': "พบจุดสิ้นสุดของไฟล์ที่ไม่คาดคิด", 'p_err_unexpected_token': "โทเค็นที่ไม่คาดคิด '{value}'",
        'p_err_expected_token': "คาดหวังโทเค็น {expected}, แต่พบ {found}", 'p_err_invalid_factor': "ไวยากรณ์ไม่ถูกต้องสำหรับ factor, พบโทเค็น {token}",
        'p_err_pipe_rhs_not_func': "ด้านขวาของ Pipe Operator (|>) ต้องเป็นฟังก์ชัน",
        'p_err_invalid_stmt_start': "คำสั่งไม่ถูกต้อง เริ่มต้นด้วย '{value}' หากต้องการกำหนดค่า ให้ใช้ LET หรือถ้าต้องการเรียกฟังก์ชัน ให้ใช้ชื่อฟังก์ชันได้เลย",
        'p_err_import_expects_string': "คาดหวังชื่อไฟล์ (ในเครื่องหมายคำพูด) หลังคำสั่ง IMPORT", 'p_err_invalid_assign_target': "เป้าหมายการกำหนดค่าไม่ถูกต้อง",
        'p_err_for_counter_not_var': "ตัวนับใน FOR loop ต้องเป็นตัวแปรธรรมดา",
        'p_err_for_next_mismatch': "ตัวแปร FOR/NEXT ไม่ตรงกัน คาดหวัง '{expected}', แต่พบ '{found}'",
        'p_err_data_expects_number': "คาดหวังตัวเลขหลังเครื่องหมายลบใน DATA",
        'p_err_data_literal_only': "DATA statement สามารถมีได้แค่ตัวเลขและข้อความเท่านั้น",
        'p_err_var_already_declared': "ตัวแปร '{name}' ถูกประกาศในขอบเขตนี้แล้ว", 'p_err_break_outside_loop': "คำสั่ง 'BREAK' สามารถใช้ได้ภายใน Loop เท่านั้น",
        'p_err_continue_outside_loop': "คำสั่ง 'CONTINUE' สามารถใช้ได้ภายใน Loop เท่านั้น", 'p_err_dict_key_must_be_string': "Key ของ Dictionary ต้องเป็นข้อความ (String) เท่านั้น",
        'p_err_unmatched_brace_in_fstring': "พบวงเล็บปีกกาไม่ครบคู่ '{{' หรือ '}}' ใน f-string",
        'p_err_empty_expr_in_fstring': "นิพจน์ภายใน {{}} ของ f-string ว่างเปล่า",
        'p_err_switch_expects_var': "คำสั่ง SWITCH ต้องการตัวแปรหรือนิพจน์เพื่อใช้ในการตรวจสอบ",
        'p_err_case_after_default': "คำสั่ง 'CASE' ไม่สามารถอยู่หลัง 'DEFAULT' ได้",
        'rt_err_tkinter_not_found': "โมดูลกราฟิกต้องการ tkinter ซึ่งไม่พบ", 'rt_err_gfx_not_init': "กราฟิกยังไม่ได้เริ่มต้น เรียกใช้ gfx_init() ก่อน",
        'rt_err_var_not_found': "ไม่พบตัวแปร '{name}'",
        'rt_err_type_error_op': "TypeError: ไม่สามารถดำเนินการ '{op}' กับ {type_a} และ {type_b} ได้",
        'rt_err_unsupported_op_matrix': "ตัวดำเนินการ {op_name} ไม่รองรับสำหรับเมทริกซ์",
        'rt_err_func_arity_mismatch': "ฟังก์ชัน '{name}' คาดหวัง {expected} อาร์กิวเมนต์ แต่ได้รับ {received}",
        'rt_err_cannot_call_async': "ไม่สามารถเรียกฟังก์ชัน async '{name}' โดยตรงได้. ใช้ 'await'",
        'rt_err_cannot_call_type': "ไม่สามารถเรียกหรือเข้าถึงข้อมูลของ '{type_name}' ได้", 'rt_err_unknown_builtin': "ฟังก์ชันในตัวที่ไม่รู้จัก: {name}",
        'rt_err_mat_inverse_failed': "ไม่สามารถหาอินเวอร์สได้: {e}", 'rt_err_mat_solve_failed': "ไม่สามารถแก้สมการได้: {e}",
        'rt_err_not_subscriptable': "ข้อมูลชนิด '{type_name}' ไม่สามารถเข้าถึงด้วย [] หรือ () ได้",
        'rt_err_invalid_key_type': "ชนิดของ Key ไม่ถูกต้องสำหรับ {container_type}: {key_type}", 'rt_err_assertion_failed': "การยืนยันล้มเหลว: {message}",
        'hint_concat_header': "คำแนะนำ: หากต้องการรวมข้อความกับข้อมูลชนิดอื่น คุณต้องแปลงข้อมูลนั้น", 'hint_concat_body': "      ให้เป็น STRING โดยใช้ฟังก์ชัน `str()` ก่อน",
        'hint_concat_example': "      ตัวอย่าง: `print(f\"ค่าคือ {my_number}\")`",
        'hint_var_undefined_header': "คำแนะนำ: ตัวแปร '{name}' ยังไม่ได้ถูกกำหนดค่าในขอบเขตปัจจุบัน",
        'hint_var_undefined_body': "      โปรดตรวจสอบว่ามีการประกาศด้วย `LET` ก่อนใช้งาน และตรวจสอบการสะกด",
        'hint_index_oob_header': "คำแนะนำ: คุณกำลังพยายามเข้าถึงข้อมูลในอาร์เรย์ตำแหน่งที่ไม่มีอยู่",
        'hint_index_oob_body': "      ตรวจสอบขอบเขตของลูปและค่าดัชนี (index) โดยจำไว้ว่าดัชนีของอาร์เรย์เริ่มที่ 0",
        'traceback_header': "Traceback (การเรียกย้อนหลังล่าสุด):",
    }
}

def t(key, **kwargs):
    lang_msgs = MESSAGES.get(LANG, MESSAGES['en'])
    msg_template = lang_msgs.get(key, MESSAGES['en'].get(key, f"<{key}>"))
    return msg_template.format(**kwargs) if kwargs else msg_template

GFX_GLOBALS = {"window": None, "canvas": None, "color": "black"}
def gfx_init(width=640, height=480, title="Momentum Graphics"):
    if not GFX_ENABLED: raise InterpreterError(t('rt_err_tkinter_not_found'), None)
    if GFX_GLOBALS["window"]: GFX_GLOBALS["window"].destroy()
    window = tkinter.Tk(); window.title(title)
    canvas = tkinter.Canvas(window, width=width, height=height, bg="white"); canvas.pack()
    window.update(); GFX_GLOBALS["window"], GFX_GLOBALS["canvas"] = window, canvas
    return 1
def gfx_set_color(r, g, b):
    if not GFX_GLOBALS["canvas"]: raise InterpreterError(t('rt_err_gfx_not_init'), None)
    GFX_GLOBALS["color"] = f'#{int(r):02x}{int(g):02x}{int(b):02x}'; return GFX_GLOBALS["color"]
def gfx_draw_line(x1, y1, x2, y2):
    if not GFX_GLOBALS["canvas"]: raise InterpreterError(t('rt_err_gfx_not_init'), None)
    GFX_GLOBALS["canvas"].create_line(x1, y1, x2, y2, fill=GFX_GLOBALS["color"])
def gfx_draw_rect(x, y, width, height, fill=0):
    if not GFX_GLOBALS["canvas"]: raise InterpreterError(t('rt_err_gfx_not_init'), None)
    fill_color = GFX_GLOBALS["color"] if fill else ""; GFX_GLOBALS["canvas"].create_rectangle(x, y, x + width, y + height, fill=fill_color, outline=GFX_GLOBALS["color"])
def gfx_draw_circle(x, y, radius, fill=0):
    if not GFX_GLOBALS["canvas"]: raise InterpreterError(t('rt_err_gfx_not_init'), None)
    fill_color = GFX_GLOBALS["color"] if fill else ""; GFX_GLOBALS["canvas"].create_oval(x - radius, y - radius, x + radius, y + radius, fill=fill_color, outline=GFX_GLOBALS["color"])
def gfx_update():
    if GFX_GLOBALS["window"]: GFX_GLOBALS["window"].update()
def gfx_wait():
    if not GFX_GLOBALS["window"]: return
    try: GFX_GLOBALS["window"].mainloop()
    except (tkinter.TclError, KeyboardInterrupt): GFX_GLOBALS["window"], GFX_GLOBALS["canvas"] = None, None

class MomentumExit(BaseException):
    def __init__(self, code): self.code = code
class MomentumError(Exception): pass
class ParserError(MomentumError):
    def __init__(self, message, token):
        self.line = token.line if token else '?'; self.raw_message = message; self.token = token
        super().__init__(f"[Line {self.line}] Syntax Error: {message}")
class InterpreterError(MomentumError):
    def __init__(self, message, node_or_line, stack_trace=None):
        line = '?'
        if isinstance(node_or_line, int): line = node_or_line
        elif node_or_line and hasattr(node_or_line, 'token') and hasattr(node_or_line.token, 'line'): line = node_or_line.token.line
        self.raw_message = message; self.line = line; self.stack_trace = stack_trace or []
        super().__init__(f"[Line {line}] {message}")

def format_momentum_error(error, source_lines):
    if isinstance(error, MomentumExit): return
    if not isinstance(error, (ParserError, InterpreterError)):
        print(f"\n--- {t('error_unhandled_vm')} ---", file=sys.stderr); traceback.print_exc()
        return
    error_type = t('error_syntax') if isinstance(error, ParserError) else t('error_runtime')
    line_num = error.line; message = error.raw_message
    print(f"\n--- Momentum {error_type} ---", file=sys.stderr); print(f"[Line {line_num}] {message}\n", file=sys.stderr)
    if line_num != '?' and line_num > 0 and source_lines:
        line_index = line_num - 1
        if 0 <= line_index < len(source_lines):
            code_line = source_lines[line_index].rstrip()
            print(f"  {line_num: >3} | {code_line}", file=sys.stderr); print(f"      | {'^' * len(code_line)}", file=sys.stderr)
    if "Cannot add a STRING" in message or "unsupported operand" in message or "TypeError" in message:
        print(f"\n{t('hint_concat_header')}", file=sys.stderr); print(t('hint_concat_body'), file=sys.stderr); print(t('hint_concat_example'), file=sys.stderr)
    elif t('rt_err_var_not_found', name='').split("'")[0] in message or "is not defined" in message:
        try: var_name = message.split("'")[1]; print(f"\n{t('hint_var_undefined_header', name=var_name)}", file=sys.stderr); print(t('hint_var_undefined_body'), file=sys.stderr)
        except IndexError: pass
    elif "out of bounds" in message or "index" in message.lower():
        print(f"\n{t('hint_index_oob_header')}", file=sys.stderr); print(t('hint_index_oob_body'), file=sys.stderr)
    if hasattr(error, 'stack_trace') and error.stack_trace:
        print(f"\n{t('traceback_header')}", file=sys.stderr)
        for frame_info in reversed(error.stack_trace):
            print(f'  File "{frame_info["file"]}", line {frame_info["line"]}, in {frame_info["context"]}', file=sys.stderr)
    print("-" * (len(error_type) + 20), file=sys.stderr)

Token = namedtuple('Token', ['type', 'value', 'line'])
class Lexer:
    ### --- CHANGE START (1/8): Add FSTRING tokens --- ###
    _token_specs = [
        ('SKIP', r'[ \t]+|//.*'), ('NEWLINE', r'\n'), ('FLOAT', r'\d+\.\d*|\.\d+'), ('INTEGER', r'\d+'),
        ('FSTRING_SQ', r"f'(?:[^'\\]|\\.)*'"), 
        ('FSTRING_DQ', r'f"(?:[^"\\]|\\.)*"'), 
        ('STRING_SQ', r"'(?:[^'\\]|\\.)*'"),
        ('STRING_DQ', r'"(?:[^"\\]|\\.)*"'), 
        ('PIPE', r'\|>'), ('EQ', r'=='), ('NEQ', r'!='), ('GTE', r'>='),
        ('LTE', r'<='), ('ASSIGN', r'='), ('PLUS', r'\+'), ('MINUS', r'-'), ('MUL', r'\*'), ('DIV', r'/'),
        ('LPAREN', r'\('), ('RPAREN', r'\)'), ('LBRACE', r'\{'), ('RBRACE', r'\}'), ('LBRACKET', r'\['),
        ('RBRACKET', r'\]'), ('COMMA', r','), ('COLON', r':'), ('SEMICOLON', r';'), ('GT', r'>'), ('LT', r'<'),
        ('ID', r'[A-Za-z_][A-Za-z0-9_]*'), ('MISMATCH', r'.'),
    ]
    ### --- CHANGE END (1/8) --- ###
    _keywords = {
        'LET': 'LET', 'PRINT': 'PRINT', 'INPUT': 'INPUT', 'IF': 'IF', 'THEN': 'THEN',
        'ELSE': 'ELSE', 'WHILE': 'WHILE', 'WEND': 'WEND', 'FOR': 'FOR', 'TO': 'TO',
        'STEP': 'STEP', 'NEXT': 'NEXT', 'FUNCTION': 'FUNCTION', 'RETURN': 'RETURN', 'DIM': 'DIM',
        'DATA': 'DATA', 'READ': 'READ', 'RESTORE': 'RESTORE', 'AND': 'AND', 'OR': 'OR', 'NOT': 'NOT',
        'AWAIT': 'AWAIT', 'IMPORT': 'IMPORT', 'ENDIF': 'ENDIF', 'ELSEIF': 'ELSEIF', 'ENDFUNCTION': 'ENDFUNCTION',
        'JIT_FUNCTION': 'JIT_FUNCTION', 'ASYNC_FUNCTION': 'ASYNC_FUNCTION', 'RUN_ASYNC': 'RUN_ASYNC',
        'BREAK': 'BREAK', 'CONTINUE': 'CONTINUE', 'TRY': 'TRY', 'CATCH': 'CATCH', 'FINALLY': 'FINALLY',
        'ENDTRY': 'ENDTRY', 'SWITCH': 'SWITCH', 'CASE': 'CASE', 'DEFAULT': 'DEFAULT', 'ENDSWITCH': 'ENDSWITCH',
        'EACH': 'EACH', 'IN': 'IN', 'DEBUG': 'DEBUG'
    }
    _multi_word_map = {
        re.compile(r'\bEND\s+IF\b', re.IGNORECASE): 'ENDIF', re.compile(r'\bELSE\s+IF\b', re.IGNORECASE): 'ELSEIF',
        re.compile(r'\bEND\s+FUNCTION\b', re.IGNORECASE): 'ENDFUNCTION', re.compile(r'\bJIT\s+FUNCTION\b', re.IGNORECASE): 'JIT_FUNCTION',
        re.compile(r'\bASYNC\s+FUNCTION\b', re.IGNORECASE): 'ASYNC_FUNCTION', re.compile(r'\bRUN\s+ASYNC\b', re.IGNORECASE): 'RUN_ASYNC',
        re.compile(r'\bEND\s+TRY\b', re.IGNORECASE): 'ENDTRY', re.compile(r'\bEND\s+SWITCH\b', re.IGNORECASE): 'ENDSWITCH'
    }
    def __init__(self, text):
        processed_text = text
        for pattern, replacement in self._multi_word_map.items(): processed_text = pattern.sub(replacement, processed_text)
        self.text = processed_text; self.line = 1; self._tokenizer = self._create_tokenizer()
    def _create_tokenizer(self):
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in self._token_specs)
        return re.finditer(tok_regex, self.text)
    def _process_string_literal(self, value):
        s = value[1:-1]
        return (s.replace('\\n', '\n').replace('\\t', '\t').replace('\\"', '"').replace("\\'", "'").replace('\\\\', '\\'))
    def tokenize_all(self):
        tokens, line = [], 1
        for mo in self._tokenizer:
            kind, value = mo.lastgroup, mo.group()
            if kind == 'NEWLINE': line += 1; continue
            if kind == 'SKIP': continue
            if kind == 'MISMATCH': raise MomentumError(f"[Line {line}] Lexer Error: Invalid character '{value}'")
            if kind == 'ID':
                upper_val = value.upper(); kind = self._keywords.get(upper_val, 'ID')
                if kind != 'ID': value = upper_val
            elif kind == 'FLOAT': value = float(value)
            elif kind == 'INTEGER': value = int(value)
            elif kind in ('STRING_DQ', 'STRING_SQ'):
                value = self._process_string_literal(value)
                kind = 'STRING'
            ### --- CHANGE START (2/8): Handle FSTRING tokens --- ###
            elif kind in ('FSTRING_DQ', 'FSTRING_SQ'):
                # We pass the full f-string with quotes to the parser
                value = value[1:] # Strip leading 'f'
                kind = 'FSTRING'
            ### --- CHANGE END (2/8) --- ###
            tokens.append(Token(kind, value, line))
        tokens.append(Token('EOF', None, line)); return tokens

class AST: pass
class BinOp(AST):
    def __init__(self, left, op, right): self.left, self.op, self.right, self.token = left, op, right, op
class UnaryOp(AST):
    def __init__(self, op, expr): self.op, self.expr, self.token = op, expr, op
class Num(AST):
    def __init__(self, token): self.token, self.value = token, token.value
class String(AST):
    def __init__(self, token): self.token, self.value = token, token.value
### --- CHANGE START (3/8): Add FString AST node and modify SubscriptAccess --- ###
class FString(AST):
    def __init__(self, parts, token): self.parts, self.token = parts, token
class SubscriptAccess(AST):
    def __init__(self, primary, index_exprs, token): self.primary, self.index_exprs, self.token = primary, index_exprs, token
### --- CHANGE END (3/8) --- ###
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
        self.name, self.params, self.block, self.token = name, params, block, token; self.is_async, self.is_jit = is_async, is_jit
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
    def __init__(self, name_token, index_exprs): self.name_token, self.index_exprs, self.token = name_token, index_exprs, self.token
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
class Import(AST):
    def __init__(self, filename_token, token): self.filename_token, self.token = filename_token, token
class Break(AST):
    def __init__(self, token): self.token = token
class Continue(AST):
    def __init__(self, token): self.token = token
class DictLiteral(AST):
    def __init__(self, pairs, token): self.pairs, self.token = pairs, token
class Try(AST):
    def __init__(self, try_block, catch_var, catch_block, finally_block, token):
        self.try_block, self.catch_var, self.catch_block, self.finally_block, self.token = try_block, catch_var, catch_block, finally_block, token
class Switch(AST):
    def __init__(self, expr, cases, default_case, token):
        self.expr, self.cases, self.default_case, self.token = expr, cases, default_case, token
class ArrayLiteral(AST):
    def __init__(self, elements, token): self.elements, self.token = elements, token
class ForEach(AST):
    def __init__(self, var_token, collection, block, token): self.var_token, self.collection, self.block, self.token = var_token, collection, block, token
class Debug(AST):
    def __init__(self, expr, expr_str, token): self.expr, self.expr_str, self.token = expr, expr_str, token
class Declare(AST):
    def __init__(self, var_node, token):
        self.var_node = var_node
        self.token = token

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens; self.pos = 0; self.current_token = tokens[0]
        self.source_text = "".join(str(t.value) if t.type not in ('STRING', 'FSTRING') else f'"{t.value}"' for t in tokens if t.type != 'EOF')

    def error(self, message): raise ParserError(message, self.current_token)
    def eat(self, token_type):
        if self.current_token and self.current_token.type == token_type:
            self.pos += 1; self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None
        else: self.error(t('p_err_expected_token', expected=token_type, found=self.current_token.type if self.current_token else 'None'))

    ### --- CHANGE START (4/8): Add f-string parsing logic --- ###
    def parse_fstring(self, token):
        parts, current_part = [], ""
        # The lexer passes the string with quotes, e.g., '"hello {x}"'
        text = token.value[1:-1]
        i = 0
        while i < len(text):
            if text[i] == '{':
                if i + 1 < len(text) and text[i+1] == '{':
                    current_part += '{'
                    i += 2
                    continue

                if current_part:
                    parts.append(String(Token('STRING', current_part, token.line)))
                    current_part = ""

                i += 1
                expr_start = i
                brace_depth = 1
                while i < len(text) and brace_depth > 0:
                    if text[i] == '{': brace_depth += 1
                    elif text[i] == '}': brace_depth -= 1
                    i += 1
                
                if brace_depth != 0: self.error(t('p_err_unmatched_brace_in_fstring'))
                
                expr_text = text[expr_start : i-1]
                if not expr_text.strip(): self.error(t('p_err_empty_expr_in_fstring'))

                # Parse the inner expression using a new lexer/parser
                expr_parser = Parser(Lexer(expr_text).tokenize_all())
                parts.append(expr_parser.expr())
            
            elif text[i] == '}':
                if i + 1 < len(text) and text[i+1] == '}':
                    current_part += '}'
                    i += 2
                    continue
                self.error(t('p_err_unmatched_brace_in_fstring'))
            else:
                current_part += text[i]
                i += 1

        if current_part:
            parts.append(String(Token('STRING', current_part, token.line)))

        return FString(parts, token)
    ### --- CHANGE END (4/8) --- ###

    def factor(self):
        token = self.current_token
        if token.type in ('INTEGER', 'FLOAT'): self.eat(token.type); return Num(token)
        if token.type == 'STRING': self.eat('STRING'); return String(token)
        ### --- CHANGE START (5/8): Handle FSTRING token in parser --- ###
        if token.type == 'FSTRING': self.eat('FSTRING'); return self.parse_fstring(token)
        ### --- CHANGE END (5/8) --- ###
        if token.type == 'LBRACKET':
            self.eat('LBRACKET')
            elements = []
            if self.current_token.type != 'RBRACKET':
                elements.append(self.expr())
                while self.current_token.type == 'COMMA':
                    self.eat('COMMA')
                    elements.append(self.expr())
            self.eat('RBRACKET')
            return ArrayLiteral(elements, token)
        if token.type == 'LBRACE':
            self.eat('LBRACE'); pairs = []
            if self.current_token.type != 'RBRACE':
                while True:
                    if self.current_token.type != 'STRING': self.error(t('p_err_dict_key_must_be_string'))
                    key_node = String(self.current_token); self.eat('STRING'); self.eat('COLON'); value_node = self.expr()
                    pairs.append((key_node, value_node))
                    if self.current_token.type != 'COMMA': break
                    self.eat('COMMA')
            self.eat('RBRACE'); return DictLiteral(pairs, token)
        if token.type == 'LPAREN': self.eat('LPAREN'); node = self.expr(); self.eat('RPAREN'); return node
        if token.type == 'ID': return self.variable_or_func_call()
        if token.type == 'AWAIT': self.eat('AWAIT'); return Await(self.expr(), token)
        self.error(t('p_err_invalid_factor', token=token))
    def primary(self):
        ### --- CHANGE START (6/8): Modify primary to call the new variable/func parser --- ###
        # This simplifies the chain and ensures subscript parsing happens in the right place
        return self.unary()
        ### --- CHANGE END (6/8) --- ###
    def unary(self):
        token = self.current_token
        if token.type in ('PLUS', 'MINUS', 'NOT'): self.eat(token.type); return UnaryOp(op=token, expr=self.unary())
        return self.factor()
    def term(self):
        node = self.primary()
        while self.current_token and self.current_token.type in ('MUL', 'DIV'):
            token = self.current_token; self.eat(token.type); node = BinOp(left=node, op=token, right=self.primary())
        return node
    def arith_expr(self):
        node = self.term()
        while self.current_token and self.current_token.type in ('PLUS', 'MINUS'):
            token = self.current_token; self.eat(token.type); node = BinOp(left=node, op=token, right=self.term())
        return node
    def comparison_expr(self):
        node = self.arith_expr()
        while self.current_token and self.current_token.type in ('EQ','NEQ','LT','LTE','GT','GTE'):
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
    def pipe_expr(self):
        node = self.logic_or_expr()
        while self.current_token and self.current_token.type == 'PIPE':
            self.eat('PIPE')
            right = self.logic_or_expr()
            if isinstance(right, Var):
                right = FuncCall(name_token=right.token, args=[])
            elif not isinstance(right, FuncCall):
                self.error(t('p_err_pipe_rhs_not_func'))
            right.args.insert(0, node)
            node = right
        return node
    def expr(self): return self.pipe_expr()

    ### --- CHANGE START (7/8): Parse multi-dimensional indexing --- ###
    def variable_or_func_call(self):
        name_token = self.current_token
        self.eat('ID')
        node = Var(name_token)
        while self.current_token and self.current_token.type in ('LPAREN', 'LBRACKET'):
            if self.current_token.type == 'LPAREN':
                # Function call parsing
                self.eat('LPAREN')
                args = []
                if self.current_token.type != 'RPAREN':
                    args.append(self.expr())
                    while self.current_token.type == 'COMMA':
                        self.eat('COMMA')
                        args.append(self.expr())
                self.eat('RPAREN')
                node = FuncCall(node.token, args)
            elif self.current_token.type == 'LBRACKET':
                # Subscript (array/dict) access parsing
                token = self.current_token
                self.eat('LBRACKET')
                index_exprs = [self.expr()] # Parse the first index
                # Parse subsequent indices separated by commas
                while self.current_token.type == 'COMMA':
                    self.eat('COMMA')
                    index_exprs.append(self.expr())
                self.eat('RBRACKET')
                node = SubscriptAccess(node, index_exprs, token)
        return node
    ### --- CHANGE END (7/8) --- ###

    def statement_list(self, end_tokens):
        statements = []
        while self.current_token and self.current_token.type not in end_tokens:
            statements.append(self.statement())
            while self.current_token and self.current_token.type == 'SEMICOLON':
                self.eat('SEMICOLON')
        return statements or [NoOp()]
    def statement(self):
        if not self.current_token or self.current_token.type == 'EOF': self.error(t('p_err_unexpected_eof'))
        tok_type = self.current_token.type; dispatch = {
            'LET': self.assignment_statement, 'PRINT': self.print_statement, 'INPUT': self.input_statement, 
            'IF': self.if_statement, 'WHILE': self.while_statement, 'FOR': self.for_statement, 
            'FUNCTION': self.func_definition, 'ASYNC_FUNCTION': self.func_definition, 'JIT_FUNCTION': self.func_definition,
            'RETURN': self.return_statement, 'DIM': self.dim_statement, 'DATA': self.data_statement,
            'READ': self.read_statement, 'RESTORE': self.restore_statement, 'RUN_ASYNC': self.run_async_statement,
            'IMPORT': self.import_statement, 'BREAK': self.break_statement, 'CONTINUE': self.continue_statement,
            'TRY': self.try_statement, 'SWITCH': self.switch_statement, 'DEBUG': self.debug_statement,
        }
        if tok_type in dispatch: return dispatch[tok_type]()
        
        potential_expr_node = self.expr()
        if self.current_token and self.current_token.type == 'ASSIGN':
            if not isinstance(potential_expr_node, (Var, SubscriptAccess)):
                self.error(t('p_err_invalid_assign_target'))
            op = self.current_token
            self.eat('ASSIGN')
            right = self.expr()
            return Assign(potential_expr_node, op, right)

        if isinstance(potential_expr_node, FuncCall):
             return potential_expr_node
        
        if self.pos == len(self.tokens) -1:
             return potential_expr_node

        self.error(t('p_err_invalid_stmt_start', value=potential_expr_node.token.value))

    def import_statement(self):
        token = self.current_token; self.eat('IMPORT')
        if self.current_token.type != 'STRING': self.error(t('p_err_import_expects_string'))
        filename_token = self.current_token; self.eat('STRING'); return Import(filename_token, token)
    
    def assignment_statement(self):
        token = self.current_token
        self.eat('LET')
        # Here we parse an expression that can be an assignment target
        # This correctly handles chained subscripts like var[i][j]
        left_node = self.expr()

        if self.current_token and self.current_token.type == 'ASSIGN':
            if not isinstance(left_node, (Var, SubscriptAccess)):
                self.error(t('p_err_invalid_assign_target'))
            op = self.current_token
            self.eat('ASSIGN')
            right = self.expr()
            return Assign(left_node, op, right)
        else:
            if not isinstance(left_node, Var):
                self.error('Declaration without an initial value must be a simple variable.')
            return Declare(left_node, token)

    def print_statement(self):
        token = self.current_token; self.eat('PRINT'); return Print(self.expr(), token)
    def input_statement(self):
        token = self.current_token; self.eat('INPUT'); var_node = self.expr()
        if not isinstance(var_node, (Var, SubscriptAccess)): self.error(t('p_err_invalid_assign_target'))
        prompt = None
        if self.current_token and self.current_token.type == 'COMMA': self.eat('COMMA'); prompt = self.expr()
        return Input(var_node, prompt, token)
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
        token = self.current_token
        self.eat('FOR')
        if self.current_token.type == 'EACH':
            self.eat('EACH')
            var_token = self.current_token
            self.eat('ID')
            self.eat('IN')
            collection_node = self.expr()
            block = self.statement_list(['NEXT'])
            self.eat('NEXT')
            if not self.current_token or self.current_token.type != 'ID' or self.current_token.value.lower() != var_token.value.lower():
                 self.error(t('p_err_for_next_mismatch', expected=var_token.value, found=self.current_token.value if self.current_token else 'None'))
            self.eat('ID')
            return ForEach(var_token, collection_node, block, token)

        var = self.expr()
        if not isinstance(var, Var): self.error(t('p_err_for_counter_not_var'))
        self.eat('ASSIGN'); start_expr = self.expr(); self.eat('TO'); end_expr = self.expr()
        step_expr = Num(Token('INTEGER', 1, token.line))
        if self.current_token and self.current_token.type == 'STEP': self.eat('STEP'); step_expr = self.expr()
        block = self.statement_list(['NEXT']); self.eat('NEXT')
        if not self.current_token or self.current_token.type != 'ID' or self.current_token.value.lower() != var.value.lower():
            expected_val = var.value if hasattr(var, 'value') else 'unknown'
            found_val = self.current_token.value if self.current_token else 'None'
            self.error(t('p_err_for_next_mismatch', expected=expected_val, found=found_val))
        self.eat('ID'); return For(var, start_expr, end_expr, step_expr, block, token)
    def func_definition(self):
        token = self.current_token; is_async = token.type == 'ASYNC_FUNCTION'; is_jit = token.type == 'JIT_FUNCTION'
        self.eat(token.type); func_name = self.current_token.value; self.eat('ID'); self.eat('LPAREN'); params = []
        if self.current_token and self.current_token.type == 'ID':
            params.append(Var(self.current_token)); self.eat('ID')
            while self.current_token and self.current_token.type == 'COMMA': self.eat('COMMA'); params.append(Var(self.current_token)); self.eat('ID')
        self.eat('RPAREN'); block = self.statement_list(['ENDFUNCTION']); self.eat('ENDFUNCTION')
        return FuncDef(func_name, params, block, token, is_async, is_jit)
    def return_statement(self):
        token = self.current_token; self.eat('RETURN'); return Return(self.expr(), token)
    def dim_statement(self):
        token = self.current_token; self.eat('DIM'); var_token = self.current_token; self.eat('ID'); self.eat('LPAREN')
        size_exprs = [self.expr()]
        while self.current_token and self.current_token.type == 'COMMA': self.eat('COMMA'); size_exprs.append(self.expr())
        self.eat('RPAREN'); return Dim(var_token, size_exprs, token)
    def data_statement(self):
        token = self.current_token; self.eat('DATA'); values = []
        stop_tokens = {'LET', 'PRINT', 'INPUT', 'IF', 'WHILE', 'FOR', 'FUNCTION', 'ASYNC_FUNCTION', 'JIT_FUNCTION', 'RETURN', 'DIM', 'DATA', 'READ', 'RESTORE', 'RUN_ASYNC', 'AWAIT', 'ID', 'EOF', 'ELSE', 'ELSEIF', 'WEND', 'NEXT', 'ENDFUNCTION', 'IMPORT', 'BREAK', 'CONTINUE', 'TRY', 'SWITCH'}
        while self.current_token and self.current_token.type not in stop_tokens:
            if self.current_token.type == 'MINUS':
                self.eat('MINUS'); num_tok = self.current_token
                if num_tok.type not in ('INTEGER', 'FLOAT'): self.error(t('p_err_data_expects_number'))
                self.eat(num_tok.type); values.append(Num(Token(num_tok.type, -num_tok.value, num_tok.line)))
            else: values.append(self.expr())
            if self.current_token and self.current_token.type == 'COMMA': self.eat('COMMA')
            else: break
        return Data(values, token)
    def read_statement(self):
        token = self.current_token; self.eat('READ'); variables = [self.expr()]
        while self.current_token and self.current_token.type == 'COMMA':
            self.eat('COMMA'); variables.append(self.expr())
        return Read(variables, token)
    def restore_statement(self):
        token = self.current_token; self.eat('RESTORE'); return Restore(token)
    def run_async_statement(self):
        token = self.current_token; self.eat('RUN_ASYNC'); tasks = [self.expr()]
        while self.current_token and self.current_token.type == 'COMMA': self.eat('COMMA'); tasks.append(self.expr())
        return RunAsync(tasks, token)
    def break_statement(self):
        token = self.current_token; self.eat('BREAK'); return Break(token)
    def continue_statement(self):
        token = self.current_token; self.eat('CONTINUE'); return Continue(token)
    def try_statement(self):
        token = self.current_token; self.eat('TRY')
        try_block = self.statement_list(['CATCH', 'FINALLY', 'ENDTRY'])
        catch_var, catch_block = None, None
        if self.current_token.type == 'CATCH':
            self.eat('CATCH'); catch_var = Var(self.current_token); self.eat('ID')
            catch_block = self.statement_list(['FINALLY', 'ENDTRY'])
        finally_block = None
        if self.current_token.type == 'FINALLY':
            self.eat('FINALLY'); finally_block = self.statement_list(['ENDTRY'])
        self.eat('ENDTRY'); return Try(try_block, catch_var, catch_block, finally_block, token)
    def switch_statement(self):
        token = self.current_token; self.eat('SWITCH'); expr = self.expr()
        if not expr: self.error(t('p_err_switch_expects_var'))
        cases, default_case, has_default = [], None, False
        while self.current_token and self.current_token.type != 'ENDSWITCH':
            if self.current_token.type == 'CASE':
                if has_default: self.error(t('p_err_case_after_default'))
                self.eat('CASE'); case_values = [self.expr()]
                while self.current_token.type == 'COMMA': self.eat('COMMA'); case_values.append(self.expr())
                self.eat('COLON'); block = self.statement_list(['CASE', 'DEFAULT', 'ENDSWITCH'])
                cases.append((case_values, block))
            elif self.current_token.type == 'DEFAULT':
                if has_default: self.error("Multiple 'DEFAULT' blocks in SWITCH statement")
                self.eat('DEFAULT'); self.eat('COLON'); default_case = self.statement_list(['ENDSWITCH']); has_default = True
            else: self.error(f"Unexpected token {self.current_token.type} inside SWITCH block")
        self.eat('ENDSWITCH'); return Switch(expr, cases, default_case, token)
    def debug_statement(self):
        token = self.current_token
        self.eat('DEBUG')
        start_pos = self.pos
        expr_node = self.expr()
        end_pos = self.pos
        expr_str = " ".join(str(t.value) for t in self.tokens[start_pos:end_pos])
        return Debug(expr_node, expr_str, token)
    def parse(self):
        statements = self.statement_list(['EOF'])
        if self.current_token and self.current_token.type != 'EOF': self.error(t('p_err_unexpected_token', value=self.current_token.value))
        return Program(statements)

### --- CHANGE START (8/8): Add new OpCodes for F-String and multi-dim index --- ###
class OpCode(Enum):
    LOAD_CONST=auto(); POP=auto(); LOAD_GLOBAL=auto(); STORE_GLOBAL=auto(); LOAD_LOCAL=auto(); STORE_LOCAL=auto();
    ADD=auto(); SUBTRACT=auto(); MULTIPLY=auto(); DIVIDE=auto(); EQUAL=auto(); NOT_EQUAL=auto(); GREATER=auto();
    LESS=auto(); GREATER_EQUAL=auto(); LESS_EQUAL=auto(); LOGIC_AND=auto(); LOGIC_OR=auto(); NEGATE=auto(); NOT=auto();
    PRINT=auto(); INPUT=auto(); JUMP_IF_FALSE=auto(); JUMP=auto(); LOOP=auto(); CALL=auto(); RETURN=auto();
    DEFINE_FUNC=auto(); BUILD_ARRAY=auto(); LOAD_SUBSCRIPT=auto(); STORE_SUBSCRIPT=auto(); READ_DATA=auto();
    RESTORE_DATA=auto(); AWAIT=auto(); CREATE_TASK=auto(); IMPORT_MODULE=auto(); BUILD_DICT=auto(); BUILD_STRING=auto();
    SETUP_TRY=auto(); POP_TRY=auto(); THROW=auto(); DUP=auto(); BUILD_ARRAY_LITERAL=auto(); DEBUG_PRINT=auto();
    GET_LENGTH=auto(); BUILD_TUPLE=auto()
### --- CHANGE END (8/8) --- ###

class FunctionObject:
    def __init__(self, name, arity, chunk, is_async=False):
        self.name, self.arity, self.chunk, self.is_async = name, arity, chunk, is_async
    def __repr__(self): return f"<Fn {self.name}/{self.arity}>"
class Chunk:
    def __init__(self, name="<script>"):
        self.name, self.code, self.constants, self.lines_rle = name, bytearray(), [], []
    def write(self, byte, line):
        self.code.append(byte)
        if not self.lines_rle or self.lines_rle[-1][0] != line: self.lines_rle.append([line, 1])
        else: self.lines_rle[-1][1] += 1
    def get_line(self, ip):
        current_ip = 0
        for line, count in self.lines_rle:
            current_ip += count;
            if ip < current_ip: return line
        return self.lines_rle[-1][0] if self.lines_rle else '?'
    def add_constant(self, value):
        # Allow tuples in constants for multi-dim indexing
        if isinstance(value, (int, float, str, bool, type(None), FunctionObject)):
             try: return self.constants.index(value)
             except ValueError: pass # Fall through to append

        for i, c in enumerate(self.constants):
            if type(c) is not type(value): continue
            if isinstance(c, np.ndarray):
                if np.array_equal(c, value): return i
            elif c == value: return i
        self.constants.append(value); return len(self.constants) - 1

class Compiler:
    def __init__(self, parent=None):
        self.chunk, self.scope_depth, self.locals, self.parent = Chunk(), 0, [], parent
        self.function = FunctionObject("<script>", 0, self.chunk) if parent is None else None
        self.loop_stack = []
        self.foreach_iterator_count = 0

    def error(self, message, token): raise ParserError(message, token)
    def compile(self, program_node):
        self.visit(program_node)
        self.emit(OpCode.LOAD_CONST, -1); self.emit_byte(self.chunk.add_constant(None), -1)
        self.emit(OpCode.RETURN, -1); return self.function
    def emit(self, opcode, line): self.chunk.write(opcode.value, line)
    def emit_byte(self, byte, line): self.chunk.write(byte, line)
    def emit_bytes(self, b1, b2, line): self.emit_byte(b1, line); self.emit_byte(b2, line)
    def emit_constant(self, value, line):
        idx = self.chunk.add_constant(value)
        self.emit(OpCode.LOAD_CONST, line); self.emit_byte(idx, line)
    def emit_jump(self, instruction, line):
        self.emit(instruction, line); self.emit_byte(0xff, line); self.emit_byte(0xff, line)
        return len(self.chunk.code) - 2
    def patch_jump(self, offset):
        jump = len(self.chunk.code) - offset - 2
        if jump > 65535: raise Exception("Jump too large")
        self.chunk.code[offset] = (jump >> 8) & 0xff; self.chunk.code[offset + 1] = jump & 0xff
    def begin_scope(self): self.scope_depth += 1
    def end_scope(self):
        self.scope_depth -= 1; pops_needed = 0
        while self.locals and self.locals[-1]['depth'] > self.scope_depth:
            pops_needed += 1; self.locals.pop()
        for _ in range(pops_needed): self.emit(OpCode.POP, -1)
    def add_local(self, name_token):
        name = name_token.value.lower()
        for i in range(len(self.locals) - 1, -1, -1):
            if self.locals[i]['depth'] < self.scope_depth: break
            if self.locals[i]['name'] == name: self.error(t('p_err_var_already_declared', name=name), name_token)
        self.locals.append({'name': name, 'depth': self.scope_depth})
    def resolve_local(self, name_token):
        name = name_token.value.lower()
        for i in range(len(self.locals) - 1, -1, -1):
            if self.locals[i]['name'] == name: return i
        return -1
    def visit(self, node): getattr(self, f'visit_{type(node).__name__}')(node)
    def visit_Program(self, node): 
        for i, stmt in enumerate(node.statements):
             self.visit(stmt)
             if not isinstance(stmt, (Print, Assign, If, While, For, ForEach, FuncDef, Return, Debug, Declare)) and i < len(node.statements) -1:
                 # Pop result of expressions used as statements, unless it's the last one in a script (for REPL)
                 self.emit(OpCode.POP, stmt.token.line if hasattr(stmt, 'token') else -1)
    def visit_NoOp(self, node): pass
    def visit_Num(self, node): self.emit_constant(node.value, node.token.line)
    def visit_String(self, node): self.emit_constant(node.value, node.token.line)
    def visit_FString(self, node):
        for part in node.parts: self.visit(part)
        self.emit_bytes(OpCode.BUILD_STRING.value, len(node.parts), node.token.line)
    def visit_BinOp(self, node):
        if isinstance(node.left, Num) and isinstance(node.right, Num):
            val_l, val_r = node.left.value, node.right.value
            op_map = {'PLUS': operator.add, 'MINUS': operator.sub, 'MUL': operator.mul, 'DIV': operator.truediv}
            if node.op.type in op_map and not (node.op.type == 'DIV' and val_r == 0):
                self.emit_constant(op_map[node.op.type](val_l, val_r), node.token.line); return
        if node.op.type == 'OR':
            self.visit(node.left); else_jump = self.emit_jump(OpCode.JUMP_IF_FALSE, node.op.line)
            self.emit(OpCode.POP, node.op.line); self.emit_constant(1, node.op.line)
            end_jump = self.emit_jump(OpCode.JUMP, node.op.line); self.patch_jump(else_jump)
            self.emit(OpCode.POP, node.op.line); self.visit(node.right); self.patch_jump(end_jump)
            return
        elif node.op.type == 'AND':
            self.visit(node.left); end_jump = self.emit_jump(OpCode.JUMP_IF_FALSE, node.op.line)
            self.emit(OpCode.POP, node.op.line); self.visit(node.right); self.patch_jump(end_jump)
            return
        self.visit(node.left); self.visit(node.right)
        op_map = {'PLUS': OpCode.ADD, 'MINUS': OpCode.SUBTRACT, 'MUL': OpCode.MULTIPLY, 'DIV': OpCode.DIVIDE, 'EQ': OpCode.EQUAL, 'NEQ': OpCode.NOT_EQUAL, 'GT': OpCode.GREATER, 'LT': OpCode.LESS, 'GTE': OpCode.GREATER_EQUAL, 'LTE': OpCode.LESS_EQUAL}
        self.emit(op_map[node.op.type], node.op.line)
    def visit_UnaryOp(self, node):
        self.visit(node.expr)
        if node.op.type == 'MINUS' and isinstance(node.expr, Num):
            self.chunk.code.pop(); self.chunk.code.pop(); self.emit_constant(-node.expr.value, node.token.line); return
        op_map = {'MINUS': OpCode.NEGATE, 'NOT': OpCode.NOT}
        if node.op.type in op_map: self.emit(op_map[node.op.type], node.op.line)
    def visit_Var(self, node):
        local_idx = self.resolve_local(node.token)
        if local_idx != -1: self.emit_bytes(OpCode.LOAD_LOCAL.value, local_idx, node.token.line)
        else: self.emit_bytes(OpCode.LOAD_GLOBAL.value, self.chunk.add_constant(node.value.lower()), node.token.line)
    
    def visit_Assign(self, node):
        if isinstance(node.left, Var):
            self.visit(node.right) # Standard: value then store
            local_idx = self.resolve_local(node.left.token)
            if local_idx != -1:
                self.emit_bytes(OpCode.STORE_LOCAL.value, local_idx, node.token.line)
            else:
                const_idx = self.chunk.add_constant(node.left.value.lower())
                self.emit_bytes(OpCode.STORE_GLOBAL.value, const_idx, node.token.line)
        elif isinstance(node.left, SubscriptAccess):
            # For store, we need container, key, then value on stack
            self.visit(node.left.primary) # 1. Container
            # 2. Key (might be a tuple)
            if len(node.left.index_exprs) > 1:
                for expr in node.left.index_exprs:
                    self.visit(expr)
                self.emit_bytes(OpCode.BUILD_TUPLE.value, len(node.left.index_exprs), node.token.line)
            else:
                self.visit(node.left.index_exprs[0])
            self.visit(node.right) # 3. Value
            self.emit(OpCode.STORE_SUBSCRIPT, node.token.line)

    def visit_Declare(self, node):
        self.emit_constant(None, node.token.line)
        var_node = node.var_node
        if self.scope_depth > 0:
            self.add_local(var_node.token)
            return # The value is already on the stack for the next instruction to store
        
        local_idx = self.resolve_local(var_node.token)
        if local_idx != -1:
            self.emit_bytes(OpCode.STORE_LOCAL.value, local_idx, node.token.line)
        elif self.scope_depth > 0:
            self.add_local(var_node.token)
            new_local_idx = self.resolve_local(var_node.token)
            self.emit_bytes(OpCode.STORE_LOCAL.value, new_local_idx, node.token.line)
        else:
            const_idx = self.chunk.add_constant(var_node.value.lower())
            self.emit_bytes(OpCode.STORE_GLOBAL.value, const_idx, node.token.line)

    def visit_Print(self, node): self.visit(node.expr); self.emit(OpCode.PRINT, node.token.line)
    def visit_Input(self, node):
        if node.prompt: self.visit(node.prompt)
        else: self.emit_constant("", node.token.line)
        self.emit(OpCode.INPUT, node.token.line)
        # Create a dummy Assign node to reuse assignment logic
        assign_node = Assign(node.var, Token('ASSIGN', '=', node.token.line), None) # Right is dummy
        
        if isinstance(assign_node.left, Var):
            # For input, the value is already on the stack from INPUT opcode
            local_idx = self.resolve_local(assign_node.left.token)
            if local_idx != -1:
                self.emit_bytes(OpCode.STORE_LOCAL.value, local_idx, node.token.line)
            else:
                self.emit_bytes(OpCode.STORE_GLOBAL.value, self.chunk.add_constant(assign_node.left.value.lower()), node.token.line)
        elif isinstance(assign_node.left, SubscriptAccess):
            # This is complex: INPUT value is on stack. We need container, key, then value.
            # We pop the input, compile container/key, then push input back.
            # A simpler way is to store input in a temp var, then do a normal assignment.
            # For now, let's re-order manually.
            self.visit(assign_node.left.primary) # push container
            
            # push key (might be a tuple)
            if len(assign_node.left.index_exprs) > 1:
                for expr in assign_node.left.index_exprs: self.visit(expr)
                self.emit_bytes(OpCode.BUILD_TUPLE.value, len(assign_node.left.index_exprs), node.token.line)
            else:
                self.visit(assign_node.left.index_exprs[0])

            # Swap stack: [..., input_val, container, key] -> [..., container, key, input_val]
            # This is tricky without a SWAP opcode. Let's handle it in the INPUT opcode instead.
            # For now, we assume INPUT assigns to a simple var. Let's simplify this visit method.
            if isinstance(node.var, Var):
                local_idx = self.resolve_local(node.var.token)
                if local_idx != -1: self.emit_bytes(OpCode.STORE_LOCAL.value, local_idx, node.token.line)
                else: self.emit_bytes(OpCode.STORE_GLOBAL.value, self.chunk.add_constant(node.var.value.lower()), node.token.line)
            else:
                 # This path is now unsupported to simplify compilation.
                 self.error("INPUT only supports assignment to simple variables.", node.token)
    def visit_If(self, node):
        exit_jumps, last_case_jump = [], -1
        for i, (condition, block) in enumerate(node.cases):
            if i > 0: self.patch_jump(last_case_jump)
            self.visit(condition); false_jump = self.emit_jump(OpCode.JUMP_IF_FALSE, condition.token.line)
            self.emit(OpCode.POP, condition.token.line); self.visit_Program(Program(block)); exit_jumps.append(self.emit_jump(OpCode.JUMP, -1))
            self.patch_jump(false_jump); self.emit(OpCode.POP, condition.token.line); last_case_jump = false_jump
        if node.else_case: self.visit_Program(Program(node.else_case))
        for jump in exit_jumps: self.patch_jump(jump)
    def visit_While(self, node):
        loop_start = len(self.chunk.code); self.loop_stack.append({'start': loop_start, 'breaks': []})
        self.visit(node.condition); exit_jump = self.emit_jump(OpCode.JUMP_IF_FALSE, node.token.line)
        self.emit(OpCode.POP, node.token.line); self.visit_Program(Program(node.block))
        offset = len(self.chunk.code) - loop_start + 3
        self.emit(OpCode.LOOP, -1); self.emit_bytes((offset >> 8) & 0xff, offset & 0xff, -1)
        self.patch_jump(exit_jump); self.emit(OpCode.POP, node.token.line)
        loop = self.loop_stack.pop()
        for break_jump in loop['breaks']: self.patch_jump(break_jump)
    def visit_For(self, node):
        self.begin_scope(); self.visit(node.start); self.add_local(node.var.token); loop_start = len(self.chunk.code)
        self.loop_stack.append({'start': loop_start, 'breaks': []})
        self.visit(node.var); self.visit(node.end); self.visit(node.step)
        self.emit_constant(0, node.token.line); self.emit(OpCode.GREATER, node.token.line); is_positive_jump = self.emit_jump(OpCode.JUMP_IF_FALSE, node.token.line)
        self.emit(OpCode.POP, node.token.line); self.emit(OpCode.LESS_EQUAL, node.token.line); end_cond_jump = self.emit_jump(OpCode.JUMP, node.token.line)
        self.patch_jump(is_positive_jump); self.emit(OpCode.POP, node.token.line); self.emit(OpCode.GREATER_EQUAL, node.token.line); self.patch_jump(end_cond_jump)
        exit_jump = self.emit_jump(OpCode.JUMP_IF_FALSE, node.token.line); self.emit(OpCode.POP, node.token.line); self.visit_Program(Program(node.block))
        offset = len(self.chunk.code) - loop_start + 3
        self.visit(node.var); self.visit(node.step); self.emit(OpCode.ADD, node.token.line)
        self.emit_bytes(OpCode.STORE_LOCAL.value, self.resolve_local(node.var.token), node.token.line); self.emit(OpCode.POP, node.token.line)
        self.emit(OpCode.LOOP, node.token.line); self.emit_bytes((offset >> 8) & 0xff, offset & 0xff, node.token.line)
        self.patch_jump(exit_jump); self.emit(OpCode.POP, node.token.line); loop = self.loop_stack.pop()
        for break_jump in loop['breaks']: self.patch_jump(break_jump)
        self.end_scope()
    def visit_FuncDef(self, node):
        if node.is_jit: return
        sub_compiler = Compiler(parent=self); sub_compiler.function = FunctionObject(node.name.lower(), len(node.params), sub_compiler.chunk, node.is_async)
        sub_compiler.begin_scope()
        for param in node.params: sub_compiler.add_local(param.token)
        sub_compiler.visit(Program(node.block)); sub_compiler.emit(OpCode.LOAD_CONST, -1); sub_compiler.emit_byte(sub_compiler.chunk.add_constant(None), -1)
        sub_compiler.emit(OpCode.RETURN, -1); function = sub_compiler.function; const_idx = self.chunk.add_constant(function)
        self.emit(OpCode.DEFINE_FUNC, node.token.line); self.emit_byte(const_idx, node.token.line)
        name_idx = self.chunk.add_constant(node.name.lower()); self.emit(OpCode.STORE_GLOBAL, node.token.line); self.emit_byte(name_idx, node.token.line)
    def visit_Return(self, node): self.visit(node.expr); self.emit(OpCode.RETURN, node.token.line)
    def visit_FuncCall(self, node):
        func_name = node.name_token.value.lower()
        if func_name in BUILTIN_FUNCTIONS or func_name in JIT_FUNCTIONS:
             for arg in node.args: self.visit(arg)
             self.emit_bytes(OpCode.CALL.value, self.chunk.add_constant(func_name), node.token.line); self.emit_byte(len(node.args), node.token.line)
             return
        self.visit(Var(node.name_token));
        for arg in node.args: self.visit(arg)
        self.emit(OpCode.CALL, node.token.line); self.emit_bytes(0xFF, len(node.args), node.token.line)
    def visit_Dim(self, node):
        for size_expr in node.size_exprs: self.visit(size_expr)
        self.emit(OpCode.BUILD_ARRAY, node.token.line); self.emit_byte(len(node.size_exprs), node.token.line)
        self.emit_bytes(OpCode.STORE_GLOBAL.value, self.chunk.add_constant(node.var_token.value.lower()), node.token.line)
    def visit_Data(self, node): pass
    def visit_Read(self, node):
        for var_node in node.variables:
            self.emit(OpCode.READ_DATA, var_node.token.line)
            assign_node = Assign(var_node, Token('ASSIGN', '=', var_node.token.line), None)
            self.visit_Assign(assign_node) # This is a bit of a hack
    def visit_Restore(self, node): self.emit(OpCode.RESTORE_DATA, node.token.line)
    def visit_Await(self, node): self.visit(node.expr); self.emit(OpCode.AWAIT, node.token.line)
    def visit_RunAsync(self, node):
        for task in node.tasks: self.visit(task); self.emit(OpCode.CREATE_TASK, task.token.line)
    def visit_Import(self, node): self.emit_bytes(OpCode.IMPORT_MODULE.value, self.chunk.add_constant(node.filename_token.value), node.token.line)
    def visit_Break(self, node):
        if not self.loop_stack: self.error(t('p_err_break_outside_loop'), node.token)
        jump = self.emit_jump(OpCode.JUMP, node.token.line); self.loop_stack[-1]['breaks'].append(jump)
    def visit_Continue(self, node):
        if not self.loop_stack: self.error(t('p_err_continue_outside_loop'), node.token)
        loop_start = self.loop_stack[-1]['start']; offset = len(self.chunk.code) - loop_start + 3
        self.emit(OpCode.LOOP, node.token.line); self.emit_bytes((offset >> 8) & 0xff, offset & 0xff, node.token.line)
    def visit_DictLiteral(self, node):
        for key_node, value_node in reversed(node.pairs): self.visit(key_node); self.visit(value_node)
        self.emit_bytes(OpCode.BUILD_DICT.value, len(node.pairs), node.token.line)
    
    def visit_SubscriptAccess(self, node):
        self.visit(node.primary) # 1. Container
        # 2. Key (might be a tuple)
        if len(node.index_exprs) > 1:
            for expr in node.index_exprs:
                self.visit(expr)
            self.emit_bytes(OpCode.BUILD_TUPLE.value, len(node.index_exprs), node.token.line)
        else:
            self.visit(node.index_exprs[0])
        self.emit(OpCode.LOAD_SUBSCRIPT, node.token.line)

    def visit_Try(self, node):
        try_jump = self.emit_jump(OpCode.SETUP_TRY, node.token.line); self.begin_scope()
        self.visit_Program(Program(node.try_block)); self.end_scope(); self.emit(OpCode.POP_TRY, node.token.line)
        finally_jump = self.emit_jump(OpCode.JUMP, node.token.line); self.patch_jump(try_jump)
        if node.catch_block:
            self.begin_scope(); self.add_local(node.catch_var.token)
            self.emit_bytes(OpCode.STORE_LOCAL.value, self.resolve_local(node.catch_var.token), node.catch_var.token.line)
            self.visit_Program(Program(node.catch_block)); self.end_scope()
        self.patch_jump(finally_jump)
        if node.finally_block: self.visit_Program(Program(node.finally_block))
    def visit_Switch(self, node):
        self.visit(node.expr); exit_jumps = []; next_case_jumps = []
        for values, block in node.cases:
            for jump in next_case_jumps: self.patch_jump(jump)
            next_case_jumps.clear()
            for value in values:
                self.emit(OpCode.DUP, value.token.line); self.visit(value); self.emit(OpCode.EQUAL, value.token.line)
                next_case_jumps.append(self.emit_jump(OpCode.JUMP_IF_FALSE, value.token.line))
                self.emit(OpCode.POP, value.token.line)
            for jump in next_case_jumps: self.patch_jump(jump); self.emit(OpCode.POP, -1)
            next_case_jumps.clear(); self.emit(OpCode.POP, -1); self.visit_Program(Program(block))
            exit_jumps.append(self.emit_jump(OpCode.JUMP, -1)); break
        for jump in next_case_jumps: self.patch_jump(jump)
        self.emit(OpCode.POP, -1)
        if node.default_case: self.visit_Program(Program(node.default_case))
        for jump in exit_jumps: self.patch_jump(jump)
    def visit_ArrayLiteral(self, node):
        for element in node.elements:
            self.visit(element)
        self.emit_bytes(OpCode.BUILD_ARRAY_LITERAL.value, len(node.elements), node.token.line)
    def visit_ForEach(self, node):
        self.begin_scope()
        self.visit(node.collection)
        coll_var_name = f"__foreach_coll_{self.foreach_iterator_count}"
        coll_token = Token('ID', coll_var_name, node.token.line)
        self.add_local(coll_token)
        coll_local_idx = self.resolve_local(coll_token)
        self.emit_constant(0, node.token.line)
        idx_var_name = f"__foreach_idx_{self.foreach_iterator_count}"
        idx_token = Token('ID', idx_var_name, node.token.line)
        self.add_local(idx_token)
        idx_local_idx = self.resolve_local(idx_token)
        self.foreach_iterator_count += 1
        loop_start = len(self.chunk.code)
        self.loop_stack.append({'start': loop_start, 'breaks': []})
        self.emit_bytes(OpCode.LOAD_LOCAL.value, idx_local_idx, node.token.line)
        self.emit_bytes(OpCode.LOAD_LOCAL.value, coll_local_idx, node.token.line)
        self.emit(OpCode.GET_LENGTH, node.token.line)
        self.emit(OpCode.LESS, node.token.line)
        exit_jump = self.emit_jump(OpCode.JUMP_IF_FALSE, node.token.line)
        self.emit(OpCode.POP, node.token.line)
        self.begin_scope()
        self.add_local(node.var_token)
        item_local_idx = self.resolve_local(node.var_token)
        self.emit_bytes(OpCode.LOAD_LOCAL.value, coll_local_idx, node.token.line)
        self.emit_bytes(OpCode.LOAD_LOCAL.value, idx_local_idx, node.token.line)
        self.emit(OpCode.LOAD_SUBSCRIPT, node.token.line)
        self.emit_bytes(OpCode.STORE_LOCAL.value, item_local_idx, node.token.line)
        self.emit(OpCode.POP, node.token.line)
        self.visit_Program(Program(node.block))
        self.end_scope()
        self.emit_bytes(OpCode.LOAD_LOCAL.value, idx_local_idx, node.token.line)
        self.emit_constant(1, node.token.line)
        self.emit(OpCode.ADD, node.token.line)
        self.emit_bytes(OpCode.STORE_LOCAL.value, idx_local_idx, node.token.line)
        self.emit(OpCode.POP, node.token.line)
        offset = len(self.chunk.code) - loop_start + 3
        self.emit(OpCode.LOOP, node.token.line)
        self.emit_bytes((offset >> 8) & 0xff, offset & 0xff, node.token.line)
        self.patch_jump(exit_jump)
        self.emit(OpCode.POP, node.token.line)
        loop = self.loop_stack.pop()
        for break_jump in loop['breaks']: self.patch_jump(break_jump)
        self.end_scope()
    def visit_Debug(self, node):
        self.visit(node.expr)
        expr_str_idx = self.chunk.add_constant(node.expr_str)
        self.emit_bytes(OpCode.DEBUG_PRINT.value, expr_str_idx, node.token.line)

class MomentumToPythonTranspiler:
    def __init__(self):
        self.numba_builtins = {'abs', 'round', 'int', 'float'}
        self.numba_math_funcs = {'sqrt', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'exp', 'log', 'log10', 'floor', 'ceil'}
    def transpile(self, func_node):
        self.indent_level = 1; param_names = {p.value.lower() for p in func_node.params}
        local_vars = self._find_local_vars(func_node.block, param_names)
        init_code = "".join([f"{self.indent()}{var} = 0.0\n" for var in local_vars])
        body_code = "".join(self._visit(stmt) for stmt in func_node.block); return init_code + body_code
    def _find_local_vars(self, block, param_names):
        locals_found = set()
        def traverse(statements):
            for stmt in statements:
                if isinstance(stmt, Assign) and isinstance(stmt.left, Var):
                    var_name = stmt.left.value.lower()
                    if var_name not in param_names: locals_found.add(var_name)
                elif isinstance(stmt, For):
                    var_name = stmt.var.value.lower()
                    if var_name not in param_names: locals_found.add(var_name); traverse(stmt.block)
                elif isinstance(stmt, If):
                    for _, case_block in stmt.cases: traverse(case_block)
                    if stmt.else_case: traverse(stmt.else_case)
        traverse(block); return locals_found
    def indent(self): return "    " * self.indent_level
    def _visit(self, node): return getattr(self, f'_visit_{type(node).__name__}', self.generic_visit)(node)
    def generic_visit(self, node): raise InterpreterError(f"Command '{type(node).__name__}' is not supported in JIT", node)
    def _visit_BinOp(self, node):
        op_map = {'PLUS':'+', 'MINUS':'-', 'MUL':'*', 'DIV':'/', 'EQ':'==', 'NEQ':'!=', 'LT':'<', 'LTE':'<=', 'GT':'>', 'GTE':'>=', 'AND':'and', 'OR':'or'}
        return f"({self._visit(node.left)} {op_map[node.op.type]} {self._visit(node.right)})"
    def _visit_UnaryOp(self, node):
        if node.op.type == 'MINUS': return f"(-{self._visit(node.expr)})"
        if node.op.type == 'NOT': return f"(not {self._visit(node.expr)})"
        return self._visit(node.expr)
    def _visit_Num(self, node): return str(node.value)
    def _visit_Var(self, node): return node.value.lower()
    def _visit_Assign(self, node): return f"{self.indent()}{self._visit(node.left)} = {self._visit(node.right)}\n"
    def _visit_If(self, node):
        code = ""; cond, block = node.cases[0]; code += f"{self.indent()}if {self._visit(cond)}:\n"
        self.indent_level += 1; code += "".join(self._visit(stmt) for stmt in block); self.indent_level -= 1
        for cond, block in node.cases[1:]:
            code += f"{self.indent()}elif {self._visit(cond)}:\n"; self.indent_level += 1; code += "".join(self._visit(stmt) for stmt in block); self.indent_level -= 1
        if node.else_case:
            code += f"{self.indent()}else:\n"; self.indent_level += 1; code += "".join(self._visit(stmt) for stmt in node.else_case); self.indent_level -= 1
        return code
    def _visit_For(self, node):
        var, start, end, step = self._visit(node.var), self._visit(node.start), self._visit(node.end), self._visit(node.step)
        end_adj = f"int({end}) + (1 if {step} > 0 else -1)"; code = f"{self.indent()}for {var} in numba.prange(int({start}), {end_adj}, int({step})):\n"
        self.indent_level += 1; code += "".join(self._visit(stmt) for stmt in node.block); self.indent_level -= 1; return code
    def _visit_FuncCall(self, node):
        func_name = node.name_token.value.lower(); args_code = ', '.join(self._visit(arg) for arg in node.args)
        if func_name in self.numba_builtins: return f"{func_name}({args_code})"
        if func_name in self.numba_math_funcs: return f"math.{func_name}({args_code})"
        return f"{func_name}({args_code})"
    def _visit_Return(self, node): return f"{self.indent()}return {self._visit(node.expr)}\n"
    def _visit_NoOp(self, node): return ""

class CallFrame:
    __slots__ = ('function', 'ip', 'stack_base');
    def __init__(self, function, ip, stack_base): self.function, self.ip, self.stack_base = function, ip, stack_base
class TryBlock:
    __slots__ = ('handler_ip', 'stack_size')
    def __init__(self, handler_ip, stack_size): self.handler_ip, self.stack_size = handler_ip, stack_size
class VM:
    def __init__(self, jit_functions, data_pool, compiled_modules, base_path):
        self.stack, self.globals, self.frames, self.try_stack = [], {}, [], []
        self.jit_functions, self.data_pool, self.data_ptr = jit_functions, data_pool, 0
        self.compiled_modules, self.base_path = compiled_modules, base_path
        self.dispatch_table = self._create_dispatch_table()
    def _create_dispatch_table(self):
        table = [None] * (len(OpCode) + 1); handlers = {
            OpCode.LOAD_CONST: self._op_load_const, OpCode.POP: self._op_pop, OpCode.LOAD_GLOBAL: self._op_load_global,
            OpCode.STORE_GLOBAL: self._op_store_global, OpCode.LOAD_LOCAL: self._op_load_local, OpCode.STORE_LOCAL: self._op_store_local,
            OpCode.ADD: self._op_add, OpCode.SUBTRACT: self._op_subtract, OpCode.MULTIPLY: self._op_multiply,
            OpCode.DIVIDE: self._op_divide, OpCode.EQUAL: self._op_equal, OpCode.NOT_EQUAL: self._op_not_equal,
            OpCode.GREATER: self._op_greater, OpCode.LESS: self._op_less, OpCode.GREATER_EQUAL: self._op_greater_equal,
            OpCode.LESS_EQUAL: self._op_less_equal, OpCode.NEGATE: self._op_negate, OpCode.NOT: self._op_not,
            OpCode.PRINT: self._op_print, OpCode.INPUT: self._op_input, OpCode.JUMP_IF_FALSE: self._op_jump_if_false,
            OpCode.JUMP: self._op_jump, OpCode.LOOP: self._op_loop, OpCode.CALL: self._op_call, OpCode.RETURN: self._op_return,
            OpCode.DEFINE_FUNC: self._op_define_func, OpCode.BUILD_ARRAY: self._op_build_array,
            OpCode.LOAD_SUBSCRIPT: self._op_load_subscript, OpCode.STORE_SUBSCRIPT: self._op_store_subscript,
            OpCode.READ_DATA: self._op_read_data, OpCode.RESTORE_DATA: self._op_restore_data,
            OpCode.AWAIT: self._op_await, OpCode.CREATE_TASK: self._op_create_task,
            OpCode.IMPORT_MODULE: self._op_import_module, OpCode.BUILD_DICT: self._op_build_dict,
            OpCode.BUILD_STRING: self._op_build_string, OpCode.SETUP_TRY: self._op_setup_try, OpCode.POP_TRY: self._op_pop_try,
            OpCode.THROW: self._op_throw, OpCode.DUP: self._op_dup,
            OpCode.BUILD_ARRAY_LITERAL: self._op_build_array_literal, OpCode.DEBUG_PRINT: self._op_debug_print,
            OpCode.GET_LENGTH: self._op_get_length, OpCode.BUILD_TUPLE: self._op_build_tuple,
        }
        for opcode, handler in handlers.items(): table[opcode.value] = handler
        return table
    def _read_byte(self, frame): ip = frame.ip; frame.ip += 1; return frame.function.chunk.code[ip]
    def _read_short(self, frame): ip = frame.ip; frame.ip += 2; chunk = frame.function.chunk; return (chunk.code[ip] << 8) | chunk.code[ip+1]
    def _read_constant(self, frame): return frame.function.chunk.constants[self._read_byte(frame)]
    def _op_load_const(self, frame): self.stack.append(self._read_constant(frame))
    def _op_pop(self, frame): self.stack.pop()
    def _op_define_func(self, frame): self.stack.append(self._read_constant(frame))
    def _op_load_global(self, frame):
        name = self._read_constant(frame)
        try: self.stack.append(self.globals[name])
        except KeyError: self._throw(InterpreterError(t('rt_err_var_not_found', name=name), self._get_current_line(frame)))
    def _op_store_global(self, frame): self.globals[self._read_constant(frame)] = self.stack[-1]
    def _op_load_local(self, frame): self.stack.append(self.stack[frame.stack_base + self._read_byte(frame)])
    def _op_store_local(self, frame): self.stack[frame.stack_base + self._read_byte(frame)] = self.stack[-1]
    def _execute_binary_op(self, op, line):
        b, a = self.stack.pop(), self.stack.pop()
        try:
            if isinstance(a, np.ndarray) or isinstance(b, np.ndarray):
                np_op_map = {operator.add: operator.add, operator.sub: operator.sub, operator.mul: operator.mul, operator.truediv: operator.truediv}
                if op not in np_op_map: self._throw(InterpreterError(t('rt_err_unsupported_op_matrix', op_name=op.__name__), line))
                self.stack.append(np_op_map[op](a, b))
            elif op is operator.add:
                if isinstance(a, str) or isinstance(b, str): self.stack.append(str(a) + str(b))
                elif isinstance(a, dict) or isinstance(b, dict): raise TypeError()
                else: self.stack.append(op(a, b))
            else: result = op(a, b); self.stack.append(int(result) if isinstance(result, bool) else result)
        except TypeError: self._throw(InterpreterError(t('rt_err_type_error_op', op=op.__name__, type_a=builtin_type(a).upper(), type_b=builtin_type(b).upper()), line))
    def _op_add(self, frame): self._execute_binary_op(operator.add, self._get_current_line(frame))
    def _op_subtract(self, frame): self._execute_binary_op(operator.sub, self._get_current_line(frame))
    def _op_multiply(self, frame): self._execute_binary_op(operator.mul, self._get_current_line(frame))
    def _op_divide(self, frame): self._execute_binary_op(operator.truediv, self._get_current_line(frame))
    def _op_equal(self, frame): self._execute_binary_op(operator.eq, self._get_current_line(frame))
    def _op_not_equal(self, frame): self._execute_binary_op(operator.ne, self._get_current_line(frame))
    def _op_greater(self, frame): self._execute_binary_op(operator.gt, self._get_current_line(frame))
    def _op_less(self, frame): self._execute_binary_op(operator.lt, self._get_current_line(frame))
    def _op_greater_equal(self, frame): self._execute_binary_op(operator.ge, self._get_current_line(frame))
    def _op_less_equal(self, frame): self._execute_binary_op(operator.le, self._get_current_line(frame))
    def _op_negate(self, frame): self.stack.append(-self.stack.pop())
    def _op_not(self, frame): self.stack.append(0 if self.stack.pop() else 1)
    def _op_print(self, frame): print(self.stack.pop())
    def _op_input(self, frame): self.stack.append(input(self.stack.pop()))
    def _op_jump_if_false(self, frame):
        offset = self._read_short(frame)
        if not self.stack[-1]: frame.ip += offset
    def _op_jump(self, frame): frame.ip += self._read_short(frame)
    def _op_loop(self, frame): frame.ip -= self._read_short(frame)
    def _op_call(self, frame):
        const_idx, arg_count = self._read_byte(frame), self._read_byte(frame); current_line = self._get_current_line(frame)
        if const_idx == 0xFF:
            callee = self.stack[-(arg_count + 1)]
            if isinstance(callee, FunctionObject):
                if callee.arity != arg_count: self._throw(InterpreterError(t('rt_err_func_arity_mismatch', name=callee.name, expected=callee.arity, received=arg_count), current_line))
                if callee.is_async: self._throw(InterpreterError(t('rt_err_cannot_call_async', name=callee.name), current_line))
                self.frames.append(CallFrame(callee, 0, len(self.stack) - arg_count -1))
            else: self._throw(InterpreterError(t('rt_err_cannot_call_type', type_name=type(callee)), current_line))
        else:
            func_name = frame.function.chunk.constants[const_idx]
            args = [self.stack.pop() for _ in range(arg_count)][::-1]
            if func_name in self.jit_functions: result = self.jit_functions[func_name](*args)
            elif func_name in BUILTIN_FUNCTIONS:
                try: result = BUILTIN_FUNCTIONS[func_name](*args)
                except MomentumExit as e: raise e
                except Exception as e: self._throw(InterpreterError(str(e), current_line))
            else: self._throw(InterpreterError(t('rt_err_unknown_builtin', name=func_name), current_line))
            self.stack.append(result if result is not None else None)
    def _op_return(self, frame):
        result = self.stack.pop()
        closed_frame = self.frames.pop()
        self.stack = self.stack[:closed_frame.stack_base]
        self.stack.append(result)
        if not self.frames:
            self.frames.append(None)
    def _op_build_array(self, frame):
        dims = self._read_byte(frame); sizes = tuple(int(s) for s in self.stack[-dims:]); self.stack = self.stack[:-dims]; self.stack.append(np.zeros(sizes))
    
    def _op_load_subscript(self, frame):
        key = self.stack.pop()
        container = self.stack.pop()
        line = self._get_current_line(frame)
        try:
            # The key can now be a single value or a tuple for multi-dim access
            self.stack.append(container[key])
        except (KeyError, IndexError): self._throw(InterpreterError(f"Key/Index error: '{key}' not found.", line))
        except TypeError:
            if isinstance(container, dict) and not isinstance(key, str):
                self._throw(InterpreterError(t('rt_err_invalid_key_type', container_type='DICTIONARY', key_type=builtin_type(key)), line))
            else:
                self._throw(InterpreterError(t('rt_err_not_subscriptable', type_name=builtin_type(container)), line))

    def _op_store_subscript(self, frame):
        value = self.stack.pop()
        key = self.stack.pop()
        container = self.stack.pop()
        line = self._get_current_line(frame)
        try:
            container[key] = value
            self.stack.append(value) # Assignment expressions should leave the value on the stack
        except (KeyError, IndexError): self._throw(InterpreterError(f"Key/Index error: '{key}' not found.", line))
        except TypeError:
            if isinstance(container, dict) and not isinstance(key, str):
                self._throw(InterpreterError(t('rt_err_invalid_key_type', container_type='DICTIONARY', key_type=builtin_type(key)), line))
            else:
                self._throw(InterpreterError(t('rt_err_not_subscriptable', type_name=builtin_type(container)), line))

    def _op_read_data(self, frame):
        if self.data_ptr >= len(self.data_pool): self._throw(InterpreterError(t('error_out_of_data'), self._get_current_line(frame)))
        self.stack.append(self.data_pool[self.data_ptr]); self.data_ptr += 1
    def _op_restore_data(self, frame): self.data_ptr = 0
    async def _op_await_async(self, frame):
        awaitable = self.stack.pop(); self.stack.append(await awaitable if asyncio.iscoroutine(awaitable) else awaitable)
    def _op_await(self, frame): return self._op_await_async(frame)
    def _op_create_task(self, frame): asyncio.create_task(self.stack.pop())
    async def _op_import_module_async(self, frame):
        module_name = self._read_constant(frame); module_path = str((self.base_path / module_name).resolve())
        module_function = self.compiled_modules[module_path]
        module_vm = VM(self.jit_functions, [], self.compiled_modules, self.base_path)
        await module_vm.run(module_function); self.globals.update(module_vm.globals)
    def _op_import_module(self, frame): return self._op_import_module_async(frame)
    def _op_build_dict(self, frame):
        count = self._read_byte(frame); new_dict = {}
        for _ in range(count): value = self.stack.pop(); key = self.stack.pop(); new_dict[key] = value
        self.stack.append(new_dict)
    def _op_build_string(self, frame):
        count = self._read_byte(frame)
        parts = [str(self.stack.pop()) for _ in range(count)]
        self.stack.append("".join(reversed(parts)))
    def _op_setup_try(self, frame):
        offset = self._read_short(frame); handler_ip = frame.ip + offset
        self.try_stack.append(TryBlock(handler_ip, len(self.stack)))
    def _op_pop_try(self, frame): self.try_stack.pop()
    def _op_throw(self, frame): self._throw(self.stack.pop())
    def _op_dup(self, frame): self.stack.append(self.stack[-1])
    def _throw(self, error_obj):
        if not self.try_stack: raise error_obj
        try_block = self.try_stack.pop(); self.stack = self.stack[:try_block.stack_size]
        self.frames[-1].ip = try_block.handler_ip
        if isinstance(error_obj, InterpreterError): self.stack.append(error_obj.raw_message)
        else: self.stack.append(str(error_obj))
    def _op_build_array_literal(self, frame):
        count = self._read_byte(frame)
        elements = self.stack[-count:]
        self.stack = self.stack[:-count]
        self.stack.append(np.array(elements, dtype=object))
    def _op_build_tuple(self, frame):
        count = self._read_byte(frame)
        elements = tuple(self.stack[-count:])
        self.stack = self.stack[:-count]
        self.stack.append(elements)
    def _op_debug_print(self, frame):
        value = self.stack.pop()
        expr_str = self._read_constant(frame)
        type_str = builtin_type(value)
        if colorama_enabled:
            print(f"{Fore.CYAN}[DEBUG]{Style.RESET_ALL} {expr_str} ({Fore.YELLOW}{type_str}{Style.RESET_ALL}): {Fore.GREEN}{repr(value)}{Style.RESET_ALL}")
        else:
            print(f"[DEBUG] {expr_str} ({type_str}): {repr(value)}")
    def _op_get_length(self, frame):
        container = self.stack.pop()
        try:
            self.stack.append(len(container))
        except TypeError:
            self._throw(InterpreterError(f"Object of type '{builtin_type(container)}' has no len()", self._get_current_line(frame)))
    def _get_current_line(self, frame): return frame.function.chunk.get_line(max(0, frame.ip - 1))
    def _generate_stack_trace(self):
        trace = []
        for frame in reversed(self.frames):
            if frame is None: continue
            context = f"function {frame.function.name}" if frame.function.name != "<script>" else "<script>"
            trace.append({"file": frame.function.chunk.name, "line": self._get_current_line(frame), "context": context})
        return trace
    async def run(self, main_function):
        main_frame = CallFrame(main_function, 0, 0)
        self.frames.append(main_frame)
        try:
            while self.frames and self.frames[-1] is not None:
                frame = self.frames[-1]
                handler = self.dispatch_table[frame.function.chunk.code[frame.ip]]; frame.ip += 1
                result = handler(frame)
                if asyncio.iscoroutine(result): await result
        except InterpreterError as e:
            if not e.stack_trace: e.stack_trace = self._generate_stack_trace()
            raise e
        except (IndexError, TypeError, ValueError, ZeroDivisionError, KeyError) as e:
            current_frame = self.frames[-1] if self.frames else None
            current_line = self._get_current_line(current_frame) if current_frame else '?'
            raise InterpreterError(f"{type(e).__name__}: {e}", current_line, self._generate_stack_trace()) from e

        return self.stack[0] if self.stack else None

JIT_FUNCTIONS, COMPILED_MODULES_CACHE = {}, {}
def extract_data(ast_root):
    data_pool = []
    def traverse(node):
        if isinstance(node, Data):
            for val_node in node.values:
                if isinstance(val_node, (Num, String)): data_pool.append(val_node.value)
                else: raise ParserError(t('p_err_data_literal_only'), val_node.token)
        elif hasattr(node, '__dict__'):
            for child in node.__dict__.values():
                if isinstance(child, list): [traverse(item) for item in child]
                elif isinstance(child, AST): traverse(child)
    traverse(ast_root); return data_pool
def compile_source(source_code, module_name, base_path, source_lines_map):
    source_lines_map[module_name] = source_code.splitlines()
    lexer = Lexer(source_code); tokens = lexer.tokenize_all(); parser = Parser(tokens); ast = parser.parse()
    for stmt in ast.statements:
        if isinstance(stmt, Import): compile_module(stmt.filename_token.value, base_path, source_lines_map)
    compiler = Compiler(); compiled_function = compiler.compile(ast)
    compiled_function.chunk.name = module_name; return (compiled_function, ast)
def compile_module(file_path_str, base_path, source_lines_map):
    full_path = (base_path / file_path_str).resolve(); full_path_str = str(full_path)
    if full_path_str in COMPILED_MODULES_CACHE: return COMPILED_MODULES_CACHE[full_path_str]
    try:
        with open(full_path, 'r', encoding='utf-8-sig') as f: code = f.read()
    except FileNotFoundError: raise InterpreterError(t('error_import_failed', path=full_path), -1)
    compiled_function, _ = compile_source(code, Path(file_path_str).name, full_path.parent, source_lines_map)
    COMPILED_MODULES_CACHE[full_path_str] = compiled_function; return compiled_function
async def run_momentum(entry_file_path):
    base_path = Path(entry_file_path).parent; source_lines_map = {}
    main_file_name = Path(entry_file_path).name
    try:
        with open(entry_file_path, 'r', encoding='utf-8-sig') as f: main_code = f.read()
        main_function, ast_for_data = compile_source(main_code, main_file_name, base_path, source_lines_map)
    except MomentumError as e:
        format_momentum_error(e, source_lines_map.get(main_file_name))
        raise

    data_pool = extract_data(ast_for_data)
    if NUMBA_ENABLED:
        try:
            transpiler = MomentumToPythonTranspiler(); jit_namespace = {'numba': numba, 'math': math}
            for stmt in ast_for_data.statements:
                if isinstance(stmt, FuncDef) and stmt.is_jit:
                    func_name = stmt.name.lower(); py_code = transpiler.transpile(stmt)
                    params_str = ", ".join(p.value.lower() for p in stmt.params)
                    full_src = f"def {func_name}_impl({params_str}):\n{py_code or '    pass'}"
                    exec(full_src, jit_namespace); py_func = jit_namespace[f"{func_name}_impl"]
                    jitted_func = numba.jit(nopython=True, parallel=True)(py_func)
                    JIT_FUNCTIONS[func_name] = jitted_func; jit_namespace[func_name] = jitted_func
        except Exception as e: print(t('error_jit_failed', e=e), file=sys.stderr); JIT_FUNCTIONS.clear()
    
    vm = VM(JIT_FUNCTIONS, data_pool, COMPILED_MODULES_CACHE, base_path)
    try:
        await vm.run(main_function)
    except InterpreterError as e:
        if not e.stack_trace: e.stack_trace = vm._generate_stack_trace()
        error_file = e.stack_trace[0]['file'] if e.stack_trace else main_file_name
        format_momentum_error(e, source_lines_map.get(error_file, []))
        raise
    except Exception as e:
        format_momentum_error(e, [])
        raise

async def run_repl():
    print(t('repl_welcome'))
    vm = VM(JIT_FUNCTIONS, [], {}, Path.cwd())
    source_lines_map = {}
    shared_globals = {} 

    while True:
        try:
            line = input(">>> ")
            if line.strip().lower() == "exit()":
                break
            if not line.strip():
                continue

            vm.frames.clear()
            vm.stack.clear()
            vm.try_stack.clear()
            vm.globals = shared_globals

            func, ast = compile_source(line, "<stdin>", Path.cwd(), source_lines_map)
            
            is_expression_statement = False
            if ast and len(ast.statements) == 1:
                stmt = ast.statements[0]
                # Check against a broader set of statement types
                if not isinstance(stmt, (Print, Assign, If, While, For, ForEach, FuncDef, Return, Dim, Read, Restore, Import, Break, Continue, Try, Switch, Debug, Declare)):
                    is_expression_statement = True

            result = await vm.run(func)
            shared_globals = vm.globals

            if is_expression_statement and result is not None:
                if colorama_enabled:
                    print(Fore.MAGENTA + repr(result))
                else:
                    print(repr(result))

        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break
        except (MomentumError, Exception) as e:
            format_momentum_error(e, source_lines_map.get("<stdin>", []))

def _ensure_array(arr, func_name):
    if not isinstance(arr, np.ndarray): raise TypeError(f"{func_name}() expects an array as input.")
    return arr
def builtin_type(value):
    if isinstance(value, int): return "INTEGER";
    if isinstance(value, float): return "FLOAT";
    if isinstance(value, str): return "STRING";
    if isinstance(value, np.ndarray): return "ARRAY";
    if isinstance(value, dict): return "DICTIONARY";
    if isinstance(value, FunctionObject): return "FUNCTION";
    if isinstance(value, tuple): return "TUPLE";
    if value is None: return "NONE" # Handle None type
    return str(type(value))
def builtin_file_read(path):
    try:
        with open(path, 'r', encoding='utf-8') as f: return f.read()
    except Exception as e: raise InterpreterError(f"File read error: {e}", -1)
def builtin_file_write(path, content):
    try:
        with open(path, 'w', encoding='utf-8') as f: f.write(str(content)); return 1
    except Exception as e: raise InterpreterError(f"File write error: {e}", -1)
def builtin_json_parse(text):
    try: return json.loads(text)
    except json.JSONDecodeError as e: raise InterpreterError(f"JSON parse error: {e}", -1)
def builtin_json_stringify(obj):
    try: return json.dumps(obj)
    except TypeError as e: raise InterpreterError(f"JSON stringify error: {e}", -1)
def builtin_exit(code=0): raise MomentumExit(int(code))
def builtin_assert(condition, message=""):
    if not condition: raise InterpreterError(t('rt_err_assertion_failed', message=message), -1)
    return 1
def builtin_is_int(v): return 1 if isinstance(v, int) else 0
def builtin_is_float(v): return 1 if isinstance(v, float) else 0
def builtin_is_string(v): return 1 if isinstance(v, str) else 0
def builtin_is_array(v): return 1 if isinstance(v, np.ndarray) else 0
def builtin_is_dict(v): return 1 if isinstance(v, dict) else 0
def builtin_keys(d):
    if not isinstance(d, dict): raise TypeError("keys() expects a dictionary.")
    return np.array(list(d.keys()))
def builtin_values(d):
    if not isinstance(d, dict): raise TypeError("values() expects a dictionary.")
    return np.array(list(d.values()))
def builtin_max(*args):
    if len(args) == 1 and isinstance(args[0], (np.ndarray, list)): return np.max(args[0])
    return max(args)
def builtin_min(*args):
    if len(args) == 1 and isinstance(args[0], (np.ndarray, list)): return np.min(args[0])
    return min(args)
def builtin_sum(arr): return np.sum(_ensure_array(arr, "sum"))
def builtin_upper(s): return str(s).upper()
def builtin_lower(s): return str(s).lower()
def builtin_trim(s): return str(s).strip()
def builtin_split(s, delimiter): return np.array(str(s).split(delimiter))
def builtin_join(arr, delimiter): return str(delimiter).join(map(str, arr))
def builtin_replace(s, old, new): return str(s).replace(str(old), str(new))
def builtin_os_cwd(): return os.getcwd()
def builtin_os_list_dir(path="."): return np.array(os.listdir(path))
def builtin_os_exists(path): return 1 if os.path.exists(path) else 0
def builtin_os_is_file(path): return 1 if os.path.isfile(path) else 0
def builtin_os_is_dir(path): return 1 if os.path.isdir(path) else 0
def builtin_os_make_dir(path): os.makedirs(path, exist_ok=True); return 1
def builtin_os_remove_file(path): os.remove(path); return 1
def builtin_os_rename(src, dst): os.rename(src, dst); return 1
async def builtin_sleep(seconds): await asyncio.sleep(seconds)
def builtin_average(arr): return np.mean(_ensure_array(arr, "AVERAGE"))
def builtin_median(arr): return np.median(_ensure_array(arr, "MEDIAN"))
def builtin_stdev_p(arr): return np.std(_ensure_array(arr, "STDEV_P"))
def builtin_var_p(arr): return np.var(_ensure_array(arr, "VAR_P"))
def builtin_mode_sngl(arr):
    arr = _ensure_array(arr, "MODE_SNGL").flatten()
    if arr.size == 0: return None
    counts = Counter(arr); max_count = max(counts.values()); return [val for val, count in counts.items() if count == max_count][0]
def builtin_frequency(data, bins):
    data = _ensure_array(data, "FREQUENCY"); bins_arg = bins if isinstance(bins, np.ndarray) else int(bins)
    frequencies, bin_edges = np.histogram(data, bins=bins_arg); result = np.zeros((2, len(frequencies)))
    result[0, :] = bin_edges[:-1]; result[1, :] = frequencies; return result
def builtin_logic_truth_table(num_vars):
    num_vars = int(num_vars)
    if num_vars < 1: return np.array([])
    return np.array(list(itertools.product([0, 1], repeat=num_vars)))
def builtin_mat_transpose(matrix): return _ensure_array(matrix, "mat_transpose").T
def builtin_mat_determinant(matrix): return np.linalg.det(_ensure_array(matrix, "mat_determinant"))
def builtin_mat_identity(n): return np.identity(int(n))
def builtin_mat_zeros(rows, cols=None): return np.zeros((int(rows), int(cols if cols is not None else rows)))
def builtin_mat_ones(rows, cols=None): return np.ones((int(rows), int(cols if cols is not None else rows)))
def builtin_mat_inverse(matrix):
    try: return np.linalg.inv(_ensure_array(matrix, "mat_inverse"))
    except np.linalg.LinAlgError as e: raise InterpreterError(t('rt_err_mat_inverse_failed', e=e), -1)
def builtin_mat_solve(A, B):
    try: return np.linalg.solve(_ensure_array(A, "mat_solve (A)"), _ensure_array(B, "mat_solve (B)"))
    except np.linalg.LinAlgError as e: raise InterpreterError(t('rt_err_mat_solve_failed', e=e), -1)
def builtin_mat_eig(matrix):
    eigenvalues, eigenvectors = np.linalg.eig(_ensure_array(matrix, "mat_eig"))
    return np.array([eigenvalues, eigenvectors], dtype=object)
def builtin_mat_mul(A, B): return np.dot(_ensure_array(A, "mat_mul A"), _ensure_array(B, "mat_mul B"))
def builtin_rows(matrix): return matrix.shape[0] if isinstance(matrix, np.ndarray) and matrix.ndim > 0 else 0
def builtin_cols(matrix): return matrix.shape[1] if isinstance(matrix, np.ndarray) and matrix.ndim > 1 else 0
class Let(AST): pass 

BUILTIN_FUNCTIONS = {
    'time': time.time, 'str': str, 'int': int, 'float': float, 'len': len, 'abs': abs, 'round': round, 'type': builtin_type,
    'is_int': builtin_is_int, 'is_float': builtin_is_float, 'is_string': builtin_is_string, 'is_array': builtin_is_array, 'is_dict': builtin_is_dict,
    'keys': builtin_keys, 'values': builtin_values, 'upper': builtin_upper, 'lower': builtin_lower, 'trim': builtin_trim, 'split': builtin_split, 
    'join': builtin_join, 'replace': builtin_replace, 'sqrt': math.sqrt, 'sin': math.sin, 'cos': math.cos,
    'random': random.random, 'randint': random.randint, 'max': builtin_max, 'min': builtin_min, 'sum': builtin_sum,
    'logic_truth_table': builtin_logic_truth_table, 'average': builtin_average, 'median': builtin_median, 'mode_sngl': builtin_mode_sngl,
    'stdev_p': builtin_stdev_p, 'var_p': builtin_var_p, 'frequency': builtin_frequency,
    'rows': builtin_rows, 'cols': builtin_cols, 'mat_mul': builtin_mat_mul, 'mat_transpose': builtin_mat_transpose, 
    'mat_determinant': builtin_mat_determinant, 'mat_inverse': builtin_mat_inverse, 'mat_identity': builtin_mat_identity,
    'mat_zeros': builtin_mat_zeros, 'mat_ones': builtin_mat_ones, 'mat_solve': builtin_mat_solve, 'mat_eig': builtin_mat_eig,
    'os_cwd': builtin_os_cwd, 'os_list_dir': builtin_os_list_dir, 'os_exists': builtin_os_exists,
    'os_is_file': builtin_os_is_file, 'os_is_dir': builtin_os_is_dir, 'os_make_dir': builtin_os_make_dir, 
    'os_remove_file': builtin_os_remove_file, 'os_rename': builtin_os_rename, 'file_read': builtin_file_read, 'file_write': builtin_file_write,
    'json_parse': builtin_json_parse, 'json_stringify': builtin_json_stringify, 'exit': builtin_exit, 'assert': builtin_assert,
    'gfx_init': gfx_init, 'gfx_set_color': gfx_set_color, 'gfx_draw_line': gfx_draw_line, 
    'gfx_draw_rect': gfx_draw_rect, 'gfx_draw_circle': gfx_draw_circle, 'gfx_update': gfx_update, 'gfx_wait': gfx_wait,
}
ASYNC_BUILTIN_FUNCTIONS = {'sleep': builtin_sleep}
BUILTIN_FUNCTIONS.update(ASYNC_BUILTIN_FUNCTIONS)

if __name__ == "__main__":
    exit_code = 0
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        if not os.path.exists(filename):
            print(t('error_file_not_found', filename=filename), file=sys.stderr); sys.exit(1)
        print(t('running_header', filename=filename))
        try:
            asyncio.run(run_momentum(filename))
            print(t('run_success'))
        except MomentumExit as e: exit_code = e.code
        except (MomentumError, Exception): exit_code = 1
        finally:
            if GFX_GLOBALS["window"]: gfx_wait()
        print(t('run_finished_divider'))
    else:
        try: asyncio.run(run_repl())
        except MomentumExit as e: exit_code = e.code
    sys.exit(exit_code)