
input.txt:
	python fetch_crossword.py $@

output.txt: input.txt
	python solve.py $^ $@

run: output.txt
	python send_solution.py $^

clean:
	rm input.txt output.txt

rerun: clean run

.PHONY: run clean rerun
