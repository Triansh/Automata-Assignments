import json
import sys


class NFA:
    def __init__(self, start_state, final_state, transitions):
        self.start_state = start_state
        self.final_state = final_state
        self.transitions = transitions


cnt = 0


def calculate_letters(regex):
    all_letters = [x for x in regex if x not in ['.', '*', '+', '(', ')']]
    return list(set(all_letters))


def get_symbol(c):
    global cnt
    start_state = [f"Q{cnt}"]
    cnt += 1
    final_state = [f"Q{cnt}"]
    cnt += 1
    transition = [[start_state[0], str(c), final_state[0]]]
    return NFA(start_state, final_state, transition)


def get_star(nfa: NFA):
    global cnt
    start_state = [f"Q{cnt}"]
    cnt += 1
    transition = nfa.transitions + [[start_state[0], '$', nfa.start_state[0]]]
    new_trans = [[x, '$', nfa.start_state[0]] for x in nfa.final_state]
    return NFA(start_state, start_state + nfa.final_state, transition + new_trans)


def get_union(nfa1: NFA, nfa2: NFA):
    global cnt
    start_state = [f"Q{cnt}"]
    cnt += 1
    transition = nfa1.transitions + nfa2.transitions
    new_trans = [[start_state[0], '$', nfa1.start_state[0]],
                 [start_state[0], '$', nfa2.start_state[0]]]
    final_states = nfa1.final_state + nfa2.final_state
    return NFA(start_state, final_states, transition + new_trans)


def get_concat(nfa1: NFA, nfa2: NFA):
    transition = nfa1.transitions + nfa2.transitions
    new_trans = [[x, '$', nfa2.start_state[0]] for x in nfa1.final_state]
    return NFA(nfa1.start_state, nfa2.final_state, transition + new_trans)


def are_both_symbol(c1, c2):
    return c1 not in ['+', '('] and c2 not in [')', '+', '*']


def add_concat(regex):
    final_regex = "".join([
        (regex[i] + '.') if are_both_symbol(regex[i], regex[i + 1]) else regex[i]
        for i in range(len(regex) - 1)
    ])
    final_regex += regex[-1]
    return final_regex


def priority(c):
    if c == '*':
        return 3
    elif c == '.':
        return 2
    elif c == '+':
        return 1
    else:
        return 0


def regex_to_postfix(regex: str):
    postfix = ""
    op = []
    for i in range(len(regex)):
        if regex[i] not in ['*', '+', '.', '(', ')']:
            postfix += regex[i]
        elif regex[i] == '(':
            op.append(regex[i])
        elif regex[i] == ')':
            while op[-1] != '(':
                postfix += op[-1]
                op.pop()
            op.pop()
        else:
            while len(op) > 0:
                if priority(op[-1]) >= priority(regex[i]):
                    postfix += op[-1]
                    op.pop()
                else:
                    break
            op.append(regex[i])

    postfix += "".join(op[::-1])
    return postfix


def get_nfa(postfix):
    op = []
    for x in postfix:
        if x == '*':
            op = op[:-1] + [get_star(op[-1])]
        elif x == '.':
            op = op[:-2] + [get_concat(op[-2], op[-1])]
        elif x == '+':
            op = op[:-2] + [get_union(op[-2], op[-1])]
        else:
            op.append(get_symbol(x))
    return op[0]


if __name__ == '__main__':
    pathToInput = sys.argv[1]
    pathToOutput = sys.argv[2]
    with open(pathToInput) as f:
        data = json.load(f)
    regex = data['regex']

    letters = calculate_letters(regex)
    final_regex = add_concat(regex)
    postfix = regex_to_postfix(final_regex)
    print(postfix)

    nfa = get_nfa(postfix)
    Q = [('Q' + str(i)) for i in range(cnt)]

    result = {
        'states': Q,
        'letters': letters,
        'transition_function': nfa.transitions,
        'start_states': nfa.start_state,
        'final_states': nfa.final_state
    }

    with open(pathToOutput, 'w') as json_file:
        json.dump(result, json_file)
