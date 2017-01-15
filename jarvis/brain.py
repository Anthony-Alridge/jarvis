from inspect import getmembers, isfunction
class Brain():
    '''
    This is the interface with which a user will interact.
    '''
    def __init__(self):
        self.pattern_map = {}
        self.actions = {}

    def add_command(self, function, command_text, pattern = None):
        #use to add an individual command to jarvis, or replace an existing one
        #with a different function
        self.actions[command_text] = function
        if pattern:
            self.pattern_map[pattern] = command_text

    def parse_command(self, command):
        '''
        Just checks if any part of the text matches one of the commands.
        If so perform the function associated with it.
        '''
        if type(command) is str:
            for action in self.actions.keys():
                if action in command:
                    function = self.actions[action]
                    function()
        else:
            if command in self.pattern_map.keys():
                command = self.pattern_map[pattern]
                parse_command(command)

    def __parsename(self, name):
        return name.replace("_", " ")

    #TODO:make some way of labelling which functions in a module should be added
    #to jarvis. Decorators?
    def add(self, module):
        '''
        Takes a python module and adds all the functions from that module to
        our dicitonary in the form 'function_name : function'.
        '''
        methods = getmembers(module, isfunction)
        text_map = { self.__parsename(name): function for name, function in methods}
        self.actions.update(text_map)
