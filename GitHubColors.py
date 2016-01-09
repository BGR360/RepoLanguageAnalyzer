from urllib import urlopen
import yaml

COLORS_FILE_URL = 'https://raw.githubusercontent.com/github/linguist/master/lib/linguist/languages.yml'
DEFAULT_COLOR = '#dddddd'

class GitHubColors(object):
    """
    Queries the GitHub languages.yml file to find the proper color
    """
    def __init__(self):
        response = urlopen(COLORS_FILE_URL)
        languages = yaml.load(response.read())
        self.colors = dict((language, info['color']) for language, info in languages.items() if 'color' in info)

    def get_color_for(self, language):
        if language in self.colors:
            return self.colors[language]
        else:
            return DEFAULT_COLOR
