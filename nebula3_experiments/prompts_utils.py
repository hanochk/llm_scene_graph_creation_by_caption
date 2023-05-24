import time
import openai
import numpy as np
import re
import ast
import copy
import nltk
import pandas as pd 
import spacy
nltk.download('punkt')
from nltk import tokenize
from database.arangodb import NEBULA_DB

try:
    with open('/storage/keys/openai.key','r') as f:
        OPENAI_API_KEY = f.readline().strip()
    openai.api_key = OPENAI_API_KEY
except:
    nebula_db = NEBULA_DB()
    openai.api_key = nebula_db.get_llm_key()

reference_prefix_pattern = "Reference tuples:"
delta_prefix_pattern = "Correction tuples:"
amr_reference_prefix_pattern = "AMR:" #"Reference abstract meaning representation:"
amr_delta_prefix_pattern = "Tuples:"
max_tuple_len = 4
margin_for_prompt_suffix = 512

def flatten(lst): return [x for l in lst for x in l]

def create_arithmetic_final_tuple_from_proposed_and_predict(self, pred_triplets, **kwargs):
    method = 'recall_support'
    _reference_tuples = kwargs.pop('reference_tuples', None)
    fusion_type = kwargs.pop('fusion_type', None)
    n_fusion = kwargs.pop('n_fusion', 1)

    assert(isinstance(pred_triplets, list))

    all_reference_tuples = [_reference_tuples]*len(pred_triplets) # support multiple GPT results
    reference_tuples_for_operator_fusion = copy.deepcopy(_reference_tuples)

    all_reconstructed_tuples = list()
    addition_tuples = list()
    subtraction_tuples = list()
    for ix, pred_triplets_sampled in enumerate(pred_triplets):
        reference_tuples_tmp = copy.deepcopy(all_reference_tuples[ix])
        delta_tuples = list(eval([x.replace("+",",").replace("-",",").strip().rstrip(',').lstrip(',') for x in [pred_triplets_sampled]][0]))
        addition_sign = np.where(['+' in x for x in pred_triplets_sampled])[0]
        sub_sign = np.where(['-' in x for x in pred_triplets_sampled])[0]
        if len(delta_tuples) != len(addition_sign) + len(sub_sign):
            print("hueston: amount of + op and - op doesnot equal to correction list len - skip in context example", addition_sign, sub_sign, pred_triplets_sampled)
            continue # skip this loop
        unify_op = list(set.union(set(sub_sign), set(addition_sign)))
        unify_op = np.sort(np.array(unify_op))

# Do the arithmetics add/subtract
        for ix, tup in enumerate(delta_tuples):
            if not isinstance(tup, list):
                tup = [tup]

            if unify_op[ix] in addition_sign:
                reference_tuples_tmp.append(tup) # add tuple
                addition_tuples.append(tup)
            elif unify_op[ix] in sub_sign:
                if tup in reference_tuples_tmp: # Might be that subtraction of non existing tuple
                    reference_tuples_tmp.remove(tup) # subtract/remove tuple
                    subtraction_tuples.append(tup)
                else:
                    print("Subtraction tuple : {} non existed in reference tuples{}".format(tup, _reference_tuples))
            else:
                raise ValueError('Option not valid')
        reconstructed_tuples = [rc_x for rc_x in reference_tuples_tmp if len(rc_x) < max_tuple_len and len(rc_x)>0]
        all_reconstructed_tuples.append(reconstructed_tuples)
# Sanity check for the tuples list
    for all_reconstructed_tuple_i in all_reconstructed_tuples:
        try:
            str(eval(str(all_reconstructed_tuple_i))).replace(" ", "") == str(all_reconstructed_tuple_i).replace(" ", "")
        except:
            print('not an intact tuple !!!', all_reconstructed_tuple_i)

        
    if len(pred_triplets) > 1: # fusion n>1 GPT responses according to n_fusion
        all_reconstructed_tuples = union_tuples_n_fusion_from_multi_sentence_completion_ind(all_reconstructed_tuples, n_fusion=n_fusion)
        all_union_addition_tuples = union_tuples_n_fusion_from_multi_sentence_completion_ind(
                                                                            pred_triplets=[addition_tuples], n_fusion=n_fusion)[0]
        all_union_subtraction_tuples = union_tuples_n_fusion_from_multi_sentence_completion_ind(
                                                                            pred_triplets=[subtraction_tuples], n_fusion=n_fusion)[0]
        if fusion_type == 'delta_operator_fusion':# first add than subtract hence unified add/sub will be ultimately subtracted since sub is the last OP.
            if method == 'precision_support': # add than subtract
                for add_tup in all_union_addition_tuples:
                    reference_tuples_for_operator_fusion.append(add_tup)
                for sub_tup in all_union_subtraction_tuples:
                    if sub_tup in reference_tuples_for_operator_fusion: # Might be that subtraction of non existing tuple
                        reference_tuples_for_operator_fusion.remove(sub_tup)
                    else:
                        print("Fusiod subtraction tuple : {} non existed in reference tuples{}".format(sub_tup, reference_tuples_for_operator_fusion))
            elif method == 'recall_support': # subtract than add
                for sub_tup in all_union_subtraction_tuples:
                    if sub_tup in reference_tuples_for_operator_fusion: # Might be that subtraction of non existing tuple
                        reference_tuples_for_operator_fusion.remove(sub_tup)
                    else:
                        print("Fusiod subtraction tuple : {} non existed in reference tuples{}".format(sub_tup, reference_tuples_for_operator_fusion))
                for add_tup in all_union_addition_tuples:
                    reference_tuples_for_operator_fusion.append(add_tup)
            if isinstance(reference_tuples_for_operator_fusion[0][0], list):
                return reference_tuples_for_operator_fusion #fusion_type == 'delta_operator_fusion'
            else:
                return [reference_tuples_for_operator_fusion] #fusion_type == 'delta_operator_fusion'
            

    return all_reconstructed_tuples #For method of 

def create_final_tuple_from_proposed_and_predict(self, pred_triplets, **kwargs):
    method = 'recall_support'
    _reference_tuples = kwargs.pop('reference_tuples', None)
    fusion_type = kwargs.pop('fusion_type', None)
    n_fusion = kwargs.pop('n_fusion', 1)

    assert(isinstance(pred_triplets, list))
    raise # not imp yest
    all_reference_tuples = [_reference_tuples]*len(pred_triplets) # support multiple GPT results
    reference_tuples_for_operator_fusion = copy.deepcopy(_reference_tuples)

    all_reconstructed_tuples = list()
    addition_tuples = list()
    subtraction_tuples = list()
    for ix, pred_triplets_sampled in enumerate(pred_triplets):
        reference_tuples_tmp = copy.deepcopy(all_reference_tuples[ix])
        delta_tuples = list(eval([x.replace("+",",").replace("-",",").strip().rstrip(',').lstrip(',') for x in [pred_triplets_sampled]][0]))
        addition_sign = np.where(['+' in x for x in pred_triplets_sampled])[0]
        sub_sign = np.where(['-' in x for x in pred_triplets_sampled])[0]
        if len(delta_tuples) != len(addition_sign) + len(sub_sign):
            print("hueston: amount of + op and - op doesnot equal to correction list len - skip in context example", addition_sign, sub_sign, pred_triplets_sampled)
            continue # skip this loop
        unify_op = list(set.union(set(sub_sign), set(addition_sign)))
        unify_op = np.sort(np.array(unify_op))

# Do the arithmetics add/subtract
        for ix, tup in enumerate(delta_tuples):
            if not isinstance(tup, list):
                tup = [tup]

            if unify_op[ix] in addition_sign:
                reference_tuples_tmp.append(tup) # add tuple
                addition_tuples.append(tup)
            elif unify_op[ix] in sub_sign:
                if tup in reference_tuples_tmp: # Might be that subtraction of non existing tuple
                    reference_tuples_tmp.remove(tup) # subtract/remove tuple
                    subtraction_tuples.append(tup)
                else:
                    print("Subtraction tuple : {} non existed in reference tuples{}".format(tup, _reference_tuples))
            else:
                raise ValueError('Option not valid')
        reconstructed_tuples = [rc_x for rc_x in reference_tuples_tmp if len(rc_x) < max_tuple_len and len(rc_x)>0]
        all_reconstructed_tuples.append(reconstructed_tuples)
