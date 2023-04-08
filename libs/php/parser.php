<?php

/**
 * @file parser.php
 * @brief IPP project 1
 * @author Marek Gergel (xgerge01)
 * @date 2023-03-11
 * @details
 * Code parser class
 */

require_once 'params.php';
require_once 'error.php';

enum XMLTag: string
{
   case PROGRAM = "program";
   case INSTRUCTION = "instruction";
   case ARG1 = "arg1";
   case ARG2 = "arg2";
   case ARG3 = "arg3";
}

enum XMLAttribute: string
{
   case LANGUAGE = "language";
   case ORDER = "order";
   case OPCODE = "opcode";
   case TYPE = "type";
}

enum XMLAttributeValue: string
{
   case LABEL = "label";
   case VAR = "var";
   case TYPE = "type";
}

class Parser
{

   public $params;

   public function __construct(Params $params)
   {
      $this->params = $params;

      //open source file
      if ($this->params->source != STDIN) {
         $this->params->source = fopen($this->params->source, "r");
         if ($this->params->source == FALSE) error_exit(ErrorCodes::ERR_INPUT, "File not found or cannot be opened\n");
      }
   }

   public function __destruct()
   {
      //close source file
      if ($this->params->source != STDIN) fclose($this->params->source);
   }

   private function readLine()
   {
      while (($line = fgets($this->params->source)) !== FALSE) {
         //skip comments and empty lines
         if (str_contains($line, "#")) $line = substr($line, 0, strpos($line, "#"));
         if (!preg_match("/\w/", $line)) continue;

         return $line;
      }
      return FALSE;
   }

   private function parseHeader(DOMDocument $xml)
   {
      $line = $this->readLine();
      $line = trim($line);
      if (!preg_match("/^[.]ippcode23$/i", $line)) {
         error_exit(ErrorCodes::ERR_HEADER, "Invalid header\n");
      }

      $xml_program = $xml->createElement(XMLTag::PROGRAM->value);
      $xml_program->setAttribute(XMLAttribute::LANGUAGE->value, "IPPcode23");
      $xml->appendChild($xml_program);
   }

