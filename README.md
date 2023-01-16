# jaql
JAQL - Just Another Quantum Language. A Lox implementation attempting to be quantum, eventually. 


This is step 1 of the classical -> quantum. Take this language, with some elements removed and generate qasm from the parser.

Clearly this isn't especially meaningful, but it's a fun experiment in getting the elements of classical computing, quantum.

There are only two types, floats and strings, I'll just use a flag qubit at the front to distinquish.

There is an interesting question on if a variable should be a state on a register or a unitary that can be 'implemented'. 
Should we allow for copying, knowing there's no quantum info here?