from PySide2.QtWidgets import QTextEdit

def setup_plain_text_qtextedit(editor: QTextEdit):
    """
    Configures a QTextEdit to handle pasted text as plain text only.

    :param editor: Instance of QTextEdit to configure
    """
    editor.setAcceptRichText(False)
    def insert_plain_text_from_mime_data(self, source):
        if source.hasText():
            self.insertPlainText(source.text())
        else:
            super(QTextEdit, self).insertFromMimeData(source)
    editor.__class__.insertFromMimeData = insert_plain_text_from_mime_data
