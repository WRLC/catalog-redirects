import mysql.connector
import settings
from flask import request

# dictionary of IZ views
views = {
    'AL': 'https://wrlc-amulaw.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_AMULAW:01WRLC_AMULAW',
    'AU': 'https://wrlc-amu.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_AMU:prod',
    'CU': 'https://wrlc-cu.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_CAA:01WRLC_CAA',
    'DC': 'https://wrlc-doc.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_DOC:01WRLC_DOC_MF',
    'GA': 'https://wrlc-gal.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_GAL:01WRLC_GAL',
    'GM': 'https://wrlc-gm.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_GML:01WRLC_GML',
    'GT': 'https://wrlc-gu.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_GUNIV:01WRLC_GUNIV',
    'GTL': 'https://wrlc-gulaw.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_GUNIVLAW:01WRLC_GUNIVLAW',
    'GW': 'https://wrlc-gwu.primo.exlibrisgroup.com/discovery/search?query={}&sortby=rank&vid=01WRLC_GWA:live',
    'HD': 'https://wrlc-gu.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_GUNIV:01WRLC_GUNIV',
    'HI': 'https://wrlc-gwahlth.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_GWAHLTH:01WRLC_GWAHLTH',
    'HU': 'https://wrlc-hu.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_HOW:01WRLC_HOW',
    'HL': 'https://wrlc-hu.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_HOW:Law_Library',
    'JB': 'https://wrlc-gwalaw.primo.exlibrisgroup.com/discovery/search?query={'
          '}&vid=01WRLC_GWALAW:PrimoTaskForceVersion',
    'MU': 'https://wrlc-mar.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_MAR:01WRLC_MAR',
    'TR': 'https://wrlc-trn.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_TRN:01WRLC_TRN',
    'WR': 'https://wrlc-scf.primo.exlibrisgroup.com/discovery/search?query={'
          '}&search_scope=DiscoveryNetwork&vid=01WRLC_SCF:01WRLC_SCF'
}

cu = {
    'CU',
    'LI',
}

hu = {
    'HU',
    'HS',
}

wr = {
    'WR'
    'HD',
    'DA',
    'E-Resources',
    'LL',
    'E-GovDoc',
}


def db_query(query, params, queryall=True):
    # database connection settings from settings.py
    cxn = mysql.connector.connect(
        user=settings.db['user'],
        password=settings.db['password'],
        host=settings.db['host'],
        database=settings.db['database']
    )
    cursor = cxn.cursor(dictionary=True)  # create a cursor object

    cursor.execute(query, params)  # execute the query
    if queryall is True:
        r = cursor.fetchall()
    else:
        r = cursor.fetchone()

    cursor.close()  # close the cursor
    cxn.close()  # close the connection
    return r


def get_record(bibid):
    query = "SELECT t.TITLE_BRIEF, t.ISBN, t.ISSN, l.LIBRARY_NAME " \
            "FROM BIB_TEXT t, BIB_MASTER m, LIBRARY l " \
            "WHERE t.BIB_ID = m.BIB_ID AND " \
            "m.LIBRARY_ID = l.LIBRARY_ID AND " \
            "t.BIB_ID = %s"
    params = (bibid,)
    r = db_query(query, params, False)
    return r


def get_record_view(bibid):
    query = "SELECT t.*, l.LIBRARY_NAME " \
            "FROM BIB_TEXT t, BIB_MASTER m, LIBRARY l " \
            "WHERE t.BIB_ID = m.BIB_ID AND " \
            "m.LIBRARY_ID = l.LIBRARY_ID AND " \
            "t.BIB_ID = %s"
    params = (bibid,)
    r = db_query(query, params, False)
    return r


def get_headings(bibid):
    # get the oclcnums
    headings_query = "SELECT DISPLAY_HEADING, NORMAL_HEADING FROM BIB_INDEX " \
                     "WHERE BIB_ID = %s AND INDEX_CODE = '035A'"
    params = (bibid,)
    r = db_query(headings_query, params)
    return r


def set_instcode(instcode):
    if instcode in cu:
        return 'CU'
    elif instcode in hu:
        return 'HU'
    elif instcode in wr:
        return 'WR'
    else:
        return instcode


def set_redirect(field, label, view):
    if field and field != '':
        return view.format(label + ',contains,' + field)
    else:
        return


def guess_institution():
    # Force the institution, or try to guess
    if request.args.get('inst') and request.args.get('inst').upper() in views.keys():
        inst = request.args.get('inst').upper()
    else:
        inst = False

    return inst
