**Training:** Outside the regular housing, Adventurer's Guild also offers training programs to adventurers.
With some fee depending on your current experience, you may access to these programs leaded by trained personnel and other adventurers to hone your skills without worrying about perilous missions.

**Command:**
`!dtd train [options...]`

**Additional Options:**
`adv`: gives advantage to all rolls
`dis`: gives disadvantage to all rolls
`-b "[number]"`: gives a bonus equal to the number to all rolls
`none`: removes all other arguments

**Roll Specific Options:**
If you are in need of giving advantage, disadvantage or a bonus only to one of the rolls, there is a simple way to do that:
Simply add the number of the roll you want to give the bonus or advantage as such: `adv1` or `-b1` for the first roll

**Saved Arguments:**
Once you run the command, it remembers your last choices (including past arguments), if you want to change them you will have to input them and run the command again. If you want to remove them you will have to add the `none` argument.
*Example*:
`!dtd train adv dis1`
For the next time: `!dtd train`
To remove: `!dtd train none`