# Sanity check for the tuples list
    for all_reconstructed_tuple_i in all_reconstructed_tuples:
        try:
            str(eval(str(all_reconstructed_tuple_i))).replace(" ", "") == str(all_reconstructed_tuple_i).replace(" ", "")
        except:
            print('not an intact tuple !!!', all_reconstructed_tuple_i)

        
    if len(pred_triplets) > 1: # fusion n>1 GPT responses according to n_fusion
        all_reconstructed_tuples = union_tuples_n_fusion_from_multi_sentence_completion_ind(all_reconstructed_tuples, n_fusion=n_fusion)
        all_union_addition_tuples = union_tuples_n_fusion_from_multi_sentence_completion_ind(
                                                                            pred_triplets=[addition_tuples], n_fusion=n_fusion)[0]
        all_union_subtraction_tuples = union_tuples_n_fusion_from_multi_sentence_completion_ind(
                                                                            pred_triplets=[subtraction_tuples], n_fusion=n_fusion)[0]
        if fusion_type == 'delta_operator_fusion':# first add than subtract hence unified add/sub will be ultimately subtracted since sub is the last OP.
            if method == 'precision_support': # add than subtract
                for add_tup in all_union_addition_tuples:
                    reference_tuples_for_operator_fusion.append(add_tup)
                for sub_tup in all_union_subtraction_tuples:
                    if sub_tup in reference_tuples_for_operator_fusion: # Might be that subtraction of non existing tuple
                        reference_tuples_for_operator_fusion.remove(sub_tup)
                    else:
                        print("Fusiod subtraction tuple : {} non existed in reference tuples{}".format(sub_tup, reference_tuples_for_operator_fusion))
            elif method == 'recall_support': # subtract than add
                for sub_tup in all_union_subtraction_tuples:
                    if sub_tup in reference_tuples_for_operator_fusion: # Might be that subtraction of non existing tuple
                        reference_tuples_for_operator_fusion.remove(sub_tup)
                    else:
                        print("Fusiod subtraction tuple : {} non existed in reference tuples{}".format(sub_tup, reference_tuples_for_operator_fusion))
                for add_tup in all_union_addition_tuples:
                    reference_tuples_for_operator_fusion.append(add_tup)
            if isinstance(reference_tuples_for_operator_fusion[0][0], list):
                return reference_tuples_for_operator_fusion #fusion_type == 'delta_operator_fusion'
            else:
                return [reference_tuples_for_operator_fusion] #fusion_type == 'delta_operator_fusion'
            

    return all_reconstructed_tuples #For method of 

# Not a class memebr but rather friend function that assignrd on runtime
def union_tuples_n_fusion_from_multi_sentence_completion(self, pred_triplets, **kwargs): #[list(x) for x in set(tuple(x) for x in pred_triplets[0])]
    n_fusion = kwargs.pop('n_fusion', None)
    if n_fusion == None:
        if self.n_fusion <1:
            raise ValueError("n_fusion was not set")
        n_fusion = self.n_fusion # backward ciompatible

    x, c = np.unique(flatten(pred_triplets), return_counts=True)
    fusion_tuples = list()
    for tup, cnt in zip(x, c):
        if cnt>=self.n_fusion:
            fusion_tuples.append(tup)
    return [fusion_tuples] # back to GPT format 

def union_tuples_n_fusion_from_multi_sentence_completion_ind(pred_triplets, **kwargs): #[list(x) for x in set(tuple(x) for x in pred_triplets[0])]
    n_fusion = kwargs.pop('n_fusion', 1)
    counts_tuple = pd.Series(flatten(pred_triplets)).value_counts()
    fusion_tuples = list()
    for tup, cnt in counts_tuple.items():
        if cnt>=n_fusion:
            fusion_tuples.append(tup)
    return [fusion_tuples] # back to GPT format 
        # x, c = np.unique(flatten(pred_triplets), return_counts=True)
        # fusion_tuples = list()
        # for tup, cnt in zip(x, c):
        #     if cnt>=n_fusion:
        #         fusion_tuples.append(tup)
        # return [fusion_tuples] # back to GPT format 

def gpt_execute(prompt_template, *args, **kwargs):
    verbose = kwargs.pop('verbose', False)
    max_tokens = kwargs.pop('max_tokens', 256)            
    prompt = prompt_template.format(*args)
    try:   # Sometimeds GPT returns HTTP 503 error
        response = openai.Completion.create(prompt=prompt, max_tokens=max_tokens, **kwargs)   
        if verbose:
            print(kwargs)
            print("Top K {}".format([x['index'] for x in response['choices']]))
            # [print(x['logprobs']) for x in response['choices']]
            # print("Top K {}".format([x['logprobs'] for x in response['choices']]))
            print("Top prompt_tokens : {} total_tokens: {}".format(response['usage']['prompt_tokens'] ,response['usage']['total_tokens']))

        # return response
        return [x['text'].strip() for x in response['choices']]
    except Exception as e:
        print(e)
        return []
    
def check_valid_in_context_examples(in_context_examples):
    # print("no op check_valid_in_context_examples")
    pass
# Anderson based made manually 
def _get_few_shot_prompt_paragraph_based_to_tuple_4K(query_paragraph, in_context_examples=None, **kwargs):
    prolog = '''Generate a list of object-relation-attribute tuples based on the paragraph description. Example:'''
    if in_context_examples:
        check_valid_in_context_examples(in_context_examples)
    else:
        in_context_examples = \
        '''
        Paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances.  There is an oven which is placed at a comfortable height for a person standing upright.  Beside that there is a stainless steel refrigerator with double doors.  The freezer compartment is on the bottom of the unit.  Atop the fridge are three potted plants.  They are in white pots and have tiny green leaves.  Also above the cupboards are two identical plants with white pots and green leaves.  There is a microwave on the counter, and next to that a stainless steel sink.  There is a one cup coffee maker to the right of the sink.  There is a center island on which the burners stand.  They are stainless steel, and the counter surrounding them is white.  There are four burners."
        Tuples: [['appliance'],['appliance', 'stainless'], ['appliance', 'steel'], ['bottom'], ['bottom', 'of', 'unit'], ['burner'], ['burner', 'four'], ['burner', 'stand'], ['ceiling'], ['compartment'], ['compartment', 'freezer'], ['compartment', 'on', 'bottom'], ['counter'], ['counter', 'surround', 'steel'], ['counter', 'white'], ['cupboard'], ['door'], ['door', 'double'], ['floor'], ['floor', 'gray'], ['floor', 'slate'], ['fridge'], ['height'], ['height', 'comfortable'], ['height', 'for', 'upright'], ['island'], ['island', 'center'], ['kitchen'], ['kitchen', 'have', 'appliance'], ['kitchen', 'have', 'ceiling'], ['kitchen', 'have', 'counter'], ['kitchen', 'have', 'floor'], ['kitchen', 'have', 'wall'], ['leaf'], ['leaf', 'green'], ['leaf', 'tiny'], ['maker'], ['maker', 'coffee'], ['maker', 'cup'], ['maker', 'to', 'right'], ['microwave'], ['microwave', 'on', 'counter'], ['oven'], ['peanut'], ['peanut', 'in', 'steel'], ['plant'], ['plant', 'above', 'cupboard'], ['plant', 'atop', 'fridge'], ['plant', 'identical'], ['plant', 'potted'], ['plant', 'three'], ['plant', 'two'], ['plant', 'with', 'leaf'], ['plant', 'with', 'pot'], ['pot'], ['pot', 'white'], ['refrigerator'], ['refrigerator', 'stainless'], ['refrigerator', 'steel'], ['refrigerator', 'with', 'door'], ['right'], ['right', 'of', 'sink'], ['sink'], ['sink', 'next to', 'that'], ['sink', 'stainless'], ['sink', 'steel'], ['steel'], ['steel', 'have', 'peanut'], ['steel', 'stainless'], ['that'], ['unit'], ['upright'], ['upright', 'person'], ['upright', 'standing'], ['wall']]
        Paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants. The table is white and has brown and gray chairs sitting around it. There is are white coffee mugs and bottles that are also on the table near the man. A gray door can be seen near a wall with a gray door handle on it."
        Tuples: [['bottle'], ['cake'], ['cake', 'small'], ['chair'], ['chair', 'brown'], ['chair', 'gray'], ['chair', 'sit around', 'table'], ['door'], ['door', 'gray'], ['man'], ['man', 'lean over', 'table'], ['man', 'stand in', 'room'], ['man', 'three'], ['mug'], ['mug', 'coffee'], ['mug', 'white'], ['pants'], ['pants', 'green'], ['room'], ['shirt'], ['shirt', 'short'], ['shirt', 'sleeve'], ['table'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], ['table', 'white'], ['wall'], ['wall', 'with', 'door']]
        Paragraph: "A woman is facing away from the camera, looking out to the ocean. She is standing in knee-deep water and facing foamy waves. The woman is holding a surfboard in her right arm. The surfboard is mostly white, with some blue at the bottom. She has blonde hair pulled back in a ponytail. She is wearing a grey shirt and swim shorts."
        Tuples: [['arm'], ['arm', 'right'], ['blue'], ['blue', 'at', 'bottom'], ['bottom'], ['camera'], ['hair'], ['hair', 'blonde'], ['hair', 'pull back in', 'ponytail'], ['ocean'], ['ponytail'], ['shirt'], ['shirt', 'grey'], ['shorts'], ['surfboard'], ['surfboard', 'in', 'arm'], ['surfboard', 'white'], ['water'], ['water', 'knee-deep'], ['wave'], ['wave', 'foamy'], ['woman']]
        Paragraph: {}
        Tuples:'''
    

    epilog = '''
    Paragraph: {}
    Tuples:'''
    
    prompt = '{} {} {}'.format(prolog, in_context_examples, epilog).strip()
    prompt = prompt.format(query_paragraph)

    return prompt

