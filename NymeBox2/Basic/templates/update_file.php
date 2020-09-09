<!DOCTYPE html>
<html>
 <body>
 <?php
        $file = "testing.txt";
        $f = fopen($file, "r") or die("Unable to open file");
        while ( $line = fgets($f, 1000) ) {
            echo $line or die("Unable to show line");
            echo "test";
        }
        echo "testing"
        fclose($file)
?>

 </body>
</html>

