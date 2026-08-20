**Eotorath Repair Job:** Within the dangerous land of Eotorath, the expeditionary force's campaign of liberation marches on! Foot by foot wrested back from the shadow of the Youkais! However, liberation alone isn't enough. 

The land itself lies scarred, its people haunted, and the human village left struggling to rebuild in the wake of destruction.

Now, a new effort has begun, an initiative to help revitalize the village and the land as a whole, speeding their recovery and giving those who call Eotorath home a real chance to heal and rebuild their lives!

**Command:**
`!dtd eoth "[tool]" "[skill]" -choice "[section]" [options...]`

**Available Choices:**
`tool`: Carpenters Tools, Masons Tools, Glassblowers Tools, Weavers Tools, Cooks Utensils, Herbalism Kit
`skill`: Persuasion, Medicine, Animal Handling, Nature, Arcana, Athletics
`section`: The name of the section you are repairing (this is required and the options available are in initiative)

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
`!dtd eoth "Carpenters Tools" "Medicine" -choice "city 1" -b1 1 -b 1`
For the next time: `!dtd eoth -choice "city 1"`