# Anderson based made manually 
def _get_few_shot_prompt_sentence_based_to_tuple_4K(query_sentence, in_context_examples=None, **kwargs):

    prolog = '''Generate a list of object-relation-attribute tuples based on the sentence description. Example:'''
    if in_context_examples:
        check_valid_in_context_examples(in_context_examples)
    else:
        in_context_examples = \
        '''
        Paragraph: "A silver train with blue writing on it."
        Tuples: [['silver'], ['silver', 'train with', 'writing'],['writing'], ['writing', 'blue'], ['writing', 'on', 'silver'], ['train']]
        Paragraph: "There is a large dark gray door and some windows on the side."
        Tuples: [['door'], ['door', 'dark'], ['door', 'gray'], ['door', 'large'], ['side'], ['windows'], ['window', 'on', 'side']]
        Paragraph: "The wheels are black and the train tracks are brown."
        Tuples: [['track'], ['track', 'brown'], ['track', 'train'], ['wheel'], ['wheel', 'black']]
        Paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances."
        Tuples: [['appliance'],['appliance', 'stainless'], ['appliance', 'steel'], ['kitchen'], ['kitchen', 'have', 'appliance'], ['kitchen', 'have', 'ceiling'], ['kitchen', 'have', 'counter'], ['kitchen', 'have', 'floor'], ['kitchen', 'have', 'wall'], ['counter', 'white'], ['floor', 'slate'], ['steel', 'stainless'], ['counter']]
        Paragraph: "There is an oven which is placed at a comfortable height for a person standing upright."
        Tuples: [['oven'], ['upright'], ['upright', 'person'], ['upright', 'standing']]
        Paragraph: "There is a stainless steel refrigerator with double doors."
        Tuples: [['refrigerator'], ['refrigerator', 'stainless'], ['refrigerator', 'steel'], ['refrigerator', 'with', 'door']]
        Paragraph: "The freezer compartment is on the bottom of the unit."
        Tuples: [['compartment'], ['compartment', 'freezer'], ['compartment', 'on', 'bottom']]
        Paragraph: "Atop the fridge are three potted plants."
        Tuples: [['plant'], ['plant', 'atop', 'fridge'], ['plant', 'identical'], ['plant', 'potted'], ['plant', 'three'], ['plant', 'with', 'pot'], ['pot'], ['pot', 'white'], ['refrigerator']]
        Paragraph: "Above the cupboards are two identical plants with white pots and green leaves."
        Tuples: [['plant', 'above', 'cupboard'], ['plant', 'with', 'leaf'], ['plant', 'two'], ['plant', 'with', 'pot'], ['pot'], ['pot', 'white'], ['leaf'], ['leaf', 'green'], ['leaf', 'tiny']]'''

    epilog = '''
    Paragraph: {}
    Tuples:'''
    
    prompt = '{} {} {}'.format(prolog, in_context_examples, epilog).strip()
    prompt = prompt.format(query_sentence)

    return prompt
    

