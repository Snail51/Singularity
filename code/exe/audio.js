// MINIFIED VERSION OF THE FILE OF THE SAME NAME IN THE `src` FOLDER
// MINIFIED WITH https://www.toptal.com/developers/javascript-minifier

window.audioState="TITLE",window.changeAudioState=function(a){console.debug(`CHANGING AUDIO STATE: ${window.audioState} -> ${a}`);try{var t=document.querySelectorAll(`#${window.audioState} audio`);for(var o of t)o.pause(),o.load()}catch{}try{var t=document.querySelectorAll(`#${a} audio`);for(var o of t)o.play()}catch{}window.audioState=a};