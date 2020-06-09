import os

# region Set up
from deployment_properties import *
from deployment_utils import *

functions = get_functions()
layers = get_layers()

os.chdir("..")
# endregion
# region Deploy layer
if LAYER_NAME in layers.keys():
    print(f"Updating layer: {LAYER_NAME}.")
else:
    print(f"Creating layer: {LAYER_NAME}.")

layer_arn = publish_layer(LAYER_NAME, LAYER_ZIP)
# endregion
# region Deploy functions
for function in FUNCTIONS_TO_DEPLOY:
    if function in functions:
        print(f"Updating function: {function}.")
        update_function(function)
    else:
        print(f"Creating function: {function}")
        create_function(function, layer_arn)
# endregion
