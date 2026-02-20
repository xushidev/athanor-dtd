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
- [x] XP DTD
- [x] Implementing time based limit (using `time()` functions)   
- [x] Implementing exhaustion system
- [ ] Add tool checks for `!dtd job`
- [ ] Add multiple job types:
    - [ ] Healing DTD
    - [ ] Eotorath DTD
- [ ] DDB friendly alias
- [ ] PTW/HRW 2.0
- [ ] All DTD into 1 alias python script

### Python script concept

The python script for the alias is supposed to do the following:
- read `build-order.json`
- figure out it's components and their build orders
- get the functions (modules) from a folder
- put them all into a few `*.alias` files under /dist folder 