from pymarkovchain import MarkovChain
# You'll need the pymarkovchain package. See README
from errbot.botplugin import BotPlugin
from errbot import botcmd
import httplib2


class MarkovBot(BotPlugin):

    def __init__(self):
        super(MarkovBot, self).__init__()
        self.markov = MarkovChain(dbFilePath='./markovdb')

    @botcmd
    def talk(self, mess, args):
        """ Generate a sentence based on database """
        return self.markov.generateString()

    @botcmd
    def complete(self, mess, args):
        """ Try to complete a sentence """
        return self.markov.generateStringWithSeed(args)

    @botcmd
    def gendbfromfile(self, mess, args):
        """ Generate markov chain word database """
        try:
            with open(args) as txtFile:
                txt = txtFile.read()
        except IOError as e:
            return 'Error: could not open text file'
        # At this point, we've got the file contents
        if self.markov.generateDatabase(txt):
            return 'Done.'
        else:
            return 'Error: Could not generate database'

    @botcmd
    def gendbfromstring(self, mess, args):
        if self.markov.generateDatabase(args):
            return 'Done.'
        else:
            return 'Error: Could not generate database from String'

    @botcmd
    def gendbfromurl(self, mess, args):
        response, content = httplib2.Http().request(args, 'GET')
        if response['status'] == '200' and self.markov.generateDatabase(content.decode('utf-8')):
            return 'Done.'
        else:
            return 'Error: Could not generate database from URL'
