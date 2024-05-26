#! /usr/bin/python3
#　*と/に対応するように改良

def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index

def read_function(line, index):
    func_name = ''
    while index < len(line) and line[index].isalpha():
        func_name += line[index]
        index += 1
    token = {'type': 'FUNCTION', 'name': func_name}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1


def read_asterisk(line, index):
    token = {'type': 'ASTERISK'}
    return token, index + 1


def read_slash(line, index):
    token = {'type': 'SLASH'}
    return token, index + 1

def read_open_paren(line, index):
    token = {'type': 'OPEN_PAREN'}
    return token, index + 1

def read_close_paren(line, index):
    token = {'type': 'CLOSE_PAREN'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0

    while index < len(line):

        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index].isalpha():
            (token, index) = read_function(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_asterisk(line, index)
        elif line[index] == '/':
            (token, index) = read_slash(line, index)
        elif line[index] == '(':
            (token, index) = read_open_paren(line, index)
        elif line[index] == ')':
            (token, index) = read_close_paren(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate(tokens):

    def evaluate_function(tokens):
        index = 0
        while index < len(tokens):
            if tokens[index]['type'] == 'FUNCTION':
                func_name = tokens[index]['name']
                print(tokens)
                if tokens[index + 1]['type'] == 'OPEN_PAREN':
                    paren_count = 1
                    sub_tokens = []
                    index += 2
                    while index < len(tokens) and paren_count > 0: #()内
                        if tokens[index]['type'] == 'OPEN_PAREN':
                            paren_count += 1
                        elif tokens[index]['type'] == 'CLOSE_PAREN':
                            paren_count -= 1
                        if paren_count > 0:
                            sub_tokens.append(tokens[index])
                        index += 1

                    print(tokens)
                    sub_value = evaluate_tokens(sub_tokens) #（）内の答え
                
                
                if func_name == 'abs':
                    result = abs(sub_value)
                elif func_name == 'int':
                    result = int(sub_value)
                elif func_name == 'round':
                    result = round(sub_value)
                else:
                    print('Invalid function name')
                    exit(1)
                
                tokens = tokens[:index - len(sub_tokens) - 3] + [{'type': 'NUMBER', 'number': result}] + tokens[index:]
                index = 0
            index += 1
        return tokens

        

    #（）内計算
    def evaluate_parentheses(tokens):
        index = 0
        while index < len(tokens):
            if tokens[index]['type'] == 'OPEN_PAREN':
                sub_tokens = [] #()内のtoken
                paren_count = 1
                index += 1

                while index < len(tokens) and paren_count > 0: #()内
                    if tokens[index]['type'] == 'OPEN_PAREN':
                        paren_count += 1
                    elif tokens[index]['type'] == 'CLOSE_PAREN':
                        paren_count -= 1
                    if paren_count > 0:
                        sub_tokens.append(tokens[index])
                    index += 1

                sub_value = evaluate_tokens(sub_tokens) #（）内の答え
                
                
                tokens = tokens[:index - len(sub_tokens) - 1] + [{'type': 'NUMBER', 'number': sub_value}] + tokens[index:] #indexの前　(　)　indexの後ろ
                index = 0
            index += 1
        return tokens
    
    
    
    def evaluate_tokens(tokens):
        #step1：*と/を処理
        index = 1

        while index < len(tokens):
            if tokens[index]['type'] == 'ASTERISK':
                tokens[index - 1]['number'] *= tokens[index + 1]['number']
                del tokens[index:index + 2] #計算済みを削除
            elif tokens[index]['type'] == 'SLASH':
                tokens[index - 1]['number'] /= tokens[index + 1]['number']
                del tokens[index:index + 2] #計算済みを削除
            else:
                index += 1

        # step2：*/がない式をもう一度頭から計算
        index = 0
        answer = 0

        tokens.insert(0, {'type' : 'PLUS'}) #先頭にdummyの+

        while index < len(tokens):
            if tokens[index]['type'] == 'NUMBER':
                if tokens[index - 1]['type'] == 'PLUS':
                    answer += tokens[index]['number']
                elif tokens[index - 1]['type'] == 'MINUS':
                    answer -= tokens[index]['number']
                else:
                    print('Invalid syntax1')
                    exit(1)
            index += 1
        return answer
    
    tokens = evaluate_parentheses(tokens)
    tokens = evaluate_function(tokens)
    return evaluate_tokens(tokens)


def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    #test("1+2")
    #test("1.0+2.1-3")
    #test("4*2")
    #test("3+4*2-1/5")
    #test("3*4+2/2-0.1")
    #test("2+(3+4)*2")
    #test("2*(1+2)*2")
    #test("3*(4+3)-1/5")
    test("abs(2)")
    #test("int(1.55)")
    #test("round(1.55)")
    #test("12 + abs(int(round(-1.55) + abs(int(-2.3 + 4))))")
    print("==== Test finished! ====\n")

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)