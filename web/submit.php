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
        You chose the color: 
    <?php
	$myfile = fopen("colorData", "w+") or die("File error");
    $color = $_GET["color"];
    $r = 0;
    $g = 0;
    $b = 0;
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
    $arr = hex2rgb($color);
    $r = $arr[0];
    $g = $arr[1];
    $b = $arr[2];

    echo $r.",".$g.",".$b."\n";
    for($c = 0; $c < 1; $c++){
        // only do this once instead of 600 times for all the leds
		fwrite($myfile, chr($r));
		fwrite($myfile, chr($g));
		fwrite($myfile, chr($b));
	}
    fclose($myfile);
    ?>
        </div>
        <div id="sub"><a href="index.html">Back to the Color Picker</a></div>
    </div>
</body>
</html>