   private function parseProgram(DOMDocument $xml)
   {
      $xml_program = $xml->getElementsByTagName(XMLTag::PROGRAM->value)->item(0);

      $frame_charset = "(LF|TF|GF)";
      $name_charset = "([a-zA-Z_\-$(&amp;)%*!?][a-zA-Z0-9_\-$(&amp;)%*!?]*)";
      $type_charset = "(int|string|bool)";
      $type_charset_nil = "(int|string|bool|nil)";
      $const_charset =  "(nil@nil|int@([+-]?[0-9]+|nil)|string@([\\\\][0-9]{3}|[^\\\\])*|bool@(true|false|nil))";
      $regex_label = "/^$name_charset$/";
      $regex_var = "/^$frame_charset@$name_charset$/";
      $regex_symb = "/^(($frame_charset@$name_charset)|$const_charset)$/";
      $regex_type = "/^$type_charset$/";

      $loc = 0;

      //parse code
      while (($line = $this->readLine()) !== FALSE) {

         $loc++;
         $line = preg_replace("/&/", "&amp;", $line);
         $line = preg_replace("/</", "&lt;", $line);
         $line = preg_replace("/>/", "&gt;", $line);
         $line = trim($line);
         $line = preg_replace("/\s+/", " ", $line);
         $line = explode(" ", $line);

         //instruction
         $instruction = $line[0];
         if (!preg_match("/^(MOVE|CREATEFRAME|PUSHFRAME|POPFRAME|DEFVAR|CALL|RETURN|PUSHS|POPS|ADD|SUB|MUL|IDIV|LT|GT|EQ|AND|OR|NOT|INT2CHAR|STRI2INT|READ|WRITE|CONCAT|STRLEN|GETCHAR|SETCHAR|TYPE|LABEL|JUMP|JUMPIFEQ|JUMPIFNEQ|EXIT|DPRINT|BREAK)$/i", $instruction)) {
            error_exit(ErrorCodes::ERR_INSTRUCTION, "Invalid instruction\n");
         }

         //create instruction
         $xml_instruction = $xml->createElement(XMLTag::INSTRUCTION->value);
         $xml_instruction->setAttribute(XMLAttribute::ORDER->value, $loc);
         $xml_instruction->setAttribute(XMLAttribute::OPCODE->value, strtoupper($instruction));
         $xml_program->appendChild($xml_instruction);

         $xml_argv1 = NULL;
         $xml_argv2 = NULL;
         $xml_argv3 = NULL;

         //instruction params
         $instruction_params = array_slice($line, 1);
         $error_message = "Invalid number of instruction parameters\n";
         switch (count($instruction_params)) {
            case 0:
               if (!preg_match("/^(CREATEFRAME|PUSHFRAME|POPFRAME|RETURN|BREAK)$/i", $instruction)) {
                  error_exit(ErrorCodes::ERR_INSTRUCTION_PARAMS, $error_message);
               }
               break;
            case 1:
               if (!preg_match("/^(DEFVAR|CALL|PUSHS|POPS|WRITE|LABEL|JUMP|EXIT|DPRINT)$/i", $instruction)) {
                  error_exit(ErrorCodes::ERR_INSTRUCTION_PARAMS, $error_message);
               }
               break;
            case 2:
               if (!preg_match("/^(MOVE|NOT|INT2CHAR|READ|STRLEN|TYPE)$/i", $instruction)) {
                  error_exit(ErrorCodes::ERR_INSTRUCTION_PARAMS, $error_message);
               }
               break;
            case 3:
               if (!preg_match("/^(ADD|SUB|MUL|IDIV|LT|GT|EQ|AND|OR|STRI2INT|CONCAT|GETCHAR|SETCHAR|JUMPIFEQ|JUMPIFNEQ)$/i", $instruction)) {
                  error_exit(ErrorCodes::ERR_INSTRUCTION_PARAMS, $error_message);
               }
               break;
            default:
               error_exit(ErrorCodes::ERR_INSTRUCTION_PARAMS, $error_message);
               break;
         }

         //label
         if (preg_match("/^(CALL|LABEL|JUMP|JUMPIFEQ|JUMPIFNEQ)$/i", $instruction)) {
            if (!preg_match($regex_label, $instruction_params[0])) error_exit(ErrorCodes::ERR_INSTRUCTION_PARAMS, "Invalid label\n");
            $xml_argv1 = $xml->createElement(XMLTag::ARG1->value, $instruction_params[0]);
            $xml_argv1->setAttribute(XMLAttribute::TYPE->value, XMLAttributeValue::LABEL->value);
         }

         //var
         if (preg_match("/^(MOVE|DEFVAR|POPS|ADD|SUB|MUL|IDIV|LT|GT|EQ|AND|OR|NOT|INT2CHAR|STRI2INT|READ|CONCAT|STRLEN|GETCHAR|SETCHAR|TYPE)$/i", $instruction)) {
            if (!preg_match($regex_var, $instruction_params[0])) error_exit(ErrorCodes::ERR_INSTRUCTION_PARAMS, "Invalid variable\n");
            $xml_argv1 = $xml->createElement(XMLTag::ARG1->value, $instruction_params[0]);
            $xml_argv1->setAttribute(XMLAttribute::TYPE->value, XMLAttributeValue::VAR->value);
         }

         //type
         if (preg_match("/^(READ)$/", $instruction)) {
            if (!preg_match($regex_type, $instruction_params[1])) error_exit(ErrorCodes::ERR_INSTRUCTION_PARAMS, "Invalid type\n");
            $xml_argv2 = $xml->createElement(XMLTag::ARG2->value, $instruction_params[1]);
            $xml_argv2->setAttribute(XMLAttribute::TYPE->value, XMLAttributeValue::TYPE->value);
         }

         //symb(1)
         if (preg_match("/^(MOVE|PUSHS|ADD|SUB|MUL|IDIV|LT|GT|EQ|AND|OR|NOT|INT2CHAR|STRI2INT|WRITE|CONCAT|STRLEN|GETCHAR|SETCHAR|TYPE|JUMPIFEQ|JUMPIFNEQ|EXIT|DPRINT)$/i", $instruction)) {
            $index = preg_match("/^(PUSHS|WRITE|EXIT|DPRINT)$/i", $instruction) ? 0 : 1;
            if (!preg_match($regex_symb, $instruction_params[$index])) error_exit(ErrorCodes::ERR_INSTRUCTION_PARAMS, "Invalid symbol\n");
            $xml_temp = $xml->createElement($index == 0 ? XMLTag::ARG1->value : XMLTag::ARG2->value, preg_replace("/^$type_charset_nil@/", "", $instruction_params[$index]));
            $xml_temp->setAttribute(XMLAttribute::TYPE->value, preg_match($regex_var, $instruction_params[$index]) ? XMLAttributeValue::VAR->value : preg_replace("/@.*$/", "", $instruction_params[$index]));
            $index == 0 ? $xml_argv1 = $xml_temp : $xml_argv2 = $xml_temp;
         }

         //symb2
         if (preg_match("/^(ADD|SUB|MUL|IDIV|LT|GT|EQ|AND|OR|STRI2INT|CONCAT|GETCHAR|SETCHAR|JUMPIFEQ|JUMPIFNEQ)$/i", $instruction)) {
            if (!preg_match($regex_symb, $instruction_params[2])) error_exit(ErrorCodes::ERR_INSTRUCTION_PARAMS, "Invalid symbol\n");
            $xml_argv3 = $xml->createElement(XMLTag::ARG3->value, preg_replace("/^$type_charset_nil@/", "", $instruction_params[2]));
            $xml_argv3->setAttribute(XMLAttribute::TYPE->value, preg_match($regex_var, $instruction_params[2]) ? XMLAttributeValue::VAR->value : preg_replace("/@.*$/", "", $instruction_params[2]));
         }

         if ($xml_argv1 !== NULL) $xml_instruction->appendChild($xml_argv1);
         if ($xml_argv2 !== NULL) $xml_instruction->appendChild($xml_argv2);
         if ($xml_argv3 !== NULL) $xml_instruction->appendChild($xml_argv3);
      }
   }

   public function getXML()
   {
      //create xml document
      $xml = new DOMDocument("1.0", "UTF-8");
      $xml->formatOutput = true;

      //parse header
      $this->parseHeader($xml);

      //parse program
      $this->parseProgram($xml);

      return $xml->saveXML();
   }
}
?>