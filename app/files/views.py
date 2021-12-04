import json
import os
from random import randint
from zipfile import ZipFile

from flask import Blueprint, render_template, redirect, url_for, request, \
    send_from_directory, current_app, flash, session
from flask_login import current_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from app.auth.forms import ChangeProfileDataForm, ProfilePictureForm
from app.auth.views import confirm_user_mail
from app.database import db
from app.file_processing.tasks import process_file
from app.files.forms import UploadForm, SearchForm
from app.files.utils import image_crop_and_resize
from app.models.file import File, Sentences, Words, Statistics, Status, Pages
from app.models.grammatical_cases import GrammaticalCase
from app.settings import Config

file_views_blueprint = Blueprint('files',
                                 __name__,
                                 template_folder='templates',
                                 url_prefix='/'
                                 )


@file_views_blueprint.route('/files', defaults={'page_num': 1}, methods=['GET', 'POST'])
@file_views_blueprint.route('/files/<int:page_num>', methods=['GET', 'POST'])
@login_required
def all_files(page_num):
    files = File.get_active_files(current_user.id).paginate(per_page=4, page=page_num)
    upload_form = UploadForm()
    profile_form = ChangeProfileDataForm()
    picture_form = ProfilePictureForm()

    # File upload handling
    if upload_form.validate_on_submit() and upload_form.submit_upload.data:
        if upload_form.file.data:
            print('file detected')
            file = upload_form.file.data
            filename = secure_filename(file.filename)
            title = filename.split(".")[0]
            print('file:', file)
            print('filename:', filename)
            print('title:', title)

        elif upload_form.text.data and upload_form.name.data:
            filename = secure_filename(upload_form.name.data + ".txt")
            title = upload_form.name.data

        path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id), filename)
        print('path:', path)
        duplicate_count = 0

        extension = filename.split('.')[1]
        while os.path.exists(path):
            duplicate_count += 1
            new_title = f"{title}-{duplicate_count}"
            filename = f"{new_title}.{extension}"
            path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id), filename)

        if duplicate_count != 0:
            title = new_title

        os.makedirs(os.path.dirname(path), exist_ok=True)

        if upload_form.file.data:
            file.save(path)
        elif upload_form.text.data:
            with open(path, 'w', encoding="utf-8") as f:
                f.write(upload_form.text.data)

        file_model = File(title, current_user.id, filename)
        print(file_model)
        file_model.save()

        file_status = Status(file_model.id, frequency_distribution_calculated="freq_dist" in upload_form.processes.data,
                             lemmatized="lemat" in upload_form.processes.data, completed=False)
        print(file_status)
        file_status.save()

        process_file(file_model.id, current_user.id, filename, upload_form.processes.data, extension)
        flash('მიმდინარეობს ფაილის დამუშავება')
        return redirect(url_for('files.all_files'))

    # Handling user data changes
    elif profile_form.validate_on_submit() and profile_form.submit_profile_changes.data:
        if current_user.check_password(profile_form.password.data):
            # password change
            if profile_form.old_password.data or profile_form.new_password.data or profile_form.confirm_password.data:
                if profile_form.old_password.data and profile_form.new_password.data and profile_form.confirm_password.data:
                    if current_user.check_password(profile_form.old_password.data):
                        if profile_form.new_password.data == profile_form.confirm_password.data:
                            if len(profile_form.new_password.data) > 5 or len(profile_form.new_password.data) < 129:
                                current_user._password = generate_password_hash(profile_form.new_password.data)
                            else:
                                flash('პაროლი უნდა შედგებოდეს 6-128 სიმბოლოსგან')
                                return redirect(url_for('files.all_files'))
                        else:
                            flash('პაროლები არ ემთხვევა ერთმანეთს; მონაცემები არ განახლდა.')
                            return redirect(url_for('files.all_files'))
                    else:
                        flash('ძველი პაროლი არასწორია; მონაცემები არ განახლდა.')
                        return redirect(url_for('files.all_files'))
                else:
                    flash('მონაცემები არ განახლდა. პაროლის შესაცვლელად შეიყვანეთ ძველი პაროლი, ახალი პაროლი და გაიმეორეთ.')
                    return redirect(url_for('files.all_files'))

            # name change
            current_user.first_name = profile_form.first_name.data
            current_user.last_name = profile_form.last_name.data
            db.session.commit()

            # email change
            if current_user.email != profile_form.new_email.data:
                current_user.email = profile_form.new_email.data
                current_user.confirmed_at = None
                confirm_user_mail(profile_form.new_email.data)
                flash('თქვენი ელ-ფოსტა განახლდა. '
                      f'ელ-ფოსტის ვერიფიკაციის შეტყობინება გაგზავნილია {profile_form.new_email.data} მისამართზე.')

            db.session.commit()
            flash('თქვენი მონაცემები განახლდა')
        else:
            flash('შეყვანილი პაროლი არასწორია. თქვენი მონაცემები არ განახლდა.', 'danger')

        return redirect(url_for('files.all_files'))

    elif picture_form.validate_on_submit() and picture_form.submit_picture.data:
        file = picture_form.picture.data
        picture_title = secure_filename(
            f'{current_user.first_name}_{current_user.last_name}_{randint(1000000, 9999999)}_{file.filename}'
        )
        file.save(f'app/static/uploads/{picture_title}')
        image_crop_and_resize(f'app/static/uploads/{picture_title}')

        current_user.picture = picture_title
        db.session.commit()
        flash('თქვენი პროფილის სურათი განახლდა')
        return redirect(url_for('files.all_files'))

    # Flash errors which are defined in forms
    if request.method == 'POST':
        submitted_form_errors = upload_form.errors   if upload_form.submit_upload.data            else \
                                profile_form.errors  if profile_form.submit_profile_changes.data  else \
                                picture_form.errors  if picture_form.submit_picture.data          else None
        if submitted_form_errors:
            for errors in submitted_form_errors.values():
                for error in errors:
                    flash(error)

    return render_template('files/all_files.html', page_num=page_num, block_files=files, upload_form=upload_form,
                           profile_form=profile_form, picture_form=picture_form)


