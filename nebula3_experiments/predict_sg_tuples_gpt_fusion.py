from nebula3_experiments.prompts_utils import *
from nebula3_experiments.predict_sg_tuples_gpt import get_likely_tuples_from_paragraph_by_sentence
from nebula3_experiments.predict_sg_tuples_via_amr import get_likely_tuples_from_paragraph_by_sentence_amr
from nebula3_experiments.predict_sg_tuples_gpt_by_delta import get_likely_tuples_from_paragraph_by_sentence_delta_anderson, get_likely_tuples_from_paragraph_by_sentence_anderson

# from prompts_utils import union_tuples_n_fusion_from_multi_sentence_completion_ind
import amrlib
import spacy



nlp_model = spacy.load('en_core_web_lg')

def get_likely_tuples_from_paragraph_by_sentence_fusion_gpt_amr_gpt_n1(cand):

    pred_triplets_gpt = get_likely_tuples_from_paragraph_by_sentence(cand)
    
    # print('gpt_triplets',len(pred_triplets_gpt))

    pred_triplets_gpt_amr = get_likely_tuples_from_paragraph_by_sentence_amr(cand,
                                                        nlp_model=nlp_model, verbose=True)
    # print('pred_triplets_gpt_amr',len(pred_triplets_gpt_amr))

    fuse_gpts = list()

    fuse_gpts.extend(pred_triplets_gpt)
    fuse_gpts.extend(pred_triplets_gpt_amr)
    # print(len(fuse_gpts))
    fuse_union = union_tuples_n_fusion_from_multi_sentence_completion_ind([fuse_gpts])
    gpt_triplets = fuse_union[0]
    
    return gpt_triplets

def get_likely_tuples_from_paragraph_by_sentence_fusion_gpt_amr_gpt_n1_gpt_n10_fusion3(cand):
    
    pred_triplets_gpt = get_likely_tuples_from_paragraph_by_sentence(cand)
    
    # print('gpt_triplets',len(pred_triplets_gpt))

    pred_triplets_gpt_amr = get_likely_tuples_from_paragraph_by_sentence_amr(cand,
                                                        nlp_model=nlp_model, verbose=True)
    # print('pred_triplets_gpt_amr',len(pred_triplets_gpt_amr))
    
    n_fusion = 3
    pred_triplets_gpt_n_10 = get_likely_tuples_from_paragraph_by_sentence(cand, n_completions_gen=10, n_fusion=n_fusion,
                                                        nlp_model=nlp_model,
                                                        verbose=True)
    
    # print('pred_triplets_gpt_n_10',len(pred_triplets_gpt_n_10))

    fuse_gpts = list()

    fuse_gpts.extend(pred_triplets_gpt)
    fuse_gpts.extend(pred_triplets_gpt_amr)
    fuse_gpts.extend(pred_triplets_gpt_n_10)
    # print(len(fuse_gpts))
    fuse_union = union_tuples_n_fusion_from_multi_sentence_completion_ind([fuse_gpts])
    gpt_triplets = fuse_union[0]

    return gpt_triplets

        # obj[TUPLES_NAME] = np.unique(gpt_triplets).tolist()
def get_likely_tuples_from_paragraph_by_sentence_fusion_gpt_amr_gpt_delta_anderson(cand, verbose=False):
    
    pred_triplets_delta_anderson = get_likely_tuples_from_paragraph_by_sentence_delta_anderson(cand,
                                                    n_completions_gen=1, nlp_model=nlp_model)

    # if verbose:
    #     print(len(pred_triplets_delta_anderson))
    #     pr_delta_anderson, re_delta_anderson = evaluator.compute_precision_recall(pred_triplets_delta_anderson, gt_triplets, assignment_method='hungarian', debug_print=False)
    #     f_score_delta_anderson = 2/(1/pr_delta_anderson+1/re_delta_anderson)
    #     print("delta_anderson Recall {} Precision {} f_score {}".format(re_delta_anderson, pr_delta_anderson, f_score_delta_anderson))
#=======================================================================
    pred_triplets_gpt_gpt_amr_gpt_n1 = get_likely_tuples_from_paragraph_by_sentence_fusion_gpt_amr_gpt_n1(cand)
    # if verbose:
    #     print(len(pred_triplets_gpt_gpt_amr_gpt_n1))
    #     pr, re = evaluator.compute_precision_recall(pred_triplets_gpt_gpt_amr_gpt_n1, gt_triplets, assignment_method='hungarian', debug_print=False)
    #     f_score = 2/(1/pr+1/re)
    #     print("Fusion(AMR-GPT-n1) Recall {} Precision {} f_score {}".format(re, pr, f_score))
#=======================================================================
    fuse_gpts = list()

    fuse_gpts.extend(pred_triplets_gpt_gpt_amr_gpt_n1)
    fuse_gpts.extend(pred_triplets_delta_anderson)
    # print(len(fuse_gpts))
    # fuse_union = union_tuples_n_fusion_from_multi_sentence_completion_ind([fuse_gpts])
    # fuse_union = fuse_union[0]
    fuse_union = np.unique(fuse_gpts).tolist()
    return fuse_union

def get_likely_tuples_from_paragraph_by_sentence_fusion_meta_methods(cand, method={1:'delta_anderson', 2:'single_response', 3:'prior_amr'}, **kwargs):
    n_fusion = kwargs.pop('n_fusion', 3)
    n_completions_gen = kwargs.pop('n_completions_gen', 10)
    fuse_gpts = list()

    meta_methods = ['prior_amr', 'delta_anderson', 'single_response', 'unified_multi_response', 'anderson']
    for k, v in method.items():
        print("combined {} method for tuple generation is : {}".format(k, v))
        if v == 'prior_amr':
            pred_triplets_gpt = get_likely_tuples_from_paragraph_by_sentence_amr(cand,
                                                            nlp_model=nlp_model)
            fuse_gpts.extend(pred_triplets_gpt)
        elif v == 'delta_anderson':
            pred_triplets_gpt = get_likely_tuples_from_paragraph_by_sentence_delta_anderson(cand,
                                                            n_completions_gen=1, nlp_model=nlp_model)
            fuse_gpts.extend(pred_triplets_gpt)

        elif v == 'single_response':
            pred_triplets_gpt = get_likely_tuples_from_paragraph_by_sentence(cand)
            fuse_gpts.extend(pred_triplets_gpt)

        elif v == 'unified_multi_response':
            pred_triplets_gpt = get_likely_tuples_from_paragraph_by_sentence(cand, n_completions_gen=n_completions_gen, 
                                                                    n_fusion=n_fusion, nlp_model=nlp_model)
            fuse_gpts.extend(pred_triplets_gpt)
        elif v == 'anderson':
            pred_triplets = get_likely_tuples_from_paragraph_by_sentence_anderson(cand)
            fuse_gpts.extend(pred_triplets)

        else:
            raise ValueError("A method for tuple generation is unknown", v)

# Remove repetative tuples    
    fuse_union = np.unique(fuse_gpts).tolist()
    return fuse_union
