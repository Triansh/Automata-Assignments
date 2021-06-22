import json
import sys

transitions = []
dfa_states = []


def make_union_str(x: list):
    s = "+".join(x)
    return (
            ('(' if len(s) != 1 else '')
            + s +
            (')' if len(s) != 1 else '')
    ) if len(s) > 0 else ''


def get_dicts(x):
    ins = {}
    outs = {}
    selfs = []
    for y in dfa_states:
        ins[y] = []
        outs[y] = []
    ins['START'] = []
    outs['END'] = []
    for y in transitions:
        if x == y[0] and x == y[2]:
            selfs.append(y[1])
            continue
        if x == y[0]:
            outs[y[2]].append(y[1])
        elif x == y[2]:
            ins[y[0]].append(y[1])

    self_exp = make_union_str(selfs)
    if len(self_exp) != 0:
        self_exp = (self_exp + '*') if len(self_exp) == 1 else ('(' + self_exp + ')*')
    for key in ins.keys():
        ins[key] = make_union_str(ins[key])
    for key in outs.keys():
        outs[key] = make_union_str(outs[key])

    return ins, outs, self_exp


if __name__ == '__main__':
    pathToInput = sys.argv[1]
    pathToOutput = sys.argv[2]
    with open(pathToInput) as f:
        data = json.load(f)
    dfa_states = data['states']
    letters = data['letters']
    transitions = data['transition_function']
    start_states = data['start_states']
    final_states = data['final_states']

    transitions += [["START", '$', x] for x in start_states]
    transitions += [[x, '$', "END"] for x in final_states]

    for x in dfa_states:
        ins, outs, selfs = get_dicts(x)
        new_trans = []
        for in_state, in_sym in ins.items():
            for out_state, out_sym in outs.items():
                if in_sym != '' and out_sym != '':
                    new_trans.append([in_state, (in_sym + selfs + out_sym), out_state])

        transitions = [y for y in transitions if x not in [y[0], y[2]]]
        transitions += new_trans

    ans = "+".join([x[1] for x in transitions])
    with open(pathToOutput, 'w') as json_file:
        json.dump({'regex': ans}, json_file)
