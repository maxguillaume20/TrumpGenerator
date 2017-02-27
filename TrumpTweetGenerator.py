# MarkovCommentor.py

import re
import numpy as np
from os import listdir, getcwd

def initialize (text_files):
	markov_dict = {}
	seed_dict = {}
	for tf in text_files:
		with open(tf) as text_file:
			# this regex finds all the words and some punctuation. Words with punctuation
			# are counted as different than just their word, e.g. boat != boat.
			text_list = re.findall(r'(\w+([\.\',?!]\w*)?)', text_file.read())
			
		for i in range(0,len(text_list) - 2, 1):
			tuple_state = (text_list[i][0], text_list[i + 1][0]) # States are two consecutive words. 
			markov_dict[tuple_state] = {}
			if str(text_list[i][0]).endswith('.'):
				seed = text_list[i + 1][0] + ' ' + text_list[i + 2][0]
				if seed not in seed_dict.keys():
					seed_dict[seed] = 1
				else:
					seed_dict[seed] += 1
		for i in range(0,len(text_list) - 2, 1):
			tuple_state = (text_list[i][0], text_list[i + 1][0]) 
			next_word = text_list[i + 2][0]	
			if next_word not in markov_dict[tuple_state].keys(): 	# Transitions are the frequencies of the next
				markov_dict[tuple_state][next_word] = 1.0			# words following the given state ('w0 w1'),
			else:													# so the next state is 'w1 w2' and so on
				markov_dict[tuple_state][next_word] += 1.0
	# Normalize counts
	for state in markov_dict.keys():
		sum_transitions_count = float(sum(markov_dict[state].values()))
		markov_dict[state] = {w:p / sum_transitions_count for w,p in markov_dict[state].items()}
	sum_seed_count = float(sum(seed_dict.values()))
	seed_dict = {s:p / sum_seed_count for s,p in seed_dict.items()}
	return markov_dict, seed_dict

def generate_sentence (markov_dict, seed_dict):
	seed = np.random.choice (seed_dict.keys(), 1, seed_dict.values())[0]
	sentence = seed
	matchObj = re.match (r'(\S+)\s(\S+)', seed)
	current_state = (matchObj.group(1), matchObj.group(2))
	sentence_probability = 1 	# the probability given the seed (first two words)
	while not sentence.endswith('.'):
		next_word = np.random.choice (markov_dict[current_state].keys(), 1, markov_dict[current_state].values())[0]
		sentence += ' ' + next_word
		sentence_probability *= markov_dict[current_state][next_word] 
		current_state = (current_state[1], next_word)
	sentence += ' ' + str(sentence_probability) + '\n'
	return sentence


def main():
	mypath = getcwd()
	text_files = ['parsed_trumptweets.txt']
	markov_dict, seed_dict = initialize (text_files)
	sentence_count = 100
	for i in range(sentence_count):
		sentence = generate_sentence (markov_dict, seed_dict)
		print sentence

if __name__ == '__main__':
	main()