import csv, glob, json, os

BASEDIR = os.path.dirname(os.path.realpath(__file__))
DATADIR = os.path.join(BASEDIR, 'datafiles')

def main():

    csvfile = os.path.join(BASEDIR, 'TrainingTypes.csv')
    training_type_records = {}

    with open(csvfile) as infile:
        training_type_reader = csv.reader(infile, delimiter=';')
        for row in training_type_reader:
            training_type_records[(row[0], row[1])] = row[2]

    idx = 0
    features = {'total_timer_time', 'training_type_name'}
    valid_files = {}
    print('JSONs with no records:\n')
    for filename in glob.iglob(DATADIR + '/*.json'):
        info = filename.split('_')
        training_type_name = training_type_records[(info[2], info[1])]

        with open(filename) as infile:
            data = json.load(infile)

        try:
            for record in data['records']:
                features.update(record.keys())
        except KeyError:
            idx += 1
            print('{:>4} {}'.format(idx, os.path.basename(filename)))
            continue

        valid_files[filename] = training_type_name

    print('\n\nWriting JSON records to csv...\n')
    with open('out.csv', 'w', newline='') as outfile:
        datawriter = csv.DictWriter(outfile, fieldnames=features, delimiter=';')
        datawriter.writeheader()
        for filenum, filename in enumerate(valid_files, 1):
            print('{:>4} {}'.format(filenum, os.path.basename(filename)))
            with open(filename) as infile:
                data = json.load(infile)
            for record in data['records']:
                record['training_type_name'] = valid_files[filename]
                record['total_timer_time'] = data['activity'].get('total_timer_time', '')
                datawriter.writerow(record)

    print('\nDONE!\n')

if __name__ == '__main__':
    main()
