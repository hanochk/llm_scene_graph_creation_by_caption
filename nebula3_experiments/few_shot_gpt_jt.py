from transformers import pipeline
from prompts_utils import get_paragraph_to_tuple_prompt_4K
from transformers import AutoTokenizer  #https://huggingface.co/docs/transformers/v4.25.1/en/model_doc/auto#transformers.AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")  # TODO find the approproate Tokenizer : huggingfaces tokenizer auto

gpt_j = pipeline(model='togethercomputer/GPT-JT-6B-v1')
resp = gpt_j('''"I love this!" Is it positive? A:''')
print(resp[0]['generated_text'].strip())
paragraph = "Two young children have skis on their feet, and ski poles, but they are both sitting on the snow covering a mountain. It's daylight out, but there's a large shady area that the children are also in. The child to the left looks like a boy, and he's smiling. He's also wearing all black clothing, and a white helmet with red goggles resting on the helmet. The child to the right looks like a girl, and she is wearing pink snow pants, pink and white snow jacket and black sunglasses. She looks like she has brown hair and doesn't appear to be wearing a helmet. Far from them and way to the back of the image, there are green trees that are scattered along the mountain."
prompt = get_paragraph_to_tuple_prompt_4K(paragraph)
few_shot_resp = gpt_j(prompt)
few_shot_resp[0]['generated_text']
# llm_task = LlmTaskInternal()



events_and_intents = []
for event_ in gr:
    #for sentence in event_.split("."):

    event = event_['candidate']
    prompt = '''The task is to make conclusion about a given event in the input.

Input: A person standing in a dark room with a window open. The person is wearing a dark cloak or bathrobe that covers their entire body and their face cannot be seen. The window is open and the light is streaming in. There is a door in the back of the room with light peeking out from the cracks of the door. The room is mostly in shadows and the only light coming in is from the window. The floor is a dark stone and the walls look to be made of brick.
Output: A man is going to warn someone by yelling out the window.

Input: There are three people sitting at a rectangular wooden table. In front of each person is a plate of food. Two of the people are men and one is a woman. All three look to be enjoying their meal.
Output: Family is going to have dinner in a cozy apartment.

Input: This image is of a person sitting alone on a bench in a park. Behind the person is a bridge that is arched and lined with red ribbon on both sides. The lake below the bridge is surrounded by trees as far as the eye can see.
Output: Man is waiting for somebody.

{}
Output:'''.format(event)
    set_seed(128)
    #print("EVENT: ",event)

    #print(prompt)
    print("tokenizer=======================================================")
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.cuda()
    intents = []
    #for i in range(10):
    print("generate========================================================")
    generated_ids = model.generate(input_ids, max_new_tokens=15, temperature=1.0, top_k=10,  do_sample=True)
    print("decode==========================================================")
    intent = tokenizer.batch_decode(generated_ids, skip_special_tokens=False, padding=True, pad_token_id=50256, max_length=260)
    #print("1    --->",intent)
    intent = intent[0].split(event)[1].split(".")
    sum_intent = intent[0].replace('\n', "").split(":")[1]
    #events_and_intents.append({"db_id":event_[3],"movie":event_[2], "caption":event, "intention":intents})
    event_['conclusion'] = sum_intent
    events_and_intents.append(event_)
