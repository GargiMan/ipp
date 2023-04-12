LOGIN=xgerge01
TEST=test.php
TASK1=parse.php
TASK2=interpret.py
RUN_TEST=php8.1 $(TEST)
RUN1=php8.1 $(TASK1)
RUN2=python3.10 $(TASK2)

.PHONY: all test-parse test-interpret check zip clean

all: test-parse test-interpret

test-parse:
	$(RUN_TEST) --directory=tests/parse-only/ --parse-only --recursive --jexampath=. > out.html

test-interpret:
	$(RUN_TEST) --directory=tests/interpret-only/ --int-only --recursive > out.html

test:
	$(RUN_TEST) --directory=tests/both/ --recursive > out.html

check: clean zip
	./is_it_ok.sh $(LOGIN).zip testDir

zip:
	zip -r $(LOGIN).zip $(TASK1) $(TASK2) libs readme1.md readme2.md rozsireni

clean:
	find tests/ -name "*_tempOut.temp" -type f -delete
	rm -rf $(LOGIN).zip testDir libs/python/__pycache__
