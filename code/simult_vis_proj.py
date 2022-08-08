# python3
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler


def main():
    """
    Produce PCA plot of a word's contextualised embeddings.
    """

    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg('--input', '-i', help='Path to the npz files directory', required=True)
    arg('--target', '-t', help='the target word', required=True)
    arg('--out', '-o', help='Output path for the PCA plot', action="store_true")
    args = parser.parse_args()

    embedding_files = [f.name for f in os.scandir(args.input)
                       if f.name.endswith('.npz') and f.is_file()]

    embeddings = {year.split('.')[0]: None for year in embedding_files}

    target = args.target

    for f in embedding_files:
        embedding = np.load(os.path.join(args.input, f))[target]
        embeddings[f.split('.')[0]] = embedding

    if args.out:
        out_path = args.out
    else:
        out_path = target + '.png'

    x = np.concatenate([embeddings[el] for el in sorted(embeddings)], axis=0)

    class_labels = []
    for el in sorted(embeddings):
        class_labels += [el] * len(embeddings[el])

    x = StandardScaler().fit_transform(x)
    x_2d = PCA(n_components=2).fit_transform(x)

    plt.figure(figsize=(15, 15))
    plt.xticks([]), plt.yticks([])
    plt.title("{} in all decades\n".format(target), fontsize=20)

    class_set = sorted([c for c in set(class_labels)])
    colors = plt.cm.Set1(np.linspace(0, 1, len(class_set)))

    for year in class_set:
        rows = [x == year for x in class_labels]
        matrix = x_2d[rows]
        plt.scatter(matrix[:, 0], matrix[:, 1], color=colors[class_set.index(year)], marker='*',
                    s=40, label=year)

    plt.legend(prop={'size': 15}, loc="best")

    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    print('Saved plot to file: {}'.format(out_path))


if __name__ == '__main__':
    main()