class PrompEngFewshotTupleCreation():
    def __init__(self):
        self.pred_tuples_sentence_based = None
        self.pred_tuples_paragraph_based = None
        self.n_fusion = -1
        self.all_pred_triplets_temp = list() # temp results for saving and debugging
        pass

    def get_paragraph_to_tuple_prompt_8K(self, query_paragraph):
        prompt = \
        '''Generate a list of object-relation-attribute tuples based on the paragraph description. Example:
        Paragraph: "A silver train with blue writing on it. There is a large dark gray door and some windows on the side."
        Tuples: [['writing'], ['train'], ['blue', 'writing'], ['silver', 'train'], ['writing', 'on', 'train'], ['door'], ['windows'], ['dark', 'door'], ['gray', 'door'], ['large', 'door'], ['windows', 'on', 'side']]
        Paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances."
        Tuples: [['kitchen'], ['floors'], ['counters'], ['wall'], [ceiling], ['appliance'], ['slate', 'floors'], ['white', 'counters'], ['gray slate', 'floors'], ['stainless', 'appliance'], ['steel', 'appliance']]
        Paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants."
        Tuples: [['cake'], ['table'], ['man'], ['pants'], ['room'], ['shirt'], ['standing', 'man'], ['small', 'cake'], ['green', 'pants'], ['man', 'lean over', 'table'], ['man', 'wear', 'shirt'], ['man', 'wear', 'pants'], ['short sleeve', 'shirt'], ['sleeve', 'shirt'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], [ 'white', 'table'], ['wall'], ['wall', 'with', 'door']]
        Paragraph: "A woman is standing in a kitchen in front of an oven. She is wearing a gray shirt with a white towel hanging over a shoulder."
        Tuples: [['shirt'], ['gray', 'shirt'], ['shoulder'], ['towel'], ['towel', 'hang over', 'shoulder'], ['white', 'towel'], ['woman'], ['woman', 'stand in', 'kitchen'], ['woman', 'wearing' 'shirt'], ['towel', 'hanging over', 'shoulder']]
        Paragraph: "Two men are on their phone while sitting next to each other."
        Tuples:  [['phone'], ['man'], ['sitting', 'man'], ['man', 'on', 'phone'], ['man', 'sitting next to', 'man']]
        Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
        Tuples: [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['woman', 'has', 'hair'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['long', 'hair'], ['woman', 'in front', 'door']]
        Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
        Tuples: ['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'], ['glass', 'on', 'table']]
        Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
        Tuples: [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'has', 'ankle']]
        Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
        Tuples: [['water'], ['ducks'], ['geese'], ['enjoying', 'ducks'], ['enjoying', 'geese']]
        Paragraph: "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40. There is graffiti on the sign and debris on the ground. The ground is cement and there are patches of grass growing near the poles holding the sign."
        Tuples: [['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']]
        Paragraph: "A bear with brown fur is looking straight into the camera. The bear's expression is neutral. Its fur appears bushy, and is in different shades of brown.  Its nose appears long.  The background consists of some trees.  It is a sunny day."
        Tuples: [['bear'], ['fur'], ['camera'], ['brown', 'fur'], ['bushy', 'fur'], ['natural', 'expression'], ['shades', 'fur'], ['long', 'nose'], ['bear', 'look into', 'camera'], ['trees'], ['nose']]
        Paragraph: "This is a group of people possibly at a rally. Some of them have video and regular cameras. The man in the front is wearing a brown pin striped suit. Under the jacket he is wearing a white collar shirt with a purple striped tie; the stripes on the tie forms diamond patterns. His skin is brown and he has dark brown hair. He has a shadow of both a mustache and a beard. The man is also holding a water bottle and a small ticket in one of this hands."
        Tuples:[['people'], ['at a rally', 'people'], ['video', 'camera'], ['regular', 'camera'], ['suit'], ['pin', 'striped', 'suit'], ['shirt'], ['white collar', 'shirt'], ['tie'], ['purple', 'striped', 'tie'], ['diamond', 'patterns'], ['skin'], ['brown', 'skin'], ['hair'], ['dark', 'brown', 'hair'], ['mustache'], ['beard'], ['mustache', 'shadow'], ['shadow', 'beard'], ['water', 'bottle'], ['ticket'], ['small', 'ticket'], ['man', 'wearing', 'suit'], ['man', 'holding', 'bottle'], ['man', 'holding', 'ticket'], ['people', 'group'] ,['jacket'], ['man', 'wear', 'tie']]
        Paragraph: "A man is lying on a bed in between two pillows. He is wearing a white shirt. The baby has a pacifier in his mouth. There are brown sheets on the bed. A tall brown headboard is at the front of the bed. There is a white painted wall beside the bed. Part of a small brown dresser can be seen beside the bed."
        Tuples: [['man'], ['bed'], ['pillow'], ['shirt'], ['baby'], ['pacifier'], ['sheet'], ['headboard'], ['wall'], ['dresser'], ['man', 'lying', 'bed'],['man', 'between', 'pillows'], ['man', 'wearing', 'shirt'], ['baby', 'pacifier', 'mouth'], ['brown', 'sheet'], ['tall', 'headboard'], ['brown', 'headboard'], ['white', 'wall'], ['small', 'dresser'], ['dresser', 'beside', 'bed'], ['white', 'painted','wall'], ['wall', 'beside', 'bed'], ['white' 'shirt']] 
        Paragraph: "A woman is facing away from the camera, looking out to the ocean. She is standing in knee-deep water and facing foamy waves. The woman is holding a surfboard in her right arm. The surfboard is mostly white, with some blue at the bottom. She has blonde hair pulled back in a ponytail. She is wearing a grey shirt and swim shorts." 
        Tuples: [['woman'], ['ocean'], ['water'], ['wave'], ['shirt'], ['foamy', 'wave'], ['surfboard'], ['right', 'arm'], ['woman', 'hold', 'surfboard'], ['white', 'surfboard'], ['blue', 'surfboard'], ['blonde', 'hair'], ['grey', 'shirt'], ['swim','shorts'], ['woman', 'face', 'ocean'], ['woman', 'standing in', 'water'], ['blonde hair', 'woman'], ['woman', 'wear', 'shirt'], ['woman', 'wear', 'swim shorts'], ['swim', 'shorts']]
        Paragraph: "Two people are crouched down on skateboards. They are both wearing helmets and uniforms of spandex.  They are racing one another down a track on the concrete road. The skater in the back has a number on the back."
        Tuples: [['skateboard'], ['helmet'], ['road'], ['track'], ['people'], ['concrete', 'road'], ['crouched down', 'people'], ['racing', 'on the' 'road'], ['spandex', 'uniform'], ['people', 'wearing', 'helmet'], ['people', 'wearing', 'spandex'], ['people', 'racing', 'down a track'], ['skater', 'with', 'number'], ['number', 'on', 'back'], ['people', 'crouch down on', 'skateboard'], ['helmet', 'of', 'spandex']]"
        Paragraph: {}
        Tuples:[]'''

        prompt = prompt.format(query_paragraph)
        return prompt

