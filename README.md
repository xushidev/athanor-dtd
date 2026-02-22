# Downtime Activities in Avrae

This repository contains the python files for downtime activities in draconic.

## Usage

For building the alias:
- Create the modules under `DTD-modules/` you need
- Add modules and their build order in `build-order.json`
- Run the build script (`python build.py`)
- Copy paste the alias in `dist/` to your alias on avrae dashboard.

## TODO list

- [x] Money DTD
- [ ] Projects DTD
- [ ] Miscellaneous DTD
- [x] XP DTD
- [x] Implementing time based limit (using `time()` functions)   
- [x] Implementing exhaustion system
- [ ] Add tool checks for `!dtd job`
- [ ] Add multiple job types:
    - [x] Healing DTD
    - [ ] Eotorath DTD
        - [x] The actual DTD
        - [ ] Adding progress bar
- [ ] DDB friendly alias
- [ ] PTW/HRW 2.0
- [ ] All DTD into 1 alias python script

### Python script concept

The python script for the alias is supposed to do the following:
- read `build-order.json`
- figure out it's components and their build orders
- get the functions (modules) from a folder
- put them all into a few `*.alias` files under /dist folder 