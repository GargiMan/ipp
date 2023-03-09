LOGIN=xgerge01
TESTS := $(wildcard testData/*)
TASK1=parse.php
TASK2=interpret.py
RUN1=php8.1 $(TASK1)
RUN2=python3.10 $(TASK2)

.PHONY: all run-test clean zip

all: run-test

run-test:
	@for test in $(TEST); do printf "$${test}\n"; $(RUN1) < $${test}; printf "\n"; done

zip:
	zip $(LOGIN).zip $(TASK1) $(TASK2) dokumentace.md

clean:
	rm -rf $(LOGIN).zip
