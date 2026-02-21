exhaustion_streak, *advantages = args
exh_msg = ""
exh_list = []

for adv in advantages:
    if exhaustion_streak > 4 and adv > -1:
        exh_msg = EXHAUSTION_PROMPTS[roll("1d20")-1]
        adv -= 1
    exh_list.append(adv)

exh_list.insert(0, exh_msg)

return tuple(exh_list)