LOGIN=xgerge01
TEST=test.php
TASK1=parse.php
TASK2=interpret.py
RUN_TEST=php8.1 $(TEST)
RUN1=php8.1 $(TASK1)
RUN2=python3.10 $(TASK2)

.PHONY: all run-test check zip clean

all: run-test

run-test:
	$(RUN_TEST) 

check: clean zip
	./is_it_ok.sh $(LOGIN).zip testDir

zip:
	zip $(LOGIN).zip $(TASK1) $(TASK2) readme1.md readme2.md

clean:
	find . -name "*.my_out" -type f -delete
	rm -rf $(LOGIN).zip testDir
