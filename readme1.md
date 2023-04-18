## Documentation of Project Implementation for 1. task IPP 2022/2023

Name and surname: Marek Gergel  
Login: xgerge01

---

## `parse.php`

### Script parameters

Script takes following parameters:

- `--help`
- `--source=filename`

Parameter parsing is done in `class Params($argv)`, where parameter values are stored in class static variables.

### Parsing of input

Input is parsed in `class Parser`. XML document generation was done by library `DOMDocument`.  
Input stream opening and closing is handled by class constructor and destructor, in constructor instance of `class Params` has to be passed to adjust parsing options.
Private function `readLine()` is used for reading filtered line from stream. Comments or empty lines of code are removed in this function. Private function `parseHeader(DOMDocument $xml)` parses input code header and creates parent element in XML document. All the other lines with code instructions are parsed in private function `parseProgram(DOMDocument $xml)`.  
Instructions are verfied for correct parameter count and for cleaner parsing code are used regular expressions stored in variables `$regex\_\*` (e.g. `$regex_var`) and are reused in `preg_match()` standard functions. Occurances of special characters are handled in function with manually replacing problematic characters.
XML tags, atrributes and values are stored in `enum XMLTags`, `enum XMLAttribute` and `enum XMLAttributeValue` respectively.  
To get XML document from `class Parser`, function `getXML()` has to be called.

### Exit codes and error handling

In `enum ExitCodes` are stored all posible exit codes that program can exit with.  
Errors in the program are handled by function `error_exit(ExitCodes $code, string $message)`, which prints `message` on `STDERR` and exits with `code`.
