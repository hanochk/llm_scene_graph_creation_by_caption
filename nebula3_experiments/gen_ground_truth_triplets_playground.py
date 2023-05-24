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
import amrlib  #  clone https://github.com/bjascob/amrlib instructions on https://amrlib.readthedocs.io/en/latest/install/ models path in pip3 show amrlib =>  /usr/local/lib/python3.9/dist-packages
from functools import partial
from sklearn.model_selection import LeaveOneOut
import ast
import copy

from nebula3_experiments.vg_eval import Sg_handler, spice_get_triplets, get_sc_graph, tuples_from_sg, VGEvaluation
from database.arangodb import NEBULA_DB
from nebula3_experiments.prompts_utils import *

def flatten(lst): return [x for l in lst for x in l]
# Not working well
# def flip_gt_tuple_ord_2_like_anderson_obj_attr(all_tuples):
#     flipped_tups = list()
#     for tups in all_tuples:
#         tups_list = ['['+x.strip().replace(',','').replace('"',"'") for x in tups.replace("]]","]").split('[')[2:]]
#         flipped_tups.append(str([tup[::-1] if len(tup)==2 else tup for tup in tups_list]))
#     return flipped_tups





os.environ["TOKENIZERS_PARALLELISM"] = "false" #huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks
unique_run_name = str(int(time.time()))
print("unique run name : {}".format(unique_run_name))

n_completions_to_generate_for_each_prompt = 1 #10

n_completions_to_generate_for_each_prompt_versitile = 10
n_fusion = 1
prompt_util = PrompEngFewshotTupleCreation()

prompt_util.n_fusion = n_fusion
# post_process_sentence_fun = union_tuples_n_fusion_from_multi_sentence_completion
# prompt_util.post_process_sentence_fun = partial(post_process_sentence_fun, prompt_util)

top_p = 0.1
FS_GPT_MODEL = 'text-davinci-003'

debug_predefined_ipc = True
path_save = "/notebooks/nebula3_experiments"

load_pre_set_in_context_ex = False # => regenerate random 
get_gpt_multi_completions = False
margin_for_prompt_suffix = 512
tuples_sanity_check = False

# task = 'predicting_sentence_delta_anderson_proposal'
# task = 'predicting_sentence_gt'
task = 'predicting_sentence_delta_amr_proposal'

# if get_gpt_multi_completions:
#     top_p = 0.1

#     if top_p != 1:
#         prompt_util.n_fusion = -1
#         post_process_sentence_fun = None
#     else:
#         n_completions_to_generate_for_each_prompt = 10


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

evaluator = VGEvaluation()

all_sentences, all_tuples = breakdown_prompt_to_list_examples(in_context_examples_my_gt)
assert(len(in_context_sentence_examples_mapping_to_parapragh_my_gt) == len(all_tuples))
check_tuples_sanity_in_context_example(in_context_examples_my_gt)

loo = LeaveOneOut()
loo.get_n_splits(range(len(all_sentences)))

results = list()
recall_gt_vs_gpt_sentence_based_n = dict()
precision_gt_vs_gpt_sentence_based_n = dict()
f_score_gt_vs_gpt_sentence_based_n = dict()

paragraph_indeces = np.unique(in_context_sentence_examples_mapping_to_parapragh_my_gt)

all_sentences = [x.replace('"',"") for x in all_sentences]

random_iter = range(1)
verbose = True
if task == 'predicting_sentence_delta_anderson_proposal':
    verbose = True
    predefined_seed = True

    size_limit_n_paragraph = limit_paragrapgs_by_prompt_size_pred_delta_anderson(all_sentences)
    if 1:
        size_limit_n_paragraph = size_limit_n_paragraph - 2 #Hack
# Random picking limited in size prompt since prompt is larger
    common_seed = 19121
    unique_run_name = str(int(time.time()))

    if predefined_seed:
        np.random.seed(common_seed)
        print("Warning pre defined seed R U sure ?")
    else:
        np.random.seed(unique_run_name)

    prmute_prompt_monte_carlo = len(all_sentences) - size_limit_n_paragraph # it is Permute n out of m where order is meaningless
    random_iter = range(prmute_prompt_monte_carlo)


    fusion_type = 'delta_operator_fusion' # 'prompt_fusion'
    # fusion_type = 'final_tuples_fusion'

    post_process_sentence_fun = create_arithmetic_final_tuple_from_proposed_and_predict # need to calculate the arithmetics and yield final result
    prompt_util.post_process_sentence_fun = partial(create_arithmetic_final_tuple_from_proposed_and_predict, prompt_util)
    csv_file_name = 'results_pred_delta_anderson_leaving_one_out_sentence_based_fusion_' + \
        str(n_fusion) + '_fusion_type_' + str(fusion_type) +'_name_' + unique_run_name + '.csv'

