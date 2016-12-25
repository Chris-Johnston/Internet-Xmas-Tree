function setPreset(buttonSrc)
{
    var sourceID = buttonSrc.id;
    var form = document.forms[0];
    switch(sourceID)
    {
        default:
        case "presetOff":
            form["pattern"].value = 0;
            form["color1"].value = "000000";
            form["color2"].value = "000000";
            form["len"].value = 1;
            form["delay"].value = 10;
            form["random1"].checked = false;
            form["random2"].checked = false;
            break;
        case "presetXmas":
            form["pattern"].value = 8;
            form["color1"].value = "FF0000";
            form["color2"].value = "00FF00";
            form["len"].value = 1;
            form["delay"].value = 5000;
            form["random1"].checked = false;
            form["random2"].checked = false;
            break;
            break;
        case "presetSeahawks":
            form["pattern"].value = 3;
            form["color1"].value = "00FF00";
            form["color2"].value = "0000FF";
            form["len"].value = 1;
            form["delay"].value = 5000;
            form["random1"].checked = false;
            form["random2"].checked = false;
            break;
        case "presetBlinky":
            form["pattern"].value = 5;
            form["color1"].value = "FFFFFF";
            form["color2"].value = "000000";
            form["len"].value = 80;
            form["delay"].value = 10;
            form["random1"].checked = true;
            form["random2"].checked = false;
            break;
    }

}