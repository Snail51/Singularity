window.addEventListener("DOMContentLoaded", () => {
    var elements = document.querySelectorAll("body *");
    console.log(elements);
    for ( var element of elements )
    {
        var r = Math.round(Math.random() * 255);
        var g = Math.round(Math.random() * 255);
        var b = Math.round(Math.random() * 255);
        var a = 200;

        var newColor = `${r.toString(16)}${g.toString(16)}${b.toString(16)}${a.toString(16)}`;
        element.style.backgroundColor = `#${r.toString(16)}${g.toString(16)}${b.toString(16)}${a.toString(16)}`;

        console.debug(`Changed color of ${element} to ${newColor}`);
    }
});