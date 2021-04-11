from flask import Flask, redirect, request, jsonify
import json
import requests

# settings should go in another file

ES = 'http://es1.wrlc2k.wrlc.org:9200/marchive'

views = {
	'AU' : 'https://wrlc-amu.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_AMU:prod',
	'AULAW' : 'https://wrlc-amulaw.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_AMULAW:01WRLC_AMULAW',
	'CU' : 'https://wrlc-cu.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_CAA:01WRLC_CAA',
	'DC' : 'https://wrlc-doc.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_DOC:01WRLC_DOC_MF',
	'GA' : 'https://wrlc-gal.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_GAL:01WRLC_GAL',
	'GM' : 'https://wrlc-gm.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_GML:01WRLC_GM',
	'GU' : 'https://wrlc-gu.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_GUNIV:01WRLC_GUNIV',
	'GULAW' : 'https://wrlc-gulaw.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_GUNIVLAW:01WRLC_GUNIVLAW',
	'GW' : 'https://wrlc-gwu.primo.exlibrisgroup.com/discovery/search?query={}&sortby=rank&vid=01WRLC_GWA:live',
	'GWMED' : 'https://wrlc-gwahlth.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_GWAHLTH:01WRLC_GWAHLTH',
	'HU' : 'https://wrlc-hu.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_HOW:01WRLC_HOW',
	'MU' : 'https://wrlc-mar.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_MAR:01WRLC_MAR',
	'TR' : 'https://wrlc-trn.primo.exlibrisgroup.com/discovery/search?query={}&vid=01WRLC_TRN:01WRLC_TRN',
	'WR' : 'https://wrlc-scf.primo.exlibrisgroup.com/discovery/search?query={}&search_scope=DiscoveryNetwork&vid=01WRLC_SCF:01WRLC_SCF'

}


app = Flask(__name__)

@app.route('/')
def doc():
    return('legacy catalog redirect service')

@app.route('/cr/<bibid>')
def cr_redirect(bibid):
    # Force the institution, or try to guess
    if request.args.get('inst') and request.args.get('inst').upper() in views.keys():
        inst = request.args.get('inst').upper()
    else:
        inst = False
    # check the index
    r = requests.get(ES + '/bib/' + bibid + '_cr')
    # if there's a record try to find it's analog in primo
    if r.json()['found'] :
        if inst:
            view = views[inst]
        else:
            view = views[r.json()['_source']['institution'][0]]
        if 'oclcnum' in r.json()['_source']:
        	return(redirect(view.format('ocolc,contains,' + r.json()['_source']['oclcnum'][0])))
        elif 'isbn' in r.json()['_source']:
        	return(redirect(view.format('isbn,contains,' + r.json()['_source']['isbn'][0])))
        elif 'title_display' in r.json()['_source']:
        	return(redirect(view.format('title,contains,' + r.json()['_source']['title_display'][0])))
        else:
        	return(redirect(view.format('')))
    # if there's no record, send to list of primo instances
    else:
        if inst != False:
            view = views[inst]
            return(redirect(view.format('')))
        else:
            return(redirect('https://redirects.wrlc.org?notfound=true'))
        
@app.route('/record/<bibid>')
def fetch_record(bibid):
    r = requests.get(ES + '/bib/' + bibid + '_cr')
    if r.json()['found']:
        return(jsonify(r.json()))
    else:
        return("no record with id: " + bibid)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    
