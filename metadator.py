"""Tool for matching system numbers with their uuids in digital library."""
from modules import config, pull, reports
import csv


def process_data(configuration, counter):
    """Read csv and try to match."""
    with open('./data/kramerius_in_856_latest.csv') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        uuidlist = list()
        results = dict()
        results['ok'] = dict()
        results['unresolved'] = dict()

        for row in reader:
            uuid = row[1]
            uuidlist.append(uuid)

        oai_target = pull.Site(configuration['TARGETS']['OAI'],
                               user=None, passw=None)
        fedora_target = pull.Site(location=configuration['TARGETS']['FEDORA'],
                                  user=configuration['AUTH']['FEDORA_USER'],
                                  passw=configuration['AUTH']['FEDORA_PASS'])
        index = pull.oai_index(oai_target.location)

        for doc in index['response']["docs"]:
            if doc['PID'] not in uuidlist:
                print('Lookup system number for ' + doc['PID'])
                sysno = pull.fedora_record_identif(fedora_target.location,
                                                   fedora_target.user,
                                                   fedora_target.passw,
                                                   uuid=doc['PID'])
                if sysno is None:
                    counter.add('unresolved')
                    results['unresolved'][doc['PID']] = None
                else:
                    counter.add('resolved')
                    results['ok'][doc['PID']] = sysno

                counter.add('total')

        counter.report()
        return results


def write_outfile(results):
    """Write output."""
    with open('./data/856_kramerius_export.txt', 'a') as outfile:
        # from dict with uuid keys and sysno values, generate file with lines
        for key, val in results['ok'].items():
            line1 = str(val) + ' 85640 L $$uhttps://kramerius.techlib.cz/search/handle/' + key + '$$yDigitalizovany dokument\n'
            line2 = str(val) + ' BAS   L di\n'
            outfile.write(line1)
            outfile.write(line2)
        for key, val in results['unresolved'].items():
            line1 = 'SYSNO' + ' 85640 L $$uhttps://kramerius.techlib.cz/search/handle/' + key + '$$yDigitalizovany dokument\n'
            line2 = 'SYSNO' + ' BAS   L di\n'
            outfile.write(line1)
            outfile.write(line2)


if __name__ == '__main__':
    configuration = config.load_config("./configuration/config.json")
    missing_counter = reports.Counter()
    results = process_data(configuration, missing_counter)
    write_outfile(results)
