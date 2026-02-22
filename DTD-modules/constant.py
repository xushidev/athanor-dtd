ch = character()

ADV_TABLE = {
    1: True,
    0: None,
    -1: False
}

SKILL_LIST = []
for (skill_name, skill) in ch.skills:
    SKILL_LIST.append(skill_name)

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

COINPURSE_BEFORE = ch.coinpurse.compact_str()

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

TOOL_LIST = load_yaml(get_gvar('e65831da-1834-4089-9bbd-93fc36a2d622'))