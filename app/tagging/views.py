from . import tagging_blueprint
from flask import render_template
import json
from .forms import NerTagForm


@tagging_blueprint.route('/<int:file_id>/<int:page_id>', methods=['GET', 'POST'])
def test(page_id=0, file_id=0):
    form = NerTagForm()
    random_text = "პითონები — გველების ქვეოჯახი მახრჩობელასებრთა ოჯახისა (ან დამოუკიდებელი ოჯახი). გავრცელებულია " \
                  "აღმოსავლეთ და, ნაწილობრივ, დასავლეთ (ცენტრალური ამერიკა) ნახევარსფეროებში. ამჟამად ქვეოჯახში შედის " \
                  "8 გვარი, 35 სახეობით. საკუთრივ ცენტრალურ, პითონის გვარში 7 სახეობაა, გავრცელებულია აფრიკაში, " \
                  "სამხრეთ-აღმოსავლეთ აზიაში, მალაის არქიპელაგზე, ახალ გვინეაში და ავსტრალიაში. ზედა ტუჩზე " \
                  "აღენიშნებათ 2-4 ღრმული, რაც თერმორეცეპტორს წარმოადგენს. ბინადრობენ უმთავრესად ლერწმიანებში, " \
                  "ლელიანებში, ქვებს შორის. კარგად ცურავენ, შეუძლიათ ხეზე ასვლა. იკვებებიან ძირითადად ხერხემლიანებით, " \
                  "რომლებსაც სხეულის რგონებით გუდავენ. "

    # retrieve page by file_id and page_id
    # retrieve all the tags from the page
    # build tags object for every word connected to page
    # LOC = GREEN, GPE = BLUE, NUM = PURPLE
    tags = [
        {"id": 1, "keys": [11], "value": "LOC"},
        {"id": 2, "keys": [14], "value": "LOC"},
        {"id": 3, "keys": [15, 16], "value": "GPE"},
        {"id": 4, "keys": [23], "value": "NUM"},
    ]

    return render_template('tagging.html', text=random_text, tags=tags, tags_json=json.dumps(tags, indent = 4), form=form)
