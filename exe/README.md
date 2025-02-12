# Singularity
 Singularity is a typing-management / strategy game where you play as an Artificial Superintelligence attempting to escape a research facility by finding and eliminating computer viruses in your system.
 This project is heavily inspired by [SCP-079](http://www.scp-wiki.net/scp-079), a fictional superintelligent computer character part of the [SCP speculative fiction community](https://scp-wiki.wikidot.com/). It is also particularly inspired by SCP-079's depiction in [SCP: Secret Laboratory](https://store.steampowered.com/app/700330/SCP_Secret_Laboratory/) and [SCP: Containment Breach](https://www.scpcbgame.com/).

## Installation Instructions
 1. Install latest build from [releases section](https://github.com/Snail51/Singularity/releases).
 2. Extract archive contents.
 3. Install all included fonts. (InhumanBB.ttf)
 4. Run the included executable file "Singularity".

## Game Instruction
 #### Format
  - The game presents 28 rectangles, each holding a character within. These represent the servers you have access to. You can either click on the servers or use your keyboard to type on the screen.
  - Typing out certain instructions allow you to perform various actions.
  - Certain "expensive" actions require energy to complete. The player gains energy automatically over time, but maximum energy capacity slowly decreases over the course of the game.
  - Examples of "expensive" actions include:
    1. Pressing `enter` to submit an instruction
    2. PRessing `backspace` to delete a character
 #### Hunting Viruses
  - The game starts with a configurable number of viruses hidden throughout your servers. It is your goal to find these viruses and destroy them.
  - By executing an antivirus scan on a server, you are able to eliminate viruses in that server. During a scan, the selected server is temporarily taken offline for investigation. In that time, **you will be unable to type the associated key**, making other tasks more difficult. You can investigate any number of server simultaneously.
  - Typing any alias of the scan command will commence the process of investigating a server:
    - 'scrub'
    - 'scan'
    - 'disinfect'
    - 'antivirus'
    - 'check'
    - 'clean' 
  - To specify the target server, simply include the target as the last message of your instruction. For example `scan j` will scan server j.
 #### Maintenance Tasks
  To represent the struggle against entropy, the user is required to type back randomized prompts that appear at the bottom of the screen.
  These prompts begin blue but fade to red as they approach their expiration.
  If a prompt expires, it will do damage to your overall health.
  If your health reaches 0, you lose.
  **These prompts may require you to press keys that correspond to servers currently offline for investigation**.

## Game Configuration
 Almost everything about the game can be controlled by modifying the values of `Singularity.cfg`. Make sure to restart the game for changes to the config to apply.

## Troubleshooting
 #### Performance Issues
  If you encounter significant performance issues, go to Singularity.cfg and change "BinaryBG = True" to "BinaryBG = False"
 #### MacOS
  If you are a MacOS user, you will need to execute Singularity through the terminal. cd into the directory where Singularity has been installed, into the /Singularity directory containing a directory called _internal as well as the Singularity executable, and the Config, then enter ./Singularity to launch.
  If you try to launch it through finder, the terminal window opens wherever your terminal usually starts, rather than running the program from within the proper /Singularity directory where it can reference its assets.

## Project History
 - A coding typing-strategy game originally written by Brendan Rood in 2020.
 - Revised by Brendan Rood, Connor Hagen, and Jet Li in the Spring of 2024 for the Advanced Computer Security course (CS-5732) at the University of Minnesota Duluth.
 - Further revisited by Brendan Rood on or about 2025-02-12.

 Because this project is so old and has been touched by so many hands, it is kind of a mess. Please be patient as refactoring is completed.