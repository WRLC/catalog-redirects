from flask import Flask, redirect, jsonify
from utilities import get_record, get_record_view, get_headings, set_redirect, guess_institution
from models import set_record, set_head

app = Flask(__name__)


@app.route('/')
def doc():
    return 'legacy catalog redirect service'


@app.route('/cr/<bibid>')
def cr_redirect(bibid):
    inst = guess_institution()  # Check for an institution code in the request
    r = get_record(bibid)  # fetch the record from the database

    if r is not None:  # if there's a record try to find it's analog in primo
        record = set_record(r, bibid, inst)  # create a record object
        view = record.set_view()  # set the view based on the institution code
        headings = get_headings(bibid)  # fetch any 35a headings for the bib id

        if len(headings) > 0:  # if there are headings
            for heading in headings:  # loop through the headings
                head = set_head(heading, bibid)  # create a heading object
                oclcnum = head.set_oclcnum()  # check if heading is an oclcnum
                if oclcnum is not None and oclcnum.strip() != '' and oclcnum.isdigit():  # if there is an oclcnum...
                    return redirect(view.format('ocolc,contains,' + oclcnum))  # ...send to primo with oclcnum

        isbn_response = set_redirect(record.isbn, 'isbn', view)  # Check for an isbn
        if isbn_response is not None:  # if there's an isbn...
            return redirect(isbn_response)  # ...send to primo with isbn

        issn_response = set_redirect(record.issn, 'issn', view)  # if there's an issn, use that
        if issn_response is not None:
            return redirect(issn_response)

        title_response = set_redirect(record.title, 'title', view)  # if there's a title, use that
        if title_response is not None:
            return redirect(title_response)

        return redirect(view.format(''))  # if there's nothing, send an empty query

    else:  # if there's no record
        return redirect('https://redirects.wrlc.org?notfound=true')  # send to list of primo instances
        

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
    
