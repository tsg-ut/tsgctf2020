from lark import Lark, Transformer, v_args

grammer = """
  ?start: expr
  ?expr: cond
  ?cond: or
    | or "?" cond ":" cond -> cond
  ?or: and
    | or "||" and          -> logical_or
  ?and: not
    | and "&&" not         -> logical_and
  ?not: compare
    | "!" not              -> not_
  ?compare: bits
    | compare "<" bits     -> lt
    | compare "<=" bits    -> le
    | compare ">" bits     -> gt
    | compare ">=" bits    -> ge
    | compare "==" bits    -> eq
    | compare "!=" bits    -> ne
  ?bits: bitshift
    | bits "|" bitshift    -> or_
    | bits "^" bitshift    -> xor
    | bits "&" bitshift    -> and_
  ?bitshift: sum
    | bitshift "<<" sum    -> lshift
    | bitshift ">>" sum    -> rshift
  ?sum: product
    | sum "+" product      -> add
    | sum "-" product      -> sub
  ?product: atom
    | product "*" atom     -> mul
    | product "/" atom     -> floordiv
    | product "%" atom     -> mod
  ?atom: INT               -> int
    | "True"               -> true
    | "False"              -> false
    | "-" atom             -> neg
    | "+" atom             -> pos
    | "N"                  -> input
    | "(" expr ")"
  %import common.INT
  %import common.WS_INLINE
  %ignore WS_INLINE
"""

@v_args(inline=True)
class Parser(Transformer):
  from operator import not_, lt, le, gt, ge, eq, ne, or_, xor, and_, lshift, rshift, add, sub, mul, floordiv, mod, neg, pos
  int = int

  def __init__(self):
    self.var = 0
  def cond(self, condition, verum, falsum):
    if condition:
      return verum
    else:
      return falsum
  def logical_or(self, a, b):
    return a or b
  def logical_and(self, a, b):
    return a and b
  def true(self):
    return True
  def false(self):
    return False
  def input(self):
    return self.var

parser = Parser()
interpreter = Lark(grammer, parser='lalr', transformer=parser)

def interpret(script, var):
  parser.var = var
  return interpreter.parse(script)