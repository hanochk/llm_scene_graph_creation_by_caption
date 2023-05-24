# export PYTHONPATH=/notebooks/pip_install/
"""
preliminaries:
# cp -p /datasets/vg_data/image_data.json to /inputs/vg-data-checkpoint
install packages;
nebula3-vg-driver 
nebula3-experiments

"""
import numpy as np
import nltk
import tqdm 
import torch 
# nltk.download('punkt')
# from nltk import tokenize
# 16-A100(40G) machine, our largest model with ViT-G and FlanT5-XXL 
import os
os.environ["TRANSFORMERS_CACHE"] = "/storage/hft_cache"
os.environ["TORCH_HOME"] = "/storage/torch_cache"
os.environ["CONFIG_NAME"] = "giltest"  # implicit overwrite the default by  : "vg_data_basedir": "/storage/vg_data"

from nebula3_experiments.ipc_utils import *
# sys.path.insert(0, "/notebooks/pipenv")
# sys.path.insert(0, "/notebooks/nebula3_database")
# sys.path.insert(0,"/notebooks/nebula3_experiments")
# sys.path.insert(0, "/notebooks/")
from nebula3_experiments.vg_eval import Sg_handler, spice_get_triplets, get_sc_graph, tuples_from_sg, VGEvaluation

from blip2 import *
import pickle
import pandas as pd
import requests

def vqa_blip2_request_uservice(image_url, question):
    headers = {
        'accept': '*/*',
        # requests won't add a boundary if this header is set when you pass files=
        # 'Content-Type': 'multipart/form-data',
    }

    # files = {
    #     'image': (None, 'http://74.82.29.209:9000//datasets/media/movies/1388863_fullriverred_499613.jpeg'),
    #     'question': (None, 'what is the left person in the image holding in his hand?'),
    # }
    files = {
        'image': (None, image_url),
        'question': (None, question),
    }

    response = requests.post('http://124.70.217.159:8086/infer', headers=headers, files=files)
    print(response.json())
    return response.json()


match_head = "itc" #"itc" # "itm"
vqa = True
obj_verb_obj = True
predefined_ipc = True
use_prefix = False

blip = BLIP2(model="blip2") #file, caption, file_or_url='file'

prefix_prompt = "A photo of a"
use_prefix_str = ''
if use_prefix:
    use_prefix_str = '_use_prefix'
    if vqa:
        raise
if vqa:
    vqa_str = '_vqa'

predefined_ipc_str = ''
if predefined_ipc:
    image_ids_related_to_ipc = [2395479, 2323701,  2410301, 2340766]#[2328018, 2336194, 2337655, 2320416]#2336194: 2*elephabnt 2337655 lady behind surfboard #[2324582, 2331094, 2323701, 2340749, 2344612]
    predefined_ipc_str = '_predefined_ipc'

#"ipc_200"
#arango_host = "http://172.83.9.249:8529"

# dialog = BLIP2GPTDialog(blip=blip)

with open(os.path.join('/notebooks/nebula3_experiments/relation.pkl'), 'rb') as f:
     relations_uniq_all = pickle.load(f)

csv_file_name = 'results_ipc_relation_best_vs_rand_' + str(match_head) + str(use_prefix_str) + str(vqa_str) + str(predefined_ipc_str) +'.csv'
result_path = '/notebooks/nebula3_experiments'

results = list()
n_rand_relationships = 10
gt_dist_to_2nd_best_dist = list()
for inx, ipc_id in enumerate(tqdm.tqdm(image_ids_related_to_ipc)):
    ipc = get_visual_genome_record_by_ipc_id(ipc_id)
    # vg_ind_related_to_ipc = [ix for ix , x in enumerate(ipc_data) if x['image_id']==ipc_id][0]
    # ipc = ipc_data[vg_ind_related_to_ipc]
    image_id = os.path.basename(ipc['url'])
    image_path = os.path.join('/datasets/visualgenome/VG', image_id)
    # from PIL import Image
    # image = Image.open(image_path).convert('RGB')   

    sg = get_sc_graph(ipc['image_id'])
    for ib, rel in enumerate(sg.relationships):
        obj_dict = dict()
        if use_prefix:
            obj_rel_obj = "{0} {1} {2} {3}".format(prefix_prompt, rel.subject, rel.predicate, rel.object)
        else:
            obj_rel_obj = "{0} {1} {2}".format(rel.subject, rel.predicate, rel.object)

        if obj_verb_obj and not(rel.subject.names[0].lower() == 'man' or rel.subject.names[0].lower() == 'woman' \
             or rel.subject.names[0].lower() == 'boy' or rel.subject.names[0].lower() == 'girl' \
                 or rel.subject.names[0].lower() == 'person' or rel.subject.names[0].lower() == 'lady' or rel.subject.names[0].lower() == 'skier'):
            continue
        
        manual = False
        if manual:
            continue

        itc_score = blip.process_image_and_captions(file=image_path, caption=obj_rel_obj, match_head = match_head)
        itc_gt = itc_score.detach().cpu().numpy()[0].item()

        obj_dict = ({'image_id':image_id, 'enum' :0, 'it_dist':itc_gt, 'tuple': obj_rel_obj})
        results.append(obj_dict)

        if vqa:
            q_questions = dict()
            q_questions.update({'do':"Question: What does the {0} do? Answer:" .format(rel.subject)})
            q_questions.update({'wears': "Question: What does the {0} wear? Answer:" .format(rel.subject)})
            q_questions.update({'holds': "Question: What does the {0} hold? Answer:" .format(rel.subject)})
            q_questions.update({'relation': "Question: What is the relation between {0} and {1} shown in the image? Answer:" .format(rel.subject, rel.object)})
            q_questions.update({'relationship': "Question: What is the relationship between {0} and {1} shown in the image? Answer:" .format(rel.subject, rel.object)})
            # Question: What is the relation between car and surfboard shown in the image? Answer:
            # What is the connection between lady and man
            # question = "what the {0} wears" .format(rel.subject)
            for q_question_key, q_question_val in q_questions.items():
                question = q_question_val
                relation_vqa = vqa_blip2_request_uservice(ipc['url'], question)
                if q_question_key.lower() == 'do':
                    vqa_obj_rel_obj = "{0} {1}".format(rel.subject, relation_vqa['answer'])
                elif q_question_key.lower() == 'wears' or q_question_key.lower() == 'holds':
                    vqa_obj_rel_obj = "{0} {1} {2}".format(rel.subject, q_question_key.lower(), relation_vqa['answer'])
                elif (q_question_key.lower() == 'relation' or q_question_key.lower() == 'relationship'):
                    if len(relation_vqa['answer'].split(' ')) ==1:
                        vqa_obj_rel_obj = "{0} {1} {2}".format(rel.subject, relation_vqa['answer'], rel.object)
                    else:
                        vqa_obj_rel_obj = "{0}".format(relation_vqa['answer'])
                else:
                    raise
                # compute_precision_recall
                itc_score = blip.process_image_and_captions(file=image_path, caption=vqa_obj_rel_obj, match_head = match_head)
                itc_ = itc_score.detach().cpu().numpy()[0].item()
                obj_dict = ({'image_id':image_id, 'enum' :n_rand_relationships, 'it_dist':itc_, 'tuple': vqa_obj_rel_obj, 'question': question})
                results.append(obj_dict)

