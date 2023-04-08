<?php

/**
 * @file params.php
 * @brief IPP project 1
 * @author Marek Gergel (xgerge01)
 * @date 2023-03-11
 * @details
 * Parameters parser class
 */

require_once 'error.php';

class Params
{
   private $help = "This script parses IPPcode23 code from STDIN (or source file) and outputs XML representation to STDOUT\n" . "Usage: php parse.php [--source=file]\n" . "--source=file - source file to parse\n" . "--help - print this help\n";
   public $source = STDIN;

   public function __construct($argv)
   {
      //parse script parameters
      for ($i = 1; $i < count($argv); $i++) {
         if (preg_match("/^--help$/", $argv[$i])) {

            if (count($argv) > 2) error_exit(ErrorCodes::ERR_PARAMS, "Parameter $argv[$i] must be used alone\n");
            echo $this->help;
            exit(0);
         } else if (preg_match("/^--source=\"?.+\"?$/", $argv[$i])) {

            $this->source = preg_replace("/^--source=\"?(.+)\"?$/", "$1", $argv[$i]);
         } else {

            error_exit(ErrorCodes::ERR_PARAMS, "Unknown parameter $argv[$i]\n");
         }
      }
   }
}

?>