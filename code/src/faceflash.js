/**
 * Every 100ms, have a certain percent chance to place a picture of 079's face at a random location on the document, then remove it 200ms later
 * This creates brief flashes of 079's face under the UI on all views except `LOSE`
 */

setInterval(() => {
    const chance = 0.05;

    if(window.backgroundState != "LOSE")
    {
        if(Math.random() < chance)
            {
                let img = document.createElement("img");
                img.src = "./assets/img/079Flash_dark.jpg";
                img.alt = "SCP-079's face, flashing briefly in a menacing manner.";
                img.style.position = "absolute";
        
                var width = window.outerWidth;
                var height = window.outerHeight;
        
                var x = Math.random() * width;
                var y = Math.random() * height;
        
                img.style.left = `${x}px`;
                img.style.top = `${y}px`;
        
                document.getElementById("faceflashholder").appendChild(img);
        
                setTimeout(() => {
                    img.remove();
                }, 200);
            }
    }
}, 100);