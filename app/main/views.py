from flask import Blueprint, render_template, request
from app.main.temp_data import people, block_files, grammar_blocks, checkboxes, \
    word_list  # TODO: მონაცემების წამოღება ბაზიდან
from app import babel
from app.settings import Config
from app.models.file import Words, Sentences


@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(Config.LANGUAGES.keys())


main_blueprint = Blueprint('main',
                           __name__,
                           template_folder='templates/jinja'
                           )


@main_blueprint.route('/', methods=['GET', 'POST'])
@main_blueprint.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html', blocks=grammar_blocks)


@main_blueprint.route('/documentation', methods=['GET', 'POST'])
def documentation():
    return render_template('files.html', block_files=block_files)


@main_blueprint.route('/about_us', methods=['GET', 'POST'])
def about_us():
    return render_template('about.html', people=people)


@main_blueprint.route('/add_files', methods=['GET', 'POST'])
def add_files():
    return render_template('add-file.html', checkboxes=checkboxes)


@main_blueprint.route('/files/<int:file_id>/<int:page_id>', methods=['GET', 'POST'])
def concrete(file_id, page_id):
    """TODO:
    - მონაცემთა ბაზიდან უნდა ჩაიტვირთოს ფაილის საწყისი გვერდი
    -
    """
    return render_template('concrete.html', word_list=word_list)


@main_blueprint.route('/files/<int:file_id>/search/<string:word>', methods=['GET', 'POST'])
def search(word, file_id):
    """TODO:
    - მონაცემთა ბაზიდან უნდა ჩაიტვირთოს ყველა სიტყვის ობიექტი Word.search_by_raw(word) მეთოდით
    - ამოვიღოთ ამ სიტყვების შესაბამისი წინადადებები
    - ამოვიღოთ ამ წინადადების ტექსტი
    - მოვნიშნოთ წინადადებაში კონკრეტული სიტყვა
    """
    words = Words.search_by_raw(file_id, word)
    sentences = []

    for word in words:
        sentence = Sentences.query.get(word.sentence_id)
        new_sentence = {
            "raw_text": "კონკრეტულად ჩემ ცნობიერებაში წარმოსახული ობიექტი კონკრეტულმა არის დამზადებული, A5 ზომისაა და "
                        "მაგარი ყდა აქვს.",  # sentence.get_text()
            "highlight": [word.start_index, word.end_index],
            "page_id": sentence.page_id,
        }
    return render_template('details.html', word_list=word_list)
