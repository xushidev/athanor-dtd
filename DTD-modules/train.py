#################
# Loading cvars #
#################

athanor_dtd = cvar_loader()

################
# Time checker #
################

before_exhaustion_streak, exhaustion_streak, athanor_dtd = time_checker(athanor_dtd)

###################
# Arguments stuff #
###################
a = LIB.numargparse(&ARGS&)

# Get possible advantage and bonus from the arguments
a.set_context(1)
bonus1 = a.get("b", 0)
adv1 = a.adv(eadv=True)
a.set_context(2)
bonus2 = a.get("b", 0)
adv2 = a.adv(eadv=True)
a.set_context(3)
bonus3 = a.get("b", 0)
adv3 = a.adv(eadv=True)

########################
# Exhaustion penalties #
########################

exh_msg, adv1, adv2, adv3 = exhaustion_penalties(exhaustion_streak, adv1, adv2, adv3)

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
dice3 = dice[adv3]

if bonus1 == 0:
    atk_roll1 = vroll(f"{dice1} + {atk_mod}")
else:
    bonuses = ""
    for bonus in bonus1:
        bonuses += "+" + bonus
    atk_roll1 = vroll(f"{dice1} + {atk_mod} {bonuses}")

if bonus2 == 0:
    atk_roll2 = vroll(f"{dice2} + {atk_mod}")
else:
    bonuses = ""
    for bonus in bonus2:
        bonuses += "+" + bonus
    atk_roll2 = vroll(f"{dice2} + {atk_mod} {bonuses}")

dex_mod = ch.saves.get("dex")

if bonus3 == 0:
    dex_save = vroll(f"{dice3} + {dexterityMod}")
else:
    bonuses = ""
    for bonus in bonus3:
        bonuses += "+" + bonus
    dex_save = vroll(f"{dice3} + {dexterityMod} {bonuses}")

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

########################
# Coin Purse Deduction #
########################

changes = ch.coinpurse.modify_coins(gp=int(-level))

COINPURSE_AFTER = ch.coinpurse.compact_str()

################
# Final Result #
################

return f'''embed
            -title "Downtime Activity: Train"
            -desc """**Player**: <@{ctx.author.id}> `{ctx.author.name}`
**Character**: {name} (Level {level} | Tier {TIER})

**First Attack Roll:** {atk_roll1}
**Second Attack Roll:** {atk_roll2}
**Dexterity Save**: {dex_save}

__**Results:**__
**Coinpurse Changes:**
{COINPURSE_BEFORE} -> {COINPURSE_AFTER} (-{level:.2f}gp)
**XP gained**:
{total}XP | run `!xp +{total} 'Combat Training'` in <#1043462883062861864>
**Exhaustion Streak:**
{before_exhaustion_streak} -> {exhaustion_streak}
{exh_msg}"""
            -thumb "{ch.image}"
            -footer "!dtd train | Athanor | !dtd help"
        '''