/*
binaryBG.js
├── ​PURPOSE
│   ​├── ​The background of the program consists of a wall of binary that is repeatedly updated to produce an interesting visual effect.
│   ​├── ​Every 100ms, a random string is created that consists of 5000 0s and 1s.
│   ​├── ​This string is written to the innerHTML of the element with ID="binaryBG".
│   ​└── ​When the game is in the `LOSE` state, the background is to become dark blue and the numbers should stop updating; communicating the look of a "crashed" computer.
├── ​Implementation
│   ​├── ​`window.backgroundState`
│   ​│       ​└── ​Possible Values: `TITLE`, `GAME`, `WIN`, `LOSE`
│   ​├── ​`window.changeBackgroundState(newState)`
│   ​│       ​├── ​Updates `window.backgroundState` to `newState` at end of execution
│   ​│       ​├── ​If `newState`==`LOSE`, the CSS class `lose` is added.
│   ​│       ​└── ​If `newState`!=`LOSE`, the CSS class `lose` is removed.
│   ​└── ​Main Interval
│   ​    ​├── ​Every 100ms, a random string is created that consists of 5000 0s and 1s. It is written to `#binaryBG.innerHTML`.
│   ​    ​└── ​If `window.backgroundState`==`LOSE`, execution aborts early and the string is not updated.
└── ​See Also
    ​├── ​`/css/binaryBG.css` -- style the elements related to this script
    ​├── ​`/code/src/audio.js` -- has the same global state structure. separation is kept for clarity.
    ​└── ​`/code/src/fadeable.js` -- has the same global state structure. separation is kept for clarity.
*/

window.backgroundState = "TITLE";

window.changeBackgroundState = function(newState) //call the desired state to handle fading
{
    console.debug(`CHANGING BACKGROUND STATE: ${window.backgroundState} -> ${newState}`);
    
    if(newState == "LOSE")
    {
        document.getElementById("binaryBG").classList.add("lose");
    }
    else
    {
        document.getElementById("binaryBG").classList.remove("lose");
    }

    window.backgroundState = newState;
}

window.setInterval(() =>
{
    if(window.backgroundState == "LOSE") //abort early if backgroundState = "LOSE", meaning don't update
    {
        return;
    }

    var bg = "";
    for ( var i = 0; i < 5000; i++)
    {
        bg += Math.round(Math.random());
    }
    document.getElementById("binaryBG").innerHTML = bg;
}, 100);

