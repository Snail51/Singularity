// MINIFIED VERSION OF THE FILE OF THE SAME NAME IN THE `src` FOLDER
// MINIFIED WITH https://www.toptal.com/developers/javascript-minifier
// MINIFIED AT Sat Apr 19 17:08:14 CDT 2025

window.audioState="TITLE",window.changeAudioState=function(a){console.debug(`CHANGING AUDIO STATE: ${window.audioState} -> ${a}`);try{var e=document.querySelectorAll(`#${window.audioState} audio`);for(var o of e)o.pause(),o.load()}catch{}try{var e=document.querySelectorAll(`#${a} audio`);for(var o of e)o.play()}catch{}window.audioState=a},window.changeAudioVolume=function(a){var e=document.querySelectorAll("audio");for(var o of e)o.volume=a},window.addEventListener("DOMContentLoaded",()=>window.changeAudioVolume(.5));