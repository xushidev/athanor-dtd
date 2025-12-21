# Downtime Activities in Avrae

This repository contains the python files for downtime activities in draconic.

## !alifestyle

The `!alifestyle.py` file contains the script in draconic for the `!alifestyle` command, which creates the necessary counters for downtime activities, though it is currently not used by the other commands.

## !job

The `!job.py` file contains the script in draconic for the `!MONEY` command, it takes in two skills and is limited to be used once a day and carries a built-in exhaustion system so that players shouldn't use it everyday and take a break every 5 days at the very least.

## TODO list

- [x] Money DTD 
- [ ] Projects DTD   
- [ ] Miscellaneous DTD   
- [ ] XP DTD   
- [x] Implementing time based limit (using `time()` functions)   
- [x] Implementing exhaustion system   

### TODO list:
#### Money DTD:
- [x] Skills rolls   
- [x] Gold rolls (per tier)   
- [x] Coinpurse changes   
- [x] Exhaustion streak system   
- [x] RP prompt   

#### Projects DTD:
- [ ] Project name + DC input implementation   
- [ ] Skill input   
- [ ] Skill rolls   
- [ ] Exhaustion streak system   

#### Miscellaneous DTD:
- [ ] Input (reason for searching, what is doing, etc...)  
- [ ] Defining what skills to use (investigation, perception, survival, etc...)  
- [ ] Assistant role ping  
- [ ] Exhaustion streak system   

#### XP DTD:
- [ ] Defining what skills / atk rolls etc... to use   
- [ ] Skill rolls  
- [ ] XP rolls per tier  
- [ ] XP log add  
- [ ] Exhaustion streak system  