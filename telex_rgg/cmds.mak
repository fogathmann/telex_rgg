${"#" * 80}
${"#"} name: New Telex Command Definition
${"#"} author: F. Oliver Gathmann
${"#"} category: telex
${"#"} preview: 

Creates a new telex command definition.

${"#" * 6}

<rgg>
__jsonclass__ = http://telex.org/relations/command-definition
name = <textfield label='Command name (unique)' size='25'/>
label = <textfield label='Command label'/>
executable = <textfield label='Executable to run'/>
submitter = <textfield label='Submitting user'/>
category = <textfield label='Command category (optional)'/>
description = <textfield label='Command description (optional)' default=''/>
working_directory = <textfield label='Working directory to use'/>
</rgg>


${"#" * 80}
${"#"} name: New Telex Parameter Definition
${"#"} author: F. Oliver Gathmann
${"#"} category: telex
${"#"} preview: 

Creates a new telex parameter definition.

${"#" * 6}

<rgg>
__jsonclass__ = http://telex.org/relations/parameter-definition
name = <textfield label='Parameter name' size='30'/>
label = <textfield label='Parameter label'/>
description = <textfield label='Description' default=''/>
value_type = <textfield label='Parameter value type' default='str'/>
default_value = <textfield label='Default value'/>
is_mandatory = <checkbox label='Is mandatory?'/>
</rgg>


% for cmd_def in commands:
${"#" * 80}
${"#"} name: ${cmd_def.name}
${"#"} author: ${cmd_def.submitter}
${"#"} category: ${cmd_def.category}
${"#"} preview: 

${cmd_def.description}
    
${"#" * 6}

<rgg>
__jsonclass__ = http://telex.org/relations/command
submitter = ${cmd_def.submitter}
command_definition = ${resource_to_url(cmd_def)}
% for param_def in cmd_def.parameter_definitions:
parameters.item#${loop.index + 1}.__jsonclass__ = http://telex.org/relations/parameter
parameters.item#${loop.index + 1}.parameter_definition = ${resource_to_url(param_def)}
parameters.item#${loop.index + 1}.value = <textfield label='${param_def.label}' size='30'/>
% endfor
</rgg>
% endfor
