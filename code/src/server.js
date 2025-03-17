window.clickServer = () =>
{
    if(event.srcElement.getAttribute("locked") == "true")
    {
        return; // if the server is locked, abort processing
    }
    var value = event.srcElement.getAttribute("serverID");
    if( value == "RETURN" )
    {
        console.log(`EXECUTING AND CLEARING TERMINAL DATA "${document.getElementById("terminal").value}"`);
        document.getElementById("terminal").value = "";
        return;
    }
    document.getElementById("terminal").value += value;
    document.getElementById("terminal").focus();
}

window.addEventListener("DOMContentLoaded", () => 
{
    var ServerDOMs = document.querySelectorAll("Server");
    for( var server of ServerDOMs )
    {
        // capture DOM element attributes
        const id = server.getAttribute("serverID");

        // create new div object to hold the button grid and slider
        var newButton = document.createElement("button");
        newButton.classList.add("serverServer");
        newButton.classList.add(id);
        newButton.innerHTML = id;
        newButton.setAttribute("serverID", id);
        newButton.setAttribute("locked", false);
        newButton.addEventListener("click", () => { window.clickServer(id) });

        // place the new div structure onto the DOM
        server.insertAdjacentElement("afterend", newButton);

        // remove placeholder node of type <AudioTile>
        server.remove();
    }
});