<?php

/**
 * @file parse.php
 * @brief IPP project 1
 * @author Marek Gergel (xgerge01)
 * @date 2023-03-11
 * @details
 * This script parses IPPcode23 code from STDIN (or source file) and outputs XML representation to STDOUT.
 * 
 * @param --help
 * @param --source=<sourcefile>
 * 
 * @return 0 on success or any other value on failure
 */

ini_set('display_errors', 'stderr');

require_once 'libs/php/params.php';
require_once 'libs/php/parser.php';

$params = new Params($argv);
$parser = new Parser($params);
echo $parser->getXML();
exit(0);
?>