elif task == 'predicting_sentence_gt':
    post_process_sentence_fun = union_tuples_n_fusion_from_multi_sentence_completion
    prompt_util.post_process_sentence_fun = partial(post_process_sentence_fun, prompt_util)
    fusion_type = None
    csv_file_name = 'results_pred_my_gt_leaving_one_out_sentence_based_fusion_' + str(n_fusion) + \
        '_name_' + unique_run_name + '.csv'
elif task == 'predicting_sentence_delta_amr_proposal':
    verbose = True
    predefined_seed = True

    if 1: # TODO next
        size_limit_n_paragraph = limit_paragrapgs_by_prompt_size_pred_delta_amr(all_sentences)
        if 1:
            size_limit_n_paragraph = size_limit_n_paragraph - 2 #Hack
    else:
        size_limit_n_paragraph = len(all_sentences) - 2
# Random picking limited in size prompt since prompt is larger
    common_seed = 19121
    unique_run_name = str(int(time.time()))

    if predefined_seed:
        np.random.seed(common_seed)
        print("Warning pre defined seed R U sure ?")
    else:
        np.random.seed(unique_run_name)

    prmute_prompt_monte_carlo = len(all_sentences) - size_limit_n_paragraph # it is Permute n out of m where order is meaningless
    random_iter = range(prmute_prompt_monte_carlo)

    post_process_sentence_fun = union_tuples_n_fusion_from_multi_sentence_completion
    prompt_util.post_process_sentence_fun = partial(union_tuples_n_fusion_from_multi_sentence_completion, prompt_util)

    fusion_type = None
    csv_file_name = 'results_pred_my_gt_leaving_one_out_prior_amr_sentence_based_fusion_' + str(n_fusion) + \
        '_name_' + unique_run_name + '.csv'

    stog = amrlib.load_stog_model(model_dir='/notebooks/amrlib/model_parse_xfm_bart_large-v0_1_0/')   #stog = amrlib.load_stog_model()

    # graphs = [stog.parse_sents([x]) for x in all_sentences]
    # for graph in graphs:
    #     print(graph)

    # pass
else:
    raise 



# for i in random_iter: # create few opportunities # TODO

for i, (train_index, test_index) in enumerate(loo.split(range(len(paragraph_indeces)))):
    print(f"Fold {i}:")
    print(f"  Train: index={train_index}")
    print(f"  Test:  index={test_index}")

    sent_indeces_train = [np.where(in_context_sentence_examples_mapping_to_parapragh_my_gt == x)[0].tolist() for x in train_index]
    sent_indeces_train = flatten(sent_indeces_train)
    sent_indeces_test = [np.where(in_context_sentence_examples_mapping_to_parapragh_my_gt == x)[0].tolist() for x in test_index][0]
    
    if task == 'predicting_sentence_delta_anderson_proposal' or task =='predicting_sentence_delta_amr_proposal':
        rand_paragraph = np.random.choice(sent_indeces_train, size_limit_n_paragraph, replace=False)
        sent_indeces_train = rand_paragraph

    loo_paragraph_train = [all_sentences[x] for x in sent_indeces_train]
    loo_tuples_train = [all_tuples[x] for x in sent_indeces_train]

    # Following test-set in pargraph level extract and concat in sentence level
    query_paragraph = ''.join([all_sentences[x] for x in sent_indeces_test]).replace('"',"")
    my_gt_tuple = flatten([eval(all_tuples[x]) for x in sent_indeces_test])

    if task == 'predicting_sentence_gt':
        # gt_tuple = my_gt_tuple
        loo_in_context_examples_sentence_based = synth_in_context_examples_based(loo_paragraph_train, loo_tuples_train)
        few_shot_prompt_func = _get_few_shot_prompt_sentence_based_to_tuple_4K
        # reference_tuples = None
        query_proposed_ngrams = None
    elif task == 'predicting_sentence_delta_anderson_proposal':
        all_proposed_tuples = [spice_get_triplets(x.replace('"',"")) for x in loo_paragraph_train]

        all_delta_tuples = calc_delta_tuples_arithmetics(all_proposed_tuples=all_proposed_tuples, 
                                                        all_gt_tuples=loo_tuples_train)

        loo_in_context_examples_sentence_based = synth_in_context_examples_based_predicting_delta_anderson(all_paragraphs=loo_paragraph_train, 
                                                        all_proposed_tuples=all_proposed_tuples, # Anderson
                                                        all_delta_tuples=all_delta_tuples)
