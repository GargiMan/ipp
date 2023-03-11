LOGIN=xgerge01
TEST=test.php
TASK1=parse.php
TASK2=interpret.py
RUN_TEST=php8.1 $(TEST)
RUN1=php8.1 $(TASK1)
RUN2=python3.10 $(TASK2)

.PHONY: all run-test clean zip

all: run-test

run-test:
	$(RUN_TEST) 

zip:
	zip $(LOGIN).zip $(TASK1) $(TASK2) dokumentace.md

clean:
	find . -name "*.my_out" -type f -delete
	rm -rf $(LOGIN).zip
