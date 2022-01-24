
output.txt: input.txt
	python main.py

input.txt:
	python fetch_crossword.py

run: output.txt
.PHONY: run
