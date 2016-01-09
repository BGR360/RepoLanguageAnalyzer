import matplotlib.pyplot as plt

class PyChart(object):
    """
    An interface for rendering a Pie Chart. Simply pass in an array of data and it call draw()
    """
    def __init__(self, title, data):
        self.title = title
        self.data = data

    def draw(self):
        """
        This implementation uses matplotlib to render a pie chart
        """
        self.data = dict(self.data)
        labels = self.data.keys()
        fracs = self.data.values()
        plt.title(self.title)
        plt.pie(fracs, labels=labels, startangle=0.0, autopct='%.2f%%')
        # Set aspect ratio to be equal so that pie is drawn as a circle.
        plt.axis('equal')
        plt.show()
