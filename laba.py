import gradio as gr  # Імпортуємо бібліотеку Gradio для створення інтерфейсів користувача
import spacy  # Імпортуємо бібліотеку spaCy для обробки природної мови

nlp = spacy.load('uk_core_news_sm')  # Завантажуємо українську модель мовлення spaCy

def highlight_verbs(text):  # Визначаємо функцію для виділення дієслів у тексті
    doc = nlp(text)  # Обробляємо текст з допомогою моделі spaCy
    highlighted_text = ''  # Ініціалізуємо змінну для збереження тексту з виділенням
    verbs = []  # Створюємо порожній список для збереження дієслів
    for token in doc:  # Проходимося по кожному токену в документі
        if token.pos_ == 'VERB':  # Якщо токен є дієсловом
            highlighted_text += f'<span style="color: #50C878; font-weight: bold;">{token.text}</span> '  # Додаємо виділений текст
            verbs.append(token.text)  # Додаємо дієслово до списку
        else:
            highlighted_text += f'{token.text} '  # Додаємо невиділений текст

    return highlighted_text, verbs  # Повертаємо виділений текст і список дієслів

def get_verb_info(verb_text):  # Визначаємо функцію для отримання інформації про дієслово
    doc = nlp(verb_text)  # Обробляємо текст з допомогою моделі spaCy
    if not doc or doc[0].pos_ != 'VERB':  # Якщо текст пустий або не є дієсловом
        return 'Вибране слово не є дієсловом.'  # Повертаємо повідомлення про помилку

    verb = doc[0]  # Отримуємо перше слово (дієслово) з обробленого тексту
    tense = verb.morph.get('Tense')  # Отримуємо час дієслова
    number = verb.morph.get('Number')  # Отримуємо число дієслова
    person = verb.morph.get('Person')  # Отримуємо особу дієслова
    gender = verb.morph.get('Gender') if 'Tense=Past' in verb.morph else 'не застосовується'  # Отримуємо рід дієслова, якщо це минулий час

    # Формуємо інформацію про дієслово
    info = f'**Дієслово:** {verb.text}\n\n'
    info += f'- **Час:** {tense[0] if tense else "невідомо"}\n'
    info += f'- **Число:** {number[0] if number else "невідомо"}\n'
    info += f'- **Особа:** {person[0] if person else "невідомо"}\n'
    info += f'- **Рід (минулий час):** {gender[0] if gender != "не застосовується" else gender}\n'

    return info  # Повертаємо сформовану інформацію

custom_css = '''
.gradio-container {
  background-color: #478778; /* Lincoln green color */
}

#custom_button {
  background-color: #04AA6D; /* Green color */
  border: none;
  color: white;
  padding: 15px 32px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  cursor: pointer;
}

#author {
  position: fixed;
  bottom: 10px;
  right: 10px;
  font-size: 14px;
  color: black; /* Black color */
}
'''  # Задаємо користувацькі стилі CSS для елементів інтерфейсу

with gr.Blocks(css=custom_css) as demo:  # Створюємо блоковий інтерфейс Gradio з користувацьким CSS
    gr.Markdown('# Verbal Marker')  # Додаємо заголовок у форматі Markdown
    inp = gr.Textbox(label='Type your text')  # Створюємо текстове поле для введення тексту
    btn = gr.Button('Submit', elem_id='custom_button')  # Створюємо кнопку для відправки тексту
    out = gr.HTML(label='Highlighted Text')  # Створюємо HTML-елемент для відображення виділеного тексту
    verbs_dropdown = gr.Dropdown(label='Select a verb to see its information', choices=[])  # Створюємо випадаючий список для вибору дієслова
    verb_info = gr.Markdown(label='Verb Information')  # Створюємо елемент для відображення інформації про дієслово
    gr.HTML('<div id=\'author\'>made by x3llga</div>')  # Додаємо HTML-елемент для відображення автора

    def update_dropdown_and_highlight(text):  # Визначаємо функцію для оновлення випадаючого списку і виділення дієслів
        highlighted_text, verbs = highlight_verbs(text)  # Виділяємо дієслова в тексті
        return highlighted_text, gr.update(choices=verbs)  # Повертаємо виділений текст і оновлений випадаючий список

    btn.click(fn=update_dropdown_and_highlight, inputs=inp, outputs=[out, verbs_dropdown])  # Додаємо обробник кліку для кнопки
    verbs_dropdown.change(fn=get_verb_info, inputs=verbs_dropdown, outputs=verb_info)  # Додаємо обробник зміни вибору в випадаючому списку

demo.launch()  # Запускаємо додаток Gradio