# Made manually by fixing Anderson+GPT : My GT

    def get_paragraph_to_tuple_prompt_4K_dash_sep(self, query_paragraph):
        prompt = \
        '''Generate a list of object-relation-attribute tuples based on the paragraph description. Example:
        Paragraph: "A silver train with blue writing on it. There is a large dark gray door and some windows on the side."
        Tuples: [['writing'], ['train'], ['blue', 'writing'], ['silver', 'train'], ['writing', 'on', 'train'], ['door'], ['windows'], ['dark', 'door'], ['gray', 'door'], ['large', 'door'], ['windows', 'on', 'side']]
        ###
        Paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances."
        Tuples: [['kitchen'], ['floors'], ['counters'], ['wall'], ['ceiling'], ['appliance'], ['slate', 'floors'], ['white', 'counters'], ['gray slate', 'floors'], ['stainless', 'appliance'], ['steel', 'appliance']]
        ###
        Paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants."
        Tuples: [['cake'], ['table'], ['man'], ['pants'], ['room'], ['shirt'], ['standing', 'man'], ['small', 'cake'], ['green', 'pants'], ['man', 'lean over', 'table'], ['man', 'wear', 'shirt'], ['man', 'wear', 'pants'], ['short sleeve', 'shirt'], ['sleeve', 'shirt'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], [ 'white', 'table'], ['wall'], ['wall', 'with', 'door']]
        ###
        Paragraph: "A woman is standing in a kitchen in front of an oven. She is wearing a gray shirt with a white towel hanging over a shoulder."
        Tuples: [['shirt'], ['gray', 'shirt'], ['shoulder'], ['towel'], ['towel', 'hang over', 'shoulder'], ['white', 'towel'], ['woman'], ['woman', 'stand in', 'kitchen'], ['woman', 'wearing' 'shirt'], ['towel', 'hanging over', 'shoulder']]
        ###
        Paragraph: "Two men are on their phone while sitting next to each other."
        Tuples: [['phone'], ['man'], ['sitting', 'man'], ['man', 'on', 'phone'], ['man', 'sitting next to', 'man']]
        ###
        Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
        Tuples: [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['woman', 'has', 'hair'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['long', 'hair'], ['woman', 'in front', 'door']]
        ###
        Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
        Tuples: [['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'], ['glass', 'on', 'table']]
        ###
        Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
        Tuples: [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'has', 'ankle']]
        ###
        Paragraph: {}
        Tuples:'''
        
        prompt = prompt.format(query_paragraph)

        return prompt

    # def get_likely_tuples_from_paragraph(self, paragraph:str, n=1, 
    #                                     fs_gpt_model='text-davinci-003', 
    #                                     opportunities=10, **kwargs):
    #     use_dash_prompt = kwargs.pop('use_dash_prompt', False)

    #     if use_dash_prompt:
    #         prompt = get_paragraph_to_tuple_prompt_4K_dash_sep(paragraph)
    #     else:
    #         prompt = get_paragraph_to_tuple_prompt_4K(paragraph)# Can try the get_paragraph_to_tuple_prompt_8K() for 2nd optinion

    #     while (opportunities):
    #         rc = gpt_execute(prompt, model=fs_gpt_model, n=n, **kwargs)
    #         try:
    #             eval(rc[0]) # if LLM returns non standard/corrupted response
    #             rc = [tup for tup in eval(rc[0]) if len(tup) < 4]
    #             return [rc] # renormalization to GPT output
    #         except:
    #             time.sleep(1)
    #             opportunities -= 1
    #     return []

    def get_likely_tuples_from_paragraph_by_sentence(self, paragraph:str,  
                                        fs_gpt_model='text-davinci-003', **kwargs):
                                            
        few_shot_prompt_func = kwargs.pop('few_shot_prompt_func', _get_few_shot_prompt_sentence_based_to_tuple_4K)
        post_process_sentence_fun = kwargs.pop('post_process_sentence_fun', None)
        reference_tuples = kwargs.pop('reference_tuples', None)
        verbose = kwargs.pop('verbose', False)      
        fusion_type = kwargs.pop('fusion_type', None)
        n_fusion = kwargs.pop('n_fusion', 1)


        if verbose:
            self.all_pred_triplets_temp = list() # clear temp debug aggregation


        all_pred_triplets = list()
        splited_par_to_sent = [[x.strip().replace('"',"") + '.'] for x in paragraph.split(".")[:-1]]
        for ix, sent in enumerate(splited_par_to_sent):
            if reference_tuples:
                reference_tuples_sent = reference_tuples[ix]
                # For Anderson based reference tuples : skip tuple creation In case reference is empty since we are a sentence based, like in  'There are black and grey and even yellow and white.'
                if fusion_type == 'delta_operator_fusion' and reference_tuples_sent == []: # Hence TODO concat that sentence to the previous one
                    continue 
            else:
                reference_tuples_sent = None

            opportunities = 2
            while (opportunities):    
                pred_triplets = self._get_likely_tuples_by_meta_few_shot_playground(paragraph=sent, 
                                                                                few_shot_prompt_func=few_shot_prompt_func, fusion_type=fusion_type, 
                                                                                reference_tuples=reference_tuples_sent, **kwargs) # get_paragraph_to_anderson_tuple_sentence_prompt_4K
                if verbose:
                    self.all_pred_triplets_temp.append(pred_triplets)

                if not (pred_triplets): 
                    print("Retries are exhausted: GPT has not returned response after few opportunities waiting 5 seconds!!", 50*'=')
                    time.sleep(5)
                    opportunities -= 1
                else:
                    break

            if post_process_sentence_fun and pred_triplets:
                if verbose:
                    print("pred_triplets", pred_triplets)
                pred_triplets = self.post_process_sentence_fun(pred_triplets, 
                                                            reference_tuples=reference_tuples_sent, 
                                                            fusion_type=fusion_type,
                                                            n_fusion=n_fusion,
                                                            **kwargs)
                if verbose:
                    print("post_process_sentence_fun", pred_triplets)

            all_pred_triplets.append(pred_triplets[0])
        pred_tuples = union_tuples_n_fusion_from_multi_sentence_completion_ind(all_pred_triplets , n_fusion=1)
        pred_tuples = pred_tuples[0]        
        #pred_tuples = flatten(all_pred_triplets)
        # pred_tuples = np.unique(pred_tuples).tolist()# for cases no post_process_sentence_fun() s.a. n=1 and still repetative tuples should be unified

        if pred_tuples == []:
            print('Hueston!!')
        
        if 1: # TODO for operational remove this option
            self.pred_tuples_sentence_based = pred_tuples 
        else:
            self.pred_tuples_sentence_based = [x for x in np.unique(pred_tuples)] # filter multiple repettive tuples 

        return self.pred_tuples_sentence_based

    def get_likely_tuples_from_paragraph(self, paragraph:str,
                                        fs_gpt_model='text-davinci-003',
                                         **kwargs):
                                            
        few_shot_prompt_func = kwargs.pop('few_shot_prompt_func', _get_few_shot_prompt_sentence_based_to_tuple_4K)
        post_process_sentence_fun = kwargs.pop('post_process_sentence_fun', None)

        self.pred_tuples_paragraph_based = self._get_likely_tuples_by_meta_few_shot_playground(paragraph=paragraph, 
                                                            few_shot_prompt_func=few_shot_prompt_func, **kwargs) # get_paragraph_to_anderson_tuple_sentence_prompt_4K
        if not self.pred_tuples_paragraph_based:
            print('Failed to get GPT response')
        else:
            if post_process_sentence_fun and self.pred_tuples_paragraph_based:
                self.pred_tuples_paragraph_based = self.post_process_sentence_fun(self.pred_tuples_paragraph_based, **kwargs)

            self.pred_tuples_paragraph_based = self.pred_tuples_paragraph_based[0]

        return self.pred_tuples_paragraph_based

    
    def _get_likely_tuples_by_meta_few_shot_playground(self, paragraph:str, few_shot_prompt_func, 
                                        fs_gpt_model='text-davinci-003', 
                                        opportunities=10, **kwargs):
        # use_dash_prompt = kwargs.pop('use_dash_prompt', False)
        
        # if use_dash_prompt:
        #     prompt = get_paragraph_to_tuple_prompt_4K_dash_sep(paragraph)
        # else:
        #     prompt = get_paragraph_to_tuple_prompt_4K(paragraph)# Can try the get_paragraph_to_tuple_prompt_8K() for 2nd optinion
        in_context_examples = kwargs.pop('in_context_examples', None) # need to flush kwargs avoiding GPT getting out of context parameters
        reference_tuples = kwargs.pop('reference_tuples', None)
        fusion_type = kwargs.pop('fusion_type', None)
        max_tokens = kwargs.pop('max_tokens', 256)            

        if fusion_type == 'delta_operator_fusion': # addressing the 't-shirt' , short-sleeved
            paragraph = [x.replace("-"," ") for x in paragraph]

        prompt = few_shot_prompt_func(paragraph, reference_tuples=reference_tuples, in_context_examples=in_context_examples)
        if fs_gpt_model == 'text-davinci-003':
            if (len(prompt) + max_tokens) > 4096:
                print("!!! Prompt + max response is prone to be greater than context window:4096 GPT check actual len(prompt)+len(output_token)!!1",len(prompt), 50* '=')
        while (opportunities):
            # paragraph = paragraph.replace("o'clock", 'of the clock') # Ad-hoc
            rc = gpt_execute(prompt, model=fs_gpt_model, **kwargs)
            if fusion_type == 'delta_operator_fusion': # addressing the 't-shirt'
                rc = [x.replace('t-shirt','t shirt').replace('short-sleeved', 'short sleeved') for x in rc]
            try:
# Special treatment for mingeled operation/arithmetics in response  - check sanity
                if any(['+' in rc_x or '-' in rc_x for rc_x in rc]) and reference_tuples and fusion_type!= None: # Arithmetics only for later fused arithmetics
                    wrong_syntax_prompt = False
                    rc_s = list()
                    for rc_t in rc:
                        normalize_response = [x.replace("+",",").replace("-",",").strip().rstrip(',').lstrip(',') for x in [rc_t]][0]
                        normalize_response = eval(normalize_response) # just check that eval() works
                        rc_s.append(rc_t)
                        delta_tuples = list(eval([x.replace("+",",").replace("-",",").strip().rstrip(',').lstrip(',') for x in [rc_t]][0]))
                        addition_sign = np.where(['+' in x for x in rc_t])[0]
                        sub_sign = np.where(['-' in x for x in rc_t])[0]
                        if len(delta_tuples) != len(addition_sign) + len(sub_sign):
                            print("gpt_execute: amount of + op and - op doesnot equal to correction list len", addition_sign, sub_sign)
                            wrong_syntax_prompt = True                                
                            continue # skip this loop
                    if len(rc) == 1 and wrong_syntax_prompt: # only one respose out of GPT (n=1) retry GPT else just skip that response
                        continue # continue GPT retries
                    return rc_s
                else:                    
                    [eval(re.sub('(?<=[a-z])\'(?=[a-z])', '', rc_x)) for rc_x in rc] # Sanity check validate that LLM returns non standard/corrupted response
                    rc_s = list()
                    for rc_x in rc:
                        rc_s.append([tup for tup in eval(re.sub('(?<=[a-z])\'(?=[a-z])', '', rc_x)) if len(tup) < max_tuple_len and len(tup) > 0])  # remove empty tuples as well as un expected >3
                        # apostrophy_loc = [m.start() for m in re.finditer('(?<=[a-z])\'(?=[a-z])', rc_x)]
                        # if apostrophy_loc:
                        #     for loc in apostrophy_loc:

                    if rc_s == []:
                        time.sleep(1)
                        opportunities -= 1
                        continue
                    return rc_s            
            except:
                time.sleep(1)
                opportunities -= 1
        print("Warning no intact response out of GPT after retries", opportunities)
        return []
