// MINIFIED VERSION OF THE FILE OF THE SAME NAME IN THE `src` FOLDER
// MINIFIED WITH https://www.toptal.com/developers/javascript-minifier

export class Game{constructor(t,e,i,s,n,r,o,a,h){for(this.virusCount=t,this.virusList=new Set;this.virusList.length<this.virusCount;){var l=65+Math.round(25*Math.random());l=String.fromCharCode(l),this.virusList.push(l)}this.virusList=Array.from(this.virusList),this.health=e,this.maxHealth=e,this.energy=0,this.maxEnergy=i,this.energyRate=s,this.energyGainInterval,this.executionCost=n,this.executionTime=r,this.prompt="",this.promptList=[],fetch("./assets/prompts.txt").then(t=>t.text()).then(t=>t.split("\n")).then(t=>t=t.filter(t=>""!=t)).then(t=>this.promptList=t),this.promptTime=o,this.promptLength=a,this.promptInterval,this.promptTimestamp=Date.now(),this.notification="",this.notificationTime=h,this.notificationTimeout,this.active=!1,document.getElementById("terminal").addEventListener("keydown",()=>{if(["ArrowLeft","ArrowRight","ArrowUp","ArrowDown"].includes(event.key)){event.preventDefault();return}if(["Backspace","Delete"].includes(event.key)&&(this.energy<this.executionCost?event.preventDefault():this.energy-=this.executionCost),"Enter"==event.key){event.preventDefault(),this.tryExecution();return}try{document.getElementById(`server${event.key.toUpperCase()}`).classList.contains("locked")&&event.preventDefault()}catch{}}),document.getElementById("serverRETURN").addEventListener("click",()=>{this.tryExecution()}),document.getElementById("terminal").addEventListener("input",()=>{document.getElementById("terminal").value=document.getElementById("terminal").value.toUpperCase()}),window.setInterval(()=>{document.getElementById("topLeftInfo").innerHTML=`Viruses remaining: ${this.virusList.length}/${this.virusCount}`,document.getElementById("bottomLeftInfo").innerHTML=`Energy: ${this.energy}/${this.maxEnergy}`,document.getElementById("bottomRightInfo").innerHTML=`Health: ${this.health}/${this.maxHealth}`;var t=Math.abs(Math.round((Date.now()-this.promptTimestamp)/this.promptTime*255)),e=Math.abs(t-255);t=t.toString(16).padStart(2,"0"),e=e.toString(16).padStart(2,"0"),document.getElementById("prompt").style.color=`#${t}00${e}`},200)}load(){if(!this.active){for(this.virusList=new Set;this.virusList.size<this.virusCount;){var t=65+Math.round(25*Math.random());t=String.fromCharCode(t),this.virusList.add(t)}this.virusList=Array.from(this.virusList),this.energy=0,this.health=this.maxHealth,this.prompt="";var e=document.querySelectorAll(".serverItem");for(var i of e)i.classList.remove("locked");this.energyGainInterval=window.setInterval(()=>{this.energy<this.maxEnergy&&this.energy++},this.energyRate),this.prompt="",this.promptTimestamp=Date.now(),this.promptInterval=window.setInterval(()=>{this.promptCycle()},this.promptTime),this.prompt="",document.getElementById("terminal").focus(),this.active=!0}}unload(){clearInterval(this.promptInterval),clearInterval(this.energyGainInterval),this.active=!1}promptCycle(){if(this.active){if(this.promptTimestamp=Date.now(),document.getElementById("prompt").style.color="blue",this.prompt.length>0&&(this.health--,0==this.health)){window.changeFadeState("LOSE"),window.changeAudioState("LOSE"),window.changeBackgroundState("LOSE"),this.unload();return}this.prompt=this.promptList[Math.round(Math.random()*(this.promptList.length-1))],document.getElementById("prompt").value=this.prompt,this.promptTimestamp=Date.now()}}tryExecution(){this.active&&!(this.energy<this.executionCost)&&(this.energy-=this.executionCost,/SCRUB|SCAN|DISINFECT|ANTIVIRUS|CHECK|CLEAN/gm.test(document.getElementById("terminal").value)&&this.scanStart(document.getElementById("terminal").value[document.getElementById("terminal").value.length-1]),document.getElementById("terminal").value==document.getElementById("prompt").value&&(this.prompt="",document.getElementById("prompt").value=""),document.getElementById("terminal").value="")}scanStart(t){this.active&&(document.getElementById(`server${t}`).classList.add("locked"),setTimeout(()=>{this.scanEnd(t)},this.executionTime))}scanEnd(t){if(this.active){var e=document.getElementById(`server${t}`);this.virusList.includes(t)&&(this.virusList=this.virusList.filter(e=>e!==t),this.newNotify(`Virus found in server ${t}!`),0==this.virusList.length&&(window.changeFadeState("WIN"),window.changeAudioState("WIN"),window.changeBackgroundState("WIN"),this.unload())),e.classList.remove("locked")}}newNotify(t){this.active&&(clearTimeout(this.notificationTimeout),this.notification=t,document.getElementById("notify").value=this.notification,this.notificationTimeout=setTimeout(()=>{this.clearNotify()},this.notificationTime))}clearNotify(){this.notification="",document.getElementById("notify").value=this.notification}}window.cheat=function(){return window.game.virusList},window.lose=function(){window.game.health=1};