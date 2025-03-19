// MINIFIED VERSION OF THE FILE OF THE SAME NAME IN THE `src` FOLDER
// MINIFIED WITH https://www.toptal.com/developers/javascript-minifier

window.fadeState="TITLE",window.changeFadeState=function(t){console.debug(`CHANGING FADE STATE: ${window.fadeState} -> ${t}`);try{document.getElementById(window.fadeState).classList.toggle("hide")}catch{}try{document.getElementById(t).classList.toggle("hide")}catch{}window.fadeState=t};