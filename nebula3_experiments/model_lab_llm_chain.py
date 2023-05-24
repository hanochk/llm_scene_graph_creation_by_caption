from langchain import LLMChain, OpenAI, Cohere, HuggingFaceHub, PromptTemplate
from langchain.model_laboratory import ModelLaboratory

from langchain.prompts import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate


import openai
try:
    with open('/storage/keys/openai.key','r') as f:
        OPENAI_API_KEY = f.readline().strip()
    openai.api_key = OPENAI_API_KEY
except:
    nebula_db = NEBULA_DB()
    openai.api_key = nebula_db.get_llm_key()

HUGGINGFACEHUB_API_TOKEN = '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'
llms = [
    # OpenAI(max_tokens=256, openai_api_key=OPENAI_API_KEY),
    # Cohere(model="command-xlarge-20221108", max_tokens=256),
    HuggingFaceHub(repo_id="google/flan-t5-xxl",huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN) # there is a larger 
]


examples = [  # HK@@TODO replace prompt in context examples with the fixed ones from get_paragraph_to_tuple_prompt_4K()
    {"paragraph": "A silver train with blue writing on it. There is a large dark gray door and some windows on the side.", 
    "tuples": "[['writing'], ['train'], ['blue', 'writing'], ['silver', 'train'], ['writing', 'on', 'train'], ['door'], ['windows'], ['dark', 'door'], ['gray', 'door'], ['large', 'door'], ['windows', 'on', 'side']] "},
    {"paragraph": "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances.", 
    "tuples": "[['kitchen'], ['floors'], ['counters'], ['wall'], ['ceiling'], ['appliance'], ['slate', 'floors'], ['white', 'counters'], ['gray slate', 'floors'], ['stainless', 'appliance'], ['steel', 'appliance']] "},
    {"paragraph": "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants.", 
    "tuples": "[['cake'], ['table'], ['man'], ['pants'], ['room'], ['shirt'], ['standing', 'man'], ['small', 'cake'], ['green', 'pants'], ['man', 'lean over', 'table'], ['man', 'wear', 'shirt'], ['man', 'wear', 'pants'], ['short sleeve', 'shirt'], ['sleeve', 'shirt'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], ['table', 'white'], ['wall'], ['wall', 'with', 'door']]"},
    {"paragraph": "A woman is standing in a kitchen in front of an oven. She is wearing a gray shirt with a white towel hanging over a shoulder.", 
    "tuples": "[['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['hair', 'on top of', 'woman'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['woman', 'in front', 'door']]"},
    {"paragraph": "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table.", 
    "tuples": "['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'] ['glass', 'on', 'table']]"},
    {"paragraph": "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle.", 
    "tuples": "[['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['ankle', 'attached', 'man']]"},
    {"paragraph": "Nature and water. There are a couple of ducks and geese enjoying.", 
    "tuples": "[['nature'], ['water'], ['ducks'], ['geese'], ['enjoying', 'ducks'], ['enjoying', 'geese']"},
    {"paragraph": "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign.", 
    "tuples": "[['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']]"},
    {"paragraph": "", 
    "tuples": ""},
]
"""
Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
Tuples: [['nature'], ['water'], ['ducks'], ['geese'], ['enjoying', 'ducks'], ['enjoying', 'geese']
paragraph: "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
Triplet: [['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']

"""
# This how we specify how the example should be formatted.
example_prompt = PromptTemplate(
    input_variables=["paragraph","tuples"],
    # template="paragraph: {paragraph}\n tuples: {tuples}",
    # input_variables=["input"],
    # template="paragraph: {paragraph}\n tuples: {tuples}",
    template= "{paragraph} : {tuples}",
)

input_to_llm = "Two women are on their phone while sitting next to each other. The women are sitting on a black leather couch."
prefix_to_prompt = "Generate a list of object-relation-attribute tuples based on the paragraph description. Example:"

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=prefix_to_prompt,
    # suffix="paragraph: {input}\n tuples:",
    suffix="paragraph: {input}\n",
    input_variables=["input"],
    example_separator="\n"
)

prompt.format(input=input_to_llm)
# model_lab = ModelLaboratory.from_llms(llms)
model_lab_with_prompt = ModelLaboratory.from_llms(llms, prompt=prompt)
res = model_lab_with_prompt.compare("tuples:")
if 0:
    model_lab = ModelLaboratory.from_llms(llms)
    model_lab.compare("What color is a flamingo?")    
print("ka")

# model_lab.compare("What color is a flamingo?")
