/*
server.js
├── ​MASTER
│   ​└── ​This file is part of the `Singularity` program written by Brendan Rood https://github.com/Snail51/Singularity.git
├── ​PURPOSE
│   ​├── ​The purpose of this file is to handle the logic of discrete "Servers" in the main game of this application.
│   ​└── ​Servers are the discrete rectangles that appear during gameplay, representing lettings A-Z, as well as SPACE and RETURN
├── ​GAMEPLAY
│   ​└── ​Clicking a server will append that key to the player's *terminal*, effectively acting as a secondary way to type
│   ​    ​
└── ​DECLARATION
    ​├── ​Servers are declared through the custom HTML tag `<Server serverID="?"></Server>`.
    ​├── ​At pageshow, this script consumes all `<Server>` elements and converts them into properly styled an initialized `<button>`s
    ​├── ​All <Server> elements must be declared with a `serverID` attribute.
    ​├── ​These custom buttons are setup with the following HTML attributes:
    ​│   ​├── ​- Key:"locked" Value:"false" (Bool as String)
    ​│   ​├── ​- Key:"serverID" Value:`${serverID}` (String)
    ​│   ​├── ​- Id: `server${serverID}`
    ​│   ​└── ​- Classes: `serverItem serverGrid${serverID}`
    ​└── ​These custom buttons are setup with the following HTML event listeners:
    ​        ​└── ​- onclick: `() => { window.clickServer(id) }`
*/


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
        return;
    }
    document.getElementById("terminal").value += value;
    document.getElementById("terminal").focus();
}

window.addEventListener("pageshow", () => 
{
    var ServerDOMs = document.querySelectorAll("Server");
    for( var server of ServerDOMs )
    {
        // capture DOM element attributes
        const id = server.getAttribute("serverID");

        // create new div object to hold the button grid and slider
        var newButton = document.createElement("button");
        newButton.classList.add("serverItem");
        newButton.classList.add(`serverGrid${id}`);
        newButton.innerHTML = id;
        newButton.id = `server${id}`;
        newButton.setAttribute("serverID", id);
        newButton.setAttribute("locked", false);
        newButton.addEventListener("click", () => { window.clickServer(id) });

        // place the new div structure onto the DOM
        server.insertAdjacentElement("afterend", newButton);

        // remove placeholder node of type <AudioTile>
        server.remove();
    }
});