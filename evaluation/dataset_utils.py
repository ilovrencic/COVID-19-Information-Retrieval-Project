import glob
import json
import os
import random
import shutil
import sys

from collections import Counter
from contextlib import ExitStack
from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap

SEED = 99999
BIOMED_SIZE = 50
REST_SIZE = 75
BIOMED = 'biorxiv_medrxiv'
NUM_QUERIES = 3

@dataclass
class Paper:
    id: str
    title: str
    abstract: str

    @classmethod
    def from_json(cls, path):
        with open(path, 'r') as fd:
            data = json.load(fd)
        
        id = data['paper_id']
        title = data['metadata']['title']
        abstract = '\n'.join([record['text'] for record in data['abstract']])
        return cls(id, title, abstract)

def build_dataset(path, target_dir):
    papers_all = glob.glob(f'{path}/**/*.json', recursive=True)
    papers_bio = [pname for pname in papers_all if BIOMED in pname]
    papers_rest = set(papers_all) - set(papers_bio)
    
    papers_rest_sample = random.sample(papers_rest, REST_SIZE)
    papers_bio_sample = random.sample(papers_bio, BIOMED_SIZE)
    papers_sample = papers_rest_sample + papers_bio_sample

    target_dir = Path(target_dir)
    target_dir.mkdir()

    dataset_path = target_dir / 'dataset'
    dataset_path.mkdir()
    
    paper_path = target_dir / 'papers.txt'
    table_path = target_dir / 'annotations.txt'

    with open(paper_path, 'w', encoding='utf8') as fpapers, open(table_path, 'w', encoding='utf8') as ftable:
        for pname in papers_sample:
            paper = Paper.from_json(pname)

            if not paper.abstract.strip() or not paper.title.strip():
                continue

            paper_dir = Path(pname).parents[1]
            paper_target_dir = dataset_path / paper_dir.parts[-1]
            if not paper_target_dir.exists():
                paper_target_dir.mkdir()
            shutil.copy(pname, paper_target_dir)

            fpapers.write(f"{20 * '#'}-{paper.id}-{20 * '#'}\n")
            fpapers.write('\n'.join(wrap(f'title: {paper.title}')) + '\n')
            fpapers.write('\n'.join(wrap(f'abstract: {paper.abstract}')) + '\n\n')
            ftable.write(f'{paper.id}: \n')
    

def dataset_to_directory(dataset_dir, target_dir):
    dataset_dir = Path(dataset_dir)
    target_dir = Path(target_dir)
    target_dir.mkdir()

    for child_dir in dataset_dir.iterdir(): 
        for paper_file in child_dir.iterdir():
            pname = str(paper_file)
            paper = Paper.from_json(str(paper_file))

            if not paper.abstract.strip() or not paper.title.strip():
                continue
            
            shutil.copy(pname, target_dir)


def merge_annotations(annotations, target_file):
    assert len(annotations) == NUM_QUERIES

    with ExitStack() as stack, open(target_file, 'w') as ftarget:
        files = [stack.enter_context(open(fname)) for fname in annotations]
        for rows_triple in zip(*files):
            row_ids = set([row.strip().split(':')[0] for row in rows_triple])
            assert len(row_ids) == 1
            paper_id = list(row_ids)[0]
            
            row_results = [row.strip().split(':')[1].split(',') for row in rows_triple]
            row_results = [[r.strip() for r in res]for res in row_results]
            if any(result == ['-'] for result in row_results):
                final_annotations = '-'
            else:
                final_annotations = ','.join([Counter(r).most_common()[0][0] for r in zip(*row_results)])

            ftarget.write(f'{paper_id}: {final_annotations}\n')
            
def ispravi_lovrencicevo_oznacavanje(file, target_file):
    d = {'R': 'R', 'N': 'I'}
    with open(file, 'r') as f1, open(target_file, 'w') as f2:
        for line in f1:
            id, annotations = line.strip().split(':')
            
            annotations = annotations.strip()
            if annotations != '-': 
                assert len(annotations) == 3
                annotations = ', '.join(d[a] for a in annotations)
            
            f2.write(f"{id}: {annotations}\n")

def results2tuple(result_file):
    results = []
    with open(result_file, 'r') as f:
        for line in f:
            id, score = line.strip().split(':')
            results.append((id.strip(), float(score)))
    return results

def annotations2tuple(annotations_file):
    annotations = []
    with open(annotations_file, 'r') as f:
        for line in f:
            id, annot = line.strip().split(':')
            annot = [a.strip() for a in annot.split(',')]
            if annot == ['-']: continue
            annotations.append((id, annot))
    return annotations

if __name__ == '__main__':
    random.seed(SEED)
    # dataset_path, target_dir = sys.argv[1], sys.argv[2]
    # build_dataset(dataset_path, target_dir)
    # dataset_to_directory('data/dataset', 'dataset')
    # ispravi_lovrencicevo_oznacavanje('data/annotations-ivan.txt', 
    #                                  'data/annotations-ivan-ispravno.txt')
    annotations = ('data/annotations-buha.txt', 
                   'data/annotations-ivan-ispravno.txt',
                   'data/annotations-mario.txt')
    # merge_annotations(annotations, 'annotations.txt')
    print(results2tuple('results/final_transmission.txt')[:3])