/*
audio.js
├── ​PURPOSE
│   ​├── ​As we navigate between views, certain audio needs to be started and stopped.
│   ​├── ​The document already has various `<audio>` elements included in the `<div>` elements that make up the Views.
│   ​└── ​This script declares a global `window.fadeState` and a function to manipulate it, `window.changeFadeState(newState)`
├── ​Implementation
│   ​├── ​`window.audioState`
│   ​│       ​└── ​Possible Values: `TITLE`, `GAME`, `WIN`, `LOSE`
│   ​└── ​`window.changeAudioState(newState)`
│   ​    ​├── ​Updates `window.audioState` to `newState` at end of execution
│   ​    ​├── ​Executes `pause()` and `load()` on the element who's ID = the old value of `window.audioState`
│   ​    ​└── ​Executes `play()` on the element who's ID = the new value of `window.audioState`
└── ​See Also
    ​├── ​`/code/src/fadeable.js` -- has the same global state structure. separation is kept for clarity.
    ​└── ​`/code/src/binaryBG.js` -- has the same global state structure. separation is kept for clarity.
*/

window.audioState = "TITLE"; // "TITLE", "GAME", "WIN", "LOSE"

window.changeAudioState = function(newState) //call the desired state to handle fading
{
    console.debug(`CHANGING AUDIO STATE: ${window.audioState} -> ${newState}`);

    try
    {
        var nodes = document.querySelectorAll(`#${window.audioState} audio`);
        for( var node of nodes )
        {
            node.pause();
            node.load();
        }
    }
    catch {}

    try
    {
        var nodes = document.querySelectorAll(`#${newState} audio`);
        for( var node of nodes )
        {
            node.play();
        }
    }
    catch {}
    
    window.audioState = newState;
}