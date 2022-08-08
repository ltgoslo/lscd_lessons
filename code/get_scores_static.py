# python3
# coding: utf-8

import gensim
import numpy as np
import argparse
import logging

if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO
    )
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg("--targets", "-t", help="Target word list", required=True)
    arg("--emb0", "-e0", help="The first model", required=True)
    arg("--emb1", "-e1", help="The second model", required=True)

    args = parser.parse_args()

    word_file = args.targets
    words = {}

    for line in open(word_file).readlines():
        word = line.strip()
        words[word] = []
    logger.info(f"We have {len(words)} target words")

    model0 = gensim.models.KeyedVectors.load(args.emb0)
    model0.init_sims(replace=True)
    model1 = gensim.models.KeyedVectors.load(args.emb1)
    model1.init_sims(replace=True)

    oov = 0

    for word in words:
        if word not in model0 or word not in model1:
            oov += 1
            logger.info(f"{word} missing")
            continue
        vector0 = model0[word]
        vector1 = model1[word]
        freq0 = model0.vocab[word].count
        freq1 = model1.vocab[word].count
        mean = np.mean([freq0, freq1])
        score = 1 - np.dot(vector0, vector1)
        words[word] = score, mean

    logger.info(f"{oov} words skipped out of {len(words)}")

    for word in sorted(words):
        print(f"{word}\t{words[word][0]}\t{words[word][1]}")
