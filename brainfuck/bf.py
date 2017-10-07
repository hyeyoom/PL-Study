import re


class DataSegment:
    def __init__(self, size=1024):
        self.data = [0] * size
        self.ds = 0

    def check_memory_bound(self):
        if self.ds >= len(self.data) or self.ds < 0:
            raise IndexError('Segment fault.')

    def inc(self):
        self.data[self.ds] += 1

    def dec(self):
        self.data[self.ds] -= 1

    def shl(self):
        self.ds -= 1
        self.check_memory_bound()

    def shr(self):
        self.ds += 1
        self.check_memory_bound()

    def dot(self):
        print chr(self.data[self.ds]),

    def com(self):
        self.data[self.ds] = raw_input()

    def cur(self):
        return self.data[self.ds]

    def __str__(self):
        s = [str(x) for x in self.data]
        return '[' + '|'.join(s) + '](ptr:' + str(self.ds) + ')'

def virtual_machine(program):
    tokens = tokenize(program) # list of operators (actual code)
    ds = DataSegment(10) # data seg
    os = list() # operand stack
    ip = 0 # instruction pointer

    while ip < len(tokens):
        token = tokens[ip]

        if token == '+':
            ds.inc()
        if token == '-':
            ds.dec()
        if token == '>':
            ds.shr()
        if token == '<':
            ds.shl()
        if token == '.':
            ds.dot()
        if token == ',':
            ds.com()
        if token == '[':
            os.append(ip) # store current instruction pointer
        if token == ']':
            t = os.pop()
            if ds.cur() != 0:
                ip = t - 1

        ip += 1

def tokenize(program):
    p = re.compile('[><.,+-\[\]]')
    t = [x for x in program if len(p.findall(x))]
    if len(t) != len(program):
        raise SyntaxError('Unexpected token!')
    return t

if __name__ == '__main__':
    code = '++++++++++[>+++++++>++++++++++>+++>+<<<<-]>++.>+.+++++++..+++.>++.<<+++++++++++++++.>.+++.------.--------.>+.>.'
    virtual_machine(code)