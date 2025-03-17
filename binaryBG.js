window.setInterval(() =>
{
    var bg = "";
    for ( var i = 0; i < 5000; i++)
    {
        bg += Math.round(Math.random());
    }
    document.getElementById("binaryBG").innerHTML = bg;
}, 100);