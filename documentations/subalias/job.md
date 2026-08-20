**Odd Jobs:** Some people around the city might find themselves in need of a hand for a one-off job, this may include finding a lost object or commissioning.
The possibilites for an odd job is endless as people constantly find themselves in necessity of something.

The pay is directly related to the rank of the adventurers, as people tend to pay you more seeing your rank.

**Command:**
`!dtd job "[skill1]" "[skill2]" [options...]`

**Available Skills:**
`skill1`: Acrobatics, Athletics, Stealth
`skill2`: Animal Handling, Deception, Intimidation, Investigation, Nature, Perception

**Additional Options:**
`adv`: gives advantage to all rolls
`dis`: gives disadvantage to all rolls
`-b "[number]"`: gives a bonus equal to the number to all rolls

**Roll Specific Options:**
If you are in need of giving advantage, disadvantage or a bonus only to one of the rolls, there is a simple way to do that:
Simply add the number of the roll you want to give the bonus or advantage as such: `adv1` or `-b1` for the first roll

**Saved Arguments:**
Once you run the command, it remembers your last choices (including past arguments), if you want to change them you will have to input them and run the command again.
*Example*:
`!dtd job "acrobatic" "deception" -b1 1 -b 1`
For the next time: `!dtd job`