# GT calculation of delta Anderson
        query_proposed_ngrams =  [spice_get_triplets(x.replace('"',"") + '.') for x in query_paragraph.split(".")[:-1]]
        # gt_tuple = calc_delta_tuples_arithmetics(all_proposed_tuples=[query_proposed_ngrams], all_gt_tuples=[my_gt_tuple])
        few_shot_prompt_func = _get_few_shot_prompt_sentence_based_to_delta_anderson_tuple_4K
    elif task =='predicting_sentence_delta_amr_proposal': 
        # Each AMR is a single rooted, directed graph. AMRs include PropBank semantic roles, within-sentence coreference, named entities and types, modality, negation, questions, quantities, and so on
        all_proposed_amr_not_linearized = [stog.parse_sents([x.strip().replace('"',"")]) for x in loo_paragraph_train]
        all_proposed_amr = list()

        for tup, par in zip(all_proposed_amr_not_linearized, loo_paragraph_train):
            # print('sentence', par, len(tup))
            amr_lin = tup[0].split('\n')[1:]
            # print("amr_lin", amr_lin)
            # print(''.join([x.strip() for x in amr_lin]))
            all_proposed_amr.append(''.join([x.strip() for x in amr_lin]))


        loo_in_context_examples_sentence_based = synth_in_context_examples_based_predicting_delta_anderson(all_paragraphs=loo_paragraph_train, 
                                                        all_proposed_tuples=all_proposed_amr, # AMR
                                                        all_delta_tuples=loo_tuples_train,
                                                        delta_prefix=amr_delta_prefix_pattern,
                                                        proposal_prefix="Reference abstract meaning representation:")

        few_shot_prompt_func = _get_few_shot_prompt_sentence_based_on_amr_tuple_4K

        query_proposed_amr_not_linearized = [stog.parse_sents([x.strip().replace('"',"") + '.']) for x in query_paragraph.split(".")[:-1]] # abuse for the name anderson
        query_proposed_ngrams = list()
        for tup in query_proposed_amr_not_linearized:
            # print('sentence', par, len(tup))
            amr_lin = tup[0].split('\n')[1:]
            # print("amr_lin", amr_lin)
            # print(''.join([x.strip() for x in amr_lin]))
            query_proposed_ngrams.append(''.join([x.strip() for x in amr_lin]))

    else:
        raise
    

    pred_triplets_n = prompt_util.get_likely_tuples_from_paragraph_by_sentence(paragraph=query_paragraph, 
                                            n=n_completions_to_generate_for_each_prompt_versitile,
                                            few_shot_prompt_func=few_shot_prompt_func,
                                            in_context_examples=loo_in_context_examples_sentence_based,
                                            post_process_sentence_fun=post_process_sentence_fun,
                                            reference_tuples=query_proposed_ngrams, 
                                            fusion_type=fusion_type, n_fusion=n_fusion,
                                            verbose=verbose) # get_paragraph_to_anderson_tuple_sentence_prompt_4K

    recall_gt_vs_gpt_sentence_based_n[n_completions_to_generate_for_each_prompt_versitile] = evaluator.recall_triplets_mean(my_gt_tuple, pred_triplets_n)
    precision_gt_vs_gpt_sentence_based_n[n_completions_to_generate_for_each_prompt_versitile] = evaluator.recall_triplets_mean(pred_triplets_n, my_gt_tuple)
    f_score_gt_vs_gpt_sentence_based_n[n_completions_to_generate_for_each_prompt_versitile] = 2/(1/recall_gt_vs_gpt_sentence_based_n[n_completions_to_generate_for_each_prompt_versitile] + 1/precision_gt_vs_gpt_sentence_based_n[n_completions_to_generate_for_each_prompt_versitile])
    locals()['all_pred_triplets_temp_n_' + str(n_completions_to_generate_for_each_prompt_versitile)] = prompt_util.all_pred_triplets_temp


    if task == 'predicting_sentence_gt':
        tmp_post_process_sentence_fun = copy.deepcopy(post_process_sentence_fun)
        post_process_sentence_fun = None # no fusion needed at that task 
    pred_triplets = prompt_util.get_likely_tuples_from_paragraph_by_sentence(paragraph=query_paragraph, 
                                                n=n_completions_to_generate_for_each_prompt,
                                                few_shot_prompt_func=few_shot_prompt_func,
                                                in_context_examples=loo_in_context_examples_sentence_based,
                                                post_process_sentence_fun=post_process_sentence_fun,
                                                reference_tuples=query_proposed_ngrams,
                                                fusion_type=fusion_type, n_fusion=n_fusion, 
                                                verbose=verbose) # get_paragraph_to_anderson_tuple_sentence_prompt_4K
    
    if task == 'predicting_sentence_gt':
        post_process_sentence_fun = copy.deepcopy(tmp_post_process_sentence_fun)

    recall_gt_vs_gpt_sentence_based_n[n_completions_to_generate_for_each_prompt] = evaluator.recall_triplets_mean(my_gt_tuple, pred_triplets)
    precision_gt_vs_gpt_sentence_based_n[n_completions_to_generate_for_each_prompt] = evaluator.recall_triplets_mean(pred_triplets, my_gt_tuple)
    f_score_gt_vs_gpt_sentence_based_n[n_completions_to_generate_for_each_prompt] = 2/(1/recall_gt_vs_gpt_sentence_based_n[n_completions_to_generate_for_each_prompt] + 1/precision_gt_vs_gpt_sentence_based_n[n_completions_to_generate_for_each_prompt])
    locals()['all_pred_triplets_temp_n_' + str(n_completions_to_generate_for_each_prompt)] = prompt_util.all_pred_triplets_temp




    if task == 'predicting_sentence_gt':
        tmp_post_process_sentence_fun = copy.deepcopy(post_process_sentence_fun)
        post_process_sentence_fun = None # no fusion needed at that task 

    top_p = 0.1
    pred_triplets_top_p = prompt_util.get_likely_tuples_from_paragraph_by_sentence(paragraph=query_paragraph, 
                                                n=n_completions_to_generate_for_each_prompt,
                                                top_p=top_p,
                                                few_shot_prompt_func=few_shot_prompt_func,
                                                in_context_examples=loo_in_context_examples_sentence_based,
                                                post_process_sentence_fun=post_process_sentence_fun,
                                                reference_tuples=query_proposed_ngrams, 
                                                fusion_type=fusion_type, n_fusion=n_fusion, 
                                                verbose=verbose) # get_paragraph_to_anderson_tuple_sentence_prompt_4K
    

    recall_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"] = evaluator.recall_triplets_mean(my_gt_tuple, pred_triplets_top_p)
    precision_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"] = evaluator.recall_triplets_mean(pred_triplets_top_p, my_gt_tuple)
    f_score_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"] = 2/(1/recall_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"] + 1/precision_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"])

    locals()['all_pred_triplets_temp_top_p_' + str(top_p)] = prompt_util.all_pred_triplets_temp

    top_p_dict = {f"pred_triplets_top_p[top_p_{top_p}]": pred_triplets_top_p,
                f"recall_gt_vs_gpt_sentence_based_n[top_p_{top_p}]" :recall_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"],
                f"precision_gt_vs_gpt_sentence_based_n[top_p_{top_p}]": precision_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"],
                f"f_score_gt_vs_gpt_sentence_based_n[top_p_{top_p}]" : f_score_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"]}

    if task == 'predicting_sentence_gt':
        post_process_sentence_fun = copy.deepcopy(tmp_post_process_sentence_fun)

    if task == 'predicting_sentence_gt':
        tmp_post_process_sentence_fun = copy.deepcopy(post_process_sentence_fun)
        post_process_sentence_fun = None # no fusion needed at that task 
    
    top_p = 0.5
    pred_triplets_top_p = prompt_util.get_likely_tuples_from_paragraph_by_sentence(paragraph=query_paragraph, 
                                                n=n_completions_to_generate_for_each_prompt,
                                                top_p=top_p,
                                                few_shot_prompt_func=few_shot_prompt_func,
                                                in_context_examples=loo_in_context_examples_sentence_based,
                                                post_process_sentence_fun=post_process_sentence_fun,
                                                reference_tuples=query_proposed_ngrams, 
                                                fusion_type=fusion_type, n_fusion=n_fusion,
                                                verbose=verbose) # get_paragraph_to_anderson_tuple_sentence_prompt_4K

    recall_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"] = evaluator.recall_triplets_mean(my_gt_tuple, pred_triplets_top_p)
    precision_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"] = evaluator.recall_triplets_mean(pred_triplets_top_p, my_gt_tuple)
    f_score_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"] = 2/(1/recall_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"] + 1/precision_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"])
    locals()['all_pred_triplets_temp_top_p_' + str(top_p)] = prompt_util.all_pred_triplets_temp

    if task == 'predicting_sentence_gt':
        post_process_sentence_fun = copy.deepcopy(tmp_post_process_sentence_fun)


    top_p_dict.update({f"pred_triplets_top_p[top_p_{top_p}]": pred_triplets_top_p,
                f"recall_gt_vs_gpt_sentence_based_n[top_p_{top_p}]" :recall_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"],
                f"precision_gt_vs_gpt_sentence_based_n[top_p_{top_p}]": precision_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"],
                f"f_score_gt_vs_gpt_sentence_based_n[top_p_{top_p}]" : f_score_gt_vs_gpt_sentence_based_n[f"top_p_{top_p}"]})

    res_dict = {'train_index': train_index, 'test_index' :test_index,
                'n_fusion': prompt_util.n_fusion, 'n_completions_to_generate_for_each_prompt': n_completions_to_generate_for_each_prompt_versitile,
                'recall_gt_vs_gpt_sentence_based': recall_gt_vs_gpt_sentence_based_n[n_completions_to_generate_for_each_prompt],
                'precision_gt_vs_gpt_sentence_based':precision_gt_vs_gpt_sentence_based_n[n_completions_to_generate_for_each_prompt],
                f"f_score_gt_vs_gpt_sentence_based_n[{n_completions_to_generate_for_each_prompt}]":f_score_gt_vs_gpt_sentence_based_n[n_completions_to_generate_for_each_prompt],
                f"recall_gt_vs_gpt_sentence_based_n[{n_completions_to_generate_for_each_prompt_versitile}]": eval(f"recall_gt_vs_gpt_sentence_based_n[{n_completions_to_generate_for_each_prompt_versitile}]"),
                f"precision_gt_vs_gpt_sentence_based_n[{n_completions_to_generate_for_each_prompt_versitile}]": eval(f"precision_gt_vs_gpt_sentence_based_n[{n_completions_to_generate_for_each_prompt_versitile}]"),
                f"f_score_gt_vs_gpt_sentence_based_n[{n_completions_to_generate_for_each_prompt_versitile}]":f_score_gt_vs_gpt_sentence_based_n[n_completions_to_generate_for_each_prompt_versitile],
                'loo_in_context_examples_sentence_based': loo_in_context_examples_sentence_based,
                'pred_tuples_sentence_based': pred_triplets,
                'gt_tuple': my_gt_tuple,
                'fusion_type': fusion_type,
                f"all_pred_triplets_temp_n_{n_completions_to_generate_for_each_prompt}":eval(f"all_pred_triplets_temp_n_{n_completions_to_generate_for_each_prompt}"),
                f"all_pred_triplets_temp_n_{n_completions_to_generate_for_each_prompt_versitile}":eval(f"all_pred_triplets_temp_n_{n_completions_to_generate_for_each_prompt_versitile}"),
                f"all_pred_triplets_temp_top_p_{top_p}": locals()['all_pred_triplets_temp_top_p_' + str(top_p)], 
                f"pred_triplets_n {n_completions_to_generate_for_each_prompt_versitile}": pred_triplets_n}
    res_dict.update(top_p_dict)
    results.append(res_dict)

    df_results = pd.DataFrame(results)
    df_results.to_csv(os.path.join("/notebooks/nebula3_experiments", csv_file_name), index=False)
    print("Saving {} ".format(os.path.join("/notebooks/nebula3_experiments", csv_file_name)))

print("End of running")

