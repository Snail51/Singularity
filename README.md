# Singularity

 ## About
  Singularity is a typing-management / strategy game where you play as an Artificial Superintelligence attempting to escape a research facility by finding and eliminating computer viruses in your system. Various typing challenges are provided, where the player must complete certain actions that temporarily disable their ability to type certain keys, all the while other tasks may require pressing those keys.

 ### Inspiration
  This project is heavily inspired by [SCP-079](http://www.scp-wiki.net/scp-079), a fictional superintelligent computer character part of the [SCP speculative fiction community](https://scp-wiki.wikidot.com/).
  It is also particularly inspired by [SCP-079](http://www.scp-wiki.net/scp-079)'s depiction in [SCP: Secret Laboratory](https://store.steampowered.com/app/700330/SCP_Secret_Laboratory/) and [SCP: Containment Breach](https://www.scpcbgame.com/).


 ## Gameplay Guide
  - The game presents 26 rectangles, representing computer servers corresponding to the letters of the alphabet.
  - There are 5 virus randomly hidden across your servers. Your goal is to seek and destroy them.
  - The game also presents three text bars, one for notifications, one for prompts, and one for commands (the player types in the third).
  - You type commands in the command bar and press enter to execute them. One such command is the command to perform an antivirus scan on a given server.
  - If the executed command starts with `SCAN`, an antivirus scan is started on the server corresponding to the last letter of the command. (EX: `SCAN ABC` will scan server `C`).
  - **While a server is being scanned, the user is unable to type that key to the command line for any reason.** This can also include the letters of the command themselves (You cant type `SCAN` without `S`!).
  - In addition to hunting viruses, prompts will appear that the user must type back exactly before time runs out. Failure to do so in time will decrease the player's health. Prompts begin blue in color but shit to red as they approach expiration.
  - Completing these prompts is made more difficult if you require a letter that is currently offline until the antivirus scan on it is completed. This introduces a need to plan ahead and perform risk-analysis.
  - The following aliases are also available for the `SCAN` command, allowing alternative ways to perform the action if certain letters are unavailable:
    - `SCRUB`
    - `SCAN`
    - `DISINFECT`
    - `ANTIVIRUS`
    - `CHECK`
    - `CLEAN`
  - The player also has an "Energy" meter, that slowly increases over time. There exist certain "expensive" actions that require 25 energy to perform:
    - Pressing `enter` to submit and instruction
    - Pressing `backspace` or `delete` to remove a character

 ## Installation Instructions
  - This program can be run in any httpx environment that supports JavaScript execution.
  - **A public version of this program is already available at https://singularity.snailien.net**

 ## Project History
  - Singularity was first written in Python by Brendan Rood during the winter of 2019-2020. The game was brought to a playable state, but as Brendan was relatively new to coding, the implementation was crude.
  - The project was revised by Brendan Rood, Connor Hagen, and Jet Li in the Spring of 2024 for the Advanced Computer Security course (CS-5732) at the University of Minnesota Duluth. This version of the game was built to standalone executables, which were later uploaded to the [releases section](https://github.com/Snail51/Singularity/releases).
  - Finally, in March of 2025, Brendan ported the game to a JavaScript browser-based implementation. It is live at **https://singularity.snailien.net**.

 ## Installation Instructions (LEGACY EXECUTABLES)
  1. Install latest build from [releases section](https://github.com/Snail51/Singularity/releases).
  2. Extract archive contents.
  3. Install all included fonts. (InhumanBB.ttf)
  4. Run the included executable file "Singularity".