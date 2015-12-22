#!/usr/bin/python
import os

start_input = "" # input word to be found or not found
found = 0 # stores found state
accepted_config = [] # here we will post end configuration that was accepted


# production rules ("read input", "pop stack", "push stack", "next state")
productions = {
	"Q": [("a", "Z", "YZ", "Q"), ("a", "Y", "YY", "Q"), ("", "Z", "Z", "P"), ("", "Y", "Y", "P")], 
	"P": [("a", "Z", "", "P"), ("a", "Y", "", "P"), ("", "Z", "", "F")]
}

# all states or non-terminals (not really necessary)
states = ["Q", "P", "F"]

# list of alphabet symbols or terminals (not really necessary)
symbols = ["a"]

# list of stack alphabet symbols (not really necessary)
stack_symbols = ["Z", "Y"]

# start state
start_symbol = "Q"

# start stack symbol
stack_start = "Z"

# list of acceptable states
acceptable_states = ["F"]

# E - accept on empty stack or F - acceptable state (default is false)
accept_with = "E" 



# rcursively generate all prossiblity tree and terminate on success
def generate(state, input, stack, config):
	global productions
	global found

	total = 0

	# check for other tree node sucess
	if found:
		return 0

	# check if our node can terminate with success
	if is_found(state, input, stack):
		found = 1 # mark that word is accepted so other tree nodes know and terminate

		# add successful configuration
		accepted_config.extend(config)

		return 1

	# check if there are further moves (or we have to terminate)
	moves = get_moves(state, input, stack, config)
	if len(moves) == 0:
		return 0

	# for each move do a tree
	for i in moves:
		total = total + generate(i[0], i[1], i[2], config + [(i[0], i[1], i[2])])  

	return total


# checks if symbol is terminal or non-terminal
def get_moves(state, input, stack, config):
	global productions

	moves = []

	for i in productions:

		if i != state:
			continue

		for j in productions[i]:
			# print j
			current = j
			new = []

			new.append(current[3])

			# read symbol from input if we have one
			if len(current[0]) > 0:
				if len(input) > 0 and input[0] == current[0]:
					new.append(input[1:])
				else:
					continue
			else:			
				new.append(input)

			# read stack symbol
			if len(current[1]) > 0:
				if len(stack) > 0 and stack[0] == current[1]:
					new.append(current[2] + stack[1:])
				else:
					continue
			else:
				new.append(current[2] + append)

			moves.append(new)

	return moves


# checks if word already was generated somewhere in past
def is_found(state, input, stack):
	global accept_with
	global acceptable_states

	# check if all symbols are read
	if len(input) > 0: 
		return 0

	# check if we accept with empty stack or end state
	if accept_with == "E":
		if len(stack) < 1:  # accept if stack is empty
			return 1

		return 0

	else:
		for i in acceptable_states:
			if i == state: # accept if we are in terminal state
				return 1

		return 0

# print list of corrent configuration
def print_config(config):
	for i in config:
		print i 


# checks if symbol is terminal or non-terminal
def done():
	if found:
		print "Hurray! Input word \"" + start_input + "\" is part of grammar." 
	else:
		print "Sorry! Input word \"" + start_input + "\" is not part of grammar." 



# UI
# here it should read automata in from file

start_input = raw_input("Please enter your word:\n")
print "Checking word \"" + start_input + "\" ..."

# magic starts here
if not generate(start_symbol, start_input, stack_start, [(start_symbol, start_input, stack_start)]):
	done()
else:
	print_config(accepted_config) # show list of configurations to acceptance
	done()


