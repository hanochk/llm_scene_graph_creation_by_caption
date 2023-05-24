# export PYTHONPATH=/notebooks/pip_install/
import os
import numpy as np
import sys
from functools import partial
import spacy

from database.arangodb import NEBULA_DB
from nebula3_experiments.vg_eval import spice_get_triplets
from nebula3_experiments.prompts_utils import *
from nebula3_experiments.prompts_utils import _get_few_shot_prompt_sentence_based_to_delta_anderson_tuple_4K

def flatten(lst): return [x for l in lst for x in l]

os.environ["TOKENIZERS_PARALLELISM"] = "false" #huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks


def get_likely_tuples_from_paragraph_by_sentence_anderson(cand):
    return spice_get_triplets(cand)

def get_likely_tuples_from_paragraph_by_sentence_delta_anderson(query_paragraph, prompt_util=PrompEngFewshotTupleCreation(),n_fusion = 2,
                                    n_completions_gen = 1, **kwargs):
    # n_completions_gen = 10
    
    prompt_util.n_fusion = n_fusion
    margin_for_prompt_suffix = 512
    verbose = kwargs.pop('verbose', False)
    max_tokens = kwargs.pop('max_tokens', 256)
    nlp_model = kwargs.pop('nlp_model', spacy.load('en_core_web_lg'))
    

    all_sentences, all_tuples = breakdown_prompt_to_list_examples(in_context_examples_my_gt)
    assert(len(in_context_sentence_examples_mapping_to_parapragh_my_gt) == len(all_tuples))
    check_tuples_sanity_in_context_example(in_context_examples_my_gt)

    paragraph_indeces = np.unique(in_context_sentence_examples_mapping_to_parapragh_my_gt)
    all_sentences = [x.replace('"',"") for x in all_sentences]

    # post_process_sentence_fun = union_tuples_n_fusion_from_multi_sentence_completion
    # prompt_util.post_process_sentence_fun = partial(post_process_sentence_fun, prompt_util)

    sents_len = [len(x.strip().replace('"',"") + '.') for x in query_paragraph.split(".")[:-1]]
    size_limit_n_paragraph = limit_paragrapgs_by_prompt_size_pred_delta_anderson(all_sentences, max_query=max(sents_len)+max_tokens)
    if 0:
        size_limit_n_paragraph = size_limit_n_paragraph - 2 #Hack
# Random picking limited in size prompt since prompt is larger
    common_seed = 19121
    unique_run_name = str(int(time.time()))
    predefined_seed = True

    if predefined_seed:
        np.random.seed(common_seed)
        print("Warning pre defined seed R U sure ?")
    else:
        np.random.seed(unique_run_name)

    prmute_prompt_monte_carlo = len(all_sentences) - size_limit_n_paragraph # it is Permute n out of m where order is meaningless
    random_iter = range(prmute_prompt_monte_carlo)


    fusion_type_for_delta_prediction = 'delta_operator_fusion' # 'prompt_fusion'
    # fusion_type = 'final_tuples_fusion'

    post_process_sentence_fun = create_arithmetic_final_tuple_from_proposed_and_predict # need to calculate the arithmetics and yield final result
    prompt_util.post_process_sentence_fun = partial(create_arithmetic_final_tuple_from_proposed_and_predict, prompt_util)



    # if n_completions_gen == 1:
    #     post_process_sentence_fun = None
    # else:
    #     post_process_sentence_fun = union_tuples_n_fusion_from_multi_sentence_completion
    #     prompt_util.post_process_sentence_fun = partial(post_process_sentence_fun, prompt_util)


    sent_indeces_train = list(np.arange(len(in_context_sentence_examples_mapping_to_parapragh_my_gt)))
    # Scramble the sentences out of paragraph among in context examples with an option to take sample out of it
    rand_paragraph = np.random.choice(sent_indeces_train, size_limit_n_paragraph, replace=False)
    sent_indeces_train = rand_paragraph

    loo_paragraph_train = [all_sentences[x] for x in sent_indeces_train]
    loo_tuples_train = [all_tuples[x] for x in sent_indeces_train]

    # gt_tuple = my_gt_tuple
    # loo_in_context_examples_sentence_based = synth_in_context_examples_based(loo_paragraph_train, loo_tuples_train)
    # few_shot_prompt_func = _get_few_shot_prompt_sentence_based_to_tuple_4K

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

    pred_triplets_n = prompt_util.get_likely_tuples_from_paragraph_by_sentence(paragraph=query_paragraph, 
                                            n=n_completions_gen,
                                            few_shot_prompt_func=few_shot_prompt_func,
                                            in_context_examples=loo_in_context_examples_sentence_based,
                                            post_process_sentence_fun=post_process_sentence_fun,
                                            reference_tuples=query_proposed_ngrams, 
                                            fusion_type=fusion_type_for_delta_prediction, n_fusion=n_fusion,
                                            verbose=verbose, **kwargs) # get_paragraph_to_anderson_tuple_sentence_prompt_4K


    if nlp_model:
        pred_triplets_n = lematize_verb_tup_3(pred_triplets_n, nlp_model)

    return pred_triplets_n



