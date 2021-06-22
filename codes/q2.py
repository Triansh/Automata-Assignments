import json
import sys


class Node:
    def __init__(self, name, state_transitions=None):
        if state_transitions is None:
            state_transitions = {}
        self.name = name
        self.transitions = state_transitions

    def add_transition(self, symbol, final_states: list):  # symbol -> 'a', final_states =[]
        if symbol not in self.transitions:
            self.transitions[symbol] = final_states
        else:
            self.transitions[symbol] += final_states
        self.transitions[symbol] = list(set(self.transitions[symbol]))
        self.transitions[symbol].sort()

    def __repr__(self):
        return f'{self.name} => {self.transitions}'


nfa_states = []
nodes = []
letters = []


def find_node(name):
    return [x for x in nodes if x.name == name][0]


def eps_closure(cur_state_node: Node, symbol):
    vis = {x: False for x in nfa_states}

    def dfs(state_name):
        vis[state_name] = True
        cur_state_node.add_transition(symbol, [state_name])
        state_node = find_node(state_name)
        if '$' in state_node.transitions:
            for x in state_node.transitions['$']:
                if not vis[x]:
                    dfs(x)

    for state in cur_state_node.transitions[symbol]:
        if not vis[state]:
            dfs(state)


def make_partial_dfa():
    for node in nodes:
        for symbol in node.transitions.keys():
            eps_closure(node, symbol)

    for node in nodes:
        for symbol in letters:
            if symbol not in node.transitions:
                node.transitions[symbol] = []


def make_dfa():
    dfa = []
    for i in range(1, 2 ** len(nodes)):
        mask = [1 if bool(i & (1 << bit)) else 0 for bit in range(len(nodes))]
        indexes = [x for x in range(len(mask)) if mask[x] != 0]
        new_name = [nodes[x].name for x in indexes]
        new_name.sort()
        new_node = Node(name=new_name)
        for idx in indexes:
            for sym in letters:
                new_node.add_transition(sym, nodes[idx].transitions[sym])
        dfa.append(new_node)
    return dfa


if __name__ == '__main__':
    pathToInput = sys.argv[1]
    pathToOutput = sys.argv[2]
    with open(pathToInput) as f:
        data = json.load(f)
    nfa_states = data['states']
    letters = data['letters']
    transitions = data['transition_function']
    start_states = data['start_states']
    final_states = data['final_states']

    nodes = [Node(name=x) for x in nfa_states]
    for node in nodes:
        for x in transitions:
            if x[0] == node.name:
                node.add_transition(x[1], [x[2]])

    visi = {x: False for x in nfa_states}
    new_start_state = []


    def dfs(state_name):
        visi[state_name] = True
        new_start_state.append(state_name)
        state_node = find_node(state_name)
        if '$' in state_node.transitions:
            for x in state_node.transitions['$']:
                if not visi[x]:
                    dfs(x)


    dfs(start_states[0])
    new_start_state.sort()
    new_start_state = [new_start_state]

    make_partial_dfa()
    dfa = make_dfa()

    result: dict = {'states': [[]], 'letters': letters, 'transition_function': [
        [[], sym, []] for sym in letters
    ], 'start_states': new_start_state, 'final_states': []}

    for node in dfa:
        result['states'].append(node.name)
        if any([x in node.name for x in final_states]):
            result['final_states'].append(node.name)
        for sym in letters:
            result['transition_function'].append([node.name, sym, node.transitions[sym]])

    with open(pathToOutput, 'w') as json_file:
        json.dump(result, json_file)
