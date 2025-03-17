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