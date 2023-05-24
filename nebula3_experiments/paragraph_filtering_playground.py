from prompts_utils import PrompEngFewshotTupleCreation, _get_my_few_shot_prompt_paragraph_to_tuple_prompt_4K, \
                            union_tuples_n_fusion_from_multi_sentence_completion

import nltk
nltk.download('punkt')
from nltk import tokenize
import numpy as np

# export PYTHONPATH=/notebooks/pip_install/
"""
An image of
A scene of 
A photo of
Camera 

Remove abstract:
Sunny day 
Background
Nature 
Mood 
Rainy day 
Snowy day 
Day 
Night 

"""
abstract_filtering_playground = False
FS_GPT_MODEL = 'text-davinci-003'
n_completions_to_generate_for_each_prompt = 1
anderson_prediction = False
prompt_util = PrompEngFewshotTupleCreation()

# candidate from Movies/-5147321700349177328 ipc_200
# senter = self.nlp.get_pipe("senter")
# sentences = [str(x) for x in senter(self.nlp(paragraph)).sents]
all_paragraph = list()
all_paragraph.append("A red fire truck is stopped on the side of a street at night. The truck is facing left. There is a firefighter standing on the street with a bright yellow helmet and riding a bright yellow bicycle. Off to the left is another fire truck parked on the street.")
all_paragraph.append("Three giraffes are standing in the middle of a field, with a cloudy sky in the background. There is a vast expanse of grassland and shrubbery all around them. The tallest giraffe is in the center, looking towards the camera, and the two smaller ones are flanking it to either side. The animals are surrounded by yellow and green grasses, low shrubs and tall trees.")
all_paragraph.append("The plate of food on the table is full of aromatic vegetables and herbs. There is a plate filled with slices of pita bread and flatbread. The plate has pesto and diced tomatoes. There are fresh herbs such as parsley and basil garnishing the plate. The plate of food has a rustic appeal, with some of the vegetables charred and smoky.")
all_paragraph.append("In the image is a man on a skateboard in a skate park. The ground is concrete and the surfaces around it are smooth. The man is wearing a blue and white striped shirt and blue jeans. He is stretching his arm out and holding onto the the ledge of the skate park while pushing off with his feet. You can see several other people in the background looking on.")
# CoRef
all_paragraph.append("A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door. There is a picture hanging on the wall.")

# paragraph = "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door. There is a picture hanging on the wall."
n_fusion = 1

if not anderson_prediction:
    top_p = 0.1
    if top_p != 1:
        prompt_util.n_fusion = -1
        post_process_sentence_fun = None
    else:
        prompt_util.n_fusion = n_fusion
        post_process_sentence_fun = union_tuples_n_fusion_from_multi_sentence_completion
        from functools import partial
        prompt_util.post_process_sentence_fun = partial(post_process_sentence_fun, prompt_util)

    all_pred_triplets = list()
    all_tup_len_freq = list()
    for paragraph in all_paragraph:
        pred_triplets = prompt_util.get_likely_tuples_from_paragraph(paragraph=paragraph, 
                                                    n=n_completions_to_generate_for_each_prompt,
                                                    _procesposts_sentence_fun=post_process_sentence_fun,
                                                    few_shot_prompt_func=_get_my_few_shot_prompt_paragraph_to_tuple_prompt_4K,
                                                    top_p=top_p, 
                                                    verbose=True) # get_paragraph_to_anderson_tuple_sentence_prompt_4K
        all_pred_triplets.append(prompt_util.pred_tuples_paragraph_based)
# Tuple statistics 
        len_tups = [len(tup) for tup in pred_triplets]
        len_tup_uniq, c = np.unique(len_tups, return_counts=True)
        tup_len_freq = c/len(pred_triplets)
        tup_len_freq = np.array([a.__format__('.3f') for a in tup_len_freq])
        all_tup_len_freq.append(tup_len_freq)

else:
    if 0:
        pred_triplets = prompt_util.get_likely_tuples_from_paragraph(paragraph=paragraph, 
                                                    few_shot_prompt_func=get_paragraph_to_anderson_tuple_prompt_4K, 
                                                        verbose=True) # get_paragraph_to_anderson_tuple_sentence_prompt_4K
    else:
        pred_triplets = prompt_util.get_likely_tuples_from_paragraph_anderson_by_sentence(paragraph=paragraph)


if 0:
    paragraph = "Two young children have skis on their feet, and ski poles, but they are both sitting on the snow covering a mountain. It's daylight out, but there's a large shady area that the children are also in. The child to the left looks like a boy, and he's smiling. He's also wearing all black clothing, and a white helmet with red goggles resting on the helmet. The child to the right looks like a girl, and she is wearing pink snow pants, pink and white snow jacket and black sunglasses. She looks like she has brown hair and doesn't appear to be wearing a helmet. Far from them and way to the back of the image, there are green trees that are scattered along the mountain."
    paragraph = "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
    rc = get_likely_tuples_from_paragraph(paragraph=paragraph, n=n_completions_to_generate_for_each_prompt)


if abstract_filtering_playground:
    paragraph1 = "This is a group of people possibly at a rally. Some of them have video and regular cameras. The man in the front is wearing a brown pin striped suit. Under the jacket he is wearing a white collar shirt with a purple striped tie; the stripes on the tie forms diamond patterns. His skin is brown and he has dark brown hair. He has a shadow of both a mustache and a beard. The man is also holding a water bottle and a small ticket in one of this hands."  
    paragraph2 = "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
    paragraph3 = "A bear with brown fur is looking straight into the camera. The bear's expression is neutral. Its fur appears bushy, and is in different shades of brown. Its nose appears long. The background consists of some trees. It is a sunny day."
    paragraph4 = "It is a rainy day. Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The background consists of some trees."

    paragraph_list = list()
    paragraph_list = [paragraph4, paragraph3, paragraph1, paragraph2]
    for par in paragraph_list:
        clean = get_likely_filtered_abstract_tokens_from_paragraph_sentence_wise(par)
        # sentences = tokenize.sent_tokenize(par)
        # gpt_filtered_sent = list()
        # for sent in sentences:
        #     sent_filt = get_likely_filtered_abstract_tokens_from_paragraph(paragraph=sent)
        #     gpt_filtered_sent.append(sent_filt[0])
        #     if sent_filt[0].lower() != sent.lower():
        #         print("Sentence level : Noise was added")
        #     else:
        #         print("Sentence level :  Nothings was filtered")
        # cleaned_par = ' '.join(gpt_filtered_sent)

        if 0:
            rc_abs_filter = get_likely_filtered_abstract_tokens_from_paragraph(paragraph=par)
            cleaned_par = rc_abs_filter[0]
        if cleaned_par.lower() != par.lower():
            print("Noise was added")
        else:
            print("Nothings was filtered")





"""
paragraph3 = "A bear with brown fur is looking straight into the camera. The bear's expression is neutral. Its fur appears bushy, and is in different shades of brown. Its nose appears long. The background consists of some trees. It is a sunny day."

"The bear's expression is neutral. Its fur appears bushy, and is in different shades of brown. Its nose appears long.  It is a sunny day."


'"The bear\'s expression is neutral. Its fur appears bushy, and is in different shades of brown. Its nose appears long. some trees"'
"""