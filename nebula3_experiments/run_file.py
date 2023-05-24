# export PYTHONPATH=/notebooks/pip_install/
from predict_sg_tuples_gpt import get_likely_tuples_from_paragraph_by_sentence
from predict_sg_tuples_via_amr import get_likely_tuples_from_paragraph_by_sentence_amr
from predict_sg_tuples_gpt_by_delta import get_likely_tuples_from_paragraph_by_sentence_delta_anderson
import spacy
import json
from ipc_utils import get_visual_genome_record_by_ipc_id
from vg_eval import get_sc_graph, tuples_from_sg, spice_get_triplets
import amrlib  #  clone https://github.com/bjascob/amrlib instructions on https://amrlib.readthedocs.io/en/latest/install/ models path in pip3 show amrlib =>  /usr/local/lib/python3.9/dist-packages
from database.arangodb import *
from vg_eval import VGEvaluation, Sg_handler
# from predict_sg_tuples_gpt_fusion import get_likely_tuples_from_paragraph_by_sentence_fusion_gpt_amr_gpt_n1
from prompts_utils import *
from predict_sg_tuples_gpt_fusion import *
import pandas as pd

nebula_db = NEBULA_DB()
evaluator = VGEvaluation()


def sort_gpt_to_anderson_dist(gpt_tuple_collection):
    benchmark = list(nebula_db.db.collection('Movies').find({'misc.benchmark_name': 'ipc_200'}))
    pre_recall_anderson_gpt = list()
    for ix ,bm in enumerate(benchmark):
        mid = MovieImageId(movie_id=bm['_id'], frame_num=0)
        obj = nebula_db.get_movie_frame_from_collection(mid, LLM_OUTPUT_COLLECTION)
        target_id = os.path.split(obj['url'])[1].split('.')[0]
        sg = get_sc_graph(int(target_id))

        gt_triplets = tuples_from_sg(sg)
        pred_triplets_gpt = obj[gpt_tuple_collection]
        pred_triplets_anderson = obj['triplets']


        pr_gpt, re_gpt = evaluator.compute_precision_recall(pred_triplets_gpt, gt_triplets, assignment_method='hungarian', debug_print=False)
        f_score_gpt = 2/(1/pr_gpt+1/re_gpt)
        print("GPT: Recall {} Precision {} f_score {}".format(re_gpt, pr_gpt, f_score_gpt))
        pr_anderson, re_anderson = evaluator.compute_precision_recall(pred_triplets_anderson, gt_triplets, assignment_method='hungarian', debug_print=False)
        f_score_anderson = 2/(1/pr_anderson+1/re_anderson)
        print("Anderson: Recall {} Precision {} f_score {}".format(re_anderson, pr_anderson, f_score_anderson))

        pre_recall_anderson_gpt.append({'pr_anderson':pr_anderson,'re_anderson':re_anderson, 'pr_gpt':pr_gpt, 're_gpt': re_gpt})
        if re_anderson - re_gpt>0.1:
            print(target_id, re_anderson , re_gpt ,f_score_anderson, f_score_gpt)
        if ix%10 == 0:
            df_results = pd.DataFrame(pre_recall_anderson_gpt)
            df_results.to_csv(os.path.join("/notebooks/nebula3_experiments", 'precision_recall_anderson_' + str(gpt_tuple_collection) + '_ipc200.csv'), index=False)


    df_results = pd.DataFrame(pre_recall_anderson_gpt)
    df_results.to_csv(os.path.join("/notebooks/nebula3_experiments", 'precision_recall_anderson_' + str(gpt_tuple_collection) + '_ipc200.csv'), index=False)

    return pre_recall_anderson_gpt
    

query_paragraph = 'The cat sat on the mat'
nlp_model = spacy.load('en_core_web_lg')
unittest = True
filter_mid_from_db = True
stog = amrlib.load_stog_model(model_dir='/notebooks/amrlib/model_parse_xfm_bart_large-v0_1_0/')   #stog = amrlib.load_stog_model()
max_token = 256 # sentence based 256 is enough

