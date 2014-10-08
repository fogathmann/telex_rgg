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
parameters.${param_def.name} = <textfield label='${param_def.label}'/>
% endfor
</rgg>
% endfor
