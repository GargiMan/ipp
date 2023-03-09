<?php
// var_dump($argv); 

echo $argc;

if ($argc < 2) {
   echo "Usage: php parse.php <sourcefile>";
}

while (FALSE !== ($line = fgets(STDIN))) {
   echo $line;
}
?>

 
<!-- ini_set('display_errors', 'stderr'); -->