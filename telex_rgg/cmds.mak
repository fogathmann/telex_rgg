${"#" * 80}
${"#"} name: New telex Command Definition
${"#"} author: F. Oliver Gathmann
${"#"} category: telex
${"#"} preview: 

Creates a new telex command definition.

${"#" * 6}

<rgg>
<h2 text="New telex Command Definition"/>
__jsonclass__ = http://telex.org/relations/command-definition
name = <textfield label='Command name (unique)' size='25'/>
label = <textfield label='Command label'/>
executable = <textfield label='Executable to run'/>
submitter = <textfield label='Submitting user'/>
category = <textfield label='Command category (optional)'/>
description = <textfield label='Command description (optional)' default=''/>
working_directory = <textfield label='Working directory to use'/>
</rgg>

% for value_type in VALUE_TYPES:
${render_param_def_command(value_type)}
% endfor

% for cmd_def in commands:
${"#" * 80}
${"#"} name: ${cmd_def.name}
${"#"} author: ${cmd_def.submitter}
${"#"} category: ${cmd_def.category}
${"#"} preview: 

${cmd_def.description}
    
${"#" * 6}

<rgg>
<h2 text="New ${cmd_def.name} Command"/>
__jsonclass__ = http://telex.org/relations/command
submitter = ${cmd_def.submitter}
command_definition = ${resource_to_url(cmd_def)}
% for param_def_mb in cmd_def.parameter_definitions:
parameters.item#${loop.index + 1}.__jsonclass__ = http://telex.org/relations/parameter
parameters.item#${loop.index + 1}.parameter_definition = ${resource_to_url(param_def_mb)}
parameters.item#${loop.index + 1}.value = ${render_entry_xml(param_def_mb.get_entity())}
% endfor
</rgg>
% endfor

<%def name="render_param_def_command(value_type)">
${"#" * 80}
${"#"} name: New ${value_type} telex Parameter Definition
${"#"} author: F. Oliver Gathmann
${"#"} category: telex
${"#"} preview: 

Creates a new ${value_type} telex parameter definition.

${"#" * 6}

<rgg>
<h2 text="New telex ${value_type} Parameter Definition"/>
__jsonclass__ = http://telex.org/relations/parameter-definition
name = <textfield label='Parameter name' size='30'/>
label = <textfield label='Parameter label'/>
description = <textfield label='Description' default=''/>
value_type = ${value_type}
<gaprow height="10"/>
<separator label="Parameter options" span="full"/>
<gaprow height="10"/>
% for option_item in get_options(value_type):
parameter_options.item#${loop.index + 1}.__jsonclass__ = http://telex.org/relations/parameter-option
parameter_options.item#${loop.index + 1}.name = ${option_item[0]}
parameter_options.item#${loop.index + 1}.value = ${render_option_value(option_item[1], option_item[2])}
% endfor
</rgg>
</%def>

<%def name="render_option_value(value_type, label)" filter="trim">
    % if value_type == VALUE_TYPES.BOOLEAN:
<checkbox label='${label}'/>
    % else:
<textfield label='${label}' 
           size='30'
        % if value_type != VALUE_TYPES.STRING:
           data-type='number'
        % endif
           />
    % endif
</%def>


<%def name="render_entry_xml(param_def)" filter="trim">
% if param_def.has_option('choices'):
<combobox label='${param_def.label}'
          items=${render_choices(param_def)}
          />
% else:
    % if param_def.value_type in (VALUE_TYPES.STRING, VALUE_TYPES.INT, VALUE_TYPES.DOUBLE, VALUE_TYPES.DATETIME):
<textfield label='${param_def.label}' 
           size='${param_def.get_option("entry_width", default_value=30)}'
           % if param_def.has_option('default_value'):
           default_value='${param_def.get_option("default_value")}'
           % endif
           % if param_def.value_type not in (VALUE_TYPES.STRING, VALUE_TYPES.DATETIME):
           data-type='number'
           % endif
           % if param_def.value_type == VALUE_TYPES.INT:
           knime-data-type='int'
           % elif param_def.value_type == VALUE_TYPES.DOUBLE:
           knime-data-type='double'
           % endif
           />
    % elif param_def.value_type == VALUE_TYPES.BOOLEAN:
<checkbox label='${param_def.label}' 
          knime-data-type='bool'/>
    % elif param_def.value_type == VALUE_TYPES.FILE:
<filechooser label='${param_def.label}'
        % if param_def.has_option('extensions'):
             accepted-extensions='${param_def.get_option("extensions")}'/>
        % endif
    % endif
% endif
</%def>

<%def name="render_choices(param_def)">
% if urlparse(param_def.get_option("choices")).scheme:
    % if param_def.has_option('choices_label_attribute'):
'$$$URL(${param_def.get_option("choices")}, ${param_def.get_option("choices_value_attribute")}, ${param_def.get_option("choices_label_attribute")})$$$'
    % elif param_def.has_option('choices_value_attribute'):
'$$$URL(${param_def.get_option("choices")}, ${param_def.get_option("choices_value_attribute")})$$$'
    % else:
'$$$URL(${param_def.get_option("choices")})$$$'
    % endif
% else:
'${param_def.get_option("choices")}'
% endif
</%def>
