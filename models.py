from utilities import views, set_instcode


###########
# Objects #
###########

# Record object
class Record:
    def __init__(self, title, isbn, issn, library_name, bibid):
        self.title = title
        self.isbn = isbn
        self.issn = issn
        self.library_name = library_name
        self.bibid = bibid

    # set the view based on the institution code in the record
    def set_view(self):
        try:
            view = views[self.library_name]  # set view based on institution code
        except KeyError:
            view = views['WR']  # default to WR if not in list
        return view


# Heading35a object
class Heading35a:
    def __init__(self, display_heading, normal_heading, bibid):
        self.display_heading = display_heading
        self.normal_heading = normal_heading
        self.bibid = bibid

    # set the oclcnum from the heading
    def set_oclcnum(self):
        if self.display_heading.startswith('(OCoLC)'):  # if the display heading starts with (OCoLC)
            oclcnum = self.normal_heading.replace('(OCoLC)', '')  # remove any extraneous '(OCoLC)'s
            return oclcnum


####################
# Helper functions #
####################

# set the record object
def set_record(r, bibid, inst):
    if inst:  # if the institution code is passed in
        instcode = inst  # use that institution code
    else:  # if the institution code is not passed in
        instcode = set_instcode(r['LIBRARY_NAME'])  # set the institution code from the database
    record = Record(r['TITLE_BRIEF'], r['ISBN'], r['ISSN'], instcode, bibid)  # create a record object
    return record


# set the heading object
def set_head(heading, bibid):
    head = Heading35a(heading['DISPLAY_HEADING'], heading['NORMAL_HEADING'], bibid)
    return head
