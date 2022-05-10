msg_0 = "Enter an equation"
msg_1 = "Do you even know what numbers are? Stay focused!"
msg_2 = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"
msg_3 = "Yeah... division by zero. Smart move..."
msg_4 = "Do you want to store the result? (y / n):"
msg_5 = "Do you want to continue calculations? (y / n):"
msg_6 = " ... lazy"
msg_7 = " ... very lazy"
msg_8 = " ... very, very lazy"
msg_9 = "You are"

msg_10 = "Are you sure? It is only one digit! (y / n)"
msg_11 = "Don't be silly! It's just one number! Add to the memory? (y / n)"
msg_12 = "Last chance! Do you really want to embarrass yourself? (y / n)"
msg_list = [msg_10, msg_11, msg_12]

run = True
memory = 0


def is_one_digit(v):
    if v > -10 and v < 10 and float(v).is_integer():
        output = True
        return output
    output = False
    return output


def check(v1, v2, v3):
    msg = ''
    if is_one_digit(v1) and is_one_digit(v2):
        msg += msg_6
    if (v1 == 1 or v2 == 1) and v3 == '*':
        msg += msg_7
    if (v1 == 0 or v2 == 0) and (v3 == '*' or v3 == '+' or v3 == '-'):
        msg += msg_8
    if msg != '':
        msg = msg_9 + msg
        print(msg)
        return True


while run:
    result = 0
    calc = input(msg_0).split()
    x, oper, y = calc
    try:
        if x == 'M':
            x = memory
        else:
            if float(x):
                x = float(x)
        if y == 'M':
            y = memory
        else:
            if float(y) or int(y):
                y = float(y)
    except ValueError:
        print(msg_1)
        continue
    if oper == '+' or oper == '-' or oper == '*' or oper == '/':
        x = float(x)
        y = float(y)
        check(x, y, oper)
        if oper == '+':
            result = x + y
        elif oper == '-':
            result = x - y
        elif oper == '*':
            result = x * y
        elif oper == '/':
            if int(y) == 0:
                print(msg_3)
                continue
            result = x / y
        print(result)
        store_result = input(msg_4)
        if store_result == 'y':
            msg_index = 0
            if is_one_digit(result):
                while True:
                    msg_ = input(msg_list[msg_index])
                    if msg_ == 'y':
                        if msg_index < 2:
                            msg_index += 1
                        else:
                            memory = result
                            break
                    else:
                        break  
            else:
                memory = result
        continue_calc = input(msg_5)
        if continue_calc == 'y':
            continue
        run = False
    else:
        print(msg_2)
        continue
