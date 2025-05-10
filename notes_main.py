
#импорт библиотек
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QRadioButton, QHBoxLayout, QMessageBox, QGroupBox, QButtonGroup, QListWidget, QLineEdit, QTextEdit, QInputDialog
import json

def show_note():
    key = list1.selectedItems()[0].text()
    change_var.setText(notes[key]['текст'])
    list2.clear()
    list2.addItems(notes[key]['теги'])

def add_note():
    notes_name, result = QInputDialog.getText(
        window, 'Добавление заметки', 'Название:'
    )
    if result:
        notes[notes_name] = {
            'текст': '',
            'теги': []
        }
        list1.addItem(notes_name)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file,
                      sort_keys=True,
                      ensure_ascii=False)

def del_note():
    if list1.selectedItems():
        key = list1.selectedItems()[0].text()
        del notes[key]
        list1.clear()
        list1.addItems(notes)
        change_var.clear()
        list2.clear()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file,
                      sort_keys=True,
                      ensure_ascii=False)

def save_note():
    if list1.selectedItems():
        key = list1.selectedItems()[0].text()
        notes[key]['текст']=change_var.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file,
                      sort_keys=True,
                      ensure_ascii=False)

def add_tag():
    if list1.selectedItems():
        key = list1.selectedItems()[0].text()
        tag = line.text()
        if tag != '' and not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list2.addItem(tag)
            line.clear()
            with open('notes_data.json', 'w') as file:
                json.dump(notes, file,
                      sort_keys=True,
                      ensure_ascii=False)

def del_tag():
    if list2.selectedItems():
        key = list1.selectedItems()[0].text()
        tag = list2.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list2.clear()
        list2.addItems(notes[key]['теги'])
        with open('notes_data.json', 'w') as file:
                json.dump(notes, file,
                        sort_keys=True,
                        ensure_ascii=False)


def search_tag():
    tag = line.text()
    if tag and btn6.text() == 'Искать заметки по тегу':
        notes_filtered = dict()
        for key in notes:
            if tag in notes[key]['теги']:
                notes_filtered[key] = notes[key]
        btn6.setText('Сбросить поиск')
        list1.clear()
        list2.clear()
        change_var.clear()
        list1.addItems(notes_filtered)
    else:
        line.clear()
        btn6.setText('Искать заметки по тегу')
        list1.clear()
        list1.addItems(notes)




#главное окно
app = QApplication([])
window = QWidget()
window.setWindowTitle('Умные заметки')
window.resize(900, 600)

#виджеты
name1 = QLabel('Список заметок')
list1 = QListWidget()
btn1 = QPushButton('Создать заметку')
btn2 = QPushButton('Удалить заметку')
btn3 = QPushButton('Сохранить заметку')

name2 = QLabel('Список тегов')
list2 = QListWidget()
line = QLineEdit()
line.setPlaceholderText('Введите тег...')
btn4 = QPushButton('Добавить к заметке')
btn5 = QPushButton('Открепить от заметки')
btn6 = QPushButton('Искать заметки по тегу')

change_var = QTextEdit()

#создание линии
v_line1 = QVBoxLayout()
v_line2 = QVBoxLayout()
h_line1 = QHBoxLayout()
h_line2 = QHBoxLayout()
h_line3 = QHBoxLayout()

#подключение виджетов к линиям
v_line1.addWidget(change_var)
h_line1.addWidget(btn1)
h_line1.addWidget(btn2)


v_line2.addWidget(name1)
v_line2.addWidget(list1)
v_line2.addLayout(h_line1)

v_line2.addWidget(btn3)
v_line2.addWidget(name2)
v_line2.addWidget(list2)
v_line2.addWidget(line)
h_line2.addWidget(btn4)
h_line2.addWidget(btn5)
v_line2.addLayout(h_line2)
v_line2.addWidget(btn6)

h_line3.addLayout(v_line1)
h_line3.addLayout(v_line2)


window.setLayout(h_line3)







with open('notes_data.json', 'r') as file:
    notes = json.load(file)

list1.addItems(notes)
list1.itemClicked.connect(show_note)

btn1.clicked.connect(add_note)
btn2.clicked.connect(del_note)
btn3.clicked.connect(save_note)
btn4.clicked.connect(add_tag)
btn5.clicked.connect(del_tag)
btn6.clicked.connect(search_tag)

window.show()
app.exec()


