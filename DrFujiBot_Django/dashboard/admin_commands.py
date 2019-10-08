from .models import Setting, Command, SimpleOutput

def handle_setgame(args):
    output = ''
    return output

def handle_addcom(args):
    output = ''
    command_name = args[0]
    simple_output_text = ' '.join(args[1:])

    if not command_name.startswith('!'):
        return 'Command must start with "!"'

    if len(simple_output_text) > 5000:
        return 'Command output too long (over 5000 characters)'

    command_matches = Command.objects.filter(command__iexact=command_name)
    if len(command_matches) == 0:
        simple_output = SimpleOutput(output_text=simple_output_text)
        simple_output.save()

        command = Command(command=command_name, output=simple_output)
        command.save()

        output = 'Command "' + command_name + '" successfully created'
    else:
        output = 'Command "' + command_name + '" already exists'
    return output

def handle_delcom(args):
    output = ''
    command_name = args[0]

    if not command_name.startswith('!'):
        return 'Command must start with "!"'

    command_matches = Command.objects.filter(command__iexact=command_name)
    if len(command_matches) == 1:
        command_matches[0].delete()
        output = 'Command "' + command_name + '" successfully deleted'
    else:
        output = 'Command "' + command_name + '" not found'
    return output

def handle_editcom(args):
    output = ''
    command_name = args[0]
    simple_output_text = ' '.join(args[1:])

    if not command_name.startswith('!'):
        return 'Command must start with "!"'

    if len(simple_output_text) > 5000:
        return 'Command output too long (over 5000 characters)'

    command_matches = Command.objects.filter(command__iexact=command_name)
    if len(command_matches) == 1:
        simple_output = command_matches[0].output
        simple_output.output_text = simple_output_text
        simple_output.save()

        command = Command(command=command_name, output=simple_output)
        command.save()

        output = 'Command "' + command_name + '" successfully modified'
    else:
        output = 'Command "' + command_name + '" not found'
    return output

def handle_alias(args):
    output = ''
    existing_command_name = args[0]
    new_command_name = args[1]

    if not new_command_name.startswith('!'):
        return 'New command must start with "!"'

    existing_command_matches = Command.objects.filter(command__iexact=existing_command_name)
    found = (len(existing_command_matches) == 1)

    if not found:
        # Try reversing the order
        temp = existing_command_name
        existing_command_name = new_command_name
        new_command_name = temp

        existing_command_matches = Command.objects.filter(command__iexact=existing_command_name)
        found = (len(command_matches) == 1)

    if found:
        # Make sure the new command doesn't already exist
        new_command_matches = Command.objects.filter(command__iexact=new_command_name)
        if len(new_command_matches) == 0:
            existing_command = existing_command_matches[0]
            if not existing_command.is_built_in:
                new_command = Command(command=new_command_name, permissions=existing_command.permissions, output=existing_command.output)
                new_command.save()
                output = new_command_name + ' is now aliased to ' + existing_command_name
            else:
                output = 'Cannot create an alias for a built-in command'
        else:
            output = 'New command already exists'
    else:
        output = 'Existing command not found'
    return output

handlers = {'!setgame': handle_setgame,
            '!addcom': handle_addcom,
            '!delcom': handle_delcom,
            '!editcom': handle_editcom,
            '!alias': handle_alias,
           }

expected_args = {'!setgame': 1,
                 '!addcom': 2,
                 '!delcom': 1,
                 '!editcom': 2,
                 '!alias': 2,
                }

usage = {'!setgame': 'Usage: !setgame <pokemon game name>',
         '!addcom': 'Usage: !addcom <command> <output>',
         '!delcom': 'Usage: !delcom <command>',
         '!editcom': 'Usage: !editcom <command> <output>',
         '!alias': 'Usage: !alias <existing command> <new command>',
        }

def handle_admin_command(line):
    output = ''
    args = line.split(' ')
    command = args[0]
    handler = handlers.get(command)
    if handler:
        args = args[1:]
        if len(args) >= expected_args[command]:
            output = handler(args)
        else:
            output = usage[command]
    return output
