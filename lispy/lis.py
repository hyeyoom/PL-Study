import re
import math
import operator as op

class Lexer:
    def __init__(self, rules):
        self.rules = rules

    def tokenize(self, program):
        '''tokenize program'''
        test_list = program.replace('(', ' ( ').replace(')', ' ) ').split()
        tokens = []
        for test in test_list:
            tokens.append(self.lex(test))
        return tokens

    def lex(self, test):
        '''test token'''
        for rule in self.rules:
            p = re.compile(rule[1], re.UNICODE)
            if p.findall(test):
                return (rule[0], test)  # token, actual value
        raise SyntaxError('Invalid token: ' + str(test))


class Parser:
    def __init__(self):
        pass

    def parse(self, tokens):
        return self.read(tokens)

    def read(self, tokens):
        token = tokens.pop(0)
        if token[0] == 'LPAREN':
            r = []
            while tokens[0][0] != 'RPAREN':
                r.append(self.read(tokens))
            tokens.pop(0)
            return r
        elif token[0] == 'RPAREN':
            raise SyntaxError('Unexpected right parentheses!')
        else:
            return self.atom(token)

    def atom(self, token):
        '''atomic operation for token'''
        if token[0] == 'NUMBER':
            return self.convert_number(token[1])
        if token[0] == 'IDENT' or token[0] == 'KEYWORD' or token[0] == 'OPERATOR':
            return str(token[1])
        raise SyntaxError('Invalid token: ' + str(token))

    def convert_number(self, number):
        f_regex = r'[+-]?\d*\.\d+' # floating number
        d_regex = r'[+-]?\d+'   # number

        pf = re.compile(f_regex)
        pd = re.compile(d_regex)

        if pf.findall(number):
            return float(number)
        if pd.findall(number):
            return int(number)
        raise ValueError('Not a number!')


def lisp_env():
    env = dict()
    env.update(vars(math))
    env.update({
        '+': op.add, '-': op.sub, '*': op.mul, '/': op.div,
        '>': op.gt , '<': op.lt , '>=': op.ge, '<=': op.le, '=': op.eq,
        'begin': lambda *x: x[-1],
        'print': lambda x: pr(x)
    })
    return env

def pr(x):
    print x

class VirtualMachine:
    def __init__(self, env=lisp_env()):
        self.env = env

    def eval(self, x):
        if isinstance(x, str):
            return self.env[x]
        elif not isinstance(x, list):
            return x
        elif x[0] == 'if':
            (_, test, conseq, alt) = x
            exp = (conseq if self.eval(test) else alt)
            return self.eval(exp)
        elif x[0] == 'define':
            (_, var, exp) = x
            self.env[var] = self.eval(exp)
        else:
            proc = self.eval(x[0])
            args = [self.eval(arg) for arg in x[1:]]
            return proc(*args)


def convert_keywords_to_regex(l):
    r = []
    for x in l:
        r.append('\\b%s\\b' % x)
    return r'|'.join(r)


def repl(rules, prompt='lisp$ '):
    lexer = Lexer(rules)
    parser = Parser()
    vm = VirtualMachine()
    while True:
        tokens = lexer.tokenize(raw_input(prompt))
        ast = parser.parse(tokens)
        try:
            vm.eval(ast)
        except KeyError:
            print 'Unable to process identifier or function.'

if __name__ == '__main__':
    keywords = [
        'begin', 'define'
    ]

    lex_rules = [
        ('LPAREN',      r'^\('),    # left parentheses
        ('RPAREN',      r'^\)'),    # right parentheses
        ('NUMBER',      r'[+-]?\d*\.\d+|\d+'),    # any number that contains floating numbers
        ('KEYWORD',     convert_keywords_to_regex(keywords)),
        ('OPERATOR',    r'^[+-/*//]'),
        ('IDENT',  r'^[^\d\W]\w*\Z'),      # identifier
        ('WHITE',  r'^[ \t\r\n]')  # whitespace
    ]

    repl(lex_rules)