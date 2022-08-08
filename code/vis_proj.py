# python3
# coding: utf-8

import pylab as plot
import numpy as np
from sklearn.decomposition import PCA
import logging
import argparse

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg('--input', '-i', help='Path to the npz file', required=True)
    arg('--word', '-w', help='Ask for a specific word')
    arg('--labels', '-l', help='Plot labels?', action="store_true")
    args = parser.parse_args()

    if args.labels:
        LABELS = True
    else:
        LABELS = False

    embeddings = np.load(args.input)

    if args.word:
        words = [args.word]
    else:
        words = embeddings.files

    year = args.input.split('/')[-1].split('.')[0]

    for word in words:
        array = embeddings[word]
        logger.info('{}, number of points: {}'.format(word, array.shape[0]))
        if array.shape[0] < 3:
            continue
        embedding = PCA(n_components=2)
        y = embedding.fit_transform(array)

        xpositions = y[:, 0]
        ypositions = y[:, 1]

        plot.clf()

        if LABELS:
            for x, y, nr in zip(xpositions, ypositions, range(len(xpositions))):
                plot.scatter(x, y, 2, marker='*', color='green')
                plot.annotate(nr, xy=(x, y), size=2, color='green')
            out = "{}_{}_labels".format(word, year)
        else:
            plot.scatter(xpositions, ypositions, 5, marker='*', color='green')
            out = "{}_{}".format(word, year)
        plot.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
        plot.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
        plot.title("{} in {}'s".format(word, year))

        plot.savefig(out + '_PCA.png', dpi=300, bbox_inches='tight')
        plot.close()
        plot.clf()
