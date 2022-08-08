# /bin/env python3

import sys
import logging
import csv
from os import path
from operator import itemgetter

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    pairs = ['60_70', '70_80', '80_90', '90_00']

    filesdir = sys.argv[1]

    changes = []
    frequencies = {}
    changes2 = {}

    for f in pairs:
        with open(path.join(filesdir, f + '.txt'), 'r') as data:
            for line in data:
                res = line.strip().split('\t')
                word, delta, freq = res
                word = word.strip()
                delta = float(delta)
                freq = float(freq)
                if delta == 0.0:
                    continue
                if word not in frequencies:
                    frequencies[word] = []
                frequencies[word].append(freq)
                out = (word, f, delta)
                changes.append(out)
                if word not in changes2:
                    changes2[word] = {p: 0 for p in pairs}
                    changes2[word]['Word'] = word
                changes2[word][f] = delta

    frequencies = {w: sum(frequencies[w]) for w in frequencies}

    TOP = 30
    sorted_changes = [d for d in sorted(changes, key=itemgetter(2), reverse=True) if frequencies[d[0]] > 1000]
    logger.info('Word\tDecades\tDegree\tFrequency')
    logger.info('=============')
    logger.info('Top {} with the strongest change:'.format(TOP))
    for i in sorted_changes[:TOP]:
        logger.info('{}\t{}\t{}\t{}'.format(i[0], i[1], round(i[2], 4), frequencies[i[0]], 4))
    logger.info('=============')
    logger.info('Top {} with the weakest change:'.format(TOP))
    for i in sorted_changes[-TOP:]:
        logger.info('{}\t{}\t{}\t{}'.format(i[0], i[1], round(i[2], 4), frequencies[i[0]], 4))
    logger.info('=============')
    year_changes = {}
    for el in changes:
        if el[1] not in year_changes:
            year_changes[el[1]] = []
        year_changes[el[1]].append(el[2])

    with open('all.tsv', 'w') as f:
        fieldnames = ['Word'] + pairs + ['Frequency']
        writer = csv.DictWriter(f, fieldnames=fieldnames, delimiter='\t', dialect='unix',
                                quoting=csv.QUOTE_NONE)
        writer.writeheader()
        for word in sorted(changes2):
            out = changes2[word]
            out['Frequency'] = int(frequencies[word])
            writer.writerow(out)