sent_indeces_test = [0, 1] # dummy creation
unit_test = False
n_completions_gen = 1
lematization = True
if lematization:
    nlp_model = spacy.load('en_core_web_lg')

query_paragraph = None
if unit_test:
    all_sentences, all_tuples = breakdown_prompt_to_list_examples(in_context_examples_my_gt)
    all_sentences = [x.replace('"',"") for x in all_sentences]

    query_paragraph = ''.join([all_sentences[x] for x in sent_indeces_test]).replace('"',"") # dummy creation
    my_gt_tuple = flatten([eval(all_tuples[x]) for x in sent_indeces_test])

    # query_paragraph = 'The image is of a brick building with a large clock mounted on the side of it. The clock has large roman numerals and hands indicating the time. There are shades of red and beige that give the clock a rustic feel. The clock has a red frame, and the words "2 o\'clock" are written on the face of the clock.'
    # query_paragraph = 'A large truck is parked in front of a single-story house in a residential neighborhood. The truck is white with a painted blue and red logo on the side. The tires are large and the windows are tinted. There are green shrubs and trees surrounding the house. The roof of the house has shingles on it.'
    # query_paragraph = "A white and gray cat is sitting in the driver's seat of a car on a desert road. The seatbelt is across the cat's chest and the steering wheel is by its side. The cat is looking out of the driver's window into the desert horizon ahead. The windshield of the car is tinted yellow from the setting sun. There are no other cars visible in the background."
    # resp_do_lematization =  [['man', 'hold', 'dog'] , ['man', 'holding', 'dog'], ['woman', 'standing']] # only over the verb part in tuple of 3 
    # query_paragraph = "There are people gathered walking on the snow. Some people are flying kites. There's a man and a child and a stroller beside the man. The stroller is grey and black. There is a man to the left that is walking his dog. The dog is on a leash. There's a building in the background. The sky is partly cloudy. One of the kites flying is yellow."
    pred_triplets_delta_anderson = get_likely_tuples_from_paragraph_by_sentence_delta_anderson(query_paragraph,
                                                    n_completions_gen=n_completions_gen, nlp_model=nlp_model)

#Evaluation
if unit_test:
    from vg_eval import VGEvaluation

    evaluator = VGEvaluation()
    pre, re = evaluator.compute_precision_recall(pred_triplets_delta_anderson, my_gt_tuple, assignment_method='hungarian', debug_print=True)
    recall_gt_vs_gpt_sentence_based_n = evaluator.recall_triplets_mean(my_gt_tuple, pred_triplets_delta_anderson)
    precision_gt_vs_gpt_sentence_based_n = evaluator.recall_triplets_mean(pred_triplets, my_gt_tuple)

pass

