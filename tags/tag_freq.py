import csv
import numpy as np
import sys

debug = False
k = 0.5

if __name__ == "__main__":
    # build list of tags
    with open(sys.argv[1], 'r') as f:
        csvin = csv.reader(f)
        tags = {}
        number_tags = 0
        for row in csvin:
            for t in range(0, len(row)):
                if not tags.has_key(row[t]):
                    tags[row[t]] = number_tags
                    number_tags += 1

    freq_matrix = np.zeros((number_tags, number_tags))

    # populate frequency matrix
    with open(sys.argv[1], 'r') as f:
        csvin = csv.reader(f)
        for row in csvin:
            if debug:
                print row
            for t1 in range(0, len(row)):
                for t2 in range(0, len(row)):
                    if t1 != t2:
                        freq_matrix[tags[row[t1]], tags[row[t2]]] += 1

    # normalise frequency
    totals = np.sum(freq_matrix, axis=1)
    freq_matrix_norm = freq_matrix / totals[:, np.newaxis]

    freq_matrix_sorted = np.argsort(freq_matrix_norm, axis=1)[:, ::-1]

    # output top k%
    if len(sys.argv) > 3:
        k = int(sys.argv[3]) / 100.0
    tags_from_indices = [''] * number_tags
    for tag in tags:
        tags_from_indices[tags[tag]] = tag
    with open(sys.argv[2], 'w+') as f:
        csvout = csv.writer(f)
        for t in range(0, number_tags):
            row = [tags_from_indices[t]]
            total_freq = 0
            col = 0
            while total_freq < k:
                row.append(tags_from_indices[freq_matrix_sorted[t, col]])
                if debug:
                    row.append(freq_matrix[t, freq_matrix_sorted[t, col]])
                total_freq += freq_matrix_norm[t, col]
                col += 1
            csvout.writerow(row)