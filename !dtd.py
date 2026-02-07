<drac2>
#########################
# CONSTANTS definitions #
#########################

using(LIB="505f607f-d8cc-44bb-8a67-df5b871c95dd")

ch = character()

TIER = int(level//4.01+1)

MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
OFFSET = 9 * HOUR

TIME = floor(time() + OFFSET)

DC_INDEX = [
    8+(level//2)+proficiencyBonus,
    8+level+proficiencyBonus
]

EXHAUSTION_PROMPTS = [
    "Your body refuses to cooperate; every movement feels heavier than the last. You need a full day of rest.",
    "Fatigue dulls your senses and slows your thoughts. Today is not a day for work.",
    "You wake up sore, drained, and unfocused. Pushing yourself further would be dangerous.",
    "Your muscles ache from overuse, protesting even simple tasks.",
    "Sleep clings to you no matter how hard you try to shake it. Productivity is impossible.",
    "Your hands tremble slightly, betraying how far you've pushed yourself.",
    "You feel worn down to the bone—rest is no longer optional.",
    "Every breath feels labored, and concentration slips away almost instantly.",
    "Your body demands recovery before it allows progress.",
    "You realize too late that you've overextended yourself. Today must be spent resting.",
    "Pain and fatigue cloud your judgment. Any serious effort would end badly.",
    "Your reflexes are slow, your thoughts sluggish. You need time to recover.",
    "Even routine tasks feel overwhelming; exhaustion has caught up with you.",
    "Your stamina is spent, and your body refuses further strain.",
    "You feel hollowed out, running on fumes. Rest is the only sensible option.",
    "Your limbs feel leaden, and your mind struggles to stay focused.",
    "Ignoring your exhaustion now would risk injury or worse.",
    "You recognize the warning signs—your body needs a full day to recover.",
    "Sleep comes easily, but waking up feels just as heavy. Today must be rest.",
    "Your exhaustion is obvious to anyone who looks at you. You need time to recover."
]

SKILL_LIST = []
for (skill_name, skill) in ch.skills:
    SKILL_LIST.append(skill_name)

GOLD_INDEX = [
    {'pp': '0',   'gp': '1d2',  'sp': '1d4', 'cp': '1d8'},
    {'pp': '0',   'gp': '1d4',  'sp': '1d4', 'cp': '1d8'},
    {'pp': '0',   'gp': '1d6',  'sp': '1d4', 'cp': '2d4'},
    {'pp': '0',   'gp': '2d4',  'sp': '1d6', 'cp': '2d6'},
    {'pp': '0',   'gp': '2d6',  'sp': '1d2', 'cp': '1d4'},
    {'pp': '0',   'gp': '3d6',  'sp': '1d4', 'cp': '1d6'},
    {'pp': '0',   'gp': '4d6',  'sp': '2d4', 'cp': '2d6'},
    {'pp': '1d2', 'gp': '3d6',  'sp': '1d8', 'cp': '1d12'}
]

VALID_SKILLS1 = ["acrobatics", "athletics", "stealth"]
VALID_SKILLS2 = ["animalHandling", "deception", "intimidation", "investigation", "nature", "perception"]

COINPURSE_BEFORE = ch.coinpurse.compact_str()

RP_PROMPTS = {
    "failure": [
        "The work is finished, but something is clearly wrong—only you notice it too late.",
        "You do everything as instructed, yet the result somehow makes the situation worse.",
        "A small mistake snowballs into an awkward, public embarrassment.",
        "You misunderstand a key detail and realize it only after committing fully.",
        "The tools betray you at the worst possible moment.",
        "You complete the task, but your employer refuses to pay full wages.",
        "Your effort draws unwanted attention from the wrong people.",
        "The job technically works… but causes an unexpected side effect.",
        "Someone else takes credit for the parts you did right, leaving you blamed for the rest.",
        "You succeed too slowly, and timing ruins the outcome.",
        "The task exposes a weakness or secret you didn't mean to reveal.",
        "You finish exhausted, empty-handed, and slightly worse off than before.",
        "Your solution is clever—but impractical.",
        "The environment ruins your focus at the worst possible time.",
        "The job is done, but you're now responsible for fixing the fallout."
    ],
    "success": [
        "You complete the work exactly as requested, no more and no less.",
        "The employer nods, satisfied, and pays you without complaint.",
        "The task takes effort, but nothing goes wrong.",
        "You handle a minor complication without it becoming a problem.",
        "The job earns you quiet respect from those watching.",
        "You finish on time, with the expected outcome.",
        "Someone notices your competence, even if they say nothing.",
        "The work blends into the day—solid, reliable, forgettable.",
        "You leave the situation stable and unchanged.",
        "The tools, plan, and timing all cooperate.",
        "You meet expectations, and that's enough.",
        "The job closes one door cleanly, with no loose ends.",
        "You're paid fairly and left alone.",
        "No one questions how it was done.",
        "You feel you've earned the reward."
    ],
    "critical": [
        "You finish the job faster and better than expected.",
        "The result exceeds what was asked for—without extra effort.",
        "Your work solves an additional problem no one mentioned.",
        "The employer offers a bonus or future work.",
        "Others use your result as the new standard.",
        "Your solution is elegant, efficient, and admired.",
        "You turn a risky task into a flawless execution.",
        "Someone important hears about what you did.",
        "The job improves your reputation immediately.",
        "You gain a valuable contact, favor, or piece of information.",
        "The work creates opportunities you didn't anticipate.",
        "You make the difficult look effortless.",
        "Your name becomes associated with reliability or skill.",
        "The outcome reshapes the situation in your favor.",
        "You leave behind something that lasts.",
        "You're trusted with more responsibility next time.",
        "The success prevents future trouble.",
        "Others ask how you did it.",
        "You're remembered.",
        "The job becomes a story people tell."
    ]
}

def contract_dtd():
    #################
    # Loading cvars #
    #################

    default = dump_json(
        {
            "last_dtd": "",
            "exhaustion_streak": 0,
            "default_skill1": "",
            "default_skill2": ""
        }
    )
    athanor_dtd = load_json(ch.get_cvar("athanor_dtd", default))

    ################
    # Time checker #
    ################

    last_dtd = athanor_dtd["last_dtd"]
    before_exhaustion_streak = athanor_dtd["exhaustion_streak"]

    athanor_dtd["last_dtd"] = TIME

    if last_dtd != "":
        if (last_dtd // DAY) == (TIME // DAY):
            return 'echo You are doing 2 dtds in the same day, please try tomorrow'
        if ((TIME // DAY) - (last_dtd // DAY)) >= 2:
            athanor_dtd["exhaustion_streak"] = 0
        else:
            athanor_dtd["exhaustion_streak"] += 1

    exhaustion_streak = athanor_dtd["exhaustion_streak"]

    ###################
    # Arguments check #
    ###################

    def_skill1 = athanor_dtd["default_skill1"]
    def_skill2 = athanor_dtd["default_skill2"]

    a = LIB.numargparse(&ARGS&)
    args1 = '&2&'.lower()
    args2 = '&3&'.lower()
    no_args1 = '&' + '2' + '&'
    no_args2 = '&' + '3' + '&'

    if (args1 == no_args1 or args2 == no_args2) and (def_skill1 == "" or def_skill2 == ""):
        return 'echo Error: No input given'

    if def_skill1 != "" and def_skill2 != "":
        args1 = def_skill1
        args2 = def_skill2

    ######################
    # Skill input checks #
    ######################

    # Search for the skill that matches a valid skill, else it is 'default'
    skill1 = ([x for x,y in ch.skills if args1.lower().replace(' ','') in x.lower()]+['default'])[0]
    skill2 = ([x for x,y in ch.skills if args2.lower().replace(' ','') in x.lower()]+['default'])[0]

    if skill1 == 'default' or skill2 == 'default':
        return 'echo Error: skills given are not skills'

    if skill1 not in VALID_SKILLS1:
        return f'''echo Error: skill given is not an accepted skill
                skill given: {skill2}
                valid skills: {', '.join(VALID_SKILLS1)}'''

    if skill2 not in VALID_SKILLS2:
        return f'''echo Error: skill given is not an accepted skill
                skill given: {skill2}
                valid skills: {', '.join(VALID_SKILLS2)}'''

    athanor_dtd["default_skill1"] = skill1
    athanor_dtd["default_skill2"] = skill2

    ch.set_cvar("athanor_dtd", dump_json(athanor_dtd))

    ######################
    # Arguments for roll #
    ######################

    # Get possible advantage from the arguments
    a.set_context(1)
    adv1 = a.adv(eadv=True)
    a.set_context(2)
    adv2 = a.adv(eadv=True)

    # Get possible rerolls from arguments (halflings)
    reroll_number = ch.csettings.get("reroll", None)

    # Gets possible minimum checks from reliable talent or argument
    minimum_check1 = a.last('mc', None, int) or (10 if ch.csettings.get("talent", False) and ch.skills[skill1].prof>=1 else None)
    minimum_check2 = a.last('mc', None, int) or (10 if ch.csettings.get("talent", False) and ch.skills[skill2].prof>=1 else None)

    ########################
    # Exhaustion penalties #
    ########################

    exh_msg = ""

    if exhaustion_streak > 4 and adv1 > 1:
        exh_msg = EXHAUSTION_PROMPTS[roll("1d20")-1]
        adv1 -= 1
    
    if exhaustion_streak > 4 and adv2 > 1:
        exh_msg = EXHAUSTION_PROMPTS[roll("1d20")-1]
        adv2 -= 1

    #####################
    # Final Skill Rolls #
    #####################

    SkillRoll1 = vroll(ch.skills[skill1].d20(adv1, reroll_number, minimum_check1))
    SkillRoll2 = vroll(ch.skills[skill2].d20(adv2, reroll_number, minimum_check2))

    # Fixes animal handling for display
    if skill2 == "animalHandling":
        skill2 = "Animal Handling"
    else:
        skill2 = skill2.capitalize()

    ##########################
    # Gold & Penalties Rolls #
    ##########################

    r1_gold = 0
    r2_gold = 0

    # Checks if failed or succeeded
    if SkillRoll1.total < DC_INDEX[0]:
        # failure
        r1_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
        r1_gold -= (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
    elif SkillRoll1.total < DC_INDEX[1]:
        # success
        r1_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
    else:
        # critical success
        r1_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
        r1_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)

    if SkillRoll2.total < DC_INDEX[0]:
        # failure
        r2_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
        r2_gold -= (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
    elif SkillRoll2.total < DC_INDEX[1]:
        # success
        r2_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
    else:
        # critical success
        r2_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)
        r2_gold += (roll(GOLD_INDEX[TIER-1]["pp"]) * 10) + roll(GOLD_INDEX[TIER-1]["gp"]) + (roll(GOLD_INDEX[TIER-1]["sp"]) / 10) + (roll(GOLD_INDEX[TIER-1]["cp"]) / 100)

    ###############################
    # Finally modifying coinpurse #
    ###############################

    # if either rolls are lower than 0, then round them up to 0
    if r1_gold < 0:
        r1_gold = 0

    if r2_gold < 0:
        r2_gold = 0

    # Summing up total gold earned
    total_gold = r1_gold + r2_gold

    # If the total gold is less than 0, make it 0
    if total_gold < 0:
        total_gold = 0

    # Parsing the gold
    parsed_coins = parse_coins(f"{total_gold}", include_total=False)

    # Modifying the coinpurse
    changes = ch.coinpurse.modify_coins(**parsed_coins)

    COINPURSE_AFTER = ch.coinpurse.compact_str()

    ###################
    # RP Prompt rolls #
    ###################

    rp_msg = ""

    final_check = (SkillRoll1.total + SkillRoll2.total) // 2

    if final_check < DC_INDEX[0]:
        rp_msg = RP_PROMPTS["failure"][roll("1d15")-1]
    elif final_check < DC_INDEX[1]:
        rp_msg = RP_PROMPTS["success"][roll("1d15")-1]
    else:
        rp_msg = RP_PROMPTS["critical"][roll("1d20")-1]

    ################
    # Final Result #
    ################

    return f'''embed
                -title "Job downtime"
                -desc """**Player**: <@{ctx.author.id}> `{ctx.author.name}`
**Character**: {name} (Level {level} | Tier {TIER})

**{skill1.capitalize()}:** {SkillRoll1}
**{skill2}:** {SkillRoll2}

__**Results:**__
**Coinpurse Changes:**
{COINPURSE_BEFORE} -> {COINPURSE_AFTER} (+{total_gold:.2f}gp)
**Exhaustion Streak:**
{before_exhaustion_streak} -> {exhaustion_streak}
{exh_msg}
**Optional Roleplay Prompt:**
{rp_msg}"""
                -thumb "{ch.image}"
                -footer "!dtd job [skill1] [skill2] | Athanor | !dtd help"
            '''

def train_dtd():
    #################
    # Loading cvars #
    #################

    default = dump_json(
        {
            "last_dtd": "",
            "exhaustion_streak": 0,
            "default_skill1": "",
            "default_skill2": ""
        }
    )
    athanor_dtd = load_json(ch.get_cvar("athanor_dtd", default))

    ################
    # Time checker #
    ################

    last_dtd = athanor_dtd["last_dtd"]
    before_exhaustion_streak = athanor_dtd["exhaustion_streak"]

    athanor_dtd["last_dtd"] = TIME

    if last_dtd != "":
        if (last_dtd // DAY) == (TIME // DAY):
            return 'echo You are doing 2 dtds in the same day, please try tomorrow'
        if ((TIME // DAY) - (last_dtd // DAY)) >= 2:
            athanor_dtd["exhaustion_streak"] = 0
        else:
            athanor_dtd["exhaustion_streak"] += 1

    exhaustion_streak = athanor_dtd["exhaustion_streak"]

    ch.set_cvar("athanor_dtd", dump_json(athanor_dtd))

    ###################
    # Arguments stuff #
    ###################
    a = LIB.numargparse(&ARGS&)

    # Get possible advantage from the arguments
    a.set_context(1)
    adv1 = a.adv(eadv=True)
    a.set_context(2)
    adv2 = a.adv(eadv=True)
    a.set_context(3)
    adv3 = a.adv(eadv=True)
    ########################
    # Exhaustion penalties #
    ########################

    exh_msg = ""

    if exhaustion_streak > 4 and adv1 > 1:
        exh_msg = EXHAUSTION_PROMPTS[roll("1d20")-1]
        adv1 -= 1
    
    if exhaustion_streak > 4 and adv2 > 1:
        exh_msg = EXHAUSTION_PROMPTS[roll("1d20")-1]
        adv2 -= 1

    if exhaustion_streak > 4 and adv3 > 1:
        exh_msg = EXHAUSTION_PROMPTS[roll("1d20")-1]
        adv3 -= 1
    #########################
    # Combat Training rolls #
    #########################

    # We don't have need for additional arguments other than simply advantage and such

    # getting the highest modifier between: strength, dexterity, intelligence, wisdom and charisma
    atk_mod = max(strengthMod, dexterityMod, intelligenceMod, wisdomMod, charismaMod) + proficiencyBonus

    dice = [
        "1d20", 
        "2d20kh1",
        "3d20kh1",
        "2d20kl1",
    ]

    dice1 = dice[adv1]
    dice2 = dice[adv2]

    atk_roll1 = vroll(f"{dice1} + {atk_mod}")
    atk_roll2 = vroll(f"{dice2} + {atk_mod}")

    dex_mod = ch.saves.get("dex")
    dex_save = vroll(dex_mod.d20(adv3))

    ############
    # XP rolls #
    ############

    xp_roll1 = 0
    xp_roll2 = 0
    xp_roll3 = 0

    if atk_roll1.total < DC_INDEX[0]:
        # fail
        xp_roll1 = roll(f"{level}d4")
    elif atk_roll1.total < DC_INDEX[1]:
        # success
        xp_roll1 = roll(f"{level}d6")
    else:
        # critical success
        xp_roll1 = roll(f"{level}d8")

    if atk_roll2.total < DC_INDEX[0]:
        # fail
        xp_roll2 = roll(f"{level}d4")
    elif atk_roll2.total < DC_INDEX[1]:
        # success
        xp_roll2 = roll(f"{level}d6")
    else:
        # critical success
        xp_roll2 = roll(f"{level}d8")

    if dex_save.total < DC_INDEX[0]:
        # fail
        xp_roll3 = roll(f"{level}d4")
    elif dex_save.total < DC_INDEX[1]:
        # success
        xp_roll3 = roll(f"{level}d6")
    else:
        # critical success
        xp_roll3 = roll(f"{level}d8")

    # tier as modifier
    total = (xp_roll1 + xp_roll2 + xp_roll3) * TIER

    if total < 0:
        total = 0

    ################
    # Final Result #
    ################

    return f'''embed
                -title "Job downtime"
                -desc """**Player**: <@{ctx.author.id}> `{ctx.author.name}`
**Character**: {name} (Level {level} | Tier {TIER})

**First Attack Roll:** {atk_roll1}
**Second Attack Roll:** {atk_roll2}
**Dexterity Save**: {dex_save}

__**Results:**__
**XP gained**:
{total}XP | run `!xp +{total} 'Combat Training'` in <#1043462883062861864>
**Exhaustion Streak:**
{before_exhaustion_streak} -> {exhaustion_streak}
{exh_msg}"""
                -thumb "{ch.image}"
                -footer "!dtd train | Athanor | !dtd help"
            '''

a_type = '&1&'.lower()

if a_type == "job":
    return contract_dtd()
elif a_type == "train":
    return train_dtd()
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
</drac2>