# Random relationship
        relation_rand = np.random.choice(relations_uniq_all, n_rand_relationships, replace=False)
        itc_dist_rand_rel = list()
        for ix, rel_rnd in enumerate(relation_rand):
            if use_prefix:
                rnd_obj_rel_obj = "{0} {1} {2} {3}".format(prefix_prompt, rel.subject, rel_rnd, rel.object)
            else:
                rnd_obj_rel_obj = "{0} {1} {2}".format(rel.subject, rel_rnd, rel.object)
            itc_score = blip.process_image_and_captions(file=image_path, caption=rnd_obj_rel_obj, match_head = match_head)
            itc_ = itc_score.detach().cpu().numpy()[0].item()
            itc_dist_rand_rel.append(itc_)
            obj_dict = ({'image_id':image_id, 'enum' :ix, 'it_dist':itc_, 'tuple': rnd_obj_rel_obj})
            results.append(obj_dict)

        gt_dist_to_2nd_best_dist = itc_gt/max(itc_dist_rand_rel)
        obj_dict = ({'gt_dist_to_2nd_best_dist' :gt_dist_to_2nd_best_dist, 'best_noisy_rel_ind': np.argmax(itc_dist_rand_rel)})
        results.append(obj_dict)
    if (inx % 10) ==0:
        df = pd.DataFrame(results)
        df.to_csv(os.path.join(result_path, csv_file_name), index=False)

    # gt_triplets = tuples_from_sg(sg)
    # for tup in gt_triplets:
    #     if len(tup)==3:
    #         print(tup)
    #         blip.process_image_and_captions(file=image_path, caption=tup)
    #         # "A photo of <your triplet>
    # break          

df = pd.DataFrame(results)
df.to_csv(os.path.join(result_path, csv_file_name), index=False)


"""
rel = list()
for ipc_id in image_ids_related_to_ipc:
    ipc,_ = get_visual_genome_record_by_ipc_id(ipc_id)
    sg = get_sc_graph(ipc['image_id'])
    rel.extend([rel.predicate for ib, rel in enumerate(sg.relationships)])


import matplotlib.pyplot as plt
plt.hist(df.gt_dist_to_2nd_best_dist, bins=50)

plt.title('BLIP2-ITM '  + str(use_prefix_str) + ' ratio of matching GT obj-rel-obj to ITM with random relation')
plt.savefig(os.path.join(result_path, 'hist_itm_' + str(use_prefix_str) + '.jpg'))


plt.title('BLIP2-ITC '  + str(use_prefix_str) + ' cosine distance ratio with GT to random relation obj-rel-obj')
plt.savefig(os.path.join(result_path, 'hist_itc_' + str(use_prefix_str) + '.jpg'))


ITM:
ITM though it is for fine grained it is claimed to test hypothesis : a binary classifier, predicting whether an image-text pair is 
positive (matched) or negative, who says that same text but with different relationship was introduced at training time! 
And it isn't necessarily a relative metric among images but may be since it measures if the text is noisy to the image. 
Maybe it goes better with less fine-grained than predicates.

for q_question_key, q_question_val in q_questions.items():
    print(q_question_key)

examples for subjects to one object
http://74.82.29.209:9000/datasets/media/services/blip2_upload/3036_IN_TIME_00.28.05.713-00.28.23.353__286.jpg
http://74.82.29.209:9000/datasets/media/services/blip2_upload/3019_COLOMBIANA_00.07.07.000-00.07.21.393__367.jpg
http://74.82.29.209:9000/datasets/media/services/blip2_upload/3006_A_GOOD_DAY_TO_DIE_HARD_01.08.46.435-01.09.06.404__288.jpg

"""

    
