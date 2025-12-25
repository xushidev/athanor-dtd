<drac2>
#########################
# CONSTANTS definitions #
#########################

ch = character()

TIER = int(level//4.01+1)

TIME = floor(time())

a = argparse(&ARGS&)

# Get possible advantage from the arguments
adv = a.adv(boolwise=True)

DC_INDEX = [
    8+(level//2)+proficiencyBonus,
    8+level+proficiencyBonus
]

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
    if (last_dtd // 86400) == (TIME // 86400):
        return 'echo You are doing 2 dtds in the same day, please try tomorrow'
    if ((last_dtd // 86400) - (TIME // 86400)) >= 2:
        athanor_dtd["exhaustion_streak"] = 0
    else:
        athanor_dtd["exhaustion_streak"] += 1

exhaustion_streak = athanor_dtd["exhaustion_streak"]

########################
# Exhaustion penalties #
########################

exh_msg = ""

if exhaustion_streak > 4:
    exh_msg = EXHAUSTION_PROMPTS[roll("1d20")-1]
    match adv:
        case None:
            adv = False
        case True:
            adv = None
        case _:
            # do nothing (can't eadv or go below dis)
            adv = adv

#########################
# Combat Training rolls #
#########################

# We don't have need for additional arguments other than simply advantage and such

# getting the highest modifier between: strength, dexterity, intelligence, wisdom and charisma
atk_mod = max(strengthMod, dexterityMod, intelligenceMod, wisdomMod, charismaMod) + proficiencyBonus

dice = "1d20"
if adv:
    dice = "2d20kh1"
elif adv == False:
    dice = "2d20kl1"
else:
    dice = "1d20"

atk_roll1 = vroll(f"{dice} + {atk_mod}")
atk_roll2 = vroll(f"{dice} + {atk_mod}")

dex_mod = ch.saves.get("dex")

dex_save = vroll(dex_mod.d20(adv))

############
# XP rolls #
############




</drac2>