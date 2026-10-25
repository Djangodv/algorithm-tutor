import sys

class DebugTracer():
    def __init__(self, target_array, shadow_idx):
        self.target_array = target_array
        self.shadow_idx = shadow_idx

        self.execution_history = []

    # Source: https://www.geeksforgeeks.org/python/python-sys-settrace/, https://docs.python.org/3.11/reference/datamodel.html#frame-objects
    def myTracer(self, frame, event, arg = None):

        variable_states = {}

        # Extract global and local variables
        global_variables = frame.f_globals
        local_variables = frame.f_locals

        # TEST:
        # print("GLOBAL VARIABLES: ", global_variables)
        # print("KEYS: ", str(local_variables.keys()))
        # print("VALUES: ", str(local_variables.values()))

        # Check whether target_array exists
        if self.target_array not in global_variables and self.target_array not in local_variables:
            return self.myTracer

        variable_states['arrayState'] = global_variables.get(self.target_array) or local_variables.get(self.target_array)

        # Explicit check to avoid returning None (when target_array returns 0 its treated as false, that's why .get() or .get() can't work)
        if self.shadow_idx in local_variables:
            variable_states['index'] = local_variables[self.shadow_idx]
        elif self.shadow_idx in global_variables:
            variable_states['index'] = global_variables[self.shadow_idx]

        # TODO
        if variable_states not in self.execution_history: # WARNING: Could cause problems later on with certain algorithms, where specific steps (variable states) are lost
            # Maybe fix by: only tracking line on which (first) for-loop is executing? 
            self.execution_history.append(variable_states)

        return self.myTracer

        # variable_states['searchTarget']