# TODO add [expanse]
    def get_prompt_few_shot_filter_abstract_tokens_from_paragraph(self, query_paragraph:str):
        prompt = \
    '''Remove abstract tokens. Examples:
        Paragraph: "The background consists of some trees."
        Cleaned: "some trees."
        Paragraph: "It is a sunny day two bicycles are parked near a fence."
        Cleaned: "two bicycles are parked near a fence."
        Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
        Cleaned: "There are a couple of ducks and geese enjoying."
        Paragraph: "They are sitting on the snow covering a mountain. It's daylight out."
        Cleaned: "They are sitting on the snow covering a mountain."
        Paragraph: "It is a snowy day. A bear with brown fur is looking straight into the camera."
        Cleaned: "A bear with brown fur is looking straight."
        Paragraph: "It is a sunny day."
        Cleaned: ""
        Paragraph: {}
        Cleaned:'''
        
        prompt = prompt.format(query_paragraph)

        return prompt

    def get_prompt_few_shot_filter_abstract_tokens_n_prefix_from_paragraph(self, query_paragraph:str):
        prompt = \
    '''Remove abstract tokens. Examples:
        Paragraph: "The background consists of some trees."
        Cleaned: "some trees."
        Paragraph: "It is a sunny day two bicycles are parked near a fence."
        Cleaned: "two bicycles are parked near a fence."
        Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
        Cleaned: "There are a couple of ducks and geese enjoying."
        Paragraph: "They are sitting on the snow covering a mountain. It's daylight out."
        Cleaned: "They are sitting on the snow covering a mountain."
        Paragraph: "It is a snowy day. A bear with brown fur is looking straight into the camera."
        Cleaned: "A bear with brown fur is looking straight."
        Paragraph: "It is a sunny day."
        Cleaned: ""
        Paragraph: "An image of."
        Cleaned: ""
        Paragraph: "A scene of."
        Cleaned: ""
        Paragraph: "A photo of."
        Cleaned: ""
        Paragraph: {}
        Cleaned:'''
        
        prompt = prompt.format(query_paragraph)

        return prompt



# Trying to predict Anderson then comapre to Anderson as GT 
    # Paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances."
    # Tuples: [['appliance'],['appliance', 'stainless'], ['appliance', 'steel'], ['ceiling'], ['counter'], ['counter', 'surround', 'steel'], ['counter', 'white'], ['floor'], ['floor', 'gray'], ['floor', 'slate'], ['kitchen'], ['kitchen', 'have', 'appliance'], ['kitchen', 'have', 'ceiling'], ['kitchen', 'have', 'counter'], ['kitchen', 'have', 'floor'], ['kitchen', 'have', 'wall'], ['steel', 'stainless'], ['wall']]
    # Paragraph: ""A silver train with blue writing on it. There is a large dark gray door and some windows on the side."
    # Tuples: [['door'], ['door', 'dark'], ['door', 'gray'], ['door', 'large'], ['side'], ['silver'], ['silver', 'train with', 'writing'],  ['window'], ['window', 'on', 'side'], ['writing'], ['writing', 'blue'], ['writing', 'on', 'silver']]
    
    # (-) There are two stainless steel bowls on the counter, and one has some peanuts in it.
    # (-) The front of the island is wood grained.  
        

    # Missing : ['oven', 'placed at', 'height'] ,[comfortable height], ['person'], ['person', 'standing'], for Paragraph: "There is an oven which is placed at a comfortable height for a person standing upright."
    # paragraph =>sentence 

    def get_likely_filtered_abstract_tokens_from_paragraph(self, paragraph:str, n=1, 
                                                            fs_gpt_model='text-davinci-003', 
                                                            **kwargs):
                                                                
        prompt = get_prompt_few_shot_filter_abstract_tokens_from_paragraph(paragraph)
        rc = gpt_execute(prompt, model=fs_gpt_model, n=n, **kwargs)
        return rc


    def get_likely_filtered_abstract_tokens_from_paragraph_sentence_wise(self, paragraph:str, n=1, 
                                                            fs_gpt_model='text-davinci-003', 
                                                            **kwargs):

        debug = kwargs.pop('debug', False)
        sentences = tokenize.sent_tokenize(paragraph)
        gpt_filtered_sent = list()
        for sent in sentences:
            sent_filt = get_likely_filtered_abstract_tokens_from_paragraph(paragraph=sent)
            gpt_filtered_sent.append(sent_filt[0].replace('"',""))
            if debug:
                if sent_filt[0].lower() != sent.lower():
                    print("Sentence level : Noise was added")
                else:
                    print("Sentence level :  Nothings was filtered")
        cleaned_par = ' '.join(gpt_filtered_sent)
        cleaned_par = cleaned_par.strip()

        return cleaned_par

# Made manually by fixing Anderson+GPT normalize API IPC
def _get_my_few_shot_prompt_paragraph_to_tuple_prompt_4K(query_sentence, in_context_examples=None):

    prolog = '''Generate a list of object-relation-attribute tuples based on the paragraph description. Example:'''
    if in_context_examples:
        check_valid_in_context_examples(in_context_examples)  # [0, 0, 1, 2, 2, 2, 3, 3, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7]
    else:
        in_context_examples = \
        '''
        Paragraph: "A silver train with blue writing on it. There is a large dark gray door and some windows on the side."
        Tuples: [['writing'], ['train'], ['blue', 'writing'], ['silver', 'train'], ['writing', 'on', 'train'], ['door'], ['windows'], ['dark', 'door'], ['gray', 'door'], ['large', 'door'], ['windows', 'on', 'side']]
        Paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances."
        Tuples: [['kitchen'], ['floors'], ['counters'], ['wall'], ['ceiling'], ['appliance'], ['slate', 'floors'], ['white', 'counters'], ['gray slate', 'floors'], ['stainless', 'appliance'], ['steel', 'appliance']]
        Paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants."
        Tuples: [['cake'], ['table'], ['man'], ['pants'], ['room'], ['shirt'], ['standing', 'man'], ['small', 'cake'], ['green', 'pants'], ['man', 'lean over', 'table'], ['man', 'wear', 'shirt'], ['man', 'wear', 'pants'], ['short sleeve', 'shirt'], ['sleeve', 'shirt'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], [ 'white', 'table'], ['wall'], ['wall', 'with', 'door'], ['man', 'stand in', 'room']]
        Paragraph: "A woman is standing in a kitchen in front of an oven. She is wearing a gray shirt with a white towel hanging over a shoulder."
        Tuples: [['shirt'], ['gray', 'shirt'], ['shoulder'], ['towel'], ['towel', 'hang over', 'shoulder'], ['white', 'towel'], ['woman'], ['woman', 'stand in', 'kitchen'], ['woman', 'wearing' 'shirt'], ['towel', 'hanging over', 'shoulder']]
        Paragraph: "Two men are on their phone while sitting next to each other."
        Tuples: [['phone'], ['man'], ['sitting', 'man'], ['man', 'on' ,'phone'], ['man', 'sitting next to', 'man']]
        Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
        Tuples: [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['woman', 'has', 'hair'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['long', 'hair'], ['woman', 'in front', 'door']]
        Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
        Tuples: [['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'], ['glass', 'on', 'table']]
        Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
        Tuples: [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'has', 'ankle']]'''

    epilog = '''
    Paragraph: {}
    Tuples:'''
    
    prompt = '{} {} {}'.format(prolog, in_context_examples, epilog).strip()
    prompt = prompt.format(query_sentence)

    return prompt
    # Global 
# added /fixed  :['white', 'wall'], ['white', 'ceiling'] + Captial letter Somone=>someone . TODO : Resolve Anderson (WrodNet) ['it.there'], ['arm.the']
# Since Paragraph is broken into sentence the  ['train', 'door'] is missing from paragraph 'A silver train with blue writing on it. There is a large dark gray door and some windows on the side.' since there is relationship between sentnces which could not inferred 

