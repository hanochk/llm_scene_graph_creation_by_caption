import os
import sys
# from database.arangodb import DatabaseConnector, DBBase, NEBULA_DB
sys.path.insert(0,"/notebooks/nebula3_database")
sys.path.insert(0,"/notebooks/nebula3_llm_task")
from llm_orchestration import *

#Collection: s4_eval_fusion_amr_gpt_n_10_fusion3_output_hungarian
#EVAL_COLLECTION_NAME = 's4_eval_fusion_gpt_amr_gpt_delta_anderson_output_hungarian'

os.environ["ARANGO_DB"]="ipc_200"
nebula_db = NEBULA_DB()

def process_benchmark(benchmark_name, **kwargs):
    benchmark_tag = kwargs.pop('benchmark_tag', None)
    target_collection_name = kwargs.pop('target_collection_name', None)
    target_db = kwargs.pop('target_db', 'ipc_200')

    results = []

    nebula_db2 = NEBULA_DB()
    if target_db != 'ipc_200':
        nebula_db2.change_db(target_db)

       
    if not nebula_db.db.has_collection(EVAL_COLLECTION_NAME):
        raise
    
    benchmark = list(nebula_db.db.collection('Movies').find({'misc.benchmark_name': benchmark_name}))

    print("Processing {} items".format(len(benchmark)))
    for mobj in benchmark:
        assert(mobj['mdfs'] == [[0]])
        mid = MovieImageId(mobj['_id'],0)
        curr_key = {'movie_id': mobj['_id'], 'benchmark_name': mobj['misc']['benchmark_name'], 'benchmark_tag': mobj['misc']['benchmark_tag']}
        curr_doc = nebula_db.get_doc_by_key2(curr_key, EVAL_COLLECTION_NAME) # why iterator poped or Cursor? where does s4_llm_output defined 
        if not curr_doc:
            print("Not Found existing eval result, moving on: ",  mobj['_id'])
            continue

        curr_doc_pop =  [x for x in curr_doc][0]
        if 'benchmark_tag' not in curr_doc_pop:
            raise
        curr_doc_pop['benchmark_tag'] = benchmark_tag
        try:
            if target_collection_name:
                del curr_doc_pop['_rev']
                del curr_doc_pop['_id']
                rc1 = nebula_db2.write_doc_by_key(curr_doc_pop, target_collection_name, key_list=['image_id', 'movie_id', 'benchmark_name','benchmark_tag'])
            else:
                raise
        except Exception as e:
                print(e)
                print("Failed to parse triplets for mid {}".format(mid))

        print("Result from writing:")
        print(rc1)
    return results

benchmark_name = 'ipc_200'
target_db = 'web_demo' # web_demo or 'ipc_200'
EVAL_COLLECTION_NAME = 's4_eval_fusion_gpt_amr_gpt_delta_anderson_output_relaxed' #'s4_eval_fusion_amr_gpt_n_1_output_relaxed' #'s4_eval_fusion_amr_gpt_n_10_fuse3_output_relaxed'
results = process_benchmark(benchmark_name=benchmark_name, assignment_method='relaxed', 
                            benchmark_tag='fusion_gpt_amr_delta_anderson_relaxed', 
                            target_collection_name='s4_eval_output',
                            target_db=target_db, EVAL_COLLECTION_NAME=EVAL_COLLECTION_NAME)