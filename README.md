# IPP

parse.php - 7,6 / 8,0  (poor documentation)  
interpret.py - 10,4 / 12,0  (poor documentation, + extension)  

Files included that I'm not author of:

- jexamxml.jar
- options
- is_it_ok.sh
- test.php
- tests/

# TESTS

- you need the following in the folder with your source file:
  - `test.php` from this gist
  - `options` and `jexamxml.jar` from the `/pub/courses/ipp/jexamxml` folder on Merlin
  - `tests` folder with test cases (original set from Moodle or extended set from Discord pins)
- run with `php8.1 test.php` on Merlin or with `php test.php` on your local machine
- you can run individual tests like this: `php test.php header/ok`, or whole groups like this: `php test.php header`
