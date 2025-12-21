<drac2>
# Arguments and constants
args = argparse(&ARGS&)
lifestyle = '&1&'.lower()
ch = character()
lifestyle_list = {
    "squalid": "-1gp",
    "poor": "-2gp",
    "modest": "-7gp",
    "comfortable": "-14gp",
    "wealthy": "-28gp",
    "aristocratic": "-56gp"
    }
no_args = '&' + '1' + '&'

# Default values from cvars
default = dump_yaml({"lifestyle": ""})
default_lifestyle = load_yaml(ch.get_cvar("lifestyle", default))

# Returns error if lifestyle and defaults aren't set.
if lifestyle == no_args and default_lifestyle["lifestyle"] == '':
    return f'echo You have to choose a lifestyle!'

# If there is a default and no argument were given, sets the lifestyle as default
if lifestyle == no_args:
    lifestyle = default_lifestyle["lifestyle"]

# Checks if the lifestyle exists in the available lifestyle lists
if lifestyle not in lifestyle_list.keys():
    return f'echo {lifestyle} is not a valid lifestyle!'

# Gets the previous values of DTDs
if ch.cc_exists("DTDs"):
    cc_before = ch.cc("DTDs").value
else:
    cc_before = 0

# If DTDs counter doesn't exists, then we create a new DTDs counter
ch.create_cc_nx("DTDs", "0", "5", "none", "bubble", None, None, None, None, None)

# We parse the coins that the lifestyle uses
parsed_coins = parse_coins(lifestyle_list[lifestyle])

# We then get the status of the coinpurse before deduction...
coins_before = ch.coinpurse.compact_str()

# We modify the coinpurse
changes = ch.coinpurse.modify_coins(parsed_coins["pp"], parsed_coins["gp"], parsed_coins["ep"], parsed_coins["sp"], parsed_coins["cp"])

# ...and after
coins_after = ch.coinpurse.compact_str()

# Gets the value of after the DTDs
cc_after = ch.cc("DTDs").set("5", True)

# We remember the value of the lifestyle command (we can change this to ARGS)
default_lifestyle["lifestyle"] = lifestyle

# We set the value to the cvar
ch.set_cvar("lifestyle", dump_yaml(default_lifestyle))

# We retake value of the lifestyle (somehow setting the cvar removes the original value)
lifestyle = '&1&'.lower()
if lifestyle == no_args:
    lifestyle = default_lifestyle["lifestyle"]

# We display everything in an embed
return f'''embed 
                -title "Lifestyle Log" 
                -desc """**Player**: <@{ctx.author.id}> `{ctx.author.name}`
                **Character**: {name}
                **Lifestyle**: {lifestyle.capitalize()}

                **Required Payment**: {lifestyle_list[lifestyle].strip("-")}
                **{ch.cc("DTDs").name}**
                {ch.cc("DTDs").full_str()} (+{cc_after - cc_before})

                **Coinpurse Changes (Payment Automated)**
                {coins_before} -> {coins_after} ({lifestyle_list[lifestyle]})"""
                -thumb "{ch.image}"
                -footer "Athanor"
                '''
</drac2>