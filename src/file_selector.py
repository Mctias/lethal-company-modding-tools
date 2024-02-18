from tkinter import Tk
from tkinter.filedialog import askopenfilename

class FileSelector:
    @staticmethod
    def select_file(title, filetypes):
        root = Tk()
        root.withdraw()  # Hide the main window

        filename = askopenfilename(title=title, filetypes=filetypes)
        if not filename:  # If the user cancels the dialog, filename will be an empty string
            return None
        return filename
