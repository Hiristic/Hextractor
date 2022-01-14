import json
import sys
from pathlib import Path
from elastic_enterprise_search import AppSearch

# Connecting to an instance on Elastic Cloud w/ an App Search private key
app_search = AppSearch(
    "https://imvelo-befed5.ent.eu-central-1.aws.cloud.es.io",
    http_auth="private-rhrakddnnoq2np1tfbpdvod2",
)

# Only executes when run as a script, not as an import.
if __name__ == "__main__":

    #with (examples_dir / "data.json").open() as f:
    #    documents = json.loads(f.read())


    id = [ 'H200' , 'H201' , 'H202' , 'H203' , 'H204' , 'H205' , 'H220' , 'H221' , 'H222' , 'H223' , 'H224' , 'H225' , 'H226' , 'H228' , 'H229' , 'H230' , 'H231' , 'H240' , 'H241' , 'H242' , 'H250' , 'H251' , 'H252' , 'H260' , 'H261' , 'H270' , 'H271' , 'H272' , 'H280' , 'H281' , 'H290']
    descr = ['Instabilt, explosivt.' , 'Explosivt. Fara för massexplosion' , 'Explosivt. Allvarlig fara för splitter och kaststycken.' , 'Explosivt. Fara för brand, tryckvåg eller splitter och kaststycken.' , 'Fara för brand eller splitter och kaststycken' , 'Fara för massexplosion vid brand' , 'Extremt brandfarlig gas' , 'Brandfarlig gas' , 'Extremt brandfarlig aerosol' , 'Brandfarlig aerosol' , 'Extremt brandfarlig vätska och ånga' , 'Mycket brandfarlig vätska och ånga' , 'Brandfarlig vätska och ånga' , 'Brandfarligt fast ämne' , 'Tryckbehållare: Kan sprängas vid uppvärmning' , 'Kan reagera explosivt även i frånvaro av luft' , 'Kan reagera explosivt även i frånvaro av luft vid förhöjt tryck och/eller temperatur' , 'Explosivt vid uppvärmning' , 'Brandfarligt eller explosivt vid uppvärmning' , 'Brandfarligt vid uppvärmning' , 'Spontanantänder vid kontakt med luft' , 'Självupphettande. Kan börja brinna.' , 'Självupphettande i stora mängder. Kan börja brinna.' , 'Vid kontakt med vatten utvecklas brandfarliga gaser som kan självantända' , 'Vid kontakt med vatten utvecklas brandfarliga gaser' , 'Kan orsaka eller intensifiera brand. Oxiderande.' , 'Kan orsaka brand eller explosion. Starkt oxiderande.' , 'Kan intensifiera brand. Oxiderande.' , 'Innehåller gas under tryck. Kan explodera vid uppvärmning.' , 'Innehåller kyld gas. Kan orsaka svåra köldskador.' , 'Kan vara korrosivt för metaller']
    type = ['Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror', 'Fysikaliska faror']
    lists = ['id', 'descr', 'type']

    data = {listname: globals()[listname] for listname in lists}
    #print(data)
    data2 = {'id': "x", 'descr': "d", 'type': 't'}
    with open('Fysikaliska_faror.json', 'w') as outfile:
        for x in range(len(id)): 
            #print(id[x]) 
            data2['id'] = id[x]
            data2['descr'] = descr[x]
            data2['type'] = type[x]
            print(data2)
            #index_doc(data2)
            json.dump(data2, outfile, indent=4)
            #print(json_out)

    print(data2)

    #with open('Fysikaliska_faror.json', 'w') as outfile:
     #   json.dump(data, outfile, indent=4)

