window.setInterval(() =>
{
    if(window.fadeState == "LOSE")
    {
        document.getElementById("binaryBG").classList.add("lose");
        return;
    }
    document.getElementById("binaryBG").classList.remove("lose");

    var bg = "";
    for ( var i = 0; i < 5000; i++)
    {
        bg += Math.round(Math.random());
    }
    document.getElementById("binaryBG").innerHTML = bg;
}, 100);

