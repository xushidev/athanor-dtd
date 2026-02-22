a_type = '&1&'.lower()

if a_type == "job":
    return job_dtd()
elif a_type == "train":
    return train_dtd()
elif a_type == "eoth":
    return eotorath_dtd()
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
`!dtd train` - Training: As all adventurers, training is an important part of the job, hence why gathering experience from such training is important. It may simply be a training related to evading attacks to a spar.

`skill1`: acrobatics, athletics, stealth.
`skill2`: animal handling, deception, intimidation, investigation, nature, perception."""
        -footer "!dtd help | Athanor"
    '''