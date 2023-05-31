from flask import Flask, redirect, jsonify
from utilities import get_record, set_instcode, views


app = Flask(__name__)


@app.route('/')
def doc():
    return 'legacy catalog redirect service'


@app.route('/cr/<bibid>')
def cr_redirect(bibid):

    # query the database for the parameter (bibid)
    query = "SELECT t.TITLE_BRIEF, t.ISBN, t.ISSN, l.LIBRARY_NAME " \
            "FROM BIB_TEXT t, BIB_MASTER m, LIBRARY l " \
            "WHERE t.BIB_ID = m.BIB_ID AND " \
            "m.LIBRARY_ID = l.LIBRARY_ID AND " \
            "t.BIB_ID = %s"

    r = get_record(bibid, query, False)  # fetch the results

    # if there's a record try to find it's analog in primo
    if r is not None:
        isbn = r['ISBN']  # isbn
        issn = r['ISSN']  # issn
        title = r['TITLE_BRIEF']  # title
        instcode = set_instcode(r['LIBRARY_NAME'])  # library
        try:
            view = views[instcode]  # set view based on institution code from the database
        except KeyError:
            view = views['WR']  # default to WR if not in list

        # get the oclcnums
        headings_query = "SELECT DISPLAY_HEADING, NORMAL_HEADING FROM BIB_INDEX " \
                         "WHERE BIB_ID = %s AND INDEX_CODE = '035A'"

        headings = get_record(bibid, headings_query)  # fetch the 35a headings for the bib id
        oclcnums = []  # empty list of oclcnums

        if len(headings) > 0:  # if there are headings
            # loop through the headings
            for heading in headings:
                if heading['DISPLAY_HEADING'].startswith('(OCoLC)'):  # if the display heading starts with (OCoLC)
                    oclcnums.append(heading['NORMAL_HEADING'].replace('(OCoLC)', ''))  # add std heading to the list

            # if there are oclcnums, check for a usable one
            if len(oclcnums) > 0:
                for oclcnum in oclcnums:  # iterate through the oclcnums
                    if oclcnum.strip() != '' and oclcnum.isdigit():  # if the oclcnum is not empty and is all digits
                        return redirect(view.format('ocolc,contains,' + oclcnum))

        # if there's an isbn, use that
        if isbn and isbn != '':
            return redirect(view.format('isbn,contains,' + isbn))

        # if there's an issn, use that
        if issn and issn != '':
            return redirect(view.format('issn,contains,' + issn))

        # if there's a title, use that
        if title and title.strip() != '':
            return redirect(view.format('title,contains,' + title))

        # if there's nothing, send an empty query
        return redirect(view.format(''))

    # if there's no record, send to list of primo instances
    else:
        return redirect('https://redirects.wrlc.org?notfound=true')
        

@app.route('/record/<bibid>')
def fetch_record(bibid):
    # query the database for the parameter (bibid)
    query = "SELECT t.*, l.LIBRARY_NAME " \
            "FROM BIB_TEXT t, BIB_MASTER m, LIBRARY l " \
            "WHERE t.BIB_ID = m.BIB_ID AND " \
            "m.LIBRARY_ID = l.LIBRARY_ID AND " \
            "t.BIB_ID = %s"
    r = get_record(bibid, query)
    if len(r) > 0:
        return jsonify(r)
    else:
        return "no record with id: " + bibid


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    
