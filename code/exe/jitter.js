// MINIFIED VERSION OF THE FILE OF THE SAME NAME IN THE `src` FOLDER
// MINIFIED WITH https://www.toptal.com/developers/javascript-minifier
// MINIFIED AT Sat Apr 19 17:08:14 CDT 2025

setInterval(()=>{var r;for(var t of r=document.querySelectorAll(".jitter-low"))e(t,3,.02);for(var t of r=document.querySelectorAll(".jitter-high"))e(t,3,.1);for(var t of r=document.querySelectorAll(".jitter-max"))e(t,5,.5);function e(r,t,e){if(Math.random()<e){var o=Math.random()*t-Math.floor(t/2),l=Math.random()*t-Math.floor(t/2);r.style.marginLeft=`${-1*o}px`,r.style.marginRight=`${1*o}px`,r.style.marginTop=`${-1*l}px`,r.style.marginBottom=`${1*l}px`}else r.style.marginLeft="0px",r.style.marginRight="0px",r.style.marginTop="0px",r.style.marginBottom="0px"}},100);