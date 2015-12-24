<!DOCTYPE HTML>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />
    <title>Xmas Tree Color Picker</title>
    <script src="js/jscolor.js"></script>
    <link rel="stylesheet" type="text/css" href="css/style.css" />
    </head>
<body>
    <div id="wrapper">
    <h1>X-mas Tree Color Picker</h1>
    
    <div id="status">
        You chose pattern: 
    <?php
	$myfile = fopen("colorData", "w+") or die("File error");
    $color1 = $_GET["color1"];
    $color2 = $_GET["color2"];

    $c1Rand = $_GET["random1"];
    $c2Rand = $_GET["random2"];

    $pattern = $_GET["pattern"];

    function hex2rgb($hex) {
        $hex = str_replace("#", "", $hex);

        if(strlen($hex) == 3) {
            $_r = hexdec(substr($hex,0,1).substr($hex,0,1));
            $_g = hexdec(substr($hex,1,1).substr($hex,1,1));
            $_b = hexdec(substr($hex,2,1).substr($hex,2,1));
        } else {
            $_r = hexdec(substr($hex,0,2));
            $_g = hexdec(substr($hex,2,2));
            $_b = hexdec(substr($hex,4,2));
        }
        $rgb = array($_r, $_g, $_b);
        //return implode(",", $rgb); // returns the rgb values separated by commas
        return $rgb; // returns an array with the rgb values
    }
    $c1 = hex2rgb($color1);
    $c2 = hex2rgb($color2);

    echo $pattern;
    for($c = 0; $c < 1; $c++){
        // write RGB for color 1
		fwrite($myfile, chr($c1[0]));
		fwrite($myfile, chr($c1[1]));
		fwrite($myfile, chr($c1[2]));
        // write RGB for color 2
        fwrite($myfile, chr($c2[0]));
		fwrite($myfile, chr($c2[1]));
		fwrite($myfile, chr($c2[2]));

        // write Random Flag Bytes
        if(strcmp($c1Rand, "on") == 0){
            fwrite($myfile, chr(1));
        } else {
            fwrite($myfile, chr(0));
        }

        if(strcmp($c2Rand, "on") == 0){
            fwrite($myfile, chr(1));
        } else {
            fwrite($myfile, chr(0));
        }
        // write the pattern byte
        fwrite($myfile, chr($pattern));
        // write the length
        fwrite($myfile, PHP_EOL);
        fwrite($myfile, $_GET["length"]);
        // write the delay
        fwrite($myfile, PHP_EOL);
        fwrite($myfile, $_GET["delay"]);
	}
    fclose($myfile);
    ?>
        </div>
        <div id="sub"><a href="index.html">Back to the Color Picker</a></div>
    </div>
</body>
</html>