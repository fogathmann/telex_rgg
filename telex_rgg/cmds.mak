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
