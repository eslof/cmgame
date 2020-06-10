# region Set up
from deployment_properties import *
from deployment_utils import *

functions = get_functions()
layers = get_layers()
print(layers)
# region Deploy layer
layer_name = f"{PREFIX}{LAYER}"
if layer_name in layers.keys():
    print(f"Updating layer: {layer_name}.")
else:
    print(f"Creating layer: {layer_name}.")

layer_arn = publish_layer(layer_name)
# endregion
# region Deploy functions
for function in FUNCTIONS:
    function_name = f"{PREFIX}{function}"
    if function in functions:
        update_function(function_name)
    else:
        create_function(function_name, layer_arn)
# endregion
