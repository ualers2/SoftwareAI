from PySide2.QtCore import QRunnable

class QAIRunnable(QRunnable):
    def __init__(self, AI):
        super().__init__()
        self.AI = AI

    def run(self):
        self.AI.run()