@file_views_blueprint.route('/files/<int:file_id>/<int:page_id>', methods=['GET', 'POST'])
@login_required
def view_file(file_id, page_id):
    file = File.file_by_id(file_id)
    page = file.pages[page_id - 1]
    statistics = Statistics.statistics_for_file(file_id)
    word_list = page.get_text()

    lemma_list = []

    for word in page.get_all_words().all():
        dict = {
            'lemma': word.lemma,
            'tags': word.pos_tags
        }

        lemma_list.append(dict)

    search_form = SearchForm()
    search_type = 0
    if search_form.validate_on_submit() and search_form.search_field.data:
        if search_form.radio_field.data == 'თავისუფალი ძიება':
            search_type = 1

        return redirect(url_for('files.search', file_id=file_id, search_word=search_form.search_field.data, page_num=1,
                                search_type=search_type))

    return render_template('files/one_file.html', file=file, word_list=word_list, statistics=statistics,
                           search_form=search_form, lemma_list=json.dumps(lemma_list, ensure_ascii=False),
                           current_page=page_id)


@file_views_blueprint.route('/files/disable_file/<int:file_id>', methods=['GET', 'POST'])
@login_required
def disable_file(file_id):
    file = File.file_by_id(file_id)

    if current_user.id == file.user_id:
        file.disable()

    return redirect(request.referrer)


@file_views_blueprint.route('/files/download_file/<int:file_id>', methods=['GET', 'POST'])
@login_required
def download_file(file_id):
    file = File.file_by_id(file_id)
    file_path = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id), file.title)
    absolute_path = os.path.join(current_app.root_path, "uploads", str(current_user.id))

    if current_user.id == file.user_id:
        with ZipFile(f"{file_path}.zip", 'w') as zipobj:
            zipobj.write(f"{file_path}.txt", f"{file.title}.txt")

            if file.status[0].lemmatized:
                file.create_json()
                zipobj.write(f"{file_path}-lemmatized.json", f"{file.title}-lemmatized.json")
                zipobj.write(f"{file_path}-lemmatized.xml", f"{file.title}-lemmatized.xml")

            if file.status[0].frequency_distribution_calculated:
                zipobj.write(f"{file_path}-freq_dist.json", f"{file.title}-freq_dist.json")

        return send_from_directory(absolute_path, f"{file.title}.zip", as_attachment=True)

    return redirect(url_for('files.all_files'))


