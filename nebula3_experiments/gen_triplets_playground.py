# export PYTHONPATH=/notebooks/pip_install/
import os
import json
import numpy as np
import re
import itertools
import time 
import tqdm
import pandas as pd
import sys

from nebula3_experiments.vg_eval import Sg_handler, spice_get_triplets, get_sc_graph, tuples_from_sg, VGEvaluation
from database.arangodb import NEBULA_DB
from nebula3_experiments.prompts_utils import PrompEngFewshotTupleCreation, _get_few_shot_prompt_paragraph_based_to_tuple_4K, \
                            union_tuples_n_fusion_from_multi_sentence_completion
# get_likely_tuples_from_paragraph, get_prompt_few_shot_filter_abstract_tokens_n_prefix_from_paragraph, \
#                                 get_likely_tuples_from_paragraph_anderson_by_sentence

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

def synth_in_context_examples_sentence_based_anderson(paragraphs, prompt_limit=4096):
    
    in_context_ex_limit = prompt_limit - margin_for_prompt_suffix # margin_for_prompt_suffix=512
    in_context_ex = list()
    
    for paragraph in paragraphs:
        for sent in paragraph.split('.'):
            dotted_sent = sent.strip() + '.'
            if dotted_sent != '.':
                triplets = spice_get_triplets(dotted_sent)
                in_context_ex.append('\nSentence: {}'.format(dotted_sent) + '\nTuples: {}'.format(triplets))

    return ''.join(in_context_ex)

def synth_in_context_examples_paragraph_based_by_anderson(paragraphs, prompt_limit=4096):
    in_context_ex_limit = prompt_limit - margin_for_prompt_suffix # margin_for_prompt_suffix=512
    in_context_ex = list()
    in_context_ex_paragraph = list()

    for paragraph in paragraphs:
        triplets = spice_get_triplets(paragraph)
        in_context_ex.append('\nParagraph: {}'.format(paragraph) + '\nTuples: {}'.format(triplets))
        in_context_ex_paragraph.append(paragraph)

    return ''.join(in_context_ex)

def synth_in_context_examples_tuples_len_2_3_paragraph_based(paragraphs, prompt_limit=4096):
    in_context_ex_limit = prompt_limit - margin_for_prompt_suffix # margin_for_prompt_suffix=512
    in_context_ex = list()
    in_context_ex_paragraph = list()

    for paragraph in paragraphs:
        triplets = spice_get_triplets(paragraph)
        triplets = [t for t in triplets if len(t)>=2]
        in_context_ex.append('\nParagraph: {}'.format(paragraph) + '\nTuples: {}'.format(triplets))
        in_context_ex_paragraph.append(paragraph)

    return ''.join(in_context_ex)

def limit_paragrapgs_by_prompt_size(paragraphs, prompt_limit=4096):
    
    in_context_ex_limit = prompt_limit - margin_for_prompt_suffix # margin_for_prompt_suffix=512
    in_context_ex = list()
    in_context_ex_paragraph = list()
    overhead_to_sent = 0
    len_of_paragraph = len('paragraph') + 1 # +1 for the \n
    len_of_tuples = len('tuples') + 1 
    
    for paragraph in tqdm.tqdm(paragraphs):
        overhead_to_sent += 2*(len(paragraph.split('.')) -1) *(len_of_paragraph + len_of_tuples)
        triplets = spice_get_triplets(paragraph)
        in_context_ex.append('\nParagraph: {}'.format(paragraph) + '\nTuples: {}'.format(triplets))
        in_context_ex_paragraph.append(paragraph)
        temp_prompt = ''.join(in_context_ex)
        if len(temp_prompt) + overhead_to_sent>in_context_ex_limit:
            in_context_ex = in_context_ex[:-1] # revert appended example since in_context example has paragraph granularity
            in_context_ex_paragraph = in_context_ex_paragraph[:-1] # revert appended paragraph Sssss
            return in_context_ex_paragraph


os.environ["TOKENIZERS_PARALLELISM"] = "false"     # HF warning prob transformer package                           

