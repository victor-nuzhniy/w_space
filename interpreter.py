def unbleach(n):
    return n.replace(' ', 's').replace('\t', 't').replace('\n', 'n')


# solution
class White:

    def __init__(self):
        self.output = ''
        self.stack = []
        self.heap = {}
        self.input = ''
        self.index = 0
        self.input_index = 0
        self.input_list = []
        self.instruction = []
        self.input_str = ''
        self.command = {'  ': self.push_to_stack,
                        ' \t ': self.duplicate_value,
                        ' \t\n': self.discard_value,
                        ' \n ': self.duplicate_top,
                        ' \n\t': self.swap,
                        ' \n\n': self.discard_top,
                        '\t   ': self.adding,
                        '\t  \t': self.subtract,
                        '\t  \n': self.multiple,
                        '\t \t ': self.division,
                        '\t \t\t': self.division_part,
                        '\t\t ': self.heap_store,
                        '\t\t\t': self.heap_pop,
                        '\t\n  ': self.output_character,
                        '\t\n \t': self.output_number,
                        '\t\n\t ': self.read_char,
                        '\t\n\t\t': self.read_number,
                        '\n  ': self.mark_location,
                        '\n \t': self.call_subroutine,
                        '\n \n': self.jump,
                        '\n\t ': self.jump_stack,
                        '\n\t\t': self.jump_stack_bzero,
                        '\n\t\n': self.subroutine_end,
                        '\n\n\n': self.end}
        self.command_par = {'  ': 0,
                            ' \t ': 0,
                            ' \t\n': 0,
                            '\n  ': 1,
                            '\n \t': 1,
                            '\n \n': 1,
                            '\n\t ': 1,
                            '\n\t\t': 1}
        self.error_marker = False
        self.end = False

    def parsing_code(self):
        help_list = []
        item_set = {' ', '\t', '\n'}
        for i in range(len(self.input_str)):
            if self.input_str[i] in item_set:
                help_list.append(self.input_str[i])
        self.input_str = ''.join(help_list)
        while self.index < len(self.input_str) - 1:
            help_str, i = '', 0
            while self.index < len(self.input_str) and i < 5 and self.command.get(help_str) is None:
                help_str = help_str + self.input_str[self.index]
                i += 1
                self.index += 1
            if self.command.get(help_str) is None:
                self.index = self.index - i
                self.instruction.append(self.input_str[self.index])
                self.index += 1
            else:
                self.instruction.append(help_str)
                if self.command_par.get(help_str) is not None:
                    help_list = []
                    while self.input_str[self.index] != '\n':
                        help_list.append(self.input_str[self.index])
                        self.index += 1
                    if self.command_par[help_str] == 0:
                        self.instruction.append(self.parsing_number(help_list))
                    else:
                        self.instruction.append(self.parsing_label(help_list))
                    self.index += 1
        self.index = 0

    def parsing_label(self, container):
        return ''.join(container)

    def parsing_number(self, container):
        number, place = 0, 0
        while len(container) > 1:
            x = container.pop()
            if ord(x) == 9:
                number += 2 ** place
            place += 1
        x = container.pop()
        if ord(x) == 9:
            number = -1 * number
        return number

    def command_check(self):
        i = 0
        while i < len(self.instruction):
            if self.command.get(self.instruction[i]) is None:
                raise Exception('Invalid command')
            if self.command_par.get(self.instruction[i]) is not None:
                i += 1
            i += 1

    def push_to_stack(self):
        self.index += 1
        self.stack.append(self.instruction[self.index])

    def duplicate_value(self):
        self.index += 1
        if len(self.stack) - 1 < self.instruction[self.index]:
            self.error_marker = True
        value = self.stack[len(self.stack) - self.instruction[self.index] - 1]
        self.stack.append(value)

    def discard_value(self):
        self.index += 1
        value = self.stack.pop()
        number = self.instruction[self.index]
        if number < 0 or number >= len(self.stack):
            self.stack = [value]
        else:
            for i in range(number):
                self.stack.pop()
            self.stack.append(value)

    def duplicate_top(self):
        value = self.stack[len(self.stack) - 1]
        self.stack.append(value)

    def swap(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(a)
        self.stack.append(b)

    def discard_top(self):
        self.stack.pop()

    def adding(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(a + b)

    def subtract(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b - a)

    def multiple(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b * a)

    def division(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.stack.append(b // a)

    def division_part(self):
        a = self.stack.pop()
        b = self.stack.pop()
        sign = a // abs(a)
        return self.stack.append(sign * abs(b % a))

    def heap_store(self):
        a = self.stack.pop()
        b = self.stack.pop()
        self.heap[b] = a

    def heap_pop(self):
        a = self.stack.pop()
        self.stack.append(self.heap[a])

    def output_character(self):
        self.output = self.output + chr(self.stack.pop())

    def output_number(self):
        self.output = self.output + str(self.stack.pop())

    def read_char(self):
        b = self.stack.pop()
        self.heap[b] = ord(self.input[self.input_index])
        self.input_index += 1

    def read_number(self):
        b = self.stack.pop()
        number_list = []
        while self.input_index < len(self.input) - 1 and self.input[self.input_index] != '\n':
            number_list.append(self.input[self.input_index])
            self.input_index += 1
        self.input_index += 1
        self.heap[b] = int(''.join(number_list))

    def mark_location(self):
        self.index += 1

    def label_location_check(self, label):
        quantity = 0
        for i in range(len(self.instruction) - 1):
            if self.instruction[i] == '\n  ' and self.instruction[i + 1] == label:
                quantity += 1
        if quantity != 1:
            raise ValueError('Unknown or repeated label')

    def call_subroutine(self):
        index_help, flag = 0, 0
        while flag == 0:
            if self.instruction[index_help] == '\n  ' and self.instruction[index_help + 1] == self.instruction[
                self.index + 1]:
                flag = 1
            index_help += 1
        mem = self.index + 1
        self.index = index_help + 1
        while self.instruction[self.index] != '\n\t\n':
            self.command[self.instruction[self.index]]()
            self.index += 1
            if self.instruction[self.index] == '\n\n\n':
                self.end = True
                break
        self.index = mem

    def jump(self):
        self.label_location_check(self.instruction[self.index + 1])
        index_help, flag = 0, 0
        self.index += 1
        while flag == 0:
            if self.instruction[index_help] == '\n  ' and self.instruction[index_help + 1] == self.instruction[
                self.index]:
                flag = 1
            index_help += 1
        self.index = index_help

    def jump_stack(self):
        self.label_location_check(self.instruction[self.index + 1])
        a = self.stack.pop()
        self.index += 1
        if a == 0:
            index_help, flag = 0, 0
            while flag == 0:
                if self.instruction[index_help] == '\n  ' and self.instruction[index_help + 1] == self.instruction[
                    self.index]:
                    flag = 1
                index_help += 1
            self.index = index_help

    def jump_stack_bzero(self):
        self.label_location_check(self.instruction[self.index + 1])
        a = self.stack.pop()
        self.index += 1
        if a < 0:
            index_help, flag = 0, 0
            while flag == 0:
                if self.instruction[index_help] == '\n  ' and (self.instruction[index_help + 1]
                                                               == self.instruction[self.index]):
                    flag = 1
                index_help += 1
            self.index = index_help

    def subroutine_end(self):
        self.index += 1

    def end(self):
        pass


def whitespace(code, inp=''):
    w = White()
    w.input_str = code
    w.input = inp
    w.parsing_code()
    w.command_check()
    while w.instruction[w.index] != '\n\n\n':
        w.command[w.instruction[w.index]]()
        if w.error_marker is True:
            raise Exception('stack index out of range')
        if w.end is True:
            return w.output
        w.index += 1
    return w.output