# @file_views_blueprint.route('/files/<int:file_id>/search/<string:search_word>/<int:search_type>/<int:page_num>',
#                             methods=['GET', 'POST'])
# @login_required
# def search(file_id, search_word, search_type, page_num):
#     if search_type == 0:
#         search_results = Words.search_by_raw(file_id, search_word).group_by(Words.sentence_id).paginate(per_page=8,
#                                                                                                         page=page_num)
#     elif search_type == 1:
#         search_word = lemmatize([search_word])[0][1]
#         search_results = Words.search_by_lemma(file_id, search_word).group_by(Words.sentence_id).paginate(per_page=8,
#                                                                                                           page=page_num)
#     sentences = []
#
#     file = File.file_by_id(file_id)
#
#     for word in search_results.items:
#         sentence_object = Sentences.query.get(word[1].id)
#         sentence = {
#             "raw_text": sentence_object.get_text(),
#             "highlight": word[2].raw,
#             "page_id": file.relative_page_by_id(sentence_object.page_id),
#         }
#
#         sentences.append(sentence)
#
#     return render_template('files/details.html', file_id=file_id, sentences=sentences, paginate=search_results,
#                            search_word=search_word, page_num=page_num, search_type=search_type)

@file_views_blueprint.route('/files/<int:file_id>/search/<int:results_page_id>')
def search(file_id, results_page_id):
    # Search form
    parts_of_speech = GrammaticalCase.query.filter_by(part_of_speech=None).all()
    grammatical_cases = GrammaticalCase.query.filter(GrammaticalCase.part_of_speech != None).all()

    search_form = {
        part_of_speech.full_name_ge: part_of_speech.to_json(part_of_speech=True)
        for part_of_speech in parts_of_speech}

    print(grammatical_cases)
    for tag in grammatical_cases:
        search_form[tag.part_of_speech]['tags'].append(tag.to_json())

    search_form = json.dumps(search_form, ensure_ascii=False)

    # Search results
    query = request.args.get('query')
    session['search_results'] = {}
    if query not in session['search_results'].keys():
        # time.sleep(5)
        all_words = (db.session.query(Words)
                     .join(Pages.sentences)
                     .join(Sentences.words)
                     .filter(Pages.file_id == file_id)).all()

        # all_queries = query.split('_')
        # all_queries = [q.split(',') for q in all_queries]
        # print('all_queries', all_queries)
        query = query.split(',')  # TODO: replace with %2c

        found_words = []
        for word in all_words:
            tags = word.pos_tags.split(',')
            for tag in query:
                if tag not in tags:
                    break
            else:
                found_words.append(word)

        result = []
        current_result_page_data = []
        count = 0
        for word in found_words:
            print(found_words)
            if len(current_result_page_data) and current_result_page_data[-1][0] == word.sentences.get_text():
                print('activated!')
                current_result_page_data[-1][1].append(word.raw)
            else:
                count += 1
                current_result_page_data.append((word.sentences.get_text(), [word.raw]))

            if count == 10:
                result.append(current_result_page_data)
                current_result_page_data = []
                count = 0
        if len(current_result_page_data):
            result.append(current_result_page_data)

        query = ','.join(query)

        session['search_results'] = {query: result}
        print(session.items())
    print(query)
    print(len(session['search_results'][query]))
    if results_page_id > len(session['search_results'][query]):
        return {'resp': 'ნაპოვნია 0 შედეგი'}
    print(session['search_results'][query][results_page_id-1])

    return render_template('files/search.html', grammar_search_form=search_form,
                           search_results=session['search_results'][query][results_page_id-1])
