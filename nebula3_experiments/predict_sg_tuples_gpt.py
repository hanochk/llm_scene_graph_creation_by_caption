# export PYTHONPATH=/notebooks/pip_install/
import os
import numpy as np
import sys
from functools import partial
import spacy

from database.arangodb import NEBULA_DB
from nebula3_experiments.prompts_utils import in_context_examples_my_gt, PrompEngFewshotTupleCreation, \
                            breakdown_prompt_to_list_examples, synth_in_context_examples_based, \
                                union_tuples_n_fusion_from_multi_sentence_completion, \
                                    in_context_sentence_examples_mapping_to_parapragh_my_gt, \
                                    check_tuples_sanity_in_context_example, \
                                    _get_few_shot_prompt_sentence_based_to_tuple_4K, reference_prefix_pattern
                                                    

def flatten(lst): return [x for l in lst for x in l]

os.environ["TOKENIZERS_PARALLELISM"] = "false" #huggingface/tokenizers: The current process just got forked, after parallelism has already been used. Disabling parallelism to avoid deadlocks



def get_likely_tuples_from_paragraph_by_sentence(query_paragraph, prompt_util=PrompEngFewshotTupleCreation(), n_fusion=2,
                                    n_completions_gen=1, task='predicting_sentence_gt',
                                    **kwargs):
    
    nlp_model = kwargs.pop('nlp_model', None)
    verbose = kwargs.pop('verbose', False)
    prompt_util.n_fusion = n_fusion
    max_tokens = kwargs.pop('max_tokens', 256)

    all_sentences, all_tuples = breakdown_prompt_to_list_examples(in_context_examples_my_gt)
    assert(len(in_context_sentence_examples_mapping_to_parapragh_my_gt) == len(all_tuples))
    check_tuples_sanity_in_context_example(in_context_examples_my_gt)

    paragraph_indeces = np.unique(in_context_sentence_examples_mapping_to_parapragh_my_gt)
    all_sentences = [x.replace('"',"") for x in all_sentences]

    if n_completions_gen == 1:
        post_process_sentence_fun = None
    else:
        post_process_sentence_fun = union_tuples_n_fusion_from_multi_sentence_completion
        prompt_util.post_process_sentence_fun = partial(post_process_sentence_fun, prompt_util)
    
    fusion_type_for_delta_prediction = None

    sent_indeces_train = list(np.arange(len(in_context_sentence_examples_mapping_to_parapragh_my_gt)))
    # Scramble the sentences out of paragraph among in context examples with an option to take sample out of it

#   GPT context window include the generated tokens as well hence in context = 4K-expected output - over_estimation_of_long_snetences_with_commas
    sents_len = [len(x.strip().replace('"',"") + '.') for x in query_paragraph.split(".")[:-1]]
    # reduction_in_prompt = int((max_tokens + max(sents_len))/256)
    spare_prompt = 4096 - len(in_context_examples_my_gt) - 96 - 10 #96=len('''Generate a list of object-relation-attribute tuples based on the paragraph description. Example:''') 10=sentence, + tuples
    reduction_in_prompt = 0
    if (max_tokens + max(sents_len)) > spare_prompt:
        reduction_in_prompt = 1

    

    rand_paragraph = np.random.choice(sent_indeces_train, len(sent_indeces_train) - reduction_in_prompt, replace=False)
    sent_indeces_train = rand_paragraph

    loo_paragraph_train = [all_sentences[x] for x in sent_indeces_train]
    loo_tuples_train = [all_tuples[x] for x in sent_indeces_train]

    my_gt_tuple = flatten([eval(all_tuples[x]) for x in sent_indeces_test])

    gt_tuple = my_gt_tuple
    loo_in_context_examples_sentence_based = synth_in_context_examples_based(loo_paragraph_train, loo_tuples_train)
    few_shot_prompt_func = _get_few_shot_prompt_sentence_based_to_tuple_4K

    pred_triplets_n = prompt_util.get_likely_tuples_from_paragraph_by_sentence(paragraph=query_paragraph, 
                                            n=n_completions_gen,
                                            few_shot_prompt_func=few_shot_prompt_func,
                                            in_context_examples=loo_in_context_examples_sentence_based,
                                            post_process_sentence_fun=post_process_sentence_fun,
                                            fusion_type=fusion_type_for_delta_prediction, n_fusion=n_fusion,
                                            **kwargs) # get_paragraph_to_anderson_tuple_sentence_prompt_4K


    
    if nlp_model:
        re_all_tup_lst = list()
        for tup in pred_triplets_n:
            if len(tup)==3:
                re_tup_lst = list()
                for ix, sub_tup in enumerate(tup):
                    lematized_ob = sub_tup
                    if ix == 1: # lematize verb only which is the 2nd element in tuple of 3 
                        doc = nlp_model(sub_tup)
                        lematized_ob = " ".join([token.lemma_ for token in doc])
                    re_tup_lst.append(lematized_ob)
                re_all_tup_lst.append(re_tup_lst)
            else:
                re_all_tup_lst.append(tup)

        # res, c = np.unique([re_all_tup_lst, pred_triplets_n], return_counts=True)
        # for ix, cnt in enumerate(c):
        #     if cnt == 1 and verbose:
        #         print('lematization processed the following', res[ix])
    else:
        re_all_tup_lst = pred_triplets_n
                
    return re_all_tup_lst


prompt_util = PrompEngFewshotTupleCreation()
# dummy creation for debug only
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
    query_paragraph = "There are people gathered walking on the snow. Some people are flying kites. There's a man and a child and a stroller beside the man. The stroller is grey and black. There is a man to the left that is walking his dog. The dog is on a leash. There's a building in the background. The sky is partly cloudy. One of the kites flying is yellow."
    pred_triplets = get_likely_tuples_from_paragraph_by_sentence(query_paragraph, prompt_util,
                                                    n_completions_gen=n_completions_gen, nlp_model=nlp_model)

#Evaluation
if unit_test:
    from vg_eval import VGEvaluation

    evaluator = VGEvaluation()
    recall_gt_vs_gpt_sentence_based_n = evaluator.recall_triplets_mean(my_gt_tuple, pred_triplets)
    precision_gt_vs_gpt_sentence_based_n = evaluator.recall_triplets_mean(pred_triplets, my_gt_tuple)
    compute_precision_recall()

pass