in_context_examples_my_gt = \
'''
Sentence: "A silver train with blue writing on it."
Tuples: [['writing'], ['train'], ['writing', 'blue'], ['train', 'silver'], ['writing', 'on', 'train']]
Sentence: "There is a large dark gray door and some windows on the side."
Tuples: [['door'], ['window'], ['door', 'dark'], ['door', 'gray'], ['door', 'large'], ['window', 'on', 'side']]
Sentence: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances."
Tuples: [['kitchen'], ['floor'], ['counter'], ['wall'], ['ceiling'], ['appliance'], ['floor', 'slate'], ['floor', 'gray'], ['counter', 'white'], ['appliance', 'steel'], ['wall', 'white'], ['ceiling', 'white'], ['kitchen', 'have', 'ceiling'], ['kitchen', 'have', 'counter'], ['kitchen', 'have', 'floor'], ['kitchen', 'have', 'appliance']]
Sentence: "Three men are standing in a room." 
Tuples: [['man'],  ['man', 'standing'], ['room'], ['man', 'stand in', 'room']]
Sentence: "One man is leaning over a table in front of a small cake."
Tuples: [['man'],['cake'], ['table'], ['cake', 'small'], ['man', 'lean over', 'table'], ['man', 'in front of', 'cake']]
Sentence: "He is wearing a short sleeve shirt and green pants."
Tuples: [['man'], ['pants'], ['shirt'], ['pants', 'green'], ['man', 'wear', 'shirt'], ['man', 'wear', 'pants'], ['shirt', 'short sleeve']]
Sentence: "A woman is standing in a kitchen in front of an oven." 
Tuples: [['woman'], ['woman', 'stand in', 'kitchen'], ['oven'], ['woman' , 'in front of', 'oven']]
Sentence: "She is wearing a gray shirt with a white towel hanging over a shoulder."
Tuples: [['woman'], ['shirt'], ['woman', 'wear' ,'shirt'], ['shirt', 'gray'], ['shoulder'], ['towel'], ['towel', 'hang over', 'shoulder'], ['towel', 'white'], ['woman', 'have', 'shoulder']]
Sentence: "Two men are on their phone while sitting next to each other."
Tuples: [['phone'], ['man'], ['man', 'sitting'], ['man', 'on', 'phone'], ['man', 'sitting next to', 'man']]
Sentence: "A woman wearing a colorful dress is holding a white remote."
Tuples: [['remote'], ['woman'], ['dress'], ['dress', 'colorful'], ['remote', 'white'], ['woman', 'hold', 'remote'], ['woman', 'wear', 'dress']]
Sentence: "She has dark long hair."
Tuples: [['woman'], ['hair'], ['woman', 'have', 'hair'], ['hair', 'dark'], ['hair', 'long']]
Sentence: "She is standing in front of a wooden door."
Tuples: [['woman'], ['door'], ['door', 'wooden'], ['woman', 'standing'], ['woman', 'in front', 'door']]
Sentence: "Someone is holding a knife and a fork in their hands."
Tuples: [['someone'], ['knife'], ['fork'], ['hand'], ['someone', 'have', 'hand'], ['hand', 'hold', 'fork'], ['hand', 'hold', 'knife']]
Sentence: "Someone is sitting at a wooden table getting ready to eat." 
Tuples: [['someone'], ['table'], ['table', 'wooden'], ['someone', 'sit at', 'table'], ['someone' ,'getting ready', 'eat']]
Sentence: "There is a glass to the right of the plate on the table."
Tuples: [['table'], ['plate'], ['glass'], ['glass', 'to the right', 'plate'], ['glass', 'on', 'table'], ['plate', 'on', 'table']]
Sentence: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm."
Tuples: [['surfboard'], ['wetsuit'], ['man'], ['man', 'hold', 'surfboard'], ['man', 'wear', 'wetsuit'], ['wetsuit', 'keep warm', 'man']]
Sentence: "There is a big wave in the distance."
Tuples: [['wave'], ['wave', 'distant'], ['wave', 'big']]
Sentence: "His surfboard has a string attached to it and the other side is attached to the man's ankle."
Tuples: [['man'], ['string'], ['surfboard'], ['ankle'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'have', 'ankle']]'''


in_context_sentence_examples_mapping_to_parapragh_my_gt = [0, 0, 1, 2, 2, 2, 3, 3, 4, 5, 5, 5, 6, 6, 6, 7, 7, 7]

def _get_my_few_shot_prompt_paragraph_to_tuple_sentence_based_prompt_4K(query_paragraph, in_context_examples=None):
    
    prolog = '''Generate a list of object-relation-atribute tuples based on the sentence description. Example:'''
    if in_context_examples:
        check_valid_in_context_examples(in_context_examples)  
    else:
        in_context_examples = in_context_examples_my_gt
    epilog = '''
    Paragraph: {}
    Tuples:'''
    
    prompt = '{} {} {}'.format(prolog, in_context_examples, epilog).strip()
    prompt = prompt.format(query_sentence)

    return prompt

def check_tuples_sanity_in_context_example(in_context_examples_my_gt,
                                            tuple_keyword='Tuples:'):

    
    tuple_keyword_end = ']]'

    sent_start = [m.start() for m in re.finditer(tuple_keyword_end, in_context_examples_my_gt)]
    tuple_start = [m.start() for m in re.finditer(tuple_keyword, in_context_examples_my_gt)]
    assert(len(sent_start) == len(tuple_start))
    for ix, start in enumerate(tuple_start):
        tuple_phrase = in_context_examples_my_gt[start+len(tuple_keyword) + 1 : sent_start[ix] + len(tuple_keyword_end)] # -1 for the \n
        try: 
            eval(tuple_phrase)
            if str(eval(tuple_phrase)).replace(" ", "") != tuple_phrase.replace(" ", ""):
                raise ValueError('not an intact tuple !!!', tuple_phrase)
        except:
            print('not an intact tuple !!!', tuple_phrase)
            
    print('Tuples are intact')


def breakdown_prompt_to_list_examples(in_context_examples_my_gt, 
                                        start_tuple_keyword='Tuples:',
                                        start_keyword = 'Sentence:',
                                        tuple_keyword_end = ']]'):
    
    
    
    # sentence_keyword_end = ".'\n"

    start_tuple_keyword_pointer = [m.start() for m in re.finditer(start_tuple_keyword, in_context_examples_my_gt)]
    start_keyword_pointer = [m.start() for m in re.finditer(start_keyword, in_context_examples_my_gt)]
    tuple_keyword_end_pointer = [m.start() for m in re.finditer(tuple_keyword_end, in_context_examples_my_gt)]
    # sentence_keyword_end_pointer = [m.start() for m in re.finditer(sentence_keyword_end, in_context_examples_my_gt)]

    assert(len(start_tuple_keyword_pointer) == len(start_keyword_pointer))
    assert(len(start_tuple_keyword_pointer) == len(tuple_keyword_end_pointer))

    all_tuples = list()
    all_paragraph = list()
    for ix in range(len(start_keyword_pointer)):
        start = start_tuple_keyword_pointer[ix]
        tuple_phrase = in_context_examples_my_gt[start+len(start_tuple_keyword) + 1 : tuple_keyword_end_pointer[ix] + len(tuple_keyword_end)] 
        try:
            eval(tuple_phrase)   
        except:
            print("Tuple is not intact !!!", tuple_phrase)    

        all_tuples.append(tuple_phrase)
        paragraph_phrase = in_context_examples_my_gt[start_keyword_pointer[ix]+len(start_keyword) + 1 : start_tuple_keyword_pointer[ix] - 1]    
        all_paragraph.append(paragraph_phrase)

    return all_paragraph, all_tuples


def synth_in_context_examples_based(all_paragraphs, all_tuples, senetence_prefix = "Sentence:",
                                    margin_for_prompt_suffix=512, prompt_limit=4096):
    
    in_context_ex_limit = prompt_limit - margin_for_prompt_suffix 

    in_context_ex = list()
    for paragraph, tuples in zip(all_paragraphs, all_tuples):
        in_context_ex.append('\n{} {}'.format(senetence_prefix, paragraph) + '\nTuples: {}'.format(tuples))

    if len(in_context_ex) >in_context_ex_limit:
        print("Warning in context examples length : {} reaches max context window {} while margin_for_prompt_suffix".format(len(in_context_ex), prompt_limit, margin_for_prompt_suffix))
    
    return ''.join(in_context_ex)


