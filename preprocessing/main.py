#!/usr/bin/env python3

from serializer import Serializer

import csv
import time
import argparse

# Positions in csv
GLOBAL_X      = 2
GLOBAL_Y      = 3
GENE          = 8
TRANSCRIPT_ID = 9

def micron_to_pixels(x, y, offset=45_000):
    return (
        (float(x) + 41.61239999999996) / 0.108 - offset,
        (float(y) + 107.97948000000231) / 0.108 - offset,
    )

def serialize(csv_in, bin_out, csv_out, header=True):
    serializer = Serializer()

    gene_tid_pairs_i = 0
    gene_tid_pairs = dict()

    i = 0
    
    start_time = time.time()
    with open(csv_in) as csv_input, open(bin_out, 'wb') as bin_output:
        for line in csv.reader(csv_input, delimiter=','):
            # Skip the header
            if header:
                header = False
                continue

            gene_tid_pair = (line[GENE], line[TRANSCRIPT_ID])
            if gene_tid_pair not in gene_tid_pairs:
                gene_tid_pairs[gene_tid_pair] = gene_tid_pairs_i
                gene_tid_pairs_i += 1

            bin_output.write(
                serializer.to_binary(
                    *micron_to_pixels(line[GLOBAL_X], line[GLOBAL_Y]),
                    gene_tid_pairs[gene_tid_pair]
                )
            )

            i += 1

            if i == 1:
                break

            if time.time() - start_time > 30:
                start_time = time.time()
                print(f'{i} / 419524962 ({i / 419524962 * 100}%)')

    with open(csv_out, 'w') as csv_output:
        writer = csv.writer(csv_output, delimiter=',')

        writer.writerow(['id', 'gene', 'transcript_id'])
        for (gene, tid), value in gene_tid_pairs.items():
            writer.writerow([value, gene, tid])

parser = argparse.ArgumentParser()
parser.add_argument('filename', type=str, help='csv file with transcripts')
parser.add_argument('output', type=str, help='Binary with compressed csv')
parser.add_argument('output_mapping', type=str, help='csv file with mapping to genes and transcript ids')
args = parser.parse_args()

serialize(args.filename, args.output, args.output_mapping)
