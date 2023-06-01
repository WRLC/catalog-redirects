from utilities import views, set_instcode


class Record:
    def __init__(self, title, isbn, issn, library_name, bibid):
        self.title = title
        self.isbn = isbn
        self.issn = issn
        self.library_name = library_name
        self.bibid = bibid

    def set_view(self):
        try:
            view = views[self.library_name]  # set view based on institution code from the database
        except KeyError:
            view = views['WR']  # default to WR if not in list
        return view


class Heading35a:
    def __init__(self, display_heading, normal_heading, bibid):
        self.display_heading = display_heading
        self.normal_heading = normal_heading
        self.bibid = bibid

    def set_oclcnum(self):
        if self.display_heading.startswith('(OCoLC)'):  # if the display heading starts with (OCoLC)
            oclcnum = self.normal_heading.replace('(OCoLC)', '')  # remove the (OCoLC)
            return oclcnum


def set_record(r, bibid):
    instcode = set_instcode(r['LIBRARY_NAME'])  # set the institution code
    record = Record(r['TITLE_BRIEF'], r['ISBN'], r['ISSN'], instcode, bibid)  # create a record object
    return record


def set_head(heading, bibid):
    head = Heading35a(heading['DISPLAY_HEADING'], heading['NORMAL_HEADING'], bibid)
    return head
