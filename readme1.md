## Documentation of Project Implementation for 1. task IPP 2022/2023

Name and surname: Marek Gergel  
Login: xgerge01

---

## <code>parse.php</code>

### Program parameters

The program takes one of the following parameters:

- <code>--help</code>
- <code>--source=filename</code>

Parameter parsing is done in <code>class Params($argv)</code>, where parameter values are stored in instance of class variables.

### Parsing of input

Input is parsed in <code>class Parser</code>. XML document generation was done by library <code>DOMDocument</code>.  
Input stream opening and closing is handled by class constructor and destructor, in constructor instance of <code>class Params</code> has to be passed to adjust parsing options.
Private function <code>readLine()</code> is used for reading filtered line from stream. Comments or empty lines of code are removed in this function. Private function <code>parseHeader(DOMDocument $xml)</code> parses input code header and creates parent element in XML document. All the other lines with code instructions are parsed in private function <code>parseProgram(DOMDocument $xml)</code>.  
Instructions are verfied for correct parameter count and for cleaner parsing code are used regular expressions stored in variables <code>$regex\_\*</code> (e.g. <code>$regex_var</code>) and are reused in <code>preg_match()</code> standard functions. Occurances of special characters are handled in function with manually replacing problematic characters.
XML tags, atrributes and values are stored in <code>enum XMLTags</code>, <code>enum XMLAttribute</code> and <code>enum XMLAttributeValue</code> respectively.  
To get XML document from <code>class Parser</code>, function <code>getXML()</code> has to be called.

### Exit codes and error handling

In <code>enum ExitCodes</code> are stored all posible exit codes that program can exit with.  
Errors in the program are handled by function <code>error_exit(ExitCodes $code, string $message)</code>, which prints <code>message</code> on <code>STDERR</code> and exits with <code>code</code>.
