import sys


class My:
    def __init__(self, code):
        self.code = code
        self.line_nr = 0
        self.token_feed = self.tokens()
        self.returned_token = None
        self.stack = []
        self.vars = {}

    def raise_error(self, message):
        raise ValueError(f'{self.line_nr}: {message}')

    def tokens(self):
        for line in self.code.strip().split('\n'):
            self.line_nr += 1
            for token in line.strip().split(' '):
                if token in ['print', '=']:
                    yield (token,)
                elif token.isnumeric():
                    yield ('number', int(token))
                elif token[0].isalpha():
                    yield ('identifier', token)
                else:
                    self.raise_error(f'Invalid token {token}')
            yield ('\n',)

    def next_token(self):
        if self.returned_token:
            token = self.returned_token
            self.returned_token = None
        else:
            try:
                token = next(self.token_feed)
            except StopIteration:
                token = None
        return token

    def return_token(self, token):
        if self.returned_token is not None:
            raise RuntimeError('Cannot return more than one token at a time')
        self.returned_token = token

    def parse_program(self):
        if not self.parse_statement():
            self.raise_error('Expected: statement')
        token = self.next_token()
        while token is not None:
            self.return_token(token)
            if not self.parse_statement():
                self.raise_error('Expected: statement')
            token = self.next_token()
        return True

    def parse_statement(self):
        if not self.parse_print_statement() and not self.parse_assignment():
            self.raise_error('Expected: print statement or assignment')
        token = self.next_token()
        if token[0] != '\n':
            self.raise_error('Expected: end of line')
        return True

    def parse_print_statement(self):
        token = self.next_token()
        if token[0] != 'print':
            self.return_token(token)
            return False
        if not self.parse_expression():
            self.raise_error('Expected: expression')

        value = self.stack_pop()
        print(value)
        return True

    def parse_assignment(self):
        token = self.next_token()
        if token[0] != 'identifier':
            self.return_token(token)
            return False
        identifier = token[1]
        token = self.next_token()
        if token[0] != '=':
            self.raise_error('Expected: =')
        if not self.parse_expression():
            self.raise_error('Expected: expression')

        self.vars[identifier] = self.stack_pop()
        return True

    def parse_expression(self):
        token = self.next_token()
        if token[0] not in ['number', 'identifier']:
            self.return_token(token)
            return False

        if token[0] == 'identifier':
            if token[1] not in self.vars:
                self.raise_error(f'Syntax Error: Unknown variable {token[1]}')
            else:
                self.stack_push(self.vars[token[1]])
        else:
            self.stack_push(token[1])
        return True

    def stack_push(self, arg):
        self.stack.append(arg)

    def stack_pop(self):
        return self.stack.pop()
 
    def run(self):
        try:
            return self.parse_program()
        except ValueError as exc:
            print(str(exc))
            return False


if __name__ == '__main__':
    with open(sys.argv[1], 'rt') as f:
        code = f.read()
    program = My(code)
    program.run()
