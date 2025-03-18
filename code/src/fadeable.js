/*
fadeable.js
├── ​PURPOSE
│   ​├── ​In order to navigate between "Views", we need to fade certain elements via CSS transitions
│   ​└── ​This script declares a global `window.fadeState` and a function to manipulate it, `window.changeFadeState(newState)`
├── ​Implementation
│   ​├── ​`window.fadeState`
│   ​│       ​└── ​Possible Values: `TITLE`, `GAME`, `WIN`, `LOSE`
│   ​└── ​`window.changeFadeState(newState)`
│   ​    ​├── ​Updates `window.fadeState` to `newState` at end of execution
│   ​    ​├── ​Toggles the `hide` CSS class of the element who's ID = the old value of `window.fadeState`
│   ​    ​└── ​Toggles the `hide` CSS class of the element who's ID = the new value of `window.fadeState`
└── ​See Also
    ​├── ​`/css/fadeable.css` -- style the elements related to this script
    ​├── ​`/code/src/audio.js` -- has the same global state structure. separation is kept for clarity.
    ​└── ​`/code/src/binaryBG.js` -- has the same global state structure. separation is kept for clarity.
*/

window.fadeState = "TITLE"; // "TITLE", "GAME", "WIN", "LOSE"

window.changeFadeState = function(newState) //call the desired state to handle fading
{
    console.debug(`CHANGING FADE STATE: ${window.fadeState} -> ${newState}`);

    try
    {
        document.getElementById(window.fadeState).classList.toggle("hide");
    }
    catch {}

    try
    {
        document.getElementById(newState).classList.toggle("hide");
    }
    catch {}
    
    window.fadeState = newState;
}