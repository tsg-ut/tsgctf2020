# Language X

## Syntax

```
<program> ::= <function> <program> | <id> ";" <program> | ""
<function> ::= <id> "(" <arguments> ")" "{" <statement>* "}"
<arguments> ::= "" | <id> ("," <id>)*
<statement_list> ::= "{" <statement>* "}" | <statement>

<statement> ::= "if" "(" <expr> ")" <statement_list> ["else" <statement_list>]
              | "while" "(" <expr> ")" <statement_list>
              | <id> "=" <expr> ";"
              | <expr> ";"
              | "return" <expr> ";"

<expr> ::= "(" <expr> ")"
         | "[" "]"
         | "[" <expr> ("," <expr>)* "]"
         | <expr> "[" <expr> "]"
         | "-" <expr>
         | "!" <expr> 
         | <expr> <binop> <expr>
         | <digit>
         | <id> 
         | <string>

<binop> ::= "+" | "-" | "*" | "/" | "%" | "||" | "&&" | "==" | "!=" | ">" | "<" | "<=" | ">="
<id> ::= [0-9A-Za-z_]*
<digit> ::= [0-9]*
<string> ::= string quoted by '"'
```

## Semantics

As expected. (As implemented)

- Program starts from main function.
- The value is an integer or a list of values.
	- String is a list of integers. (eg. `"abc"` is syntax suger for `[97, 98, 99]`)
	- Operator `+`, `==` and `!=` are overloaded
- Scope of variables:
	- If the variable is appeared in the argument of the function, it is local variable.
	- Otherwise if the variable is already declared in the global scope, it is global variable.
	- Otherwise, it is local variable.
- built-in functions:
	- `read()`
		- Read a character from stdin and return its character code.
	- `write(s)`
		- Write string `s` to stdout.
	- `len(v)`
		- Return the length of `v`.

# Assembly Y

## Syntax

```
<assembly> ::= <operation>* 
<operation> ::= "mov" <operand> <operand>
              | "makelist" <operand> "[" "]"
              | "makelist" <operand> "["<operand> ("," <operand>)* "]"
              | <binop> <operand> <operand> <operand>
              | "push"
              | "pop"
              | "call" <digit>
              | "ret" 
              | "jz" <digit>
              | "read"
              | "write"
              | "len"
              | "get"
              | "hlt"

<binop> ::= "add" | "sub" | "mul" | "div" | "lt" | "eq" 
<operand> ::= "bp" | "sp" | "bp[" <digit> "]" | "#" <digit> | <digit>
<digit> ::= [0-9]+
```

## Semantics

As expected. (As implemented.)

- The VM has two registers `bp` and `sp`, and has memory.
- The value is an integer or a list of values.
- Initialization:
	- Two registers and instruction pointer are set to 0.
	- Memory is filled with None.
- The address of `call` and `jz` is an absolute address. 

The address of nth instruction is n.

# Attached Programs

## `compiler.x`

The self-hosted compiler of Language X.

* Input: Program to compile.
* Output: Compiled Assembly Y of the input program.

## `interpreter.py`

The interpreter of Language X.

Usage: `python interpreter.py [program.x]`

* stdin: Input to the program
* stdout: Output of the program

## `simulator.py`

The simulator of Assembly Y.

Usage: `python simulator.py [program.y]`

* stdin: Input to the assembly
* stdout: Output of the assembly

## `program.py`

The server to validate your compiler :)

Usage: `python program.py`

* stdin: The compiler of Language X written in Assembly Y
* stdout: Output