ids_to_eval = [2406250, 2372386, 2337492 ,2385334]#[2337219, 2406250, 2372386, 2337492 ,2385334] #[2337219] #[2406250, 2372386, 2337492 ,2385334]
for image_id in ids_to_eval:
    if unittest:
        # pre_recall_anderson_gpt_dist = sort_gpt_to_anderson_dist(gpt_tuple_collection='gpt_triplets_fusion_amr_gpt_n_1')

        # image_id = 2406250 #2372386 #2337492 ,2385334
        if filter_mid_from_db:
            
            # from llm_api import *    
            # 'There is a man flying a kite on the beach. The man is dressed in a blue t-shirt and white shorts. He is wearing sandals on the sand. Behind him are other people sunbathing and walking in the sand. The beach is lined with palm trees and there is a horizon of blue sea in the distance.'
            benchmark = list(nebula_db.db.collection('Movies').find({'misc.benchmark_name': 'ipc_200'}))
            if 1:
                x = benchmark[94]
            else:
                x = [x for x in benchmark if x['name']==str(image_id)][0]

            # mid = MovieImageId(movie_id='Movies/8260685760535150098', frame_num=0)
            mid = MovieImageId(movie_id=x['_id'], frame_num=0)
            obj = nebula_db.get_movie_frame_from_collection(mid, LLM_OUTPUT_COLLECTION)
            target_id = os.path.split(obj['url'])[1].split('.')[0]   

            sg = get_sc_graph(int(target_id))
            gt_triplets = tuples_from_sg(sg)
            pred_triplets_gpt5 = obj['gpt_triplets5']
            query_paragraph = obj['candidate']
            # nebula_db.get_movie_frame_from_collection
        else:
            # query_paragraph = 'This picture shows a desk with a computer on its right side. On the left side of the desk is a pile of books. At least nine titles can be seen on the spines of the books, including at least one that has the title “Fiction Classics.”'
            # query_paragraph = 'The image is of a brick building with a large clock mounted on the side of it. The clock has large roman numerals and hands indicating the time. There are shades of red and beige that give the clock a rustic feel. The clock has a red frame, and the words "2 o\'clock" are written on the face of the clock.'
            # query_paragraph = 'A large truck is parked in front of a single-story house in a residential neighborhood. The truck is white with a painted blue and red logo on the side. The tires are large and the windows are tinted. There are green shrubs and trees surrounding the house. The roof of the house has shingles on it.'
            # query_paragraph = "A white and gray cat is sitting in the driver's seat of a car on a desert road. The seatbelt is across the cat's chest and the steering wheel is by its side. The cat is looking out of the driver's window into the desert horizon ahead. The windshield of the car is tinted yellow from the setting sun. There are no other cars visible in the background."
            # resp_do_lematization =  [['man', 'hold', 'dog'] , ['man', 'holding', 'dog'], ['woman', 'standing']] # only over the verb part in tuple of 3 
            # query_paragraph = "There are people gathered walking on the snow. Some people are flying kites. There's a man and a child and a stroller beside the man. The stroller is grey and black. There is a man to the left that is walking his dog. The dog is on a leash. There's a building in the background. The sky is partly cloudy. One of the kites flying is yellow."
            query_paragraph = 'The image is of a flock of birds perched on a dead tree branch silhouetted against a vibrant blue sky. There are several different types of bird in the flock, including pelicans, ibis, and cockateels, as well as a few woodpeckers. The tree branch is a greyish-brown color, and is splitting in the center where the flock of birds is gathered. The dead tree looks as if it has been thriving at one point and the leaves have since died and fallen off.'

        #2387231
        if 0:
            # import nebula_vg_driver.visual_genome.api as vg_api
            # vg_api.get_scene_graph_of_image(image_id)
            from  ipc_utils import vgenome_metadata
            sg_handler = Sg_handler(images_path=vgenome_metadata,  # data = json.load(open(image_data_dir + fname, 'r')) [(x['attribute']) for x in data['attributes']][1]['attributes']
                image_data_dir=vgenome_metadata+'/by-id/',
                synset_file=vgenome_metadata+'/synsets.json')

            region_gr = json.load(open('/api/region_graphs.json', 'r'))
            sg_handler.get_scene_graph_of_image(image_id)

            vg_record = get_visual_genome_record_by_ipc_id(image_id)
            query_paragraph = vg_record['paragraph']
            ipc_triplets = spice_get_triplets(vg_record['paragraph'])
            sg = get_sc_graph(vg_record['image_id'])
            gt_triplets = tuples_from_sg(sg)

    if 0:
        pred_triplets = get_likely_tuples_from_paragraph_by_sentence(query_paragraph,
                                                            nlp_model=nlp_model,
                                                            stog=stog)
    else:

        # query_paragraph = 'There are black and grey and even yellow and white.'
        pred_triplets_fusion_gpt_amr_gpt_delta_anderson_api = get_likely_tuples_from_paragraph_by_sentence_fusion_meta_methods(query_paragraph)
        pred_triplets_fusion_gpt_amr_gpt_delta_anderson = get_likely_tuples_from_paragraph_by_sentence_fusion_gpt_amr_gpt_delta_anderson(query_paragraph, verbose=False)
        
        pr_fusion_gpt_amr_gpt_delta_anderson, re_fusion_gpt_amr_gpt_delta_anderson = evaluator.compute_precision_recall(pred_triplets_fusion_gpt_amr_gpt_delta_anderson, gt_triplets, assignment_method='hungarian', debug_print=False)
        f_score_fusion_gpt_amr_gpt_delta_anderson = 2/(1/pr_fusion_gpt_amr_gpt_delta_anderson + 1/re_fusion_gpt_amr_gpt_delta_anderson)
        print("fusion_gpt_amr_gpt_delta_anderson Recall {} Precision {} f_score {}".format(re_fusion_gpt_amr_gpt_delta_anderson, pr_fusion_gpt_amr_gpt_delta_anderson, f_score_fusion_gpt_amr_gpt_delta_anderson))


        pr_anderson, re_anderson = evaluator.compute_precision_recall(obj['triplets'], gt_triplets, assignment_method='hungarian', debug_print=False)
        f_score_anderson = 2/(1/pr_anderson+1/re_anderson)
        print("Anderson Recall {} Precision {} f_score {}".format(re_anderson, pr_anderson, f_score_anderson))

        print(len(pred_triplets_gpt5))

        pr_gpt5, re_gpt5 = evaluator.compute_precision_recall(pred_triplets_gpt5, gt_triplets, assignment_method='hungarian', debug_print=False)
        f_score_gpt5 = 2/(1/pr_gpt5+1/re_gpt5)
        print("gpt5: Recall {} Precision {} f_score {}".format(re_gpt5, pr_gpt5, f_score_gpt5))


        pred_triplets_delta_anderson = get_likely_tuples_from_paragraph_by_sentence_delta_anderson(query_paragraph,
                                                        n_completions_gen=1, nlp_model=nlp_model)

        print(len(pred_triplets_delta_anderson))
        pr_delta_anderson, re_delta_anderson = evaluator.compute_precision_recall(pred_triplets_delta_anderson, gt_triplets, assignment_method='hungarian', debug_print=False)
        f_score_delta_anderson = 2/(1/pr_delta_anderson+1/re_delta_anderson)
        print("delta_anderson Recall {} Precision {} f_score {}".format(re_delta_anderson, pr_delta_anderson, f_score_delta_anderson))
