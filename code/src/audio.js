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