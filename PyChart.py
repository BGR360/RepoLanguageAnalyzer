import matplotlib.pyplot as plt
from GitHubColors import GitHubColors

class PyChart(object):
    """
    An interface for rendering a Pie Chart. Simply pass in an array of data and it call draw()
    """
    def __init__(self, data):
        self.data = data
        self.colors = GitHubColors()

    def draw(self):
        """
        This implementation uses matplotlib to render a pie chart
        """
        unzipped = zip(*self.data)
        labels = list(unzipped[0])
        pieces = list(unzipped[1])

        # Get the proper colors for the sectors
        piece_colors = []
        for language in labels:
            color = self.colors.get_color_for(language)
            piece_colors.append(color)

        plt.pie(pieces, labels=labels, colors=piece_colors, startangle=0.0, autopct='%.2f%%')
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        plt.show()
