export class Game
{
    constructor(virusCount, maxHealth, maxEnergy, energyRate, executionCost, executionTime, promptTime, promptLength, notificationTime)
    {
        this.virusCount = virusCount;
        this.virusList = new Set();
        while(this.virusList.length < this.virusCount)
        {
            var newVirus = 65 + Math.round(Math.random() * 25);
            newVirus = String.fromCharCode(newVirus);
            this.virusList.push(newVirus);
        }
        this.virusList = Array.from(this.virusList);

        this.health = maxHealth;
        this.maxHealth = maxHealth;

        this.energy = 0;
        this.maxEnergy = maxEnergy;
        this.energyRate = energyRate;
        this.energyGainInterval; // initialize on state change

        this.executionCost = executionCost;
        this.executionTime = executionTime;

        this.prompt = "";
        this.promptTime = promptTime;
        this.promptLength = promptLength;
        this.promptInterval; // initialize on state change
        this.promptTimestamp = Date.now();

        this.notification = "";
        this.notificationTime = notificationTime;
        this.notificationTimeout; // initialized and overwritten as new notifications are requested

        this.active = false; // only true if the game is currently happening (not on any other view). used to prevent actions after win/loss

        document.getElementById("terminal").addEventListener('keydown', () => {
            if(["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(event.key)) // disallow arrow keys
            {
                event.preventDefault();
                return;
            }

            if(["Backspace", "Delete"].includes(event.key)) // `Backspace` and `Delete` have executionCost, block if cant afford
            {
                if(this.energy < this.executionCost)
                {
                    event.preventDefault();
                }
                else
                {
                    this.energy -= this.executionCost;
                }
            }

            if (event.key == 'Enter') // if the keypress is `Enter`, prevent default and tryExecution
            {
                event.preventDefault();
                this.tryExecution();
                return;
            }

            try //prevent the keypress if the corresponding server is currently locked
            {
                if(document.getElementById(`server${event.key.toUpperCase()}`).classList.contains("locked"))
                {
                    event.preventDefault();
                }
            }
            catch {}
        });
        document.getElementById("serverRETURN").addEventListener('click', () => {
            this.tryExecution();
        })
        document.getElementById("terminal").addEventListener("input", () => {
            document.getElementById("terminal").value = document.getElementById("terminal").value.toUpperCase();
        });

        window.setInterval(() => {
            document.getElementById("topLeftInfo").innerHTML = `Viruses remaining: ${this.virusList.length}/${this.virusCount}`;
            document.getElementById("bottomLeftInfo").innerHTML = `Energy: ${this.energy}/${this.maxEnergy}`;
            document.getElementById("bottomRightInfo").innerHTML = `Health: ${this.health}/${this.maxHealth}`;

            var r = Math.abs(Math.round(((Date.now() - this.promptTimestamp) / this.promptTime)*255));
            var b = Math.abs(r - 255);
            r = r.toString(16).padStart(2, "0");
            b = b.toString(16).padStart(2, "0");
            document.getElementById("prompt").style.color = `#${r}00${b}`;
        }, 200);
    }

    load()
    {
        // enforce mutex; don't load if already loaded
        if(this.active) 
        {
            return;
        }

        // reinitialize with starting values
        this.virusList = new Set();
        while(this.virusList.size < this.virusCount)
        {
            var newVirus = 65 + Math.round(Math.random() * 25);
            newVirus = String.fromCharCode(newVirus);
            this.virusList.add(newVirus);
        }
        this.virusList = Array.from(this.virusList);
        this.energy = 0;
        this.health = this.maxHealth;
        this.prompt = "";

        // ensure all servers are in unlocked state
        var servers = document.querySelectorAll(".serverItem");
        for( var server of servers )
        {
            server.classList.remove("locked");
        }

        // setup energy gain interval
        this.energyGainInterval = window.setInterval(() => {
            if(this.energy < this.maxEnergy)
            {
                this.energy++;
            }
        }, this.energyRate);

        // setup prompt interval
        this.prompt = "";
        this.promptTimestamp = Date.now();
        this.promptInterval = window.setInterval(() => {
            this.promptCycle();
        }, this.promptTime);
        this.prompt = "";

        // focus the terminal <input> so the user doesn't need to click it
        document.getElementById("terminal").focus();

        this.active = true; // mark the game as active, allowing timeouts and intervals to resolve.
    }

    unload()
    {
        // stop intervals now that execution is done
        clearInterval(this.promptInterval);
        clearInterval(this.energyGainInterval);

        // mark the game as inactive, preventing resolution of timeouts and intervals
        this.active = false; 
    }

    promptCycle()
    {
        // abort early and do nothing if the game has ended
        if(!this.active) 
        {
            return;
        }

        this.promptTimestamp = Date.now();
        document.getElementById("prompt").style.color = "blue";

        // if the prompt hasn't been cleared and we are making a new one, that indicates the user failed to complete it
        if(this.prompt.length > 0) 
        {
            this.health--; // lose health
            if(this.health == 0) // if health == 0, die
            {
                window.changeFadeState('LOSE');
                window.changeAudioState('LOSE');
                window.changeBackgroundState('LOSE');
                this.unload();
                return;
            }
        }

        // make a new prompt
        var promptBuilder = new Array();
        while(promptBuilder.length < this.promptLength)
        {
            var letter = 65 + Math.round(Math.random() * 25);
            letter = String.fromCharCode(letter);
            promptBuilder.push(letter);
        }
        this.prompt = promptBuilder.join("");
        document.getElementById("prompt").value = this.prompt;

        this.promptTimestamp = Date.now();
    }

    tryExecution()
    {
        // abort early and do nothing if the game has ended
        if(!this.active)
        {
            return;
        }

        // do nothing if not enough energy
        if(this.energy < this.executionCost)
        {
            return; 
        }
        this.energy -= this.executionCost;

        // check for scanning
        if(/SCRUB|SCAN|DISINFECT|ANTIVIRUS|CHECK|CLEAN/gm.test(document.getElementById("terminal").value))
        {
            this.scanStart(document.getElementById("terminal").value[document.getElementById("terminal").value.length-1]);
        }

        // check for prompt resolution
        if(document.getElementById("terminal").value == document.getElementById("prompt").value)
        {
            this.prompt = "";
            document.getElementById("prompt").value = "";
        }

        // clear the terminal
        document.getElementById("terminal").value = "";
    }

    scanStart(serverID)
    {
        if(!this.active) // abort early and do nothing if the game has ended
        {
            return;
        }

        var element = document.getElementById(`server${serverID}`);
        element.classList.add("locked");
        setTimeout(() => {
           this.scanEnd(serverID); 
        }, this.executionTime);
    }

    scanEnd(serverID)
    {
        if(!this.active) // abort early and do nothing if the game has ended
        {
            return;
        }

        var element = document.getElementById(`server${serverID}`);

        if(this.virusList.includes(serverID))
        {
            // NOTIFY
            this.virusList = this.virusList.filter(virus => virus !== serverID); //remove that virus
            this.newNotify(`Virus found in server ${serverID}!`);

            if(this.virusList.length == 0)
            {
                window.changeFadeState('WIN');
                window.changeAudioState('WIN');
                window.changeBackgroundState('WIN');
                this.unload();
            }
        }

        element.classList.remove("locked");
    }

    newNotify(notification)
    {
        if(!this.active) // abort early and do nothing if the game has ended
        {
            return;
        }

        clearTimeout(this.notificationTimeout);
        this.notification = notification;
        document.getElementById("notify").value = this.notification;
        this.notificationTimeout = setTimeout(() => {
           this.clearNotify(); 
        }, this.notificationTime);
    }

    clearNotify()
    {
        this.notification = "";
        document.getElementById("notify").value = this.notification;
    }
}

// print the virus list to console
window.cheat = function() {
    return window.game.virusList;
}

// set player health to 1, such that the next missed prompt will kill them
window.lose = function() {
    window.game.health = 1;
}