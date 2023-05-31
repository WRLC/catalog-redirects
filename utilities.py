import mysql.connector
import settings

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


def get_record(bibid, query, queryall=True):
    # database connection settings from settings.py
    cxn = mysql.connector.connect(
        user=settings.db['user'],
        password=settings.db['password'],
        host=settings.db['host'],
        database=settings.db['database']
    )
    cursor = cxn.cursor(dictionary=True)  # create a cursor object

    params = (bibid,)  # set the bibid as the parameter
    cursor.execute(query, params)  # execute the query
    if queryall is True:
        r = cursor.fetchall()
    else:
        r = cursor.fetchone()

    cursor.close()  # close the cursor
    cxn.close()  # close the connection
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
