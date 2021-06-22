import json
import sys

transMapper = {}
reachable_states = {}


def state_leads_to_A(A, c):
    states = []
    for s in reachable_states:
        if transMapper[s][c] in A:
            states.append(s)
    return set(states)


if __name__ == '__main__':
    pathToInput = sys.argv[1]
    pathToOutput = sys.argv[2]
    with open(pathToInput) as f:
        data = json.load(f)
    all_states = data['states']
    letters = data['letters']
    transitions = data['transition_function']
    start_states = data['start_states']
    final_states = data['final_states']

    transMapper = {x: {} for x in all_states}
    for s, l, ns in transitions:
        transMapper[s][l] = ns

    reachable_states = set(start_states)
    next_states = reachable_states.copy()
    while next_states != set():
        temp = set()
        for q in next_states:
            for c in letters:
                temp = temp.union({transMapper[q][c]})
        next_states = temp - reachable_states
        reachable_states = reachable_states.union(next_states)

    final_reachable_states = [x for x in reachable_states if x in final_states]
    P = [set(final_reachable_states), set([x for x in reachable_states if x not in final_states])]
    W = P.copy()

    while len(W) > 0:
        A = W[-1]
        W.pop()
        for c in letters:
            X = state_leads_to_A(A, c)
            Z = P.copy()
            for Y in Z:
                if not ((X & Y != set()) and (Y - X != set())): continue
                P.remove(Y)
                P += [X & Y, Y - X]
                if Y in W:
                    W.remove(Y)
                    W += [X & Y, Y - X]
                else:
                    W += [X & Y] if len(X & Y) <= len(Y - X) else [Y - X]

    new_states = [list(x) for x in P]
    for x in new_states:
        x.sort()
    idMap = {x: i for i in range(len(P)) for x in P[i]}

    new_final_states = [new_states[i] for i in range(len(new_states)) if
                        P[i] & set(final_reachable_states) != set()]
    new_start_state = [new_states[i] for i in range(len(new_states)) if
                       P[i] & set(start_states) != set()]
    new_transitions = [[x, c, new_states[idMap[transMapper[x[0]][c]]]]
                       for x in new_states for c in letters]

    result = {'states': new_states,
              'letters': letters,
              'transition_function': new_transitions,
              'start_states': new_start_state,
              'final_states': new_final_states}

    with open(pathToOutput, 'w') as json_file:
        json.dump(result, json_file)
