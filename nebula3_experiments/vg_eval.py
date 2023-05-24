import sys
from PIL import Image
import requests
import os
from scipy.optimize import linear_sum_assignment
# sys.path.append('/notebooks')
# sys.path.append('/notebooks/nebula_vg_driver/visual_genome')
# curr_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
# sys.path.append(curr_dir)
# directory = os.path.abspath(__file__)
# os.path.abspath(os.path.join(__file__, os.pardir))

import visual_genome.local as vg
# import nebula_vg_driver.visual_genome.local as vg

import json
import copy
import subprocess

import numpy as np
import torch
import spacy
import nltk
from spacy_wordnet.wordnet_annotator import WordnetAnnotator 
from sentence_transformers import SentenceTransformer
from experts.pipeline.api import PipelineConf

VG_DATA = '/storage/vg_data'
settings = None

def spice_get_triplets(text):
    SPICE_FNAME = '/app_data/SPICE-1.0/spice-1.0.jar'
    INP_FNAME = '/tmp/example.json'
    OUT_FNAME = '/tmp/example_output.json'

    inp = {
        'image_id': 1,
        'test': "",
        'refs': [text],        
    }
    json.dump([inp],open(INP_FNAME,'w'))
    p = subprocess.Popen('java -Xmx8G -jar {} {} -detailed -silent -subset -out {}'.format(SPICE_FNAME,INP_FNAME,OUT_FNAME),shell=True,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
    p.communicate()
    outp = json.load(open(OUT_FNAME,'r'))
    return [x['tuple'] for x in outp[0]['ref_tuples']]
    

def cosine_sim(x,y):
    return np.dot(x,y) / (np.linalg.norm(x)*np.linalg.norm(y))

def compare_cross_lists(l1, l2):
    return np.any([x in l2 for x in l1])

def triplet_from_rel(rel):
    return (rel.subject.names[0], rel.predicate, rel.object.names[0])

def tuples_from_sg(sg, triplets_size=[1,2,3]):
    rel_triplets = list(set(map(triplet_from_rel,sg.relationships)))
    obj_tuples = []
    attr_tuples = []
    for obj in sg.objects:
        obj_tuples.append((obj.names[0],))
        for attr in obj.attributes:
            attr_tuples.append((obj.names[0], attr))
    return [x for x in list(set(obj_tuples))+list(set(attr_tuples))+rel_triplets if len(x) in triplets_size]

def get_sc_graph(id):
    global settings
    if settings is None:
        settings = PipelineConf()
    basedir = settings['vg_data_basedir']
    return vg.get_scene_graph(id, images=basedir,
                    image_data_dir=basedir+'/by-id/',
                    synset_file=basedir+'/synsets.json')
rel_to_triplet = lambda rel: (rel['subject'].id, rel['predicate'], rel['object'].id)


def recall_paragraph_sg(paragraph, sg, **kwargs):
    ipc_triplets = spice_get_triplets(paragraph)
    rel_triplets = list(map(triplet_from_rel,sg.relationships))
    return total_recall_triplets(rel_triplets, ipc_triplets, **kwargs)

class SimilarityManager:
    def __init__(self):
        # nlp = spacy.load('en_core_web_sm')
        nlp = spacy.load('en_core_web_lg')
        nlp.add_pipe("spacy_wordnet", after='tagger')
        # nlp.add_pipe("spacy_wordnet", after='tagger', config={'lang': nlp.lang})
        self.nlp = nlp
        self.similarity_model = SentenceTransformer('sentence-transformers/paraphrase-xlm-r-multilingual-v1')
        if torch.cuda.device_count() > 0:
            self.similarity_model.cuda()

    def similarity(self, src, target):
        rc = []
        s1 = self.nlp(src)
        s2 = self.nlp(target)
        for w in s1:
            if w.pos_ not in ['NOUN', 'ADJ', 'ADV', 'VERB', 'PROPN'] and len(s1)>1:
                continue
            rc.append(max([w.similarity(x) for x in s2]))
        return np.mean(rc)
    
    def compare_cross_synsets(self, text1, text2):
        t1 = self.nlp(text1)
        t2 = self.nlp(text2)
        return compare_cross_lists([x._.wordnet.synsets() for x in t1], [x._.wordnet.synsets() for x in t2])
    
    def compare_triplet(self, t1, t2, method='bert', invert_src=False, invert_dst=False, **kwargs):
        if len(t1) != len(t2):
            return 0.
        sim = 1.
        if method=='bert':
            if len(t1)==2:     # attribute tuple, invert
                if invert_src:
                    t1 = [t1[1], t1[0]]
                if invert_dst:
                    t2 = [t2[1], t2[0]]
            embs = self.similarity_model.encode([' '.join(t1).lower(), ' '.join(t2).lower()])
            sim = cosine_sim(*embs)
        elif method=='meteor':
            return nltk.translate.meteor_score.single_meteor_score(' '.join(t1).lower().split(),' '.join(t2).lower().split())
        else:
            for x,y in zip(t1,t2):
                if method=='wordnet':
                    sim *= self.compare_cross_synsets(x,y)
                elif method=='spacy':
                    sim *= self.similarity(x,y)
                else:
                    print("Unknown similarity method: {}".format(method))
        return sim

def greedy_match(similarity_matrix):
    A = similarity_matrix
    indices = []
    while np.any(A>0):
        ind = np.unravel_index(np.argmax(A, axis=None), A.shape)
        indices.append(ind)
        A[ind[0]]=0
        A[:,ind[1]]=0
        
    return indices

def hungarian_match(similarity_matrix):
    B = similarity_matrix
    return list(zip(*linear_sum_assignment(-B)))

class VGEvaluation:
    def __init__(self):
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        self.smanager = SimilarityManager()
        
    def recall_triplet(self, src, dst, **kwargs):
        if not dst:
            return 0.    
        scores = [self.smanager.compare_triplet(src,x, **kwargs) for x in dst]
        return max(scores)

    #src: A list of triplets
    #dst: A list of triplets
    def recall_triplets(self, src, dst, **kwargs):
        rc = [self.recall_triplet(x,dst, **kwargs) for x in src]
        return rc
        # return np.mean(rc)
        
    def compute_triplet_scores(self, src, dst, **kwargs):
        scores_matrix = [[self.smanager.compare_triplet(x,y,**kwargs) for y in dst] for x in src]
        return np.array(scores_matrix)  
    
    def compute_precision_recall(self, src, dst, assignment_method="hungarian", debug_print=False, **kwargs) -> (float, float):
        if not src or not dst:
            return (0., 0.)
        A = self.compute_triplet_scores(src,dst,**kwargs)
        if assignment_method == 'greedy':
            func = greedy_match
        elif assignment_method == 'hungarian':
            func = hungarian_match
        elif assignment_method == 'relaxed':
            recall = self.recall_triplets_mean(dst,src, **kwargs)
            precision = self.recall_triplets_mean(src,dst, **kwargs)
            return (precision, recall)
        else:
            raise "compute_precision_recall: Unknown method"
        res = func(A.copy())
        if debug_print:
            for ind in res:
                print("{} --- {} ({})".format(src[ind[0]], dst[ind[1]], A[ind]))
        return np.sum([A[x] for x in res]) / A.shape
          
             
    def recall_triplets_mean(self, src, dst, **kwargs):
        rc = self.recall_triplets(src,dst,**kwargs)
        if not rc:
            return 0.
        return np.mean(rc)

    def total_recall_triplets(self, src_triplets, dst_triplets, methods=('bert', 'bert', 'bert')):
        total_recall = []
        for i in [1,2,3]:
            dst_i = [x for x in dst_triplets if len(x)==i]
            src_i = [x for x in src_triplets if len(x)==i]
            total_recall.extend(self.recall_triplets(src_i,dst_i,method=methods[i-1]))
        return total_recall

# objetc based avoiding loading             vg.get_all_image_data(images_path) per image
class Sg_handler():
    def __init__(self, images_path, image_data_dir='data/by-id/',
                    synset_file='data/synsets.json') -> None:
        self.image_data_dir = image_data_dir
        self.synset_file = synset_file
        if type(images_path) is str:
            # Instead of a string, we can pass this dict as the argument `images`
            self.images = {img.id: img for img in vg.get_all_image_data(images_path)}

        pass
    def get_scene_graph(self, image_id):
    # Load a single scene graph from a .json file.

        fname = str(image_id) + '.json'
        image = self.images[image_id]
        data = json.load(open(self.image_data_dir + fname, 'r'))

        scene_graph = vg.parse_graph_local(data, image)
        scene_graph = vg.init_synsets(scene_graph, self.synset_file)
        return scene_graph