n_completions_to_generate_for_each_prompt = 1 #10
FS_GPT_MODEL = 'text-davinci-003'
paragraph_to_tuple_gpt = False
filter_abstract_tokens = False
debug_predefined_ipc = True
predict_anderson = True
find_co_ref = False
predefined_seed = True
path_save = "/notebooks/nebula3_experiments"
prompt_util = PrompEngFewshotTupleCreation()
n_monte_carlo = 3
paragraph_based = False

load_pre_set_in_context_ex = False # => regenerate random 
get_gpt_multi_completions = True
margin_for_prompt_suffix = 512


if get_gpt_multi_completions:
    n_fusion = 2
    post_process_sentence_fun = union_tuples_n_fusion_from_multi_sentence_completion
    n_completions_to_generate_for_each_prompt = 10


gradient_env_path_based = True
if gradient_env_path_based:
    result_path = "/notebooks/nebula3_playground/images"
    vgenome_images = '/media/vg_data/visualgenome/VG'
    vgenome_metadata = "/storage/vg_data/"
else:
    result_path = "/notebooks/nebula3_playground/images"
    vgenome_images = '/datasets/dataset/vgenome/images/VG_100K'
    vgenome_metadata = "/datasets/dataset/vgenome/metadata"

if result_path and not os.path.exists(result_path):
    os.makedirs(result_path)

with open(os.path.join('/storage/ipc_data/paragraphs_v1.json'), "r") as f:
    images_data = json.load(f)
sample_ids = np.loadtxt(os.path.join(vgenome_metadata, "sample_ids_ipc_vgenome_ids.txt"))

if debug_predefined_ipc:
    print("Predefined images IDs/IPc examples !!!!!!!  ", 50* '=')
    descriptive_img_id_list = [2356133]
    co_ref_ids_list = [2402585, 2319404, 2322108, 2398895, 2383585, 2395503]
    image_ids_related_to_ipc = [2394361, 2396735, 2333990, 2352948] # low recall of paragraph GPT vs Vgenoe GT 
    image_ids_related_to_ipc += co_ref_ids_list
else:
    image_ids_related_to_ipc = [images_data[int(ix)]['image_id'] for ix in sample_ids]


if n_completions_to_generate_for_each_prompt>1:
    print("N completion>1 R U sure ", 50*'=')
sg_handler = Sg_handler(images_path=vgenome_metadata,  # data = json.load(open(image_data_dir + fname, 'r')) [(x['attribute']) for x in data['attributes']][1]['attributes']
            image_data_dir=vgenome_metadata+'/by-id/',
            synset_file=vgenome_metadata+'/synsets.json')

ipc_data = json.load(open('/storage/ipc_data/paragraphs_v1.json','r'))

random_iter = range(1)
if predict_anderson:
    random_iter = range(n_monte_carlo)
    results = list()
    context_examples_sentence_based = list()
    evaluator = VGEvaluation()
    common_seed = 19121
    unique_run_name = str(int(time.time()))
    if predefined_seed:
        np.random.seed(common_seed)
        print("Warning pre defined seed R U sure ?")
    else:
        np.random.seed(unique_run_name)
    
    all_image_ids_related_to_ipc = [images_data[int(ix)]['image_id'] for ix in sample_ids]
    if not load_pre_set_in_context_ex:
        all_rand_in_context_examples_sentence_based = list()
        all_rand_in_context_examples_paragraph_based = list()
        all_rand_in_context_examples_tuples_len_2_3_paragraph_based = list()
        for i in random_iter: # create few opportunities 
            rand_paragraph = np.random.choice(all_image_ids_related_to_ipc,(10), replace=False)
            all_rand_paragraphs = list()
            for rnd_ind in rand_paragraph:
                rand_vg_equiv_ipc = [ix for ix , x in enumerate(ipc_data) if x['image_id']==rnd_ind][0]
                rnd_ipc = ipc_data[rand_vg_equiv_ipc]
                all_rand_paragraphs.append(rnd_ipc['paragraph'])

            limited_by_size_rand_paragraphs = limit_paragrapgs_by_prompt_size(all_rand_paragraphs)

            rand_in_context_examples_sentence_based = synth_in_context_examples_sentence_based_anderson(limited_by_size_rand_paragraphs)
            rand_in_context_examples_paragraph_based = synth_in_context_examples_paragraph_based_by_anderson(limited_by_size_rand_paragraphs)
            rand_in_context_examples_tuples_len_2_3_paragraph_based = synth_in_context_examples_tuples_len_2_3_paragraph_based(limited_by_size_rand_paragraphs)

            all_rand_in_context_examples_sentence_based.append(rand_in_context_examples_sentence_based)
            all_rand_in_context_examples_paragraph_based.append(rand_in_context_examples_paragraph_based)
            all_rand_in_context_examples_tuples_len_2_3_paragraph_based.append(rand_in_context_examples_tuples_len_2_3_paragraph_based)
    # to Dataframe
            context_examples_sentence_based.append({'rand_in_context_examples_sentence_based': rand_in_context_examples_sentence_based, 
                                                    'rand_in_context_examples_paragraph_based': rand_in_context_examples_paragraph_based,
                                                    'rand_in_context_examples_tuples_len_2_3_paragraph_based': rand_in_context_examples_tuples_len_2_3_paragraph_based})
            df_context_examples_ipc = pd.DataFrame(context_examples_sentence_based)
            df_context_examples_ipc.to_csv(os.path.join(path_save, 'context_examples_ipc.csv'), index=False)
    else:
        df_context_examples_ipc = pd.read_csv(os.path.join(path_save, 'context_examples_ipc.csv'))
        all_rand_in_context_examples_sentence_based = df_context_examples_ipc['rand_in_context_examples_sentence_based']
        all_rand_in_context_examples_paragraph_based = df_context_examples_ipc['rand_in_context_examples_paragraph_based']
        all_rand_in_context_examples_tuples_len_2_3_paragraph_based = df_context_examples_ipc['rand_in_context_examples_tuples_len_2_3_paragraph_based']

