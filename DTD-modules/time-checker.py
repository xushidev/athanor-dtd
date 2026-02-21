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

return (before_exhaustion_streak, exhaustion_streak, athanor_dtd)