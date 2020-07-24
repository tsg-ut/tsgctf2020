import random
import copy
from utility import interpret


def new_id():
    global env
    cs = list(map(chr, list(range(0x41, 0x5b)) +
                  list(range(0x61, 0x7b)) + [0x5f]))
    tcs = list('1234567890') + cs
    while True:
        res = random.choice(
            cs) + ''.join([random.choice(tcs) for _ in range(random.randrange(5))])
        if res.isdigit():
            continue
        if res in (env['ok'] + env['ng']):
            continue
        env['ng'].append(res)
        return res


def new_func_id():
    global env
    v = new_id()
    env['ng'].remove(v)
    return v


def oknize(v):
    global env
    env['ng'].remove(v)
    env['ok'].append(v)


def random_id():
    global env
    return random.choice(env['ok'])


def random_number():
    return str(random.randrange(-200, 200))


def random_expr():
    global env
    x = random.randrange(100)
    if x in range(0, 5):
        return f"({random_expr()})"
    elif x in range(5, 25):
        return random_id()
    elif x in range(25, 50):
        return random_number()
    elif x in range(50, 60):
        if x in range(50, 52):
            if len(env['funcs']) == 0:
                return random_expr()
            fn, argn = random.choice(env['funcs'])
            return f"{fn}({''.join([random_id() for _ in range(args)])})"
        elif x in range(53, 55):
            return "read()"
        else:
            vs = [
                f"(({random_expr()}) % 256 + 256) % 256" for _ in range(random.randrange(5))]
            return f"write([{','.join(vs)}])"
    elif x in range(60, 100):
        if x <= 80:
            ops = ["+", "-", "*"]
        else:
            ops = ["||", "&&", "==", "!=", ">", "<", ">=", "<="]
        return f"{random_expr()} {random.choice(ops)} {random_expr()}"


def random_statement():
    global env
    x = random.randrange(100)
    if x <= 35:
        v = new_id()
        res = f"{v} = {random_expr()};"
        oknize(v)
        return res
    if x <= 35:
        return f"{random_id()} = {random_expr()};"
    elif x <= 70:
        return f"{random_expr()};"
    elif x <= 80:
        cond = random_expr()
        memenv = copy.deepcopy(env)
        ift = random_statements()
        env = copy.deepcopy(memenv)
        iff = random_statements()
        env = memenv
        return f"if({cond}){{{ift}}}else{{{iff}}}"
    elif x <= 90:
        return f"return {random_expr()};"
    else:
        v = new_id()
        return f"{v}=0; while({v} < {random.randrange(1,3)}){{ {random_statements()} {v} = {v} + 1; }}"


def random_statements():
    ls = random.randrange(5)
    return "".join([random_statement() for _ in range(ls)])


def random_program():
    global env
    res = ""
    funcnum = random.randrange(1, 5)
    for c in range(funcnum):
        env = {'ok': [], 'ng': [], 'funcs': []}
        if c == funcnum - 1:
            fn = "main"
            args = []
            iv = new_id()
            oknize(iv)
        else:
            fn = new_func_id()
            args = [new_id() for _ in range(random.randrange(1, 5))]
        for v in args:
            oknize(v)
        body = random_statements() + f"return {random_expr()};"
        env['funcs'].append((fn, len(args)))
        if fn == 'main':
            body = f'{iv} = {random.randrange(200)};' + body
        res += f"{fn}({','.join(args)}){{{body}}}"

    if len(res) in range(3000, 5000):
        return bytes(res, 'ascii')
    else:
        return random_program()


default_testcase = [(open(f'tests/{s}.x', 'rb').read(), [])
                    for s in ['helloworld', 'list', 'scope']]
default_testcase.append((open('tests/fib.x', 'rb').read(),
                         bytes(str(random.randrange(10, 20)), 'ascii')))


def generate_testcases():
    res = []
    while len(res) < 5:
        prog = random_program()
        inputstr = [random.randrange(256)
                    for _ in range(random.randrange(100))]
        if len(interpret(prog, inputstr)) == 0:
            continue
        res.append((prog, inputstr))

    return default_testcase + res


if __name__ == '__main__':
    import sys
    c, _ = generate_testcases()[0]
    sys.stdout.buffer.write(c)
