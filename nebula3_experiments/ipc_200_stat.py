# export PYTHONPATH=/notebooks/pip_install/
from nebula3_experiments.predict_sg_tuples_gpt import get_likely_tuples_from_paragraph_by_sentence
from nebula3_experiments.predict_sg_tuples_via_amr import get_likely_tuples_from_paragraph_by_sentence_amr
import spacy
import json
from nebula3_experiments.ipc_utils import get_visual_genome_record_by_ipc_id
from nebula3_experiments.vg_eval import get_sc_graph, tuples_from_sg, spice_get_triplets
import amrlib  #  clone https://github.com/bjascob/amrlib instructions on https://amrlib.readthedocs.io/en/latest/install/ models path in pip3 show amrlib =>  /usr/local/lib/python3.9/dist-packages
from database.arangodb import *
from nebula3_experiments.vg_eval import VGEvaluation, Sg_handler
nebula_db = NEBULA_DB()
evaluator = VGEvaluation()
import pandas as pd


def sort_gpt_to_anderson_dist():
    benchmark = list(nebula_db.db.collection('Movies').find({'misc.benchmark_name': 'ipc_200'}))
    pre_recall_anderson_gpt = list()
    for ix, bm in enumerate(benchmark):
        mid = MovieImageId(movie_id=bm['_id'], frame_num=0)
        obj = nebula_db.get_movie_frame_from_collection(mid, LLM_OUTPUT_COLLECTION)
        target_id = os.path.split(obj['url'])[1].split('.')[0]
        sg = get_sc_graph(int(target_id))

        gt_triplets = tuples_from_sg(sg)
        pred_triplets_gpt = obj['gpt_triplets5']
        pred_triplets_anderson = obj['triplets']


        pr_gpt, re_gpt = evaluator.compute_precision_recall(pred_triplets_gpt, gt_triplets, assignment_method='hungarian', debug_print=False)
        f_score_gpt = 2/(1/pr_gpt+1/re_gpt)
        print("GPT: Recall {} Precision {} f_score {}".format(re_gpt, pr_gpt, f_score_gpt))
        pr_anderson, re_anderson = evaluator.compute_precision_recall(pred_triplets_anderson, gt_triplets, assignment_method='hungarian', debug_print=False)
        f_score_anderson = 2/(1/pr_anderson+1/re_anderson)

        pre_recall_anderson_gpt.append({'target_id':target_id, 'pr_anderson':pr_anderson,'re_anderson':re_anderson, 'pr_gpt':pr_gpt, 're_gpt': re_gpt, 'mid': mid})
        if re_anderson - re_gpt>0.1:
            print(target_id, re_anderson , re_gpt ,f_score_anderson, f_score_gpt)
        if ix%10 == 0:
            df_results = pd.DataFrame(pre_recall_anderson_gpt)
            df_results.to_csv(os.path.join("/notebooks/nebula3_experiments", 'precision_recall_anderson_gpt5_ipc200.csv'), index=False)
    
    df_results = pd.DataFrame(pre_recall_anderson_gpt)
    df_results.to_csv(os.path.join("/notebooks/nebula3_experiments", 'precision_recall_anderson_gpt5_ipc200.csv'), index=False)

    return pre_recall_anderson_gpt
    

query_paragraph = 'The cat sat on the mat'
nlp_model = spacy.load('en_core_web_lg')
unittest = True
filter_mid_from_db = True
stog = amrlib.load_stog_model(model_dir='/notebooks/amrlib/model_parse_xfm_bart_large-v0_1_0/')   #stog = amrlib.load_stog_model()
max_token = 256+128

pre_recall_anderson_gpt_dist = sort_gpt_to_anderson_dist()

