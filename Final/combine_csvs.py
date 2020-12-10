import csv

def loadCSV(input, output, position):
    with open(output, 'a') as file1:
        writer = csv.writer(file1, delimiter=',')
        counter = 0
        with open(input, 'r') as file2:
            reader = csv.reader(file2, delimiter=',')
            for row in reader:
                d = ''.join(row[2:])
                if counter<2000:
                    writer.writerow([d, position])
                    counter+=1
                else:
                    break
    print('Loaded {}'.format(position))


def run():
    filePaths = ['data/TextCSV/de.csv', 'data/TextCSV/ds.csv', 'data/TextCSV/swe.csv']
    postiions = ['Data Engineer', 'Data Scientist', 'Software Engineer']
    outputpath = 'data/TextCSV/combined.csv'

    for pos, path in zip(postiions, filePaths):
        loadCSV(path, outputpath, pos)

run()