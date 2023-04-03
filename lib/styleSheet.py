class Style:
    def __init__(self, widget):
        widget.setStyleSheet(
            "QWidget {"
            "background-color: #323246;"
            "selection-background-color: #77a2b8;}"
        )

    @staticmethod
    def _btn_(button):
        button.setStyleSheet(
            "QPushButton {"
            "color: white; color: #FFFFE0;"
            "background-color: #46465A;"
            "border: none;"
            "padding: 5, 5, 5, 5;}"
            "QPushButton: hover {"
            "color:  # 46465A;/*color: #FFFFE0;*/"
            "background - color: lightgray;"
            "border: none;}"
        )
