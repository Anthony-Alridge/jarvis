#Controls the computer

class Brain():

    def __init__(self):
        self.clap_actions = {}
        self.text_actions = {}


    def create_command(self, function, command_text, clap_pattern):
        self.text_actions[command_text] = function
        if clap_pattern:
            self.clap_actions[clap_pattern] = function

    def parse_command(self, command, clap, isClap):
        '''
        Just checks if any part of the text matches one of the commands.
        If so perform the function associated with it
        '''
        if isClap:
            if clap in self.clap_actions.keys():
                function = self.clap_actions[action]
                function()
        else:
            for action in self.text_actions.keys():
                if action in command:
                    function = self.text_actions[action]
                    function()