# Delta Anderson  : Paragraph:{} Anderson_tuples <> delta_anderson_gt_tuples <>
def synth_in_context_examples_based_predicting_delta_anderson(all_paragraphs, 
                                                                all_proposed_tuples, 
                                                                all_delta_tuples,
                                                                senetence_prefix = "Sentence:",
                                                                margin_for_prompt_suffix=512, prompt_limit=4096,
                                                                delta_prefix=delta_prefix_pattern,
                                                                proposal_prefix = reference_prefix_pattern):
    
    in_context_ex_limit = prompt_limit - margin_for_prompt_suffix 
    
    
    
    
    in_context_ex = list()
    for paragraph, proposed_tuples, delta_tuples in zip(all_paragraphs, all_proposed_tuples, all_delta_tuples):
        in_context_ex.append('{}{}\n{}{}\n{}{}\n'.format(senetence_prefix, ''.join(('"',paragraph,'"')), #paragraph.replace('"',""), 
                            proposal_prefix, proposed_tuples, delta_prefix, delta_tuples))

    if len(in_context_ex) >in_context_ex_limit:
        print("Warning in context examples length : {} reaches max context window {} while margin_for_prompt_suffix".format(len(in_context_ex), prompt_limit, margin_for_prompt_suffix))
    
    return ''.join(in_context_ex)

# proposed_tuples = anderson reference TODO Oremove prolog see if it matters
def _get_few_shot_prompt_sentence_based_to_delta_anderson_tuple_4K(paragraph, in_context_examples=None, **kwargs):
    reference_tuples = kwargs.pop('reference_tuples', None)

    prolog = '''Generate a list of correction of object-relation-attribute tuples out of proposed list based on the sentence description. Example:'''
    if in_context_examples:
        check_valid_in_context_examples(in_context_examples)
    else:
        raise

    epilog = '''
    Paragraph:{}
    {}{}
    {}'''
    
    prompt = '{}{}{}'.format(prolog, in_context_examples, epilog).strip()
    prompt = prompt.format(paragraph, reference_prefix_pattern, reference_tuples, delta_prefix_pattern)

    return prompt
    
def _get_few_shot_prompt_sentence_based_on_amr_tuple_4K(paragraph, in_context_examples=None, **kwargs):
    reference_tuples = kwargs.pop('reference_tuples', None)

    prolog = '''Generate a list of object-relation-attribute tuples out of proposed abstract meaning representation. Example:'''
    if in_context_examples:
        check_valid_in_context_examples(in_context_examples)
    else:
        raise

    epilog = '''Paragraph:{}\n{}{}\n{}'''
    
    prompt = '{}{}{}'.format(prolog, in_context_examples, epilog).strip()
    prompt = prompt.format(paragraph, amr_reference_prefix_pattern, reference_tuples, amr_delta_prefix_pattern)

    return prompt
    
def calc_delta_tuples_arithmetics(all_proposed_tuples, all_gt_tuples):
    delta_tuples = list()
    for prop_tuples, gt_tuples in zip(all_proposed_tuples, all_gt_tuples): # add replace('"',"")
        if isinstance(gt_tuples, str):
            gt_tuples = ast.literal_eval(gt_tuples)  # eval(gt_tuples)
        if 0: # a + b 
            addition_tuples_prompt = ''.join([str(x) + ' + ' for i, x in enumerate(gt_tuples) if x not in prop_tuples])[:-3]
        else: # +a + b
            addition_tuples_prompt = ''.join(['+' + str(x) for i, x in enumerate(gt_tuples) if x not in prop_tuples])
        subtract_tuples_prompt = ''.join(['-' + str(x) for i, x in enumerate(prop_tuples) if x not in gt_tuples])
        delta_tuples.append(addition_tuples_prompt + subtract_tuples_prompt)
# Sanity check
        comb_delta_tuples = delta_tuples[-1] # take the current value which is the last from appended list
        delta_tuples_norm = list(eval([x.replace("+",",").replace("-",",").strip().rstrip(',').lstrip(',') for x in [comb_delta_tuples]][0]))
        # Single tuple loose its double brackets [[]]
        if not isinstance(delta_tuples_norm[0], list):
            delta_tuples_norm = [delta_tuples_norm]

        addition_sign = np.where(['+' in x for x in comb_delta_tuples])[0]
        sub_sign = np.where(['-' in x for x in comb_delta_tuples])[0]
        if len(delta_tuples_norm) != len(addition_sign) + len(sub_sign):
            print("hueston: amount of + op and - op doesnot equal to correction list len", addition_sign, sub_sign, comb_delta_tuples)
            raise

    return delta_tuples

def limit_paragrapgs_by_prompt_size_pred_delta_amr(paragraphs, prompt_limit=4096, max_query=50): #max_query in characters
    
    in_context_ex_limit = prompt_limit - margin_for_prompt_suffix-max_query*2 # margin_for_prompt_suffix=512  max_query*2 for query and AMR reference
    in_context_ex = list()
    # in_context_ex_paragraph = list()
    overhead_to_sent = 0
    len_of_paragraph = len('paragraph') + 1 # +1 for the \n
    len_of_tuples = len('Corrected tuples:') + 1 + len(amr_reference_prefix_pattern) + 1 
    

    for ix, paragraph in enumerate(paragraphs):
        overhead_to_sent += 2*(len(paragraph.split('.')) -1) * (len_of_paragraph + len_of_tuples)
        if 0:
            triplets = spice_get_triplets(paragraph)
        else: # dummy triplet
            triplets = paragraph[:int(2.54*len(paragraph))]

        dummy_triplets = triplets
        in_context_ex.append('\nParagraph: {}'.format(paragraph) + '\n{}'.format(amr_reference_prefix_pattern) + '{}'.format(triplets) + '\nCorrected tuples:{}'.format(dummy_triplets)) #    Paragraph: {}     Reference tuples: {}     Corrected tuples:''' 
        # in_context_ex_paragraph.append(paragraph)
        temp_prompt = ''.join(in_context_ex)
        if len(temp_prompt) + overhead_to_sent>in_context_ex_limit:
            return ix + 1 # no of paragraph sentetnces

def lematize_verb_tup_3(pred_triplets_n, nlp_model=spacy.load('en_core_web_lg'), verbose=False):
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
        if verbose:
            res, c = np.unique([re_all_tup_lst, pred_triplets_n], return_counts=True)
            for ix, cnt in enumerate(c):
                if cnt == 1 and verbose:
                    print('lematization processed the following', res[ix])
    else:
        re_all_tup_lst = pred_triplets_n

    return re_all_tup_lst

def limit_paragrapgs_by_prompt_size_pred_delta_anderson(paragraphs, prompt_limit=4096, max_query=50):
    
    in_context_ex_limit = prompt_limit - margin_for_prompt_suffix - max_query*2 # margin_for_prompt_suffix=512  max_query*2 : for prompt and anderson reference
    in_context_ex = list()
    # in_context_ex_paragraph = list()
    overhead_to_sent = 0
    len_of_paragraph = len('paragraph') + 1 # +1 for the \n
    len_of_tuples = len('Corrected tuples:') + 1 + len('Reference tuples:') + 1 
    

    for ix, paragraph in enumerate(paragraphs):
        overhead_to_sent += 2*(len(paragraph.split('.')) -1) * (len_of_paragraph + len_of_tuples)
        if 0:
            triplets = spice_get_triplets(paragraph)
        else: # dummy triplet
            triplets = paragraph

        dummy_triplets = triplets
        in_context_ex.append('\nParagraph: {}'.format(paragraph) + '\nReference tuples: {}'.format(triplets) + '\nCorrected tuples:{}'.format(dummy_triplets)) #    Paragraph: {}     Reference tuples: {}     Corrected tuples:''' 
        # in_context_ex_paragraph.append(paragraph)
        temp_prompt = ''.join(in_context_ex)
        if len(temp_prompt) + overhead_to_sent>in_context_ex_limit:
            return ix + 1 # no of paragraph sentetnces

"""
Try 
Given the current state of a graph and a prompt, extrapolate as many relationships as possible from the prompt and update the state. Every node has an id, label, and color (in hex). Every edge has a to and from with node ids, and a label. Edges are directed, so the order of the from and to is important.
From Graph GPT : https://github.com/varunshenoy/GraphGPT/blob/main/public/prompts/main.prompt
"""