# OpenCodeBlock an open-source tool for modular visual programing in python
# Copyright (C) 2021 Mathïs FEDERICO <https://www.gnu.org/licenses/>

""" Module for OCB in block python editor. """

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFocusEvent, QFont, QFontMetrics, QColor
from PyQt5.Qsci import QsciScintilla, QsciLexerPython

from opencodeblocks.graphics.blocks.block import OCBBlock

from opencodeblocks.graphics.function_parsing import execute_function, extract_args


class PythonEditor(QsciScintilla):

    def __init__(self, block:OCBBlock, parent=None):
        super().__init__(parent)
        self.block = block
        self.setText(self.block.source)

        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(1)
        self.setFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        foreground_color = QColor("#dddddd")
        background_color = QColor("#212121")
        self.setMarginsFont(font)
        self.setMarginWidth(2, fontmetrics.width("00") + 6)
        self.setMarginLineNumbers(2, True)
        self.setMarginsForegroundColor(foreground_color)
        self.setMarginsBackgroundColor(background_color)

        # Set Python lexer
        lexer = QsciLexerPython()
        lexer.setDefaultFont(font)
        lexer.setDefaultPaper(QColor("#1E1E1E"))
        lexer.setDefaultColor(QColor("#D4D4D4"))

        string_types = [
            QsciLexerPython.SingleQuotedString,
            QsciLexerPython.DoubleQuotedString,
            QsciLexerPython.UnclosedString,
            QsciLexerPython.SingleQuotedFString,
            QsciLexerPython.TripleSingleQuotedString,
            QsciLexerPython.TripleDoubleQuotedString,
            QsciLexerPython.TripleSingleQuotedFString,
            QsciLexerPython.TripleDoubleQuotedFString,
        ]

        for string_type in string_types:
            lexer.setColor(QColor('#CE9178'), string_type)

        lexer.setColor(QColor('#DCDCAA'), QsciLexerPython.FunctionMethodName)
        lexer.setColor(QColor('#569CD6'), QsciLexerPython.Keyword)
        lexer.setColor(QColor('#4EC9B0'), QsciLexerPython.ClassName)
        lexer.setColor(QColor('#7FB347'), QsciLexerPython.Number)
        lexer.setColor(QColor('#D8D8D8'), QsciLexerPython.Operator)

        self.setLexer(lexer)

        # Set caret
        self.setCaretForegroundColor(QColor("#D4D4D4"))

        # Indentation
        self.setAutoIndent(False)
        self.setTabWidth(4)
        self.setIndentationGuides(True)
        self.setIndentationsUseTabs(False)
        self.setBackspaceUnindents(True)

        # Disable horizontal scrollbar
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # # Add folding
        # self.setFolding(QsciScintilla.FoldStyle.CircledTreeFoldStyle, 1)
        # self.setFoldMarginColors(background_color, background_color)
        # self.setMarkerForegroundColor(foreground_color, 0)
        # self.setMarkerBackgroundColor(background_color, 0)

        # Add background transparency
        self.setStyleSheet("background:transparent")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

    def set_views_mode(self, mode:str):
        for view in self.graphicsProxyWidget().scene().views():
            if mode == "MODE_EDITING" or view.is_mode("MODE_EDITING"):
                view.set_mode(mode)

    def focusInEvent(self, event: QFocusEvent):
        self.set_views_mode("MODE_EDITING")
        return super().focusInEvent(event)

    def focusOutEvent(self, event: QFocusEvent):
        self.set_views_mode("MODE_NOOP")
        if self.isModified():
            self.block.source = self.text()
            self.setModified(False)
        
        # This is the part that parses and executes the code
        # Predefine the args and kwargs here
        args = ["'Hello'","10","[1,2,3]"]
        kwargs = ["d='World'"]

        print("")
        print("args are: " + str(args))
        print("kwargs are: " + str(kwargs))

        code = str(self.text())
        print("default args are: " + str(extract_args(code)))
        print("")
        print("Execution result:")
        print(str(execute_function(code,args,kwargs)))

        return super().focusInEvent(event)

"""
Here is a test function:
def test(a,b, c, d='Nope', e=20):
    print(a + ' ' + d)
    print(b + e)
    return max(c)
"""