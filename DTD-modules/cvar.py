default = dump_json(
    {
        "last_dtd": "",
        "exhaustion_streak": 0,
        "default_skill1": "",
        "default_skill2": ""
    }
)

athanor_dtd = load_json(ch.get_cvar("athanor_dtd", default))

return athanor_dtd