for randomizing_prompt_ix in random_iter:
    rand_in_context_examples_sentence_based = all_rand_in_context_examples_sentence_based[randomizing_prompt_ix]
    rand_in_context_examples_paragraph_based = all_rand_in_context_examples_paragraph_based[randomizing_prompt_ix]
    rand_in_context_examples_tuples_len_2_3_paragraph_based = all_rand_in_context_examples_tuples_len_2_3_paragraph_based[randomizing_prompt_ix]

    for inx, ipc_id in enumerate(tqdm.tqdm(image_ids_related_to_ipc)):
        vg_ind_related_to_ipc = [ix for ix , x in enumerate(ipc_data) if x['image_id']==ipc_id][0]

        # sg = sg_handler.get_scene_graph(ipc_id)
        ipc = ipc_data[vg_ind_related_to_ipc]
        ipc_triplets = spice_get_triplets(ipc['paragraph'])

        if predict_anderson:
            prompt_util.n_fusion = n_fusion
            
            if post_process_sentence_fun:
                from functools import partial
                prompt_util.post_process_sentence_fun = partial(post_process_sentence_fun, prompt_util)

            prompt_util.get_likely_tuples_from_paragraph_by_sentence(paragraph=ipc['paragraph'], 
                                                        n=n_completions_to_generate_for_each_prompt,  
                                                        post_process_sentence_fun=post_process_sentence_fun,
                                                        in_context_examples=rand_in_context_examples_sentence_based) # get_paragraph_to_anderson_tuple_sentence_prompt_4K
            if paragraph_based: 
                prompt_util.get_likely_tuples_from_paragraph(paragraph=ipc['paragraph'], 
                                                            few_shot_prompt_func=_get_few_shot_prompt_paragraph_based_to_tuple_4K,
                                                            in_context_examples=rand_in_context_examples_paragraph_based) # get_paragraph_to_anderson_tuple_sentence_prompt_4K
            else:
                prompt_util.pred_tuples_paragraph_based = True # dummy

            if any(prompt_util.pred_tuples_sentence_based) and prompt_util.pred_tuples_paragraph_based==True: # GPT may return broken tuples
                recall_gt_anderson_gpt_anderson_sentence_based = evaluator.recall_triplets_mean(ipc_triplets, prompt_util.pred_tuples_sentence_based)
                precision_gt_anderson_gpt_anderson_sentence_based = evaluator.recall_triplets_mean(prompt_util.pred_tuples_sentence_based, ipc_triplets)

                if paragraph_based: 
                    recall_gt_anderson_gpt_anderson_paragraph_based = evaluator.recall_triplets_mean(ipc_triplets, prompt_util.pred_tuples_paragraph_based)
                    precision_gt_anderson_gpt_anderson_paragraph_based = evaluator.recall_triplets_mean(prompt_util.pred_tuples_paragraph_based, ipc_triplets)
                else:
                    recall_gt_anderson_gpt_anderson_paragraph_based =-1
                    precision_gt_anderson_gpt_anderson_paragraph_based = -1

                results.append({'ipc_id': ipc_id, 'in_context_permutation' :randomizing_prompt_ix, 
                                'recall_gt_anderson_gpt_anderson_sentence_based': recall_gt_anderson_gpt_anderson_sentence_based,
                                'recall_gt_anderson_gpt_anderson_paragraph_based':recall_gt_anderson_gpt_anderson_paragraph_based,
                                'pred_tuples_sentence_based': prompt_util.pred_tuples_sentence_based,
                                'pred_tuples_paragraph_based': prompt_util.pred_tuples_paragraph_based,
                                'rand_in_context_examples_sentence_based': rand_in_context_examples_sentence_based,
                                'rand_in_context_examples_paragraph_based': rand_in_context_examples_paragraph_based,
                                'precision_gt_anderson_gpt_anderson_sentence_based': precision_gt_anderson_gpt_anderson_sentence_based,
                                'precision_gt_anderson_gpt_anderson_paragraph_based': precision_gt_anderson_gpt_anderson_paragraph_based,
                                'paragraph': ipc['paragraph'], 
                                'n_completions_to_generate_for_each_prompt': n_completions_to_generate_for_each_prompt,
                                'n_fusion' :n_fusion})

                df_results = pd.DataFrame(results)
                df_results.to_csv(os.path.join("/notebooks/nebula3_experiments", 'results_pred_anderson_sentence_fusion_' + str(n_fusion) + '_response_ipc.csv'), index=False)

        elif find_co_ref:
            coref_ex = ['he', 'she', 'it', 'they']
            # coref_ex = ['An image of', 'A scene of', 'A photo of', 'Camera', 'Nature', 'mood', 'day', 'night', 'sunny', 'snow'] 
            for coref in coref_ex:
                if findWholeWord(coref.lower())(ipc['paragraph'].lower()):
                    f_res = findWholeWord(coref)(ipc['paragraph'])
                    print(f_res.span(1), ipc['paragraph'])
                    print("Triplet: {} paragraph: {} IPC:{}".format(ipc_triplets, ipc['paragraph'], vg_ind_related_to_ipc))

                    if filter_abstract_tokens: # Test FP/FN
                        rc_abs_filter = get_prompt_few_shot_filter_abstract_tokens_n_prefix_from_paragraph(paragraph)

                    if paragraph_to_tuple_gpt:
                        paragraph = "Two young children have skis on their feet, and ski poles, but they are both sitting on the snow covering a mountain. It's daylight out, but there's a large shady area that the children are also in. The child to the left looks like a boy, and he's smiling. He's also wearing all black clothing, and a white helmet with red goggles resting on the helmet. The child to the right looks like a girl, and she is wearing pink snow pants, pink and white snow jacket and black sunglasses. She looks like she has brown hair and doesn't appear to be wearing a helmet. Far from them and way to the back of the image, there are green trees that are scattered along the mountain."
                        rc = get_likely_tuples_from_paragraph(paragraph, n=n_completions_to_generate_for_each_prompt, use_dash_prompt=True)
                        # rc = gpt_execute(uncertaint_prompt, model=FS_GPT_MODEL, n=n_completions_to_generate_for_each_prompt)
                        if n_completions_to_generate_for_each_prompt>1:
                            rc = sorted([(x[0],len(list(x[1]))) for x in itertools.groupby(sorted(rc)) if len(x[0].split())==2], key=lambda x:-x[1])
                            try:
                                rc = rc[0][0].split()
                            except Exception as e:
                                print('gah, exception:')
                                print(rc)
                        else:
                            rc = rc[0].split()
                    break
            # print("Triplet: {} paragraph: {} IPC:{}".format(ipc_triplets, ipc['paragraph'], vg_ind_related_to_ipc))

            sg = get_sc_graph(ipc['image_id'])
            gt_triplets = tuples_from_sg(sg)
        else:
            raise