<drac2>
def add_section():
    # Get the combat channel
    combat_channel = combat()

    # Error if channel is not in combat
    if combat_channel is None:
        return "echo Error: channel not in combat"

    # Arguments
    args1 = '&2&'
    args2 = '&3&'
    no_args1 = '&' + '2' + '&'
    no_args2 = '&' + '3' + '&'

    # Gets checks if all arguments are given
    if (args1, args2) == (no_args1, no_args2):
        return "echo Error: no input given"

    try:
        args2 = int(args2)
    except:
        return "echo Error: input error"

    # args1 = "sect_name"
    # args2 = "dc"
    sections = load_json(combat_channel.get_metadata("sections", []))
    sections.append(args1)

    section = {
        "dc": args2,
        "progress": 0
    }

    # Finally set all the metadata in the combat
    combat_channel.set_metadata("sections", dump_json(sections))
    combat_channel.set_metadata(args1, dump_json(section))
    return f"echo Successfully added {args1} section with DC {args2}"

def remove_section():
    # Get the combat channel
    combat_channel = combat()

    # Error if channel is not in combat
    if combat_channel is None:
        return "echo Error: channel not in combat"

    # Arguments
    args1 = '&2&'
    no_args1 = '&' + '2' + '&'

    # Gets checks if all arguments are given
    if args1 == no_args1:
        return "echo Error: no input given"

    # Check the section for empty
    sections = load_json(combat_channel.get_metadata("sections"))

    if sections is None:
        return "echo Error: sections empty"

    # fuzzy search section
    choice = ([x for x in load_json(combat_channel.get_metadata("sections")) if args1.lower().replace(' ', '') in x.lower()])[0]

    if choice is None:
        return "echo Error: section not found"

    sections.remove(choice)

    # Finally set all the metadata in the combat
    combat_channel.set_metadata("sections", dump_json(sections))
    combat_channel.delete_metadata(args1)
    return f"echo Successfully removed {choice}"

def modify_dc():
    # Get the combat channel
    combat_channel = combat()

    # Error if channel is not in combat
    if combat_channel is None:
        return "echo Error: channel not in combat"

    # Arguments
    args1 = '&2&'
    args2 = '&3&'
    no_args1 = '&' + '2' + '&'
    no_args2 = '&' + '3' + '&'

    # Gets checks if all arguments are given
    if (args1, args2) == (no_args1, no_args2):
        return "echo Error: no input given"

    try:
        args2 = int(args2)
    except:
        return "echo Error: input error"

    # Fuzzy search the section
    choice = ([x for x in load_json(combat_channel.get_metadata("sections")) if args1.lower().replace(' ', '') in x.lower()])[0]

    if choice is None:
        return "echo Error: section does not seem to exist"

    section = load_json(combat_channel.get_metadata(choice))
    pre_dc = section["dc"]
    section["dc"] = args2
    post_dc = section["dc"]
    combat_channel.set_metadata(choice, dump_json(section))
    return f"echo Successfully modified {choice} section DC from {pre_dc} to {post_dc}"


args = '&1&'

if args == "add":
    return add_section()
elif args == "remove":
    return remove_section()
elif args == "edit":
    return modify_dc()
else:
    return '''echo Eotorath section editor:
- `!eoth add "section_name" "section_dc"`
- `!eoth edit "section_name" "section_dc"`
- `!eoth remove "section_name"`'''

</drac2>
