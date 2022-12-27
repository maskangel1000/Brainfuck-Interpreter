# Function by Baltasarq on StackOverflow
def find_loops(code: str):
    toret = {}
    pstack = []

    for index, char in enumerate(code):
        if char == '[':
            pstack.append(index)
        elif char == ']':
            if len(pstack) == 0:
                raise SyntaxError('No matching closing bracket at: ' + str(index))
            toret[pstack.pop()] = index

    if len(pstack) > 0:
        raise SyntaxError('No matching opening bracket at: ' + str(pstack.pop()))
    
    return toret

'''
Runs the brainfuck code

code: str - The code string to run.
user_input: str - The input given to the code. If None, the code will prompt the user for input.
overflow: int - The maximum possible value in a cell. Overflows to 0.
tape: list[int] - Initial state of the tape. Tape length is effectively infinite.
verbose: bool - Whether the '.' operator should print output.

Returns a tuple (tape, pointer)
'''
def run(code: str, user_input: str = '', overflow: int = 255, tape: list[int] = [0], verbose: bool = True):
    pointer = 0
    input_char = 0

    code_index = 0

    toret = find_loops(code)

    while code_index < len(code):
        cmd = code[code_index]

        match cmd:

            # Get input
            case ',':
                if user_input == '':
                    tape[pointer] = ord(input('Input: '))
                else:   
                    try:
                        tape[pointer] = ord(user_input[input_char])
                    except IndexError:
                        pass
                    input_char += 1

            # Output
            case '.':
                if verbose:
                    print(chr(tape[pointer]), end = '')

            # Move pointer right
            case '>':
                pointer += 1
                try:
                    tape[pointer]
                except:
                    tape.append(0)
            
            # Move pointer left
            case '<':
                pointer -= 1
                try:
                    tape[pointer]
                except IndexError:
                    raise IndexError('Pointer out of bounds')
            
            # Increment cell
            case '+':
                tape[pointer] += 1
                if tape[pointer] > overflow:
                    tape[pointer] = 0
            
            # Decrement cell
            case '-':
                tape[pointer] -= 1
                if tape[pointer] < 0:
                    tape[pointer] = overflow
            
            # Start loop
            case '[':
                if tape[pointer] == 0:
                    code_index = toret[code_index]
                    continue
            
            # End loop
            case ']':
                if tape[pointer] != 0:
                    code_index = [k for k, v in toret.items() if v == code_index][0]
                    continue

        code_index += 1

    # Return tape and pointer position after running all code
    return tape, pointer