#=======================================================================
        pred_triplets_gpt_gpt_amr_gpt_n1 = get_likely_tuples_from_paragraph_by_sentence_fusion_gpt_amr_gpt_n1(query_paragraph)
        print(len(pred_triplets_gpt_gpt_amr_gpt_n1))

        pr, re = evaluator.compute_precision_recall(pred_triplets_gpt_gpt_amr_gpt_n1, gt_triplets, assignment_method='hungarian', debug_print=False)
        f_score = 2/(1/pr+1/re)
        print("Fusion(AMR-GPT-n1) Recall {} Precision {} f_score {}".format(re, pr, f_score))
#=======================================================================
        fuse_gpts = list()

        fuse_gpts.extend(pred_triplets_gpt_gpt_amr_gpt_n1)
        fuse_gpts.extend(pred_triplets_delta_anderson)
        print(len(fuse_gpts))
        # fuse_union = union_tuples_n_fusion_from_multi_sentence_completion_ind([fuse_gpts])
        # fuse_union = fuse_union[0]
        fuse_union = np.unique(fuse_gpts).tolist()

        pr_gpt_amr_gpt_n1_gpt_delta_anderson, re_gpt_amr_gpt_n1_gpt_delta_anderson = evaluator.compute_precision_recall(fuse_union, gt_triplets, assignment_method='hungarian', debug_print=False)
        f_score_gpt_amr_gpt_n1_gpt_delta_anderson = 2/(1/pr_gpt_amr_gpt_n1_gpt_delta_anderson+1/re_gpt_amr_gpt_n1_gpt_delta_anderson)
        print("score_gpt_amr_gpt_n1_gpt_delta_anderson: Recall {} Precision {} f_score {}".format(re_gpt_amr_gpt_n1_gpt_delta_anderson, pr_gpt_amr_gpt_n1_gpt_delta_anderson, f_score_gpt_amr_gpt_n1_gpt_delta_anderson))

        # pred_triplets_gpt_m1 = get_likely_tuples_from_paragraph_by_sentence(query_paragraph,
        #                                                     nlp_model=nlp_model,
        #                                                     max_tokens=max_token, logit_bias={"50256":-1}, verbose=True)
        
        # print(len(pred_triplets_gpt_m1))

        # pred_triplets_gpt = get_likely_tuples_from_paragraph_by_sentence(query_paragraph,
        #                                                     nlp_model=nlp_model,
        #                                                     max_tokens=max_token, verbose=True)

        n_fusion = 3
        pred_triplets_gpt_n_10 = get_likely_tuples_from_paragraph_by_sentence(query_paragraph, n_completions_gen=10, n_fusion=n_fusion,
                                                            nlp_model=nlp_model,
                                                            max_tokens=max_token, verbose=True)
        print(len(pred_triplets_gpt_n_10))

        pr_gpt_n10, re_gpt_n10 = evaluator.compute_precision_recall(pred_triplets_gpt_n_10, gt_triplets, assignment_method='hungarian', debug_print=False)
        f_score_gpt_n10 = 2/(1/pr_gpt_n10+1/re_gpt_n10)
        print("gpt_n_10_fusion_n: Recall {} Precision {} f_score {} n_fusion {}".format(re_gpt_n10, pr_gpt_n10, f_score_gpt_n10, n_fusion))

        if 0:
            pred_triplets_gpt_amr = get_likely_tuples_from_paragraph_by_sentence_amr(query_paragraph,
                                                                nlp_model=nlp_model,
                                                                max_tokens=max_token, verbose=True)
            print(len(pred_triplets_gpt_amr))

            # pred_triplets = get_likely_tuples_from_paragraph_by_sentence(query_paragraph,
            #                                                     nlp_model=nlp_model,
            #                                                     max_tokens=256+128, logit_bias={50256:-1})
            from prompts_utils import union_tuples_n_fusion_from_multi_sentence_completion_ind
            fuse_gpts = list()

            fuse_gpts.extend(pred_triplets_gpt5)
            fuse_gpts.extend(pred_triplets_gpt_amr)
            print(len(fuse_gpts))
            fuse_union = union_tuples_n_fusion_from_multi_sentence_completion_ind([fuse_gpts])
            fuse_union = fuse_union[0]
    if unittest:

        print("image_id", image_id)
        # recall_gt_vs_gpt_sentence_based_n = evaluator.recall_triplets_mean(gt_triplets, pred_triplets)
        # precision_gt_vs_gpt_sentence_based_n = evaluator.recall_triplets_mean(pred_triplets, gt_triplets)



        pr_gpt5, re_gpt5 = evaluator.compute_precision_recall(pred_triplets_gpt5, gt_triplets, assignment_method='hungarian', debug_print=False)
        f_score_gpt5 = 2/(1/pr_gpt5+1/re_gpt5)
        print("gpt5: Recall {} Precision {} f_score {}".format(re_gpt5, pr_gpt5, f_score_gpt5))
        


    # print(pred_triplets)