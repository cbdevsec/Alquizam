from main import load_flashcards, save_flashcards
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui

class Alquizam(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alquizam - Flashcards")
        self.resize(800, 600)

        self.cards = load_flashcards()
        
        self.stack = QtWidgets.QStackedWidget()
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addWidget(self.stack)

        self.menu_page = self.create_menu_page()
        self.add_page = self.create_add_page()
        self.list_page = self.create_list_page()
        self.study_page = self.create_study_page()

        self.stack.addWidget(self.menu_page)   
        self.stack.addWidget(self.add_page)    
        self.stack.addWidget(self.list_page)   
        self.stack.addWidget(self.study_page)  

        self.stack.setCurrentIndex(0)

    def create_menu_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)

        label = QtWidgets.QLabel("Welcome to Alquizam!")
        add_btn = QtWidgets.QPushButton("Add Flashcards")
        list_btn = QtWidgets.QPushButton("List Flashcards")
        study_btn = QtWidgets.QPushButton("Study Flashcards")
        quit_btn = QtWidgets.QPushButton("Quit")

        layout.addWidget(label)
        layout.addWidget(add_btn)
        layout.addWidget(list_btn)
        layout.addWidget(study_btn)
        layout.addWidget(quit_btn)

        add_btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        list_btn.clicked.connect(self.show_list_page)
        study_btn.clicked.connect(lambda: self.stack.setCurrentIndex(3))
        quit_btn.clicked.connect(self.close)

        return page

    def create_add_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)

        self.q_input = QtWidgets.QLineEdit()
        self.q_input.setPlaceholderText("Enter Question")
        self.a_input = QtWidgets.QLineEdit()
        self.a_input.setPlaceholderText("Enter Answer")

        save_btn = QtWidgets.QPushButton("Save Flashcard")
        back_btn = QtWidgets.QPushButton("Back to Menu")

        layout.addWidget(QtWidgets.QLabel("Add a new flashcard"))
        layout.addWidget(self.q_input)
        layout.addWidget(self.a_input)
        layout.addWidget(save_btn)
        layout.addWidget(back_btn)

        save_btn.clicked.connect(self.save_new_card)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        return page

    def save_new_card(self):
        q = self.q_input.text().strip()
        a = self.a_input.text().strip()
        if q and a:
            self.cards.append({"question": q, "answer": a})
            save_flashcards(self.cards)
            self.q_input.clear()
            self.a_input.clear()
            QtWidgets.QMessageBox.information(self, "Saved", "Flashcard added")
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Both fields required")

    def create_list_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)

        self.list_widget = QtWidgets.QListWidget()
        back_btn = QtWidgets.QPushButton("Back to Menu")

        layout.addWidget(QtWidgets.QLabel("All Flashcards:"))
        layout.addWidget(self.list_widget)
        layout.addWidget(back_btn)

        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        return page

    def show_list_page(self):
        self.list_widget.clear()
        for card in self.cards:
            self.list_widget.addItem(f"Q: {card['question']} | A: {card['answer']}")
        self.stack.setCurrentIndex(2)

    def create_study_page(self):
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        
        self.study_label = QtWidgets.QLabel("Press Next to study")
        next_btn = QtWidgets.QPushButton("Next Flashcard")
        back_btn = QtWidgets.QPushButton("Back to Menu")

        layout.addWidget(self.study_label)
        layout.addWidget(next_btn)
        layout.addWidget(back_btn)

        next_btn.clicked.connect(self.study_one)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

        return page

    def study_one(self):
        if not self.cards:
            self.study_label.setText(" No flashcards found :<")
            return

        card = random.choice(self.cards)
        self.study_label.setText(f"Q: {card['question']}")

        reveal_btn = QtWidgets.QPushButton("Reveal Answer")
        next_btn = QtWidgets.QPushButton("Next Flashcard")
        back_btn = QtWidgets.QPushButton("Back to Menu")

        
        for i in reversed(range(self.layout().count())):
            widget = self.layout().itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)

        self.layout().addWidget(self.study_label)
        self.layout().addWidget(reveal_btn)
        self.layout().addWidget(next_btn)
        self.layout().addWidget(back_btn)


        reveal_btn.clicked.connect(lambda: self.study_label.setText(f"A: {card['answer']}"))
        next_btn.clicked.connect(self.study_one)
        back_btn.clicked.connect(lambda: self.stack.setCurrentIndex(0))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = Alquizam()
    widget.show()
    sys.exit(app.exec())
