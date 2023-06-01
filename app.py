from flask import Flask, redirect, jsonify
from utilities import get_record, get_record_view, get_headings, set_redirect
from models import set_record, set_head


app = Flask(__name__)


@app.route('/')
def doc():
    return 'legacy catalog redirect service'


@app.route('/cr/<bibid>')
def cr_redirect(bibid):
    r = get_record(bibid)  # fetch the record from the database

    # if there's a record try to find it's analog in primo
    if r is not None:
        record = set_record(r, bibid)  # create a record object
        view = record.set_view()  # set the view based on the institution code
        headings = get_headings(bibid)  # fetch any 35a headings for the bib id

        if len(headings) > 0:  # if there are headings
            # loop through the headings
            for heading in headings:
                # create a heading object
                head = set_head(heading, bibid)  # create a heading object
                oclcnum = head.set_oclcnum()  # set the oclcnum from the heading
                if oclcnum.strip() != '' and oclcnum.isdigit():  # if the oclcnum is not empty and is all digits
                    return redirect(view.format('ocolc,contains,' + oclcnum))

        # if there's an isbn, use that
        isbn_response = set_redirect(record.isbn, 'isbn', view)
        if isbn_response is not None:
            return redirect(isbn_response)

        # if there's an issn, use that
        issn_response = set_redirect(record.issn, 'issn', view)
        if issn_response is not None:
            return redirect(issn_response)

        # if there's a title, use that
        title_response = set_redirect(record.title, 'title', view)
        if title_response is not None:
            return redirect(title_response)

        # if there's nothing, send an empty query
        return redirect(view.format(''))

    # if there's no record, send to list of primo instances
    else:
        return redirect('https://redirects.wrlc.org?notfound=true')
        

@app.route('/record/<bibid>')
def fetch_record(bibid):
    # query the database for the parameter (bibid)
    r = get_record_view(bibid)

    if r is not None:
        return jsonify(r)
    else:
        return "no record with id: " + bibid


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
