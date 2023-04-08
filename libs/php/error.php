<?php

/**
 * @file exit.php
 * @brief IPP project 1
 * @author Marek Gergel (xgerge01)
 * @date 2023-03-11
 * @details
 * Error handling class
 */

 enum ErrorCodes: int
{
   case ERR_PARAMS = 10;
   case ERR_INPUT = 11;
   case ERR_HEADER = 21;
   case ERR_INSTRUCTION = 22;
   case ERR_INSTRUCTION_PARAMS = 23;
}

function error_exit(ErrorCodes $code, string $message)
{
   fwrite(STDERR, "Error: $message");
   exit($code->value);
}