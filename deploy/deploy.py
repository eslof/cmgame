# region Set up
from deployment_properties import *
from deployment_utils import *

functions = get_functions()
layers = get_layers()
# region Deploy layer
if LAYER in layers.keys():
    print(f"Updating layer: {PREFIX}{LAYER}.")
else:
    print(f"Creating layer: {PREFIX}{LAYER}.")

layer_arn = publish_layer(LAYER)
# endregion
# region Deploy functions
for function in FUNCTIONS_TO_DEPLOY:
    if function in functions:
        update_function(function)
    else:
        create_function(function, layer_arn)
# endregion
