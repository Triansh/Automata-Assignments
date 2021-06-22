# Automata Programming Assignment

**Note: For Q2, Q3, Q4; It is assumed that only one start state shall be given.**

### Question 1 (Regex -> NFA)

Steps involved:

* Since concatenation operator was not present, '.' was added between 2 symbols to represent
  concatenation
* Then, the regex was converted to a postfix expression using stack
* The postfix expression was used to evaluate the expression using a stack and appropriate states
  and transitions were added as per needed.
* All the transitions were made using the properties of union, star and concatenation operators (How
  state diagrams change on applying these operations).

### Question 2 (NFA -> DFA)

Steps Involved:

* The new start was calculated by taking the epsilon closure of given start state.
* Now for each state among given N states, for a particular symbol, what all possible states shall
  be reached taking in account the epsilon transitions.
* The algorithm used to calculate the epsilon closure is dfs.
* The rest 2^N - N state transitions were calculated by taking union of all possible states reached
  from given states.

### Question 3  (DFA -> Regex)

Steps Involved:

* A new START and a new END state was created such that there were no incoming edges in START state
  and no outgoing edges in END state.
* We loop each state from {1 , ..., N} and remove them one by one.
* The new transitions are made by maintaining three dictionaries for incoming edges to state 'X' ,
  outgoing edges from tate 'X' and self loops in state 'X'. Each dictionary stored final state and
  regex expression for that transition.
* After removal of all states, union was taken for all the edges going from start state to end state

### Question 4 (DFA minimization)

Steps Involved:

* Firstly, all the unreachable states were removed.
* The new set of states obtained were partitioned in 2 sets, rejecting and non rejecting states.
* The partition was represented by a list containing sets.
* Then we chose any set from the partition, named as A and set it as the reference set.
* Now we loop over all sets for a particular symbol and check whether the states present in that
  set. can be partitioned into 2 sets. First, containing the states that go to A via given symbol
  and the other containing the rest.
* If none of the above sets is found empty , we break the set into 2 sets and repeat the procedure
  until no more partitions are possible.
  