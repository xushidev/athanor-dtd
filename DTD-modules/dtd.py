a_type = '&1&'.lower()

if a_type == "job":
    return job_dtd()
elif a_type == "train":
    return train_dtd()
elif a_type == "eoth":
    return eotorath_dtd()
elif a_type == "med":
    return med_dtd()
else:
    return f'''embed
        -title "Athanor DownTime Days (DTD) Activities"
        -desc """The DownTime Days are whatever free time the adventurers of Athanor have.
    
This time can be used to perform a few activities, such as completing a random task for the city, or completing a small job for an employer or training in general.

===
:warning: This is a currently Work In Progress (WIP) alias, please report to staff if *any* error occurs
===
**Commands**:
`!dtd job "[skill1]" "[skill2]"` - Random Job: Some people around the city might find themselves in need of a hand for a one-off job, this may include finding a lost object or commissioning. The pay is directly related to the rank of the adventurers.
> `skill1`: acrobatics, athletics, stealth.
> `skill2`: animal handling, deception, intimidation, investigation, nature, perception.

`!dtd train` - Training: As all adventurers, training is an important part of the job, hence why gathering experience from such training is important. It may simply be a training related to evading attacks to a spar.

`!dtd med "[skill1]" "[skill2]"` - Medic Job: The guild is in constant need of people for help, as the numbers of injured seems to pile up day by day, as such the guild calls upon the adventurers to help the injured people as one-off job. Of course the guild will pay based on the rank of the adventurer.
> `skill1`: medicine, nature, investigation, survival, animal handling.
> `skill2`: sleight of hand, insight, history, persuasion, perception."""
        -footer "!dtd help | Athanor"
    '''

VALID_SKILLS1 = ["medicine", "nature", "investigation", "survival", "animalHandling"]
VALID_SKILLS2 = ["sleightOfHand", "insight", "history", "persuasion", "perception"]