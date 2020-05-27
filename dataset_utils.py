import glob
import json
import os
import random
import shutil
import sys

from dataclasses import dataclass
from pathlib import Path
from textwrap import wrap

SEED = 99999
BIOMED_SIZE = 50
REST_SIZE = 75
BIOMED = 'biorxiv_medrxiv'

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

    with open(paper_path, 'a', encoding='utf8') as fpapers, open(table_path, 'a', encoding='utf8') as ftable:
        for pname in papers_sample:
            paper = Paper.from_json(pname)
            paper_dir = Path(pname).parents[1]
            paper_target_dir = dataset_path / paper_dir.parts[-1]
            if not paper_target_dir.exists():
                paper_target_dir.mkdir()
            shutil.copy(pname, paper_target_dir)

            fpapers.write(f"{20 * '#'}-{paper.id}-{20 * '#'}\n")
            fpapers.write('\n'.join(wrap(f'title: {paper.title}')) + '\n')
            fpapers.write('\n'.join(wrap(f'abstract: {paper.abstract}')) + '\n\n')
            ftable.write(f'{paper.id}: \n')

if __name__ == '__main__':
    random.seed(SEED)
    dataset_path, target_dir = sys.argv[1], sys.argv[2]
    build_dataset(dataset_path, target_dir)