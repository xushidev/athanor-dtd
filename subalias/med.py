<drac2>

# LIBRARIES
# Arguments, tools, progress bar
using(arguments="505f607f-d8cc-44bb-8a67-df5b871c95dd")
using(tool="6251e20c-7545-4c63-92af-31e0745f2b0c")
using(progress_bar="505f607f-d8cc-44bb-8a67-df5b871c95dd")

# Gets the character
ch = character()

# Gets a list of skills and tools
skills_list = [skill_name for (skill_name, skill) in ch.skills if skill_name not in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']]
tools_list = load_yaml(get_gvar('e65831da-1834-4089-9bbd-93fc36a2d622'))

global_args = arguments.numargparse(&ARGS&)

# Gets the tier of the character
tier = global_args.get("level", int(ch.levels.total_level//4.01+1))

# Gets the current time in Japan (+9 hours)
MINUTE = 60
HOUR = 60 * MINUTE
DAY = 24 * HOUR
OFFSET = 9 * HOUR
TIME = floor(time() + OFFSET)

# Gold reward table
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

# Coinpurse before alias completion
pre_coins = ch.coinpurse.compact_str()

# Default athanor_dtd cvar to use
better_default = dump_json(
    {
        "last_dtd": 0,
        "exhaustion_streak": 0,
        "med_args": [],
        "job_args": [],
        "train_args": [],
        "eoth_args": []
    }
)
athanor_dtd = load_json(ch.get_cvar("athanor_dtd", better_default))

valid_skills = {
    "job": [
        ["acrobatics", "athletics", "stealth"],
        ["animalHandling", "deception", "intimidation", "investigation", "nature", "perception"]
    ],
    "med": [
        ["medicine", "nature", "investigation", "survival", "animalHandling"],
        ["sleightOfHand", "insight", "history", "persuasion", "perception"]
    ],
    "eoth": [
        ["carpenterstools", "masonstools", "glassblowerstools", "weaverstools", "cooksutensils", "herbalismkit"],
        ["persuasion", "medicine", "animalHandling", "nature", "arcana", "athletics"]
    ]
}

# Checks if no arguments is given:
args1 = '&1&'.lower()
args2 = '&2&'.lower()
no_args1 = '&' + '1' + '&'
no_args2 = '&' + '2' + '&'

def get_random_job_rp(final_check):
    # Prompt for roleplay
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
    # Returns a roleplay prompt depending on the level of success
    if final_check < (8+(global_args.get("level", level)//2)+proficiencyBonus):
        return RP_PROMPTS["failure"][roll("1d15")-1]
    elif final_check < (8+(global_args.get("level", level))+proficiencyBonus):
        return RP_PROMPTS["success"][roll("1d15")-1]
    else:
        return RP_PROMPTS["critical"][roll("1d20")-1]

def get_random_med_rp(final_check):
    # Prompt for roleplay
    RP_PROMPTS = {
        "failure": [
            "...You realised too late that you forgot to wash your hands before applying the bandages, now you have to wash it and do it again, properly this time.",
            "Despite the patient's wishes, you continued the procedure, as painful as it sounds and looks.",
            "You underestimated your strength and tightened the bandage too much.",
            "You were too fast and did everything before anyone realised it happened, the patient magically healed and you were never acknowledged for your works.",
            "The tools betray you at the worst possible moment.",
            "The lack of money leaves you with little pay, as you had to do beneficiary work.",
            "Your effort are null as they didn't seem to work despite following the right procedures.",
            "The job technically worked, but not in the way anyone would consider a success.",
            "Someone else speaks first and takes credit, leaving you to explain what went wrong.",
            "You finish just a little too late, and that small delay makes all the difference.",
            "In trying to help, you reveal something you would have preferred to keep private.",
            "You complete the task, but the effort leaves you worse than when you started.",
            "Your idea makes sense on paper, yet falls apart the moment you apply it pratically.",
            "A small distraction breaks your concentration, and the mistake follows immediately.",
            "You do what was asked, only to be told you should have known better.",
            "You are fined slightly for a work done wrongly, you are lucky no life has been taken.",
            "You thought everything was going alright, but a professional comes and points out your mistakes.",
            "Where is your cap to prevent sweat from falling down?",
            "You talked... And talked... And talked... And the old lady left without doing anything, feeling better, but of course you didn't get paid for talking",
            "You inspire someone and pull them out from a dark mentality. But nobody acknowledges your effort.",
            "You run swiftly from a patient to another... And bump into someone.",
            "You bump into someone running too fast in the opposite direction."
        ],
        "success": [
            "You follow the correct steps, and this time they work as intended.",
            "The patient endures, and the procedure concludes without further complication.",
            "You keep a steady hand, and nothing slips out of place, fortunately.",
            "The tools cooperate, and that alone makes the difference.",
            "You finish without attracting attention, which is sometimes the best outcome.",
            "The employer pays you what was agreed, nothing more, nothing less.",
            "No one complains, and that is taken as approval.",
            "You correct a small mistake before it becomes visible on the patient.",
            "You leave the situation stable, if not improved.",
            "Your timing is precise enough to avoid further trouble.",
            "You feel the work was done properly, even if unnoticed.",
            "The result holds... at least for now.",
            "You are allowed to leave without questions.",
            "The process hurts, but it heals.",
            "You did what you were meant to do.",
            "The wounds is closed perfectly, nothing more and nothing less.",
            "A depressed person leaves you a tip as your speech with them leaves them much more willing to push on with life.",
            "You distract a patient enough for the medic to carry on a painful procedure.",
            "...You are left to write down all the informations about patients and which medicine to use in which condition."
        ],
        "critical": [
            "You anticipate the complication before it happens and adjust accordingly.",
            "The procedure succeeds so cleanly that no correction is needed.",
            "You fix an issue no one realised was there.",
            "The employer offers more work, trusting your steady hands, which means a bigger pay.",
            "Word spreads quietly about how well it went.",
            "Your method proves more efficient than expected.",
            "You turn a delicate situation into a controlled one.",
            "Someone important in the guild notices the precision of your work.",
            "The result lasts longer than anyone predicted.",
            "You gain the trust that is rarely given twice.",
            "The outcome prevents future problems before they arise.",
            "You make it look easier than it was.",
            "Your name is mentioned with respect and gratitude by the patient's family afterward.",
            "You leave behind something that will not need fixing for a while.",
            "You will be trusted with something more difficult next time.",
            "The recovery is faster than it should have been.",
            "Others ask how you managed to do it.",
            "You will be remembered for doing it right.",
            "The success feels earned.",
            "You feel warm in your chest watching the smile of your patient.",
            "The patient seems magically healed and you take the credit for it despite never doing anything",
            "The job becomes proof of your competence.",
            "Someone won't miss their family, you broke a circle of death by incompetence.",
            "A kind smile inspires you to keep up with the good work.",
            "A kid's laughter fills your ears with joy and happiness.",
            "'I want to see the sky one more time... I want to feel the rays of the sun one more time...' . . . 'Thank you. Kind person. You did the right thing.'",
            "A burning sense of duty fills, as you watch over the tent filled with despair. You feel the need to fill it with HOPE"
        ]
    }
    # Returns a roleplay prompt depending on the level of success
    if final_check < (8+(global_args.get("level", level)//2)+proficiencyBonus):
        return RP_PROMPTS["failure"][roll("1d22")-1]
    elif final_check < (8+(global_args.get("level", level))+proficiencyBonus):
        return RP_PROMPTS["success"][roll("1d19")-1]
    else:
        return RP_PROMPTS["critical"][roll("1d27")-1]

def get_random_exhaustion_rp():
    if exhaustion():
        # Prompt for exhaustion
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
        # Returns a random prompt for exhaustion depending on the exhaustion streak
        exhaustion_message = "\n**Exhaustion:**\n"
        return exhaustion_message + EXHAUSTION_PROMPTS[roll("1d20")-1]
    else:
        return ""

def exhaustion():
    # check exhaustion, returns True or False depending on exhaustion streak
    if athanor_dtd["exhaustion_streak"] >= 4:
        return True
    return False

def roll_gold():
    gold = GOLD_INDEX[tier - 1]
    return (
        roll(gold["pp"]) * 10
        + roll(gold["gp"])
        + roll(gold["sp"]) / 10
        + roll(gold["cp"]) / 100
    )

def calculate_gold(skill_roll):
    if skill_roll.total < (8+(global_args.get("level", level)//2)+proficiencyBonus):
        # failure
        return roll_gold() - roll_gold()
    elif skill_roll.total < (8+(global_args.get("level", level))+proficiencyBonus):
        # success
        return roll_gold()
    else:
        # critical success
        return roll_gold() + roll_gold()

def calculate_xp(result_roll):
    die = (
            4 if result_roll.total < (8+(global_args.get("level", level)//2)+proficiencyBonus)
            else 6 if result_roll.total < (8+(global_args.get("level", level))+proficiencyBonus)
            else 8
        )
    return roll(f"{global_args.get('level', level)}d{die}")

# Downtime Activities available
def med_dtd():
    # Variable to store the arguments given
    local_args = athanor_dtd.copy()

    # Get exhaustion before alias running
    pre_exhaustion = local_args["exhaustion_streak"]

    # Check time and add exhaustion to local_args
    if ((TIME // DAY) - (int(local_args["last_dtd"]) // DAY)) >= 2:
        local_args["exhaustion_streak"] = 0
    else:
        local_args["exhaustion_streak"] += 1

    # Get exhaustion after alias running
    post_exhaustion = local_args["exhaustion_streak"]

    # Log this as the last DTD done after having checked for exhaustion
    local_args["last_dtd"] = TIME

    # Parse arguments with context
    args = arguments.numargparse(&ARGS&)

    # Check if any inputs are given,
    # if we already have them, we use that
    # else it is error
    if (args1, args2) == (no_args1, no_args2):
        # If no skills are given, then we check the defaults
        if len(athanor_dtd["med_args"]) != 0:
            # If there are defaults, we use defaults (assume they are valid)
            args1, args2 = athanor_dtd["med_args"][0]
            skill1_arg, skill2_arg = athanor_dtd["med_args"][1]
            bonus1, adv1 = skill1_arg
            bonus2, adv2 = skill2_arg
        else:
            # If we don't have skills given and defaults, then it is an error
            return "echo Error: No input given"
    else:
        # If we have skills given by user
        # Gets the bonuses / advantages for 1st skill
        args.set_context(1)
        bonus1, adv1 = args.get("b", 0), args.adv()

        # Gets the bonuses / advantages for 2nd skill
        args.set_context(2)
        bonus2, adv2 = args.get("b", 0), args.adv()
        # dis = -1, None = 0, adv = 1, eadv = 2

        # Stores them as tuple for easy deconstruction
        local_args["med_args"] = []

        # Check if they are valid or not before writing
        # Search the exact skills in the arguments
        args1 = ([x for x in skills_list if args1.lower().replace(' ', '') in x.lower()]+["default"])[0]
        args2 = ([x for x in skills_list if args2.lower().replace(' ', '') in x.lower()]+["default"])[0]

        # Checks if any of the arguments is "default"
        if {args1, args2} == {"default"}:
            return "echo Error: Invalid input"

        # Checks if the argument is in the valid skills
        if (args1 not in valid_skills["med"][0]) or (args2 not in valid_skills["med"][1]):
            return "echo Error: Invalid skill input"

        # If it passes all the checks above, add them to the default arguments
        local_args["med_args"].extend([(args1, args2), ((bonus1, adv1), (bonus2, adv2))])

        # Write new variables in cvar
        ch.set_cvar("athanor_dtd", dump_json(local_args))

    # Get eventual rerolls from character (Halfling)
    reroll_number = ch.csettings.get("reroll", None)

    # Get reliable taleng or mc
    minimum_check1 = args.last('mc', None, int) or (10 if ch.csettings.get("talent", False) and ch.skills[args1].prof>=1 else None)
    minimum_check2 = args.last('mc', None, int) or (10 if ch.csettings.get("talent", False) and ch.skills[args2].prof>=1 else None)

    # Check for exhaustion and apply
    if exhaustion():
        # apply exhaustion
        adv1 -= 1
        adv2 -= 1
        adv1 = -1 if adv1 < -1 else adv1
        adv2 = -1 if adv2 < -1 else adv2

    # Roll the skills checks
    # Table to convert advantage:
    adv_table = {
        1: True,
        0: None,
        -1: False
    }

    # Roll the skill checks along with bonus
    if bonus1 == 0:
        skill_roll1 = vroll(ch.skills[args1].d20(adv_table[adv1], reroll_number, minimum_check1))
    else:
        bonuses = ""
        for bonus in bonus1:
            bonuses += "+" + bonus
        skill_roll1 = vroll(f"{ch.skills[args1].d20(adv_table[adv1], reroll_number, minimum_check1)} {bonuses}")

    if bonus2 == 0:
        skill_roll2 = vroll(ch.skills[args2].d20(adv_table[adv2], reroll_number, minimum_check2))
    else:
        bonuses = ""
        for bonus in bonus2:
            bonuses += "+" + bonus
        skill_roll2 = vroll(f"{ch.skills[args2].d20(adv_table[adv2], reroll_number, minimum_check2)} {bonuses}")

    # Roll the gold reward
    gold_roll1 = calculate_gold(skill_roll1)
    gold_roll2 = calculate_gold(skill_roll2)

    # Fix gold if it is less than 0
    gold_roll1 = 0 if gold_roll1 < 0 else gold_roll1
    gold_roll2 = 0 if gold_roll2 < 0 else gold_roll2

    # Parse the gold for avrae
    parsed_gold = parse_coins(f"{gold_roll1 + gold_roll2}", include_total=False)

    # Modify the coin purse and get the delta
    changes = ch.coinpurse.modify_coins(**parsed_gold)

    # Get the coinpurse after alias completion
    post_coins = ch.coinpurse.compact_str()

    # Return embed result
    return f'''embed
            -title "Downtime Activity: Medic"
            -desc """**Player**: <@{ctx.author.id}> `{ctx.author.name}`
**Character**: {name} (Level {(global_args.get("level", level))} | Tier {tier})

**{args1.capitalize() if args2 != "animalHandling" else "Animal Handling"}:** {skill_roll1}
**{args2.capitalize() if args2 != "sleightOfHand" else "Sleight of Hand"}:** {skill_roll2}

__**Results:**__
**Coinpurse Changes:**
{pre_coins} -> {post_coins} (+{(gold_roll1 + gold_roll2):.2f}gp)
**Exhaustion Streak:**
{pre_exhaustion} -> {post_exhaustion}

**Optional Roleplay Prompt:**
{get_random_med_rp(((skill_roll1.total + skill_roll2.total)//2))}{get_random_exhaustion_rp()}"""
            -thumb "{ch.image}"
            -footer "!dtd med [skill1] [skill2] | Athanor | !dtd help"
        '''

# Check if it is using the old cvar or not, if it is, we update to the new schema
if athanor_dtd.get("default_skill1") != None:
    leg_last_dtd = athanor_dtd["last_dtd"]
    leg_exhaustion_streak = athanor_dtd["exhaustion_streak"]

    # Transfer old data
    new_schema = dump_json(
        {
            "last_dtd": leg_last_dtd,
            "exhaustion_streak": leg_exhaustion_streak,
            "med_args": [],
            "job_args": [],
            "train_args": [],
            "eoth_args": []
        }
    )

    # Write update to cvar
    ch.set_cvar("athanor_dtd", new_schema)

    # Update
    athanor_dtd = load_json(ch.get_cvar("athanor_dtd", better_default))

# Check the time, returns error directly if trying to do DTDs before reset.
if athanor_dtd["last_dtd"] != "":
    if (athanor_dtd["last_dtd"] // DAY) == (TIME // DAY):
        return f'echo You are doing 2 dtds in the same day, please try again tomorrow'

return med_dtd()

</drac2>
