import interpreter
import simulator


def generate_read(inputstr):
    def read():
        nonlocal inputstr
        if len(inputstr) > 0:
            res = int(inputstr[0])
            inputstr = inputstr[1:]
            return res
        else:
            return 255

    return read


def generate_write():
    output = b''

    def write(s):
        nonlocal output
        output += bytes(s)

    def get_output():
        return output

    return write, get_output


def execute(assembly, inputstr):
    read = generate_read(inputstr)
    write, output = generate_write()

    simulator.simulate(assembly, read, write)
    return output()


def interpret(code, inputstr):
    read = generate_read(inputstr)
    write, output = generate_write()

    interpreter.interpret(code, read, write)
    return output()
