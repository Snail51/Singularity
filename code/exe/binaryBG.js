// MINIFIED VERSION OF THE FILE OF THE SAME NAME IN THE `src` FOLDER
// MINIFIED WITH https://www.toptal.com/developers/javascript-minifier
// MINIFIED AT Sat Apr 19 17:08:14 CDT 2025

window.backgroundState="TITLE",window.changeBackgroundState=function(e){console.debug(`CHANGING BACKGROUND STATE: ${window.backgroundState} -> ${e}`),"LOSE"==e?document.getElementById("binaryBG").classList.add("lose"):document.getElementById("binaryBG").classList.remove("lose"),window.backgroundState=e},window.setInterval(()=>{if("LOSE"!=window.backgroundState){for(var e="",t=0;t<5e3;t++)e+=Math.round(Math.random());document.getElementById("binaryBG").innerHTML=e}},100);