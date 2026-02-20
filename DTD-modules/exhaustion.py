exh_msg = ""

if exhaustion_streak > 4 and adv1 > -1:
    exh_msg = EXHAUSTION_PROMPTS[roll("1d20")-1]
    adv1 -= 1

if exhaustion_streak > 4 and adv2 > -1:
    exh_msg = EXHAUSTION_PROMPTS[roll("1d20")-1]
    adv2 -= 1