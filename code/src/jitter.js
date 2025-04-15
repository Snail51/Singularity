setInterval(() => {
    var jitterelements;

    jitterelements = document.querySelectorAll(".jitter-low");
    for( var element of jitterelements )
    {
        jitter(element, 3, 0.02);
    }

    jitterelements = document.querySelectorAll(".jitter-high");
    for( var element of jitterelements )
    {
        jitter(element, 3, 0.10);
    }

    jitterelements = document.querySelectorAll(".jitter-max");
    for( var element of jitterelements )
    {
        jitter(element, 5, 0.50);
    }



    function jitter(element, amount, chance)
    {
        if(Math.random() < chance) // only jitter if the number is less than the chance
        {
            var x = ((Math.random() * amount) - (Math.floor(amount/2)));
            var y = ((Math.random() * amount) - (Math.floor(amount/2)));

            element.style.marginLeft = `${x * -1}px`;
            element.style.marginRight = `${x *  1}px`;
            element.style.marginTop = `${y * -1}px`;
            element.style.marginBottom = `${y *  1}px`;
        }
        else
        {
            element.style.marginLeft = `0px`;
            element.style.marginRight = `0px`;
            element.style.marginTop = `0px`;
            element.style.marginBottom = `0px`;
        }
    }
}, 100);