<?php
    $fileName = "data.json";
	$myfile = fopen($fileName, "w+") or die("File error");
    
    $color1 = $_GET["color1"];
    $color2 = $_GET["color2"];

    $c1Rand = $_GET["random1"];
    $c2Rand = $_GET["random2"];

    $pattern = $_GET["pattern"];

    $length = $_GET["length"];
    $delay = $_GET["delay"];

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

    $data = array (
        "color1" => $color1,
        "color2" => $color2,
        "isRandom1" => $c1Rand,
        "isRandom2" => $c2Rand,
        "pattern" => intval($pattern),
        "length" => intval($length),
        "delay" => intval($delay));

    $jsondata = json_encode($data);
    echo "Data: ";
    echo $jsondata;

    file_put_contents($fileName, $jsondata);
    fclose($myfile);
?>
