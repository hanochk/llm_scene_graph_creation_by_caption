#  IPC:7092 ,   IPC:3696, IPC:18127
# ['silver', 'train with', 'writing'] ? the order of [window on a side]?
# '''Find the most likely triplet from a paragraph:    

eval("[['silver'], ['silver', 'train with', 'writing'],['writing'], ['writing', 'blue'], ['writing', 'on', 'silver'], ['train']]")
[['silver'], ['silver', 'train with', 'writing'], ['writing'], ['writing', 'blue'], ['writing', 'on', 'silver'], ['train']]")

Anderson: 
'''Generate a list of object-relation-attribute tuples based on the paragraph description. Example:
Paragraph: "A silver train with blue writing on it. There is a large dark gray door and some windows on the side. The wheels are black and the train tracks are brown. It is night time and the sky is dark."
Tuples: [['door'], ['door', 'dark'], ['door', 'gray'], ['door', 'large'], ['side'], ['silver'], ['silver', 'train with', 'writing'], ['sky'], ['sky', 'dark'], ['time'], ['time', 'night'], ['track'], ['track', 'brown'], ['track', 'train'], ['wheel'], ['wheel', 'black'], ['window'], ['window', 'on', 'side'], ['writing'], ['writing', 'blue'], ['writing', 'on', 'silver']]
Paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances.  There is an oven which is placed at a comfortable height for a person standing upright.  Beside that there is a stainless steel refrigerator with double doors.  The freezer compartment is on the bottom of the unit.  Atop the fridge are three potted plants.  They are in white pots and have tiny green leaves.  Also above the cupboards are two identical plants with white pots and green leaves.  There is a microwave on the counter, and next to that a stainless steel sink.  There is a one cup coffee maker to the right of the sink.  There is a center island on which the burners stand.  They are stainless steel, and the counter surrounding them is white.  There are four burners.  The front of the island is wood grained.  There are two stainless steel bowls on the counter, and one has some peanuts in it."
Tuples: [['appliance'],['appliance', 'stainless'], ['appliance', 'steel'], ['bottom'], ['bottom', 'of', 'unit'], ['bowl'], ['bowl', 'on', 'counter'], ['bowl', 'stainless'], ['bowl', 'steel'], ['bowl', 'two'], ['burner'], ['burner', 'four'], ['burner', 'stand'], ['ceiling'], ['compartment'], ['compartment', 'freezer'], ['compartment', 'on', 'bottom'], ['counter'], ['counter', 'surround', 'steel'], ['counter', 'white'], ['cupboard'], ['door'], ['door', 'double'], ['floor'], ['floor', 'gray'], ['floor', 'slate'], ['fridge'], ['front'], ['front', 'of', 'island'], ['front', 'wood'], ['height'], ['height', 'comfortable'], ['height', 'for', 'upright'], ['island'], ['island', 'center'], ['kitchen'], ['kitchen', 'have', 'appliance'], ['kitchen', 'have', 'ceiling'], ['kitchen', 'have', 'counter'], ['kitchen', 'have', 'floor'], ['kitchen', 'have', 'wall'], ['leaf'], ['leaf', 'green'], ['leaf', 'tiny'], ['maker'], ['maker', 'coffee'], ['maker', 'cup'], ['maker', 'to', 'right'], ['microwave'], ['microwave', 'on', 'counter'], ['oven'], ['peanut'], ['peanut', 'in', 'steel'], ['plant'], ['plant', 'above', 'cupboard'], ['plant', 'atop', 'fridge'], ['plant', 'identical'], ['plant', 'potted'], ['plant', 'three'], ['plant', 'two'], ['plant', 'with', 'leaf'], ['plant', 'with', 'pot'], ['pot'], ['pot', 'white'], ['refrigerator'], ['refrigerator', 'stainless'], ['refrigerator', 'steel'], ['refrigerator', 'with', 'door'], ['right'], ['right', 'of', 'sink'], ['sink'], ['sink', 'next to', 'that'], ['sink', 'stainless'], ['sink', 'steel'], ['steel'], ['steel', 'have', 'peanut'], ['steel', 'stainless'], ['that'], ['unit'], ['upright'], ['upright', 'person'], ['upright', 'standing'], ['wall'], ['wood']]
Paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants. The table is white and has brown and gray chairs sitting around it. There is are white coffee mugs and bottles that are also on the table near the man. A gray door can be seen near a wall with a gray door handle on it."
Tuples: [['bottle'], ['cake'], ['cake', 'small'], ['chair'], ['chair', 'brown'], ['chair', 'gray'], ['chair', 'sit around', 'table'], ['door'], ['door', 'gray'], ['front'], ['man'], ['man', 'lean over', 'table'], ['man', 'stand in', 'room'], ['man', 'three'], ['mug'], ['mug', 'coffee'], ['mug', 'white'], ['pants'], ['pants', 'green'], ['room'], ['shirt'], ['shirt', 'short'], ['shirt', 'sleeve'], ['table'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], ['table', 'white'], ['wall'], ['wall', 'with', 'door']]
Paragraph: "A woman is facing away from the camera, looking out to the ocean. She is standing in knee-deep water and facing foamy waves. The woman is holding a surfboard in her right arm. The surfboard is mostly white, with some blue at the bottom. She has blonde hair pulled back in a ponytail. She is wearing a grey shirt and swim shorts."
Tuples: [['arm'], ['arm', 'right'], ['blue'], ['blue', 'at', 'bottom'], ['bottom'], ['camera'], ['hair'], ['hair', 'blonde'], ['hair', 'pull back in', 'ponytail'], ['ocean'], ['ponytail'], ['shirt'], ['shirt', 'grey'], ['shorts'], ['surfboard'], ['surfboard', 'in', 'arm'], ['surfboard', 'white'], ['water'], ['water', 'knee-deep'], ['wave'], ['wave', 'foamy'], ['woman']]


'''Generate a list of object-relation-triplet based on the paragraph description. Example:
paragraph: "A silver train with blue writing on it. There is a large dark gray door and some windows on the side. The wheels are black and the train tracks are brown. It is night time and the sky is dark."
Triplet: [['door'], ['windows'], ['door', 'dark'], ['door', 'gray'], ['door', 'large'], ['windows', 'on', 'side'],  ['writing'], ['train'] , ['blue', 'writing'], ['silver', 'train'], ['writing', 'on', 'train'], ['sky'], ['sky', 'dark'], ['time'], ['time', 'night'], ['track'], ['track', 'brown'], ['track', 'train'], ['wheel'], ['wheel', 'black'], ['window'], ['window', 'on', 'side'], ['writing'], ['writing', 'blue'], ['writing', 'on', 'silver']] 
paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances.  There is an oven which is placed at a comfortable height for a person standing upright.  Beside that there is a stainless steel refrigerator with double doors.  The freezer compartment is on the bottom of the unit.  Atop the fridge are three potted plants.  They are in white pots and have tiny green leaves.  Also above the cupboards are two identical plants with white pots and green leaves.  There is a microwave on the counter, and next to that a stainless steel sink.  There is a one cup coffee maker to the right of the sink.  There is a center island on which the burners stand.  They are stainless steel, and the counter surrounding them is white.  There are four burners.  The front of the island is wood grained.  There are two stainless steel bowls on the counter, and one has some peanuts in it."
triplet: [['kitchen'], ['floors'], ['counters'], ['wall'], [ceiling], ['appliance'], ['slate', 'floors'], ['white' 'counters'], ['appliance', 'stainless'], ['appliance', 'steel'], ['bottom'], ['bottom', 'of', 'unit'], ['bowl'], ['bowl', 'on', 'counter'], ['bowl', 'stainless'], ['bowl', 'steel'], ['bowl', 'two'], ['burner'], ['burner', 'four'], ['burner', 'stand'], ['ceiling'], ['compartment'], ['compartment', 'freezer'], ['compartment', 'on', 'bottom'], ['counter'], ['counter', 'surround', 'steel'], ['counter', 'white'], ['cupboard'], ['door'], ['door', 'double'], ['floor'], ['floor', 'gray'], ['floor', 'slate'], ['fridge'], ['front'], ['front', 'of', 'island'], ['front', 'wood'], ['height'], ['height', 'comfortable'], ['height', 'for', 'upright'], ['island'], ['island', 'center'], ['kitchen'], ['kitchen', 'have', 'appliance'], ['kitchen', 'have', 'ceiling'], ['kitchen', 'have', 'counter'], ['kitchen', 'have', 'floor'], ['kitchen', 'have', 'wall'], ['leaf'], ['leaf', 'green'], ['leaf', 'tiny'], ['maker'], ['maker', 'coffee'], ['maker', 'cup'], ['maker', 'to', 'right'], ['microwave'], ['microwave', 'on', 'counter'], ['oven'], ['peanut'], ['peanut', 'in', 'steel'], ['plant'], ['plant', 'above', 'cupboard'], ['plant', 'atop', 'fridge'], ['plant', 'identical'], ['plant', 'potted'], ['plant', 'three'], ['plant', 'two'], ['plant', 'with', 'leaf'], ['plant', 'with', 'pot'], ['pot'], ['pot', 'white'], ['refrigerator'], ['refrigerator', 'stainless'], ['refrigerator', 'steel'], ['refrigerator', 'with', 'door'], ['right'], ['right', 'of', 'sink'], ['sink'], ['sink', 'next to', 'that'], ['sink', 'stainless'], ['sink', 'steel'], ['steel'], ['steel', 'have', 'peanut'], ['steel', 'stainless'], ['that'], ['unit'], ['upright'], ['upright', 'person'], ['upright', 'standing'], ['wall'], ['wood']] 
paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants. The table is white and has brown and gray chairs sitting around it. There is are white coffee mugs and bottles that are also on the table near the man. A gray door can be seen near a wall with a gray door handle on it."
triplet: [['bottle'], ['cake'], ['cake', 'small'], ['chair'], ['chair', 'brown'], ['chair', 'gray'], ['chair', 'sit around', 'table'], ['door'], ['door', 'gray'], ['front'], ['man'], ['man', 'lean over', 'table'], ['standing', 'man'], ['man', 'wear', 'shirt'], ['man', 'wear', 'pants'], ['man'], ['mug'], ['mug', 'coffee'], ['mug', 'white'], ['pants'], ['pants', 'green'], ['room'], ['shirt'], ['shirt', 'short'], ['shirt', 'sleeve'], ['table'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], ['table', 'white'], ['wall'], ['wall', 'with', 'door']]

paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants. The table is white and has brown and gray chairs sitting around it. There is are white coffee mugs and bottles that are also on the table near the man. A gray door can be seen near a wall with a gray door handle on it."
triplet:[]'''




'''Generate a list of object-relation-triplet based on the paragraph description. Example:
    paragraph: "A silver train with blue writing on it. There is a large dark gray door and some windows on the side. The wheels are black and the train tracks are brown. It is night time and the sky is dark."
Triplet: [['door'], ['windows'], ['door', 'dark'], ['door', 'gray'], ['door', 'large'], ['windows', 'on', 'side'],  ['writing'], ['train'] , ['blue', 'writing'], ['silver', 'train'], ['writing', 'on', 'train'], ['sky'], ['sky', 'dark'], ['time'], ['time', 'night'], ['track'], ['track', 'brown'], ['track', 'train'], ['wheel'], ['wheel', 'black'], ['window'], ['window', 'on', 'side'], ['writing'], ['writing', 'blue'], ['writing', 'on', 'silver']] 
paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances.  There is an oven which is placed at a comfortable height for a person standing upright.  Beside that there is a stainless steel refrigerator with double doors.  The freezer compartment is on the bottom of the unit.  Atop the fridge are three potted plants.  They are in white pots and have tiny green leaves.  Also above the cupboards are two identical plants with white pots and green leaves.  There is a microwave on the counter, and next to that a stainless steel sink.  There is a one cup coffee maker to the right of the sink.  There is a center island on which the burners stand.  They are stainless steel, and the counter surrounding them is white.  There are four burners.  The front of the island is wood grained.  There are two stainless steel bowls on the counter, and one has some peanuts in it."
triplet: [['kitchen'], ['floors'], ['counters'], ['wall'], [ceiling], ['appliance'], ['slate', 'floors'], ['white' 'counters'], ['appliance', 'stainless'], ['appliance', 'steel'], ['bottom'], ['bottom', 'of', 'unit'], ['bowl'], ['bowl', 'on', 'counter'], ['bowl', 'stainless'], ['bowl', 'steel'], ['bowl', 'two'], ['burner'], ['burner', 'four'], ['burner', 'stand'], ['ceiling'], ['compartment'], ['compartment', 'freezer'], ['compartment', 'on', 'bottom'], ['counter'], ['counter', 'surround', 'steel'], ['counter', 'white'], ['cupboard'], ['door'], ['door', 'double'], ['floor'], ['floor', 'gray'], ['floor', 'slate'], ['fridge'], ['front'], ['front', 'of', 'island'], ['front', 'wood'], ['height'], ['height', 'comfortable'], ['height', 'for', 'upright'], ['island'], ['island', 'center'], ['kitchen'], ['kitchen', 'have', 'appliance'], ['kitchen', 'have', 'ceiling'], ['kitchen', 'have', 'counter'], ['kitchen', 'have', 'floor'], ['kitchen', 'have', 'wall'], ['leaf'], ['leaf', 'green'], ['leaf', 'tiny'], ['maker'], ['maker', 'coffee'], ['maker', 'cup'], ['maker', 'to', 'right'], ['microwave'], ['microwave', 'on', 'counter'], ['oven'], ['peanut'], ['peanut', 'in', 'steel'], ['plant'], ['plant', 'above', 'cupboard'], ['plant', 'atop', 'fridge'], ['plant', 'identical'], ['plant', 'potted'], ['plant', 'three'], ['plant', 'two'], ['plant', 'with', 'leaf'], ['plant', 'with', 'pot'], ['pot'], ['pot', 'white'], ['refrigerator'], ['refrigerator', 'stainless'], ['refrigerator', 'steel'], ['refrigerator', 'with', 'door'], ['right'], ['right', 'of', 'sink'], ['sink'], ['sink', 'next to', 'that'], ['sink', 'stainless'], ['sink', 'steel'], ['steel'], ['steel', 'have', 'peanut'], ['steel', 'stainless'], ['that'], ['unit'], ['upright'], ['upright', 'person'], ['upright', 'standing'], ['wall'], ['wood']] 
paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants. The table is white and has brown and gray chairs sitting around it. There is are white coffee mugs and bottles that are also on the table near the man. A gray door can be seen near a wall with a gray door handle on it."
triplet: [['bottle'], ['cake'], ['cake', 'small'], ['chair'], ['chair', 'brown'], ['chair', 'gray'], ['chair', 'sit around', 'table'], ['door'], ['door', 'gray'], ['front'], ['man'], ['man', 'lean over', 'table'], ['man', 'stand in', 'room'], ['man', 'three'], ['mug'], ['mug', 'coffee'], ['mug', 'white'], ['pants'], ['pants', 'green'], ['room'], ['shirt'], ['shirt', 'short'], ['shirt', 'sleeve'], ['table'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], ['table', 'white'], ['wall'], ['wall', 'with', 'door']]

paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants. The table is white and has brown and gray chairs sitting around it. There is are white coffee mugs and bottles that are also on the table near the man. A gray door can be seen near a wall with a gray door handle on it."
triplet:'''

# =>Overfitting example : 
rc[0]
"[['bottle'], ['cake'], ['cake', 'small'], ['chair'], ['chair', 'brown'], ['chair', 'gray'], ['chair', 'sit around', 'table'], ['door'], ['door', 'gray'], ['front'], ['man'], ['man', 'lean over', 'table'], ['man', 'stand in', 'room'], ['man', 'three'], ['mug'], ['mug', 'coffee'], ['mug', 'white'], ['pants'], ['pants', 'green'], ['room'], ['shirt'], ['shirt', 'short'], ['shirt', 'sleeve'], ['table'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], ['table', 'white'], ['wall'], ['wall', 'with', 'door']]"


# man is leaning over a table in front of a small cake : should implies : ['table', 'in front of', 'cake'] + ['man', 'in front of', 'cake']
# Paragraph: "A woman is standing in a kitchen in front of an oven. She is wearing a gray shirt with a white towel hanging over a shoulder. A tray of food is sitting on a rack in the oven. The oven is black in color. The kitchen has brown cabinets in it. Part of a sink can be seen sitting below a window in the kitchen."
# Tuples: [['cabinet'], ['cabinet', 'brown'], ['cabinet', 'in', 'kitchen'], ['color'], ['food'], ['front'], ['kitchen'], ['kitchen', 'have', 'cabinet'], ['kitchen', 'in front of', 'oven'], ['oven'], ['oven', 'black'], ['part'], ['part', 'of', 'sink'], ['rack'], ['rack', 'in', 'oven'], ['shirt'], ['gray', 'shirt'], ['shoulder'], ['sink'], ['towel'], ['towel', 'hang over', 'shoulder'], ['white', 'towel'], ['tray'], ['tray', 'of', 'food'], ['tray', 'sit on', 'rack'], ['window'], ['window', 'in', 'kitchen'], ['woman'], ['woman', 'stand in', 'kitchen'], ['woman', 'wearing' 'shirt']]

'''Generate a list of object-relation-attribute tuples based on the paragraph description. Example:
Paragraph: "A silver train with blue writing on it. There is a large dark gray door and some windows on the side."
Tuples: [['writing'], ['train'], ['blue', 'writing'], ['silver', 'train'], ['writing', 'on', 'train'], ['door'], ['windows'], ['dark', 'door'], ['gray', 'door'], ['large', 'door'], ['windows', 'on', 'side']] 
Paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances." 
Tuples: [['kitchen'], ['floors'], ['counters'], ['wall'], [ceiling], ['appliance'], ['slate', 'floors'], ['white', 'counters'], ['gray slate', 'floors'], ['stainless', 'appliance'], ['steel', 'appliance']] 
Paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants."
Tuples: [['cake'], ['table'], ['man'], ['pants'], ['room'], ['shirt'], ['standing', 'man'], ['small', 'cake'], ['green', 'pants'], ['man', 'lean over', 'table'], ['man', 'wear', 'shirt'], ['man', 'wear', 'pants'], ['short sleeve', 'shirt'], ['sleeve', 'shirt'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], ['table', 'white'], ['wall'], ['wall', 'with', 'door']]
Paragraph: "A woman is standing in a kitchen in front of an oven. She is wearing a gray shirt with a white towel hanging over a shoulder."
Tuples: [['shirt'], ['gray', 'shirt'], ['shoulder'], ['towel'], ['towel', 'hang over', 'shoulder'], ['white', 'towel'], ['woman'], ['woman', 'stand in', 'kitchen'], ['woman', 'wearing' 'shirt'], ['towel', 'hanging over', 'shoulder']]
Paragraph: "Two women are on their phone while sitting next to each other. The women are sitting on a black leather couch."
Tuples:[]'''

rc[0]

"[['phone'], ['women'], ['sitting'], ['couch'], ['black', 'couch'], ['leather', 'couch'], ['next', 'to'], ['woman', 'sitting', 'on', 'phone'], ['woman', 'sitting', 'next', 'to', 'phone'], ['woman', 'sitting', 'next', 'to', 'another', 'woman'], ['woman', 'sitting', 'on', 'couch']]"



'''Generate a list of object-relation-attribute tuples based on the paragraph description. Example:
    Paragraph: "A silver train with blue writing on it. There is a large dark gray door and some windows on the side."
Tuples: [['writing'], ['train'], ['blue', 'writing'], ['silver', 'train'], ['writing', 'on', 'train'], ['door'], ['windows'], ['dark', 'door'], ['gray', 'door'], ['large', 'door'], ['windows', 'on', 'side']] 
Paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances." 
Tuples: [['kitchen'], ['floors'], ['counters'], ['wall'], [ceiling], ['appliance'], ['slate', 'floors'], ['white', 'counters'], ['gray slate', 'floors'], ['stainless', 'appliance'], ['steel', 'appliance']] 
Paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants."
Tuples: [['cake'], ['table'], ['man'], ['pants'], ['room'], ['shirt'], ['standing', 'man'], ['small', 'cake'], ['green', 'pants'], ['man', 'lean over', 'table'], ['man', 'wear', 'shirt'], ['man', 'wear', 'pants'], ['short sleeve', 'shirt'], ['sleeve', 'shirt'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], ['table', 'white'], ['wall'], ['wall', 'with', 'door']]
Paragraph: "A woman is standing in a kitchen in front of an oven. She is wearing a gray shirt with a white towel hanging over a shoulder."
Tuples: [['shirt'], ['gray', 'shirt'], ['shoulder'], ['towel'], ['towel', 'hang over', 'shoulder'], ['white', 'towel'], ['woman'], ['woman', 'stand in', 'kitchen'], ['woman', 'wearing' 'shirt'], ['towel', 'hanging over', 'shoulder']]
Paragraph: "Two men are on their phone while sitting next to each other."
Tuples:  [['phone'], ['man'], ['sitting'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]"

Paragraph: "Two women are on their phone while sitting next to each other. The women are sitting on a black leather couch."
Tuples:[]'''

rc[0]
"[['phone'], ['women'], ['sitting'], ['sitting', 'women'], ['women', 'on', 'phone'], ['women', 'sitting next to', 'women'], ['black leather couch'], ['sitting on', 'couch']]"
 




'''Generate a list of object-relation-attribute tuples based on the paragraph description. Example:
Paragraph: "A silver train with blue writing on it. There is a large dark gray door and some windows on the side."
Tuples: [['writing'], ['train'], ['blue', 'writing'], ['silver', 'train'], ['writing', 'on', 'train'], ['door'], ['windows'], ['dark', 'door'], ['gray', 'door'], ['large', 'door'], ['windows', 'on', 'side']] 
Paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances." 
Tuples: [['kitchen'], ['floors'], ['counters'], ['wall'], [ceiling], ['appliance'], ['slate', 'floors'], ['white', 'counters'], ['gray slate', 'floors'], ['stainless', 'appliance'], ['steel', 'appliance']] 
Paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants."
Tuples: [['cake'], ['table'], ['man'], ['pants'], ['room'], ['shirt'], ['standing', 'man'], ['small', 'cake'], ['green', 'pants'], ['man', 'lean over', 'table'], ['man', 'wear', 'shirt'], ['man', 'wear', 'pants'], ['short sleeve', 'shirt'], ['sleeve', 'shirt'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], ['table', 'white'], ['wall'], ['wall', 'with', 'door']]
Paragraph: "A woman is standing in a kitchen in front of an oven. She is wearing a gray shirt with a white towel hanging over a shoulder."
Tuples: [['shirt'], ['gray', 'shirt'], ['shoulder'], ['towel'], ['towel', 'hang over', 'shoulder'], ['white', 'towel'], ['woman'], ['woman', 'stand in', 'kitchen'], ['woman', 'wearing' 'shirt'], ['towel', 'hanging over', 'shoulder']]
Paragraph: "Two men are on their phone while sitting next to each other."
Tuples:  [['phone'], ['man'], ['sitting'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]"
Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Tuples:[]'''

rc[0]
"[['TV'], ['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden door'], ['standing', 'woman'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['woman', 'standing', 'in front of', 'door']]"



'''Generate a list of object-relation-attribute tuples based on the paragraph description. Example:
Paragraph: "A silver train with blue writing on it. There is a large dark gray door and some windows on the side."
Tuples: [['writing'], ['train'], ['blue', 'writing'], ['silver', 'train'], ['writing', 'on', 'train'], ['door'], ['windows'], ['dark', 'door'], ['gray', 'door'], ['large', 'door'], ['windows', 'on', 'side']] 
Paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances." 
Tuples: [['kitchen'], ['floors'], ['counters'], ['wall'], [ceiling], ['appliance'], ['slate', 'floors'], ['white', 'counters'], ['gray slate', 'floors'], ['stainless', 'appliance'], ['steel', 'appliance']] 
Paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants."
Tuples: [['cake'], ['table'], ['man'], ['pants'], ['room'], ['shirt'], ['standing', 'man'], ['small', 'cake'], ['green', 'pants'], ['man', 'lean over', 'table'], ['man', 'wear', 'shirt'], ['man', 'wear', 'pants'], ['short sleeve', 'shirt'], ['sleeve', 'shirt'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], ['table', 'white'], ['wall'], ['wall', 'with', 'door']]
Paragraph: "A woman is standing in a kitchen in front of an oven. She is wearing a gray shirt with a white towel hanging over a shoulder."
Tuples: [['shirt'], ['gray', 'shirt'], ['shoulder'], ['towel'], ['towel', 'hang over', 'shoulder'], ['white', 'towel'], ['woman'], ['woman', 'stand in', 'kitchen'], ['woman', 'wearing' 'shirt'], ['towel', 'hanging over', 'shoulder']]
Paragraph: "Two men are on their phone while sitting next to each other."
Tuples:  [['phone'], ['man'], ['sitting'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]"
Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Tuples: "[['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['hair', 'on top of', 'woman'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['woman', 'in front', 'door']]"
Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
Tuples:[]'''

rc[0]


"['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['sitting', 'at', 'table'], ['right', 'of', 'plate', 'on', 'table'], ['to', 'the', 'right', 'of', 'the', 'plate', 'on', 'the', 'table']]"



'''Generate a list of object-relation-attribute tuples based on the paragraph description. Example:
Paragraph: "A silver train with blue writing on it. There is a large dark gray door and some windows on the side."
Tuples: [['writing'], ['train'], ['blue', 'writing'], ['silver', 'train'], ['writing', 'on', 'train'], ['door'], ['windows'], ['dark', 'door'], ['gray', 'door'], ['large', 'door'], ['windows', 'on', 'side']] 
Paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances." 
Tuples: [['kitchen'], ['floors'], ['counters'], ['wall'], [ceiling], ['appliance'], ['slate', 'floors'], ['white', 'counters'], ['gray slate', 'floors'], ['stainless', 'appliance'], ['steel', 'appliance']] 
Paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants."
Tuples: [['cake'], ['table'], ['man'], ['pants'], ['room'], ['shirt'], ['standing', 'man'], ['small', 'cake'], ['green', 'pants'], ['man', 'lean over', 'table'], ['man', 'wear', 'shirt'], ['man', 'wear', 'pants'], ['short sleeve', 'shirt'], ['sleeve', 'shirt'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], ['table', 'white'], ['wall'], ['wall', 'with', 'door']]
Paragraph: "A woman is standing in a kitchen in front of an oven. She is wearing a gray shirt with a white towel hanging over a shoulder."
Tuples: [['shirt'], ['gray', 'shirt'], ['shoulder'], ['towel'], ['towel', 'hang over', 'shoulder'], ['white', 'towel'], ['woman'], ['woman', 'stand in', 'kitchen'], ['woman', 'wearing' 'shirt'], ['towel', 'hanging over', 'shoulder']]
Paragraph: "Two men are on their phone while sitting next to each other."
Tuples:  [['phone'], ['man'], ['sitting'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]"
Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Tuples: "[['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['hair', 'on top of', 'woman'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['woman', 'in front', 'door']]"
Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
Tuples: "['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'] ['glass', 'on', 'table']]"
Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
Tuples:[]'''

rc[0] : 
"[['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['ankle', 'attached', 'man']]"

w/o prompt
"[['surfboard'],['wetsuit'], ['wave'], ['string'], ['man'], ['ankle'], ['guy', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['surfboard', 'have', 'string'], ['string', 'attached to', 'surfboard'], ['other', 'side', 'attached to', 'man'], ['man', 'ankle']]"



'''Generate a list of object-relation-attribute tuples based on the paragraph description. Example:
Paragraph: "A silver train with blue writing on it. There is a large dark gray door and some windows on the side."
Tuples: [['writing'], ['train'], ['blue', 'writing'], ['silver', 'train'], ['writing', 'on', 'train'], ['door'], ['windows'], ['dark', 'door'], ['gray', 'door'], ['large', 'door'], ['windows', 'on', 'side']] 
Paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances." 
Tuples: [['kitchen'], ['floors'], ['counters'], ['wall'], [ceiling], ['appliance'], ['slate', 'floors'], ['white', 'counters'], ['gray slate', 'floors'], ['stainless', 'appliance'], ['steel', 'appliance']] 
Paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants."
Tuples: [['cake'], ['table'], ['man'], ['pants'], ['room'], ['shirt'], ['standing', 'man'], ['small', 'cake'], ['green', 'pants'], ['man', 'lean over', 'table'], ['man', 'wear', 'shirt'], ['man', 'wear', 'pants'], ['short sleeve', 'shirt'], ['sleeve', 'shirt'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], ['table', 'white'], ['wall'], ['wall', 'with', 'door']]
Paragraph: "A woman is standing in a kitchen in front of an oven. She is wearing a gray shirt with a white towel hanging over a shoulder."
Tuples: [['shirt'], ['gray', 'shirt'], ['shoulder'], ['towel'], ['towel', 'hang over', 'shoulder'], ['white', 'towel'], ['woman'], ['woman', 'stand in', 'kitchen'], ['woman', 'wearing' 'shirt'], ['towel', 'hanging over', 'shoulder']]
Paragraph: "Two men are on their phone while sitting next to each other."
Tuples:  [['phone'], ['man'], ['sitting', 'men'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]
Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Tuples: [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['hair', 'on top of', 'woman'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['woman', 'in front', 'door']]
Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
Tuples: ['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'] ['glass', 'on', 'table']]
Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
Tuples: [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['ankle', 'attached', 'man']]
Paragraph: "A beautiful scene of nature and some water. There are a couple of ducks and geese enjoying."
Tuples:[]'''

rc[0] = 
0:"[['nature'], ['water'], ['ducks'], ['geese'], ['beautiful', 'scene'], ['scene', 'with', 'nature'], ['scene', 'with', 'water'], ['ducks', 'enjoying'], ['geese', 'enjoying']"



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
Tuples:  [['phone'], ['man'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]
Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Tuples: [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['woman', 'has', 'hair'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['long', 'hair'], ['woman', 'in front', 'door']]
Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
Tuples: ['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'] ['glass', 'on', 'table']]
Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
Tuples: [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'has', 'ankle']]
Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
Tuples: [['nature'], ['water'], ['ducks'], ['geese'], ['enjoying', 'ducks'], ['enjoying', 'geese']
paragraph: "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
Triplet: [['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']]
Paragraph: "Two women are on their phone while sitting next to each other. The women are sitting on a black leather couch."
Tuples:[]'''

rc[0] 
"[['phone'], ['woman'], ['sitting', 'woman'], ['woman', 'on', 'phone'], ['woman', 'sitting next to', 'woman'], ['couch'], ['leather', 'couch'], ['black', 'couch']]"

# Robustnes of the same prompt

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
Tuples:  [['phone'], ['man'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]
Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Tuples: [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['woman', 'has', 'hair'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['long', 'hair'], ['woman', 'in front', 'door']]
Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
Tuples: ['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'] ['glass', 'on', 'table']]
Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
Tuples: [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'has', 'ankle']]
Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
Tuples: [['water'], ['ducks'], ['geese'], ['enjoying', 'ducks'], ['enjoying', 'geese']
paragraph: "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
Tuples: [['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']]
Paragraph: "A bear with brown fur is looking straight into the camera.  The bear's expression is neutral.  Its fur appears bushy, and is in different shades of brown.  Its nose appears long.  The background consists of some trees.  It is a sunny day."
Tuples: [['bear'], ['fur'], ['camera'], ['brown', 'fur'], ['bushy', 'fur'], ['natural', 'expression'], ['shades', 'fur'], ['long', 'nose'], ['bear', 'look into', 'camera'], ['trees'], ['nose']]]
Paragraph: ""
Tuples:[]'''

# Ive fixed the prompt afterwards so rc[0] no longer sustains
rc[0] = 
0:"[['bear'], ['fur'], ['camera'], ['expression'], ['brown', 'fur'], ['bushy', 'fur'], ['shades', 'fur'], ['long', 'nose'], ['look', 'into', 'camera'], ['trees'], ['background'], ['background', 'with', 'trees'], ['sunny', 'day']]"

Robustness :
    
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
Tuples:  [['phone'], ['man'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]
Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Tuples: [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['woman', 'has', 'hair'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['long', 'hair'], ['woman', 'in front', 'door']]
Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
Tuples: ['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'] ['glass', 'on', 'table']]
Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
Tuples: [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'has', 'ankle']]
Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
Tuples: [['water'], ['ducks'], ['geese'], ['enjoying', 'ducks'], ['enjoying', 'geese']
Paragraph: "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
Tuples: [['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']]
Paragraph: "A bear with brown fur is looking straight into the camera.  The bear's expression is neutral.  Its fur appears bushy, and is in different shades of brown.  Its nose appears long.  The background consists of some trees.  It is a sunny day."
Tuples: [['bear'], ['fur'], ['camera'], ['brown', 'fur'], ['bushy', 'fur'], ['natural', 'expression'], ['shades', 'fur'], ['long', 'nose'], ['bear', 'look into', 'camera'], ['trees'], ['nose']]]
Paragraph: "This is a group of people possibly at a rally. Some of them have video and regular cameras. The man in the front is wearing a brown pin striped suit. Under the jacket he is wearing a white collar shirt with a purple striped tie; the stripes on the tie forms diamond patterns. His skin is brown and he has dark brown hair. He has a shadow of both a mustache and a beard. The man is also holding a water bottle and a small ticket in one of this hands."
Tuples:[['people'], ['at a rally', 'people'], ['video', 'camera'], ['regular', 'camera'], ['suit'], ['pin', 'striped', 'suit'], ['shirt'], ['white collar', 'shirt'], ['tie'],
 ['purple', 'striped', 'tie'], ['diamond', 'patterns'], ['skin'], ['brown', 'skin'], ['hair'], ['dark', 'brown', 'hair'], ['mustache'], ['beard'],
  ['mustache', 'shadow'], ['shadow', 'beard'], ['water', 'bottle'], ['ticket'], ['small', 'ticket'], ['man', 'wearing', 'suit'], ['man', 'holding', 'bottle'], 
  ['man', 'holding', 'ticket'], ['people', 'group'] ,['jacket'], ['man', 'wear', 'tie']]
  
  '''

rc[0];
0:"[['people'], ['at a rally', 'people'], ['video', 'camera'], ['regular', 'camera'], ['suit'], ['pin', 'striped', 'suit'], ['shirt'], ['white', 'collar', 'shirt'], ['tie'],
 ['purple', 'striped', 'tie'], ['diamond', 'patterns'], ['skin'], ['brown', 'skin'], ['hair'], ['dark', 'brown', 'hair'], ['mustache'], ['beard'],
  ['shadow', 'mustache'], ['shadow', 'beard'], ['water', 'bottle'], ['ticket'], ['small', 'ticket'], ['man', 'wearing', 'suit'], ['man', 'holding', 'bottle'], 
  ['man', 'holding', 'ticket']]"


Paragraph: "This is a group of people possibly at a rally. Some of them have video and regular cameras. The man in the front is wearing a brown pin striped suit. 
Under the jacket he is wearing a white collar shirt with a purple striped tie; the stripes on the tie forms diamond patterns. 
His skin is brown and he has dark brown hair. He has a shadow of both a mustache and a beard. The man is also holding a water bottle and a small ticket in one of this hands."

missing : ['people', 'group'] ,['jacket'], ['man', 'WEAR', 'tie']
['white', 'collar', 'shirt'] => ['white collar', 'shirt']
['shadow', 'mustache'] => ['mustache', 'shadow']

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
Tuples:  [['phone'], ['man'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]
Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Tuples: [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['woman', 'has', 'hair'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['long', 'hair'], ['woman', 'in front', 'door']]
Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
Tuples: ['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'] ['glass', 'on', 'table']]
Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
Tuples: [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'has', 'ankle']]
Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
Tuples: [['water'], ['ducks'], ['geese'], ['enjoying', 'ducks'], ['enjoying', 'geese']]
Paragraph: "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
Tuples: [['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']]
Paragraph: "A bear with brown fur is looking straight into the camera.  The bear's expression is neutral.  Its fur appears bushy, and is in different shades of brown.  Its nose appears long.  The background consists of some trees.  It is a sunny day."
Tuples: [['bear'], ['fur'], ['camera'], ['brown', 'fur'], ['bushy', 'fur'], ['natural', 'expression'], ['shades', 'fur'], ['long', 'nose'], ['bear', 'look into', 'camera'], ['trees'], ['nose']]]
Paragraph: "A man is lying on a bed in between two pillows. He is wearing a white shirt. The baby has a pacifier in his mouth. There are brown sheets on the bed. A tall brown headboard is at the front of the bed. There is a white painted wall beside the bed. Part of a small brown dresser can be seen beside the bed."
Tuples:[]'''


rc[0]:"[['man'], ['bed'], ['pillow'], ['shirt'], ['baby'], ['pacifier'], ['sheet'], ['headboard'], ['wall'], ['dresser'], ['man', 'lying', 'bed'], ['man', 'between', 'pillows'], ['man', 'wearing', 'shirt'], ['baby', 'pacifier', 'mouth'], ['brown', 'sheet'], ['tall', 'headboard'], ['brown', 'headboard'], ['white', 'wall'], ['small', 'dresser'], ['dresser', 'beside', 'bed'], ['white', 'painted','wall']]"

Paragraph: "A man is lying on a bed in between two pillows. He is wearing a white shirt. The baby has a pacifier in his mouth. 
There are brown sheets on the bed. A tall brown headboard is at the front of the bed. 
There is a white painted wall beside the bed. Part of a small brown dresser can be seen beside the bed."

rc[0]:""

missing : ['wall', 'beside', 'bed'], ['white' 'shirt']


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
Tuples:  [['phone'], ['man'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]
Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Tuples: [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['woman', 'has', 'hair'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['long', 'hair'], ['woman', 'in front', 'door']]
Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
Tuples: ['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'] ['glass', 'on', 'table']]
Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
Tuples: [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'has', 'ankle']]
Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
Tuples: [['water'], ['ducks'], ['geese'], ['enjoying', 'ducks'], ['enjoying', 'geese']
Paragraph: "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
Tuples: [['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']]
Paragraph: "A bear with brown fur is looking straight into the camera.  The bear's expression is neutral.  Its fur appears bushy, and is in different shades of brown.  Its nose appears long.  The background consists of some trees.  It is a sunny day."
Tuples: [['bear'], ['fur'], ['camera'], ['brown', 'fur'], ['bushy', 'fur'], ['natural', 'expression'], ['shades', 'fur'], ['long', 'nose'], ['bear', 'look into', 'camera'], ['trees'], ['nose']]]
Paragraph: "A woman is facing away from the camera, looking out to the ocean. She is standing in knee-deep water and facing foamy waves. The woman is holding a surfboard in her right arm. The surfboard is mostly white, with some blue at the bottom. She has blonde hair pulled back in a ponytail. She is wearing a grey shirt and swim shorts." 
Tuples:[]'''

rc[0]:"[['woman'], ['ocean'], ['water'], ['wave'], ['foamy', 'wave'], ['surfboard'], ['right', 'arm'], ['woman', 'hold', 'surfboard'], ['white', 'surfboard'], ['blue', 'surfboard'], ['blonde', 'hair'], ['ponytail'], ['grey', 'shirt'], ['swim','shorts'], ['woman', 'face', 'ocean'], ['woman', 'knee-deep', 'water'], ['woman', 'have', 'blonde', 'hair'], ['woman', 'wear', 'shirt'], ['woman', 'wearing', 'swim shorts']]"

FN : ['swim shorts'], ['shirt']
FP : ['ponytail'], ['woman', 'have', 'blonde', 'hair']=>['blonde hair', 'woman'] , ['woman' 'has' 'blonde hair'] ['ponytail', 'woman'] and "have" is wrong grammer  
['woman', 'wearing', 'swim shorts'] = >['woman', 'wear', 'swim shorts']
['woman', 'knee-deep', 'water'] =>['woman', 'standing in', 'water'] ,['knee-deep', 'water']
pros: the "camera" is only perspective not a real camera
    
Paragraph: "A woman is facing away from the camera, looking out to the ocean. She is standing in knee-deep water and facing foamy waves. 
The woman is holding a surfboard in her right arm. The surfboard is mostly white, with some blue at the bottom. She has blonde hair pulled back in a ponytail. 
She is wearing a grey shirt and swim shorts." 

rc[0]:"[['woman'], ['ocean'], ['water'], ['wave'], ['foamy', 'wave'], ['surfboard'], ['right', 'arm'], ['woman', 'hold', 'surfboard'], ['white', 'surfboard'],
 ['blue', 'surfboard'], ['blonde', 'hair'], ['ponytail'], ['grey', 'shirt'], ['swim','shorts'], ['woman', 'face', 'ocean'], ['woman', 'knee-deep', 'water'], 
 ['woman', 'have', 'blonde', 'hair'], ['woman', 'wear', 'shirt'], ['woman', 'wearing', 'swim shorts']]"


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
Tuples:  [['phone'], ['man'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]
Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Tuples: [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['woman', 'has', 'hair'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['long', 'hair'], ['woman', 'in front', 'door']]
Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
Tuples: ['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'] ['glass', 'on', 'table']]
Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
Tuples: [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'has', 'ankle']]
Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
Tuples: [['water'], ['ducks'], ['geese'], ['enjoying', 'ducks'], ['enjoying', 'geese']
Paragraph: "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
Tuples: [['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']]
Paragraph: "A bear with brown fur is looking straight into the camera.  The bear's expression is neutral.  Its fur appears bushy, and is in different shades of brown.  Its nose appears long.  The background consists of some trees.  It is a sunny day."
Tuples: [['bear'], ['fur'], ['camera'], ['brown', 'fur'], ['bushy', 'fur'], ['natural', 'expression'], ['shades', 'fur'], ['long', 'nose'], ['bear', 'look into', 'camera'], ['trees'], ['nose']]]
Paragraph: "Two people are crouched down on skateboards. They are both wearing helmets and uniforms of spandex.  They are racing one another down a track on the concrete road. The skater in the back has a number on the back."
Tuples:[]'''

rc[0]:"[['skateboard'], ['helmet'], ['spandex'], ['track'], ['concrete', 'road'], ['people', 'crouched down'], ['people', 'wearing', 'helmet'], ['people', 'wearing', 'spandex'], ['people', 'racing', 'down', 'track'], ['skater', 'with', 'number'], ['back', 'with', 'number'], ['number', 'on', 'back']]"


Paragraph: "Two people are crouched down on skateboards. They are both wearing helmets and uniforms of spandex.  
They are racing one another down a track on the concrete road. The skater in the back has a number on the back."
rc[0]:"[['skateboard'], ['helmet'], ['road'], ['track'], ['concrete', 'road'], ['people', 'crouched down'], ['racing', 'on the' 'road'], ['spandex', 'uniform'], 
['people', 'wearing', 'helmet'], 
['people', 'wearing', 'spandex'], ['people', 'racing', 'down a track'], ['skater', 'with', 'number'], ['back', 'with', 'number'], ['number', 'on', 'back']]"

FP: ['spandex']
FN: ['spandex', 'uniform'], ['road']
['people', 'racing', 'down', 'track'] => ['people', 'racing', 'down a track'] ,['racing', 'on the' 'road']


===========================================================================================================
Build new prompt


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
Tuples:  [['phone'], ['man'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]
Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Tuples: [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['woman', 'has', 'hair'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['long', 'hair'], ['woman', 'in front', 'door']]
Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
Tuples: ['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'] ['glass', 'on', 'table']]
Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
Tuples: [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'has', 'ankle']]
Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
Tuples: [['water'], ['ducks'], ['geese'], ['enjoying', 'ducks'], ['enjoying', 'geese']
Paragraph: "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
Tuples: [['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']]
Paragraph: "A bear with brown fur is looking straight into the camera.  The bear's expression is neutral.  Its fur appears bushy, and is in different shades of brown.  Its nose appears long.  The background consists of some trees.  It is a sunny day."
Tuples: [['bear'], ['fur'], ['camera'], ['brown', 'fur'], ['bushy', 'fur'], ['natural', 'expression'], ['shades', 'fur'], ['long', 'nose'], ['bear', 'look into', 'camera'], ['trees'], ['nose']]]
Paragraph: "This is a group of people possibly at a rally. Some of them have video and regular cameras. The man in the front is wearing a brown pin striped suit. Under the jacket he is wearing a white collar shirt with a purple striped tie; the stripes on the tie forms diamond patterns. His skin is brown and he has dark brown hair. He has a shadow of both a mustache and a beard. The man is also holding a water bottle and a small ticket in one of this hands."
Tuples:[['people'], ['at a rally', 'people'], ['video', 'camera'], ['regular', 'camera'], ['suit'], ['pin', 'striped', 'suit'], ['shirt'], ['white collar', 'shirt'], ['tie'], ['purple', 'striped', 'tie'], ['diamond', 'patterns'], ['skin'], ['brown', 'skin'], ['hair'], ['dark', 'brown', 'hair'], ['mustache'], ['beard'], ['mustache', 'shadow'], ['shadow', 'beard'], ['water', 'bottle'], ['ticket'], ['small', 'ticket'], ['man', 'wearing', 'suit'], ['man', 'holding', 'bottle'], ['man', 'holding', 'ticket'], ['people', 'group'] ,['jacket'], ['man', 'wear', 'tie']]
Paragraph: "A man is lying on a bed in between two pillows. He is wearing a white shirt. The baby has a pacifier in his mouth. There are brown sheets on the bed. A tall brown headboard is at the front of the bed. There is a white painted wall beside the bed. Part of a small brown dresser can be seen beside the bed."
Tuples: [['man'], ['bed'], ['pillow'], ['shirt'], ['baby'], ['pacifier'], ['sheet'], ['headboard'], ['wall'], ['dresser'], ['man', 'lying', 'bed'],['man', 'between', 'pillows'], ['man', 'wearing', 'shirt'], ['baby', 'pacifier', 'mouth'], ['brown', 'sheet'], ['tall', 'headboard'], ['brown', 'headboard'], ['white', 'wall'], ['small', 'dresser'], ['dresser', 'beside', 'bed'], ['white', 'painted','wall'], ['wall', 'beside', 'bed'], ['white' 'shirt']] 
Paragraph: "A woman is facing away from the camera, looking out to the ocean. She is standing in knee-deep water and facing foamy waves. The woman is holding a surfboard in her right arm. The surfboard is mostly white, with some blue at the bottom. She has blonde hair pulled back in a ponytail. She is wearing a grey shirt and swim shorts." 
Tuples: [['woman'], ['ocean'], ['water'], ['wave'], ['shirt'], ['foamy', 'wave'], ['surfboard'], ['right', 'arm'], ['woman', 'hold', 'surfboard'], ['white', 'surfboard'], ['blue', 'surfboard'], ['blonde', 'hair'], ['grey', 'shirt'], ['swim','shorts'], ['woman', 'face', 'ocean'], ['woman', 'standing in', 'water'], ['blonde hair', 'woman'], ['woman', 'wear', 'shirt'], ['woman', 'wear', 'swim shorts'], ['swim', 'shorts']]
Paragraph: "Two people are crouched down on skateboards. They are both wearing helmets and uniforms of spandex.  They are racing one another down a track on the concrete road. The skater in the back has a number on the back."
Tuples: [['skateboard'], ['helmet'], ['road'], ['track'], ['people'], ['concrete', 'road'], ['crouched down', 'people'], ['racing', 'on the' 'road'], ['spandex', 'uniform'], ['people', 'wearing', 'helmet'], ['people', 'wearing', 'spandex'], ['people', 'racing', 'down a track'], ['skater', 'with', 'number'], ['number', 'on', 'back']]"
Paragraph: "An older woman with gray hair and a blue zip up sweatshirt is holding a racket about to hit a tennis ball that is coming toward her. She is wearing a white visor and black pants with white sneakers. Another grey haired woman is standing behind her also in a darker blue sweater and black pants. On the court next to them a young man in a white shirt and blue pants is recovering from having just swung at a ball. Behind the courts is a chain link fence blocking them from a large brick building."
Tuples:[]'''


len = > 8418

rc[0]:"[['woman'],['racket'], ['ball'], ['blue', ' sweatshirt'], ['white', 'visor'], ['black', 'pants'], ['white', 'sneakers'], ['darker', 'blue', 'sweater'], 
['man'], ['white', 'shirt'], ['blue', 'pants'], ['court'], ['chain', 'link','fence'], ['large', 'brick', 'building'], ['older', 'woman'], ['gray', 'hair'], 
['holding', 'racket'], ['woman', 'about', 'hit'], ['ball', 'coming toward her'], ['woman', 'wearing', 'visor'], ['woman', 'wearing', 'sneakers'], 
['woman', 'in', 'sweater'], ['man', 'in', 'shirt'], ['man', 'in', 'pants'], ['court', 'next to', 'woman'], ['man', 'swing', 'at', 'ball'], ['court', 'blocks', 'building'], 
['chain', 'link'], ['fence', 'to', 'building']]"
Paragraph: "An older woman with gray hair and a blue zip up sweatshirt is holding a racket about to hit a tennis ball that is coming toward her. 
She is wearing a white visor and black pants with white sneakers. Another grey haired woman is standing behind her also in a darker blue sweater and black pants. 
On the court next to them a young man in a white shirt and blue pants is recovering from having just swung at a ball. 
Behind the courts is a chain link fence blocking them from a large brick building."

FN: ['sweatshirt'], ['white', 'shirt'], ['young',  'man'], ['recovering', 'man']
['ball', 'coming toward her'] =>['ball', 'coming toward', 'her']
['man', 'swing', 'at', 'ball'] = >['man', 'swing at', 'ball']
it doesn;t learn tuple_size<=3
Another grey haired woman : what do we expect from ?



New FewShot prompt : avoiding the un grounded "Another grey haired woman"


New example based prompt:
"Generate a list, less than or equal to 3, of object-relation-attribute tuples based on the paragraph description. Example:"

rc[0]:"[['woman'], ['racket'], ['tennis', 'ball'], ['zip up', 'sweatshirt'], ['visor'], ['sneakers'], ['sweater'], ['court'],['man'], ['white', 'shirt'],
 ['blue', 'pants'], ['young', 'man'], ['fence'], ['brick', 'building'], ['woman', 'gray', 'hair'], ['woman', 'blue', 'sweatshirt'], ['woman', 'holding', 'racket'],
  ['woman', 'wearing', 'visor'], ['woman', 'wearing', 'sneakers'], ['woman', 'hiting', 'ball'], ['woman', 'behind', 'woman'], ['woman', 'darker', 'blue', 'sweater'],
   ['man', 'white', 'shirt'], ['man', 'blue', 'pants'], ['man', 'swinging', 'ball'], ['chain', 'link', 'fence'], ['fence', 'in front of', 'building'], 
   ['large', 'brick', 'building']]"


New example based prompt:
    "Generate a list, of size less than or equal to 3, of object-relation-attribute tuples based on the paragraph description. Example:"
    
rc[0]:"[['woman'], ['racket'], ['ball'], ['coming', 'toward'], ['woman'], ['visor'], ['sneaker'], ['pants'], ['second', 'woman'], ['court'], 
['man'], ['white', 'shirt'],['fence'], ['building'], ['brick', 'building'], ['older', 'woman'], ['gray', 'hair'], ['blue', 'zip', 'sweatshirt'], 
 ['woman', 'hold', 'racket'],  ['woman', 'wear', 'visor'], ['woman', 'wear', 'sneaker'], ['woman', 'wear', 'black', 'pants'],  
 ['second', 'woman', 'wear', 'darker', 'blue', 'sweater'], 
 ['man', 'in', 'white', 'shirt'], ['man', 'in', 'blue', 'pants'],  ['court', 'next', 'woman'], ['behind', 'court', 'fence'], ['fence', 'block', 'brick', 'building']]"


"Generate a list of object and or relation and or attribute tuples based on the paragraph description. Example:"
    
rc[0]:"[['woman'], ['tennis ball'], ['gray', 'hair'], ['blue', 'zip up sweatshirt'], ['white', 'visor'], ['black', 'pants'], ['white', 'sneakers'], 
['darker', 'blue', 'sweater'], ['young', 'man'], ['white', 'shirt'], ['blue', 'pants'], ['chain link', 'fence'], ['large', 'brick', 'building'], 
['woman', 'hold', 'racket'], ['tennis ball', 'coming toward', 'woman'], ['woman', 'wear', 'visor'], ['woman', 'wear', 'sneakers'], 
['woman','wearing','pants'], ['man', 'swing', 'ball'], ['fence', 'blocking', 'building']]"


"Generate a list of object with or without a relation with or without an attribute tuples based on the paragraph description. Example:"
rc[0]:"[['woman'], ['gray', 'hair'], ['blue', 'sweatshirt'], ['racket'], ['tennis', 'ball'], ['visor'], ['pants'], ['sneakers'], 
['blue', 'sweater'], ['man'], ['white', 'shirt'], ['blue', 'pants'], ['chain', 'fence'], ['brick', 'building'], ['woman', 'holding', 'racket'], 
['ball', 'coming', 'toward'], ['woman', 'wearing', 'visor'], ['woman', 'wear', 'pants'], ['woman', 'wear', 'sneakers'], 
['man', 'wearing', 'white', 'shirt'], ['man', 'wearing', 'blue', 'pants'], ['fence', 'blocking'], ['building', 'behind', 'court'], 
['court', 'beside', 'woman']]"

==========================================
new prompt

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
Tuples:  [['phone'], ['man'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]
Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Tuples: [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['woman', 'has', 'hair'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['long', 'hair'], ['woman', 'in front', 'door']]
Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
Tuples: ['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'] ['glass', 'on', 'table']]
Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
Tuples: [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'has', 'ankle']]
Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
Tuples: [['water'], ['ducks'], ['geese'], ['enjoying', 'ducks'], ['enjoying', 'geese']
Paragraph: "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
Tuples: [['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']]
Paragraph: "A bear with brown fur is looking straight into the camera.  The bear's expression is neutral.  Its fur appears bushy, and is in different shades of brown.  Its nose appears long.  The background consists of some trees.  It is a sunny day."
Tuples: [['bear'], ['fur'], ['camera'], ['brown', 'fur'], ['bushy', 'fur'], ['natural', 'expression'], ['shades', 'fur'], ['long', 'nose'], ['bear', 'look into', 'camera'], ['trees'], ['nose']]]
Paragraph: "This is a group of people possibly at a rally. Some of them have video and regular cameras. The man in the front is wearing a brown pin striped suit. Under the jacket he is wearing a white collar shirt with a purple striped tie; the stripes on the tie forms diamond patterns. His skin is brown and he has dark brown hair. He has a shadow of both a mustache and a beard. The man is also holding a water bottle and a small ticket in one of this hands."
Tuples:[['people'], ['at a rally', 'people'], ['video', 'camera'], ['regular', 'camera'], ['suit'], ['pin', 'striped', 'suit'], ['shirt'], ['white collar', 'shirt'], ['tie'], ['purple', 'striped', 'tie'], ['diamond', 'patterns'], ['skin'], ['brown', 'skin'], ['hair'], ['dark', 'brown', 'hair'], ['mustache'], ['beard'], ['mustache', 'shadow'], ['shadow', 'beard'], ['water', 'bottle'], ['ticket'], ['small', 'ticket'], ['man', 'wearing', 'suit'], ['man', 'holding', 'bottle'], ['man', 'holding', 'ticket'], ['people', 'group'] ,['jacket'], ['man', 'wear', 'tie']]
Paragraph: "A man is lying on a bed in between two pillows. He is wearing a white shirt. The baby has a pacifier in his mouth. There are brown sheets on the bed. A tall brown headboard is at the front of the bed. There is a white painted wall beside the bed. Part of a small brown dresser can be seen beside the bed."
Tuples: [['man'], ['bed'], ['pillow'], ['shirt'], ['baby'], ['pacifier'], ['sheet'], ['headboard'], ['wall'], ['dresser'], ['man', 'lying', 'bed'],['man', 'between', 'pillows'], ['man', 'wearing', 'shirt'], ['baby', 'pacifier', 'mouth'], ['brown', 'sheet'], ['tall', 'headboard'], ['brown', 'headboard'], ['white', 'wall'], ['small', 'dresser'], ['dresser', 'beside', 'bed'], ['white', 'painted','wall'], ['wall', 'beside', 'bed'], ['white' 'shirt']] 
Paragraph: "A woman is facing away from the camera, looking out to the ocean. She is standing in knee-deep water and facing foamy waves. The woman is holding a surfboard in her right arm. The surfboard is mostly white, with some blue at the bottom. She has blonde hair pulled back in a ponytail. She is wearing a grey shirt and swim shorts." 
Tuples: [['woman'], ['ocean'], ['water'], ['wave'], ['shirt'], ['foamy', 'wave'], ['surfboard'], ['right', 'arm'], ['woman', 'hold', 'surfboard'], ['white', 'surfboard'], ['blue', 'surfboard'], ['blonde', 'hair'], ['grey', 'shirt'], ['swim','shorts'], ['woman', 'face', 'ocean'], ['woman', 'standing in', 'water'], ['blonde hair', 'woman'], ['woman', 'wear', 'shirt'], ['woman', 'wear', 'swim shorts'], ['swim', 'shorts']]
Paragraph: "Two people are crouched down on skateboards. They are both wearing helmets and uniforms of spandex.  They are racing one another down a track on the concrete road. The skater in the back has a number on the back."
Tuples: [['skateboard'], ['helmet'], ['road'], ['track'], ['people'], ['concrete', 'road'], ['crouched down', 'people'], ['racing', 'on the' 'road'], ['spandex', 'uniform'], ['people', 'wearing', 'helmet'], ['people', 'wearing', 'spandex'], ['people', 'racing', 'down a track'], ['skater', 'with', 'number'], ['number', 'on', 'back']]"
Paragraph: "An older woman with gray hair and a blue zip up sweatshirt is holding a racket about to hit a tennis ball that is coming toward her. She is wearing a white visor and black pants with white sneakers. Another grey haired woman is standing behind her also in a darker blue sweater and black pants. On the court next to them a young man in a white shirt and blue pants is recovering from having just swung at a ball. Behind the courts is a chain link fence blocking them from a large brick building."
Tuples: [['woman'],['racket'], ['ball'],  ['sweatshirt'], ['blue', ' sweatshirt'], ['white', 'shirt'], ['young',  'man'], ['recovering', 'man'], ['white', 'visor'], ['black', 'pants'], ['white', 'sneakers'], ['darker', 'blue', 'sweater'], ['man'], ['white', 'shirt'], ['blue', 'pants'], ['court'], ['chain', 'link','fence'], ['large', 'brick', 'building'], ['older', 'woman'], ['gray', 'hair'], ['holding', 'racket'], ['woman', 'about', 'hit'], ['ball', 'coming toward', 'her'], ['woman', 'wearing', 'visor'], ['woman', 'wearing', 'sneakers'], ['woman', 'in', 'sweater'], ['man', 'in', 'shirt'], ['man', 'in', 'pants'], ['court', 'next to', 'woman'], ['man', 'swing at', 'ball'], ['court', 'blocks', 'building'], ['chain', 'link'], ['fence', 'to', 'building']]
Paragraph: "Two young children have skis on their feet, and ski poles, but they are both sitting on the snow covering a mountain. It's daylight out, but there's a large shady area that the children are also in. The child to the left looks like a boy, and he's smiling. He's also wearing all black clothing, and a white helmet with red goggles resting on the helmet. The child to the right looks like a girl, and she is wearing pink snow pants, pink and white snow jacket and black sunglasses. She looks like she has brown hair and doesn't appear to be wearing a helmet. Far from them and way to the back of the image, there are green trees that are scattered along the mountain."
Tuples:[]'''


rc[0]
0:"[['skis'], ['children'], ['mountain'], ['ski', 'poles'], ['sitting'], ['snow'], ['daylight'], ['large', 'shady', 'area'], ['left', 'child'], 
['boy'], ['smile'], ['black', 'clothing'], ['white helmet'], ['red', 'goggles'], ['right', 'child'], ['girl'], ['pink', 'snow', 'pants'], ['pink', 'white', 'jacket'], 
['black', 'sunglasses'], ['brown', 'hair'], ['green', 'trees'], ['scattered', 'mountain'], ['children', 'sitting', 'snow'], ['children', 'in', 'shady area'], 
['child', 'wear', 'black', 'clothing'], ['child', 'resting', 'white helmet'], ['child', 'wear', 'goggles'], ['child', 'wear', 'pink', 'snow', 'pants'], 
['child', 'wear', 'pink', 'white', 'jacket'], ['child', 'wear',"
Paragraph: "Two young children have skis on their feet, and ski poles, but they are both sitting on the snow covering a mountain. It's daylight out, 
but there's a large shady area that the children are also in. The child to the left looks like a boy, and he's smiling. 
He's also wearing all black clothing, and a white helmet with red goggles resting on the helmet. The child to the right looks like a girl, and she is wearing pink snow pants,
pink and white snow jacket and black sunglasses. She looks like she has brown hair and doesn't appear to be wearing a helmet. 
Far from them and way to the back of the image, there are green trees that are scattered along the mountain." 

fp :  ['sitting'] ['daylight']

# REmove on shot from Few shot

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
Tuples:  [['phone'], ['man'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]
Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Tuples: [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['woman', 'has', 'hair'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['long', 'hair'], ['woman', 'in front', 'door']]
Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
Tuples: ['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'] ['glass', 'on', 'table']]
Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
Tuples: [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'has', 'ankle']]
Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
Tuples: [['water'], ['ducks'], ['geese'], ['enjoying', 'ducks'], ['enjoying', 'geese']
Paragraph: "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
Tuples: [['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']]
Paragraph: "A bear with brown fur is looking straight into the camera.  The bear's expression is neutral.  Its fur appears bushy, and is in different shades of brown.  Its nose appears long.  The background consists of some trees.  It is a sunny day."
Tuples: [['bear'], ['fur'], ['camera'], ['brown', 'fur'], ['bushy', 'fur'], ['natural', 'expression'], ['shades', 'fur'], ['long', 'nose'], ['bear', 'look into', 'camera'], ['trees'], ['nose']]]
Paragraph: "This is a group of people possibly at a rally. Some of them have video and regular cameras. The man in the front is wearing a brown pin striped suit. Under the jacket he is wearing a white collar shirt with a purple striped tie; the stripes on the tie forms diamond patterns. His skin is brown and he has dark brown hair. He has a shadow of both a mustache and a beard. The man is also holding a water bottle and a small ticket in one of this hands."
Tuples:[['people'], ['at a rally', 'people'], ['video', 'camera'], ['regular', 'camera'], ['suit'], ['pin', 'striped', 'suit'], ['shirt'], ['white collar', 'shirt'], ['tie'], ['purple', 'striped', 'tie'], ['diamond', 'patterns'], ['skin'], ['brown', 'skin'], ['hair'], ['dark', 'brown', 'hair'], ['mustache'], ['beard'], ['mustache', 'shadow'], ['shadow', 'beard'], ['water', 'bottle'], ['ticket'], ['small', 'ticket'], ['man', 'wearing', 'suit'], ['man', 'holding', 'bottle'], ['man', 'holding', 'ticket'], ['people', 'group'] ,['jacket'], ['man', 'wear', 'tie']]
Paragraph: "A man is lying on a bed in between two pillows. He is wearing a white shirt. The baby has a pacifier in his mouth. There are brown sheets on the bed. A tall brown headboard is at the front of the bed. There is a white painted wall beside the bed. Part of a small brown dresser can be seen beside the bed."
Tuples: [['man'], ['bed'], ['pillow'], ['shirt'], ['baby'], ['pacifier'], ['sheet'], ['headboard'], ['wall'], ['dresser'], ['man', 'lying', 'bed'],['man', 'between', 'pillows'], ['man', 'wearing', 'shirt'], ['baby', 'pacifier', 'mouth'], ['brown', 'sheet'], ['tall', 'headboard'], ['brown', 'headboard'], ['white', 'wall'], ['small', 'dresser'], ['dresser', 'beside', 'bed'], ['white', 'painted','wall'], ['wall', 'beside', 'bed'], ['white' 'shirt']] 
Paragraph: "A woman is facing away from the camera, looking out to the ocean. She is standing in knee-deep water and facing foamy waves. The woman is holding a surfboard in her right arm. The surfboard is mostly white, with some blue at the bottom. She has blonde hair pulled back in a ponytail. She is wearing a grey shirt and swim shorts." 
Tuples: [['woman'], ['ocean'], ['water'], ['wave'], ['shirt'], ['foamy', 'wave'], ['surfboard'], ['right', 'arm'], ['woman', 'hold', 'surfboard'], ['white', 'surfboard'], ['blue', 'surfboard'], ['blonde', 'hair'], ['grey', 'shirt'], ['swim','shorts'], ['woman', 'face', 'ocean'], ['woman', 'standing in', 'water'], ['blonde hair', 'woman'], ['woman', 'wear', 'shirt'], ['woman', 'wear', 'swim shorts'], ['swim', 'shorts']]
Paragraph: "Two people are crouched down on skateboards. They are both wearing helmets and uniforms of spandex.  They are racing one another down a track on the concrete road. The skater in the back has a number on the back."
Tuples: [['skateboard'], ['helmet'], ['road'], ['track'], ['people'], ['concrete', 'road'], ['crouched down', 'people'], ['racing', 'on the' 'road'], ['spandex', 'uniform'], ['people', 'wearing', 'helmet'], ['people', 'wearing', 'spandex'], ['people', 'racing', 'down a track'], ['skater', 'with', 'number'], ['number', 'on', 'back']]"
Paragraph: "Two young children have skis on their feet, and ski poles, but they are both sitting on the snow covering a mountain. It's daylight out, but there's a large shady area that the children are also in. The child to the left looks like a boy, and he's smiling. He's also wearing all black clothing, and a white helmet with red goggles resting on the helmet. The child to the right looks like a girl, and she is wearing pink snow pants, pink and white snow jacket and black sunglasses. She looks like she has brown hair and doesn't appear to be wearing a helmet. Far from them and way to the back of the image, there are green trees that are scattered along the mountain."
Tuples:[]'''


rc[0] :"[['child'], ['skis'], ['poles'], ['snow'], ['mountain'], ['daylight'], ['shady', 'area'], ['boy', 'smiling'], ['black', 'clothing'], 
['white', 'helmet'], ['red', 'goggles'], ['girl', 'pink', 'pants'], ['pink', 'snow', 'jacket'], ['white', 'snow', 'jacket'], ['black', 'sunglasses'], 
['brown', 'hair'], ['trees'], ['green', 'trees'], ['mountain', 'with', 'trees'], ['child', 'with', 'skis'], ['child', 'with', 'poles'], ['child', 'covering', 'snow'], 
['child', 'on', 'mountain'], ['child', 'in', 'shady', 'area'], ['child', 'wearing', 'helmet'], ['child', 'wearing', 'sunglasses'], ['child', 'holding', 'poles']]"

Paragraph: "Two young children have skis on their feet, and ski poles, but they are both sitting on the snow covering a mountain. It's daylight out, 
but there's a large shady area that the children are also in. The child to the left looks like a boy, and he's smiling. 
He's also wearing all black clothing, and a white helmet with red goggles resting on the helmet. The child to the right looks like a girl, and she is wearing pink snow pants,
pink and white snow jacket and black sunglasses. She looks like she has brown hair and doesn't appear to be wearing a helmet. 
Far from them and way to the back of the image, there are green trees that are scattered along the mountain." 





Examples of few entities :
['snow'], ['daylight'] an issue 


New 4K prompt

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
Tuples:  [['phone'], ['man'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]
Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Tuples: [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['woman', 'has', 'hair'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['long', 'hair'], ['woman', 'in front', 'door']]
Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table."
Tuples: ['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'] ['glass', 'on', 'table']]
Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
Tuples: [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'has', 'ankle']]
Paragraph: "Two young children have skis on their feet, and ski poles, but they are both sitting on the snow covering a mountain. It's daylight out, but there's a large shady area that the children are also in. The child to the left looks like a boy, and he's smiling. He's also wearing all black clothing, and a white helmet with red goggles resting on the helmet. The child to the right looks like a girl, and she is wearing pink snow pants, pink and white snow jacket and black sunglasses. She looks like she has brown hair and doesn't appear to be wearing a helmet. Far from them and way to the back of the image, there are green trees that are scattered along the mountain."
Tuples:[]'''

rc[0]:"[['children'], ['skis'], ['poles'], ['mountain'], ['daylight'], ['shady', 'area'], ['child', 'left'], ['boy'], ['clothing'], ['helmet'], 
['goggles'], ['child', 'right'], ['girl'], ['snow pants'], ['snow jacket'], ['black', 'sunglasses'], ['brown', 'hair'], ['tree'], ['mountain'], 
['black', 'clothing'], ['white', 'helmet'], ['red', 'goggles'], ['pink', 'snow pants'], ['pink', 'white', 'snow jacket'], ['children', 'sitting', 'snow'], 
['mountain', 'with', 'green', 'trees']]"
 
 ['mountain', 'with', 'green', 'trees']

8K prompt:
    rc[0] :"[['child'], ['skis'], ['poles'], ['snow'], ['mountain'], ['daylight'], ['shady', 'area'], ['boy', 'smiling'], ['black', 'clothing'], 
['white', 'helmet'], ['red', 'goggles'], ['girl', 'pink', 'pants'], ['pink', 'snow', 'jacket'], ['white', 'snow', 'jacket'], ['black', 'sunglasses'], 
['brown', 'hair'], ['trees'], ['green', 'trees'], ['mountain', 'with', 'trees'], ['child', 'with', 'skis'], ['child', 'with', 'poles'], ['child', 'covering', 'snow'], 
['child', 'on', 'mountain'], ['child', 'in', 'shady', 'area'], ['child', 'wearing', 'helmet'], ['child', 'wearing', 'sunglasses'], ['child', 'holding', 'poles']]"

    
    
'''
Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
Tuples: [['water'], ['ducks'], ['geese'], ['enjoying', 'ducks'], ['enjoying', 'geese']
Paragraph: "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
Tuples: [['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']]
Paragraph: "A bear with brown fur is looking straight into the camera.  The bear's expression is neutral.  Its fur appears bushy, and is in different shades of brown.  Its nose appears long.  The background consists of some trees.  It is a sunny day."
Tuples: [['bear'], ['fur'], ['camera'], ['brown', 'fur'], ['bushy', 'fur'], ['natural', 'expression'], ['shades', 'fur'], ['long', 'nose'], ['bear', 'look into', 'camera'], ['trees'], ['nose']]]
Paragraph: "This is a group of people possibly at a rally. Some of them have video and regular cameras. The man in the front is wearing a brown pin striped suit. Under the jacket he is wearing a white collar shirt with a purple striped tie; the stripes on the tie forms diamond patterns. His skin is brown and he has dark brown hair. He has a shadow of both a mustache and a beard. The man is also holding a water bottle and a small ticket in one of this hands."
Tuples:[['people'], ['at a rally', 'people'], ['video', 'camera'], ['regular', 'camera'], ['suit'], ['pin', 'striped', 'suit'], ['shirt'], ['white collar', 'shirt'], ['tie'], ['purple', 'striped', 'tie'], ['diamond', 'patterns'], ['skin'], ['brown', 'skin'], ['hair'], ['dark', 'brown', 'hair'], ['mustache'], ['beard'], ['mustache', 'shadow'], ['shadow', 'beard'], ['water', 'bottle'], ['ticket'], ['small', 'ticket'], ['man', 'wearing', 'suit'], ['man', 'holding', 'bottle'], ['man', 'holding', 'ticket'], ['people', 'group'] ,['jacket'], ['man', 'wear', 'tie']]
Paragraph: "A man is lying on a bed in between two pillows. He is wearing a white shirt. The baby has a pacifier in his mouth. There are brown sheets on the bed. A tall brown headboard is at the front of the bed. There is a white painted wall beside the bed. Part of a small brown dresser can be seen beside the bed."
Tuples: [['man'], ['bed'], ['pillow'], ['shirt'], ['baby'], ['pacifier'], ['sheet'], ['headboard'], ['wall'], ['dresser'], ['man', 'lying', 'bed'],['man', 'between', 'pillows'], ['man', 'wearing', 'shirt'], ['baby', 'pacifier', 'mouth'], ['brown', 'sheet'], ['tall', 'headboard'], ['brown', 'headboard'], ['white', 'wall'], ['small', 'dresser'], ['dresser', 'beside', 'bed'], ['white', 'painted','wall'], ['wall', 'beside', 'bed'], ['white' 'shirt']] 
Paragraph: "A woman is facing away from the camera, looking out to the ocean. She is standing in knee-deep water and facing foamy waves. The woman is holding a surfboard in her right arm. The surfboard is mostly white, with some blue at the bottom. She has blonde hair pulled back in a ponytail. She is wearing a grey shirt and swim shorts." 
Tuples: [['woman'], ['ocean'], ['water'], ['wave'], ['shirt'], ['foamy', 'wave'], ['surfboard'], ['right', 'arm'], ['woman', 'hold', 'surfboard'], ['white', 'surfboard'], ['blue', 'surfboard'], ['blonde', 'hair'], ['grey', 'shirt'], ['swim','shorts'], ['woman', 'face', 'ocean'], ['woman', 'standing in', 'water'], ['blonde hair', 'woman'], ['woman', 'wear', 'shirt'], ['woman', 'wear', 'swim shorts'], ['swim', 'shorts']]
Paragraph: "Two people are crouched down on skateboards. They are both wearing helmets and uniforms of spandex.  They are racing one another down a track on the concrete road. The skater in the back has a number on the back."
Tuples: [['skateboard'], ['helmet'], ['road'], ['track'], ['people'], ['concrete', 'road'], ['crouched down', 'people'], ['racing', 'on the' 'road'], ['spandex', 'uniform'], ['people', 'wearing', 'helmet'], ['people', 'wearing', 'spandex'], ['people', 'racing', 'down a track'], ['skater', 'with', 'number'], ['number', 'on', 'back']]"
Paragraph: "Two young children have skis on their feet, and ski poles, but they are both sitting on the snow covering a mountain. It's daylight out, but there's a large shady area that the children are also in. The child to the left looks like a boy, and he's smiling. He's also wearing all black clothing, and a white helmet with red goggles resting on the helmet. The child to the right looks like a girl, and she is wearing pink snow pants, pink and white snow jacket and black sunglasses. She looks like she has brown hair and doesn't appear to be wearing a helmet. Far from them and way to the back of the image, there are green trees that are scattered along the mountain."
Tuples:[]'''







# New few-shot from HELD WikiFAct : https://crfm.stanford.edu/helm/v1.0/?group=wikifact&subgroup=subject%3A%20position_held&runSpecs=%5B%22wikifact%3Ak%3D5%2Csubject%3Dposition_held%2Cmodel%3Dopenai_text-davinci-002%22%5D

'''The tuples of paragraph: "A silver train with blue writing on it. There is a large dark gray door and some windows on the side" are [['writing'], ['train'], ['blue', 'writing'], ['silver', 'train'], ['writing', 'on', 'train'], ['door'], ['windows'], ['dark', 'door'], ['gray', 'door'], ['large', 'door'], ['windows', 'on', 'side']]
The tuples of paragraph: "The kitchen has gray slate floors, white counters, walls, and ceilings, and stainless steel appliances" are [['kitchen'], ['floors'], ['counters'], ['wall'], [ceiling], ['appliance'], ['slate', 'floors'], ['white', 'counters'], ['gray slate', 'floors'], ['stainless', 'appliance'], ['steel', 'appliance']]
The tuples of paragraph: "Three men are standing in a room. One man is leaning over a table in front of a small cake. He is wearing a short sleeve shirt and green pants." are [['cake'], ['table'], ['man'], ['pants'], ['room'], ['shirt'], ['standing', 'man'], ['small', 'cake'], ['green', 'pants'], ['man', 'lean over', 'table'], ['man', 'wear', 'shirt'], ['man', 'wear', 'pants'], ['short sleeve', 'shirt'], ['sleeve', 'shirt'], ['table', 'have', 'chair'], ['table', 'in front of', 'cake'], ['table', 'near', 'man'], [ 'white', 'table'], ['wall'], ['wall', 'with', 'door']]
The tuples of paragraph: "A woman is standing in a kitchen in front of an oven. She is wearing a gray shirt with a white towel hanging over a shoulder." are [['shirt'], ['gray', 'shirt'], ['shoulder'], ['towel'], ['towel', 'hang over', 'shoulder'], ['white', 'towel'], ['woman'], ['woman', 'stand in', 'kitchen'], ['woman', 'wearing' 'shirt'], ['towel', 'hanging over', 'shoulder']]
The tuples of paragraph: "Two men are on their phone while sitting next to each other." are [['phone'], ['man'], ['sitting', 'man'], ['man' 'on' 'phone']. ['man', 'sitting next to', 'man']]
The tuples of paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door." are [['remote'], ['woman'], ['dress'], ['hair'], ['door'], ['wooden', 'door'], ['standing', 'woman'], ['colorful', 'dress'], ['white', 'remote'], ['woman', 'has', 'hair'], ['woman', 'holding', 'remote'], ['woman', 'wearing', 'dress'], ['dark', 'hair'], ['long', 'hair'], ['woman', 'in front', 'door']]
The tuples of paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table." are ['Someone'], ['knife'], ['fork'], ['hand'], ['table'], ['plate'], ['glass'], ['wooden', 'table'], ['holding', 'knife'], ['hand', 'holding', 'fork'], ['hand', 'holding', 'knife'], ['sitting', 'at', 'table'], ['glass', 'to the right', 'plate'] ['glass', 'on', 'table']]
The tuples of paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle." are [['surfboard'], ['wetsuit'], ['wave'], ['string'], ['ankle'], ['man'], ['holding', 'surfboard'], ['distant', 'wave'], ['man', 'holding', 'surfboard'], ['man', 'wearing', 'wetsuit'], ['big', 'wave'], ['string', 'attached', 'surfboard'], ['string', 'attached', 'ankle'], ['man', 'has', 'ankle']] 
The tuples of paragraph: "Two young children have skis on their feet, and ski poles, but they are both sitting on the snow covering a mountain. It's daylight out, but there's a large shady area that the children are also in. The child to the left looks like a boy, and he's smiling. He's also wearing all black clothing, and a white helmet with red goggles resting on the helmet. The child to the right looks like a girl, and she is wearing pink snow pants, pink and white snow jacket and black sunglasses. She looks like she has brown hair and doesn't appear to be wearing a helmet. Far from them and way to the back of the image, there are green trees that are scattered along the mountain." are 
'''

rc[0] :"[['skis'], ['poles'], ['snow'], ['mountain'], ['children'], ['daylight'], ['shady', 'area'], ['child'], ['boy'], ['smiling'], ['black', 'clothing'], ['white', 'helmet'], ['red', 'goggles'], ['girl'], ['pink', 'pants'], ['pink', 'jacket'], ['white', 'jacket'], ['sunglasses'], ['brown', 'hair'], ['trees'], ['green', 'trees'], ['children', 'on', 'snow'], ['children', 'in', 'shady', 'area'], ['boy', 'smiling'], ['boy', 'wearing', 'clothing'], ['boy', 'wearing', 'helmet'], ['boy', 'wearing', 'goggles'], ['girl', 'wearing', 'pants'], ['girl', 'wearing', 'jacket'], ['girl', 'wearing', 'sunglasses'], ['girl', 'have', 'brown', 'hair'], ['trees', 'on', 'mountain"
FP : ['smiling']
FP : ['daylight']    
['girl', 'have', 'brown', 'hair']

'''
Paragraph: "Nature and water. There are a couple of ducks and geese enjoying."
Tuples: [['water'], ['ducks'], ['geese'], ['enjoying', 'ducks'], ['enjoying', 'geese']
Paragraph: "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
Tuples: [['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']]
Paragraph: "A bear with brown fur is looking straight into the camera.  The bear's expression is neutral.  Its fur appears bushy, and is in different shades of brown.  Its nose appears long.  The background consists of some trees.  It is a sunny day."
Tuples: [['bear'], ['fur'], ['camera'], ['brown', 'fur'], ['bushy', 'fur'], ['natural', 'expression'], ['shades', 'fur'], ['long', 'nose'], ['bear', 'look into', 'camera'], ['trees'], ['nose']]]
Paragraph: "This is a group of people possibly at a rally. Some of them have video and regular cameras. The man in the front is wearing a brown pin striped suit. Under the jacket he is wearing a white collar shirt with a purple striped tie; the stripes on the tie forms diamond patterns. His skin is brown and he has dark brown hair. He has a shadow of both a mustache and a beard. The man is also holding a water bottle and a small ticket in one of this hands."
Tuples:[['people'], ['at a rally', 'people'], ['video', 'camera'], ['regular', 'camera'], ['suit'], ['pin', 'striped', 'suit'], ['shirt'], ['white collar', 'shirt'], ['tie'], ['purple', 'striped', 'tie'], ['diamond', 'patterns'], ['skin'], ['brown', 'skin'], ['hair'], ['dark', 'brown', 'hair'], ['mustache'], ['beard'], ['mustache', 'shadow'], ['shadow', 'beard'], ['water', 'bottle'], ['ticket'], ['small', 'ticket'], ['man', 'wearing', 'suit'], ['man', 'holding', 'bottle'], ['man', 'holding', 'ticket'], ['people', 'group'] ,['jacket'], ['man', 'wear', 'tie']]
Paragraph: "A man is lying on a bed in between two pillows. He is wearing a white shirt. The baby has a pacifier in his mouth. There are brown sheets on the bed. A tall brown headboard is at the front of the bed. There is a white painted wall beside the bed. Part of a small brown dresser can be seen beside the bed."
Tuples: [['man'], ['bed'], ['pillow'], ['shirt'], ['baby'], ['pacifier'], ['sheet'], ['headboard'], ['wall'], ['dresser'], ['man', 'lying', 'bed'],['man', 'between', 'pillows'], ['man', 'wearing', 'shirt'], ['baby', 'pacifier', 'mouth'], ['brown', 'sheet'], ['tall', 'headboard'], ['brown', 'headboard'], ['white', 'wall'], ['small', 'dresser'], ['dresser', 'beside', 'bed'], ['white', 'painted','wall'], ['wall', 'beside', 'bed'], ['white' 'shirt']] 
Paragraph: "A woman is facing away from the camera, looking out to the ocean. She is standing in knee-deep water and facing foamy waves. The woman is holding a surfboard in her right arm. The surfboard is mostly white, with some blue at the bottom. She has blonde hair pulled back in a ponytail. She is wearing a grey shirt and swim shorts." 
Tuples: [['woman'], ['ocean'], ['water'], ['wave'], ['shirt'], ['foamy', 'wave'], ['surfboard'], ['right', 'arm'], ['woman', 'hold', 'surfboard'], ['white', 'surfboard'], ['blue', 'surfboard'], ['blonde', 'hair'], ['grey', 'shirt'], ['swim','shorts'], ['woman', 'face', 'ocean'], ['woman', 'standing in', 'water'], ['blonde hair', 'woman'], ['woman', 'wear', 'shirt'], ['woman', 'wear', 'swim shorts'], ['swim', 'shorts']]
Paragraph: "Two people are crouched down on skateboards. They are both wearing helmets and uniforms of spandex.  They are racing one another down a track on the concrete road. The skater in the back has a number on the back."
Tuples: [['skateboard'], ['helmet'], ['road'], ['track'], ['people'], ['concrete', 'road'], ['crouched down', 'people'], ['racing', 'on the' 'road'], ['spandex', 'uniform'], ['people', 'wearing', 'helmet'], ['people', 'wearing', 'spandex'], ['people', 'racing', 'down a track'], ['skater', 'with', 'number'], ['number', 'on', 'back']]"
Paragraph: "Two young children have skis on their feet, and ski poles, but they are both sitting on the snow covering a mountain. It's daylight out, but there's a large shady area that the children are also in. The child to the left looks like a boy, and he's smiling. He's also wearing all black clothing, and a white helmet with red goggles resting on the helmet. The child to the right looks like a girl, and she is wearing pink snow pants, pink and white snow jacket and black sunglasses. She looks like she has brown hair and doesn't appear to be wearing a helmet. Far from them and way to the back of the image, there are green trees that are scattered along the mountain."
Tuples:[]'''


['boy', 'smiling'] => ['smiling', 'boy']
Triplet: [['area'], ['area', 'large'], ['area', 'shady'], ['back'], ['back', 'of', 'image'], ['boy'], ['child'], ['child', 'have', 'foot'], ['child', 'in'], 
['child', 'look like', 'boy'], ['child', 'look like', 'girl'], ['child', 'sit on', 'snow'], ['child', 'ski on', 'foot'], ['child', 'ski on', 'pole'], ['child', 'smile'], 
['child', 'to', 'left'], ['child', 'to', 'right'], ['child', 'two'], ['child', 'wear', 'jacket'], ['child', 'wear', 'pants'], ['child', 'wear', 'sunglass'], ['child', 'young'],
'clothing'], ['clothing', 'black'], ['foot'], ['girl'], ['goggles'], ['goggles', 'red'], ['hair'], ['hair', 'brown'], ['helmet'], ['helmet', 'rest on', 'helmet'], 
['helmet', 'white'], ['helmet', 'with', 'goggles'], ['image'], ['jacket'], ['jacket', 'pink'], ['jacket', 'snow'], ['left'], ['mountain'], ['pants'], ['pants', 'pink'], 
['pants', 'snow'], ['pole'], ['pole', 'ski'], ['right'], ['snow'], ['snow', 'cover', 'mountain'], ['sunglass'], ['sunglass', 'black'], ['tree'], ['tree', 'green'], 
['tree', 'to', 'back'], ['way']] 



Changing order !!!
rc[0]:"[['children'], ['skis'], ['young', 'children'], ['ski', 'service'], ['snow'], ['mountain'], ['daylight'], ['shady', 'area'], ['child', 'left'], 
['boy'], ['black', 'clothing'], ['white', 'helmet'], ['red', 'goggles'], ['child', 'right'], ['girl'], ['pink', 'snow'], ['pink', 'jacket'], ['white', 'jacket'],
 ['black', 'sunglasses'], ['brown', 'hair'], ['helmet'], ['green', 'trees'], ['trees', 'scattered', 'mountain'], ['children', 'sit', 'snow'], 
 ['children', 'snow', 'mountain']]"


rc[0]:"[['ski'], ['ski pole'], ['snow'], ['mountain'], ['children'], ['daylight'], ['shady', 'area'], ['boy'], ['smiling', 'boy'], ['black', 'clothing'], 
['white', 'helmet'], ['red', 'goggles'], ['resting', 'helmet'], ['girl'], ['pink', 'snow', 'pants'], ['pink', 'white', 'snow', 'jacket'], ['black', 'sunglasses'], 
['brown', 'hair'], ['green', 'trees'], ['mountain', 'have', 'trees'], ['children', 'wearing', 'helmet'], ['children', 'sitting', 'snow'], ['mountain', 'have', 'snow'], 
['children', 'have', 'ski'], ['children', 'have', 'ski poles'], ['children', 'in', 'shady area'], ['children', 'in', 'daylight'], ['children', 'in', 'green', 'trees']]"



def get_paragraph_to_tuple_prompt_4K_dash_sep(query_paragraph):
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
    Tuples: [['phone'], ['man'], ['sitting', 'man'], ['man' 'on' 'phone'], ['man', 'sitting next to', 'man']]
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
    Paragraph: "Two young children have skis on their feet, and ski poles, but they are both sitting on the snow covering a mountain. It's daylight out, but there's a large shady area that the children are also in. The child to the left looks like a boy, and he's smiling. He's also wearing all black clothing, and a white helmet with red goggles resting on the helmet. The child to the right looks like a girl, and she is wearing pink snow pants, pink and white snow jacket and black sunglasses. She looks like she has brown hair and doesn't appear to be wearing a helmet. Far from them and way to the back of the image, there are green trees that are scattered along the mountain."
    Tuples:'''

rc[0] : "[['skis'], ['poles'], ['snow'], ['mountain'], ['daylight'], ['shady', 'area'], ['child'], ['clothing'], ['helmet'], [' child', 'smiling'], 
['left', 'child', 'boy'], ['black', 'clothing'], ['white', 'helmet'], ['red', 'goggles'], ['right', 'child', 'girl'], ['pink', 'snow', 'pants'],
['pink', 'white', 'snow', 'jacket'], ['black', 'sunglasses'], ['brown', 'hair'], ['back', 'image'], ['green', 'trees'], ['scattered', 'trees'], 
['mountain', 'have', 'trees'], ['mountain', 'have', 'snow']]"

FP : ['pink', 'white', 'snow', 'jacket']
FN : 'children'


w/o

rc[0]:"[['ski'], ['ski pole'], ['snow'], ['mountain'], ['children'], ['daylight'], ['shady', 'area'], ['boy'], ['smiling', 'boy'], ['black', 'clothing'], 
['white', 'helmet'], ['red', 'goggles'], ['resting', 'helmet'], ['girl'], ['pink', 'snow', 'pants'], ['pink', 'white', 'snow', 'jacket'], ['black', 'sunglasses'], 
['brown', 'hair'], ['green', 'trees'], ['mountain', 'have', 'trees'], ['children', 'wearing', 'helmet'], ['children', 'sitting', 'snow'], ['mountain', 'have', 'snow'], 
['children', 'have', 'ski'], ['children', 'have', 'ski poles'], ['children', 'in', 'shady area'], ['children', 'in', 'daylight'], ['children', 'in', 'green', 'trees']]"



Paragraph: "Two young children have skis on their feet, and ski poles, but they are both sitting on the snow covering a mountain. It's daylight out, but there's a large shady area that the children are also in. The child to the left looks like a boy, and he's smiling. He's also wearing all black clothing, and a white helmet with red goggles resting on the helmet. The child to the right looks like a girl, and she is wearing pink snow pants, pink and white snow jacket and black sunglasses. She looks like she has brown hair and doesn't appear to be wearing a helmet. Far from them and way to the back of the image, there are green trees that are scattered along the mountain." 
IPC:17648

Perspective:

Triplet: [['ans'], ['ans', 'pan'], ['ans', 'square'], ['blue'], ['blue', 'reach over', 'ans'], ['bowl'], ['bowl', 'white'], ['food'], ['holiday'], ['holiday', 'in', 'yard'], ['one'], ['pan'], ['pan', 'of', 'food'], ['pan', 'square'], ['people'], ['people', 'cook on', 'holiday'], ['people', 'in', 'shirt'], ['people', 'stand'], ['people', 'two'], ['person'], ['person', 'in', 'blue'], ['person', 'in', 'one'], ['person', 'in', 'shirt'], ['person', 'see', 'people'], ['person', 'see tmod', 'person'], ['pit'], ['plate'], ['plate', 'white'], ['round'], ['round', 'pan'], ['shirt'], ['shirt', 'beige'], ['shirt', 'grey'], ['shirt', 'white'], ['smoke'], ['smoke', 'look from', 'smoke'], ['smoke', 'of', 'pit'], ['top'], ['yard'], ['yard', 'back']] 
Paragraph: "From what I see it look like people are cooking in  on a holiday in the back yard.   People are standing around being served some food.  From the smoke of the pit it looks like the food is almost done.  I see a square pan of food being cooked and a round pan that food is being cooked.  I see a white bowl on top of a white plate  I see a person in blue reaching over the square pan ans I see two people in white shirts one person in a beige shirt and one in a grey shirt."
IPC:4232


paragraph: There is a visible portion of an asphalt-covered road, without sidewalks, abutting a forested area to the left of it. The forested region shows green and  yellow overgrown grass and numerous tall pine trees, spaced to allow most a circumference of two feet  or more. It would appear that many of the pines to the forefront are strong and middle-aged, although one nearest to the road shows signs of disease, or age, as its lowest regions are dry and lifeless. Crossing the road and headed in the direction of the trees are two goats.They are brown and white and of a similar size. They appear well-fed. There is a pair of neat horns on each head. The second shows a red decoration on its head and a wide, leather collar on its neck.
Triplet: [['age'], ['area/region'], ['area/region', 'dry'], ['area/region', 'forested'], ['area/region', 'lifeless'], ['area/region', 'lowest'], ['area/region', 'show', 'grass'], ['area/region', 'show', 'tree'], ['circumference'], ['circumference', 'of', 'foot'], ['collar'], ['collar', 'leather'], ['collar', 'on', 'neck'], ['collar', 'wide'], ['decoration'], ['decoration', 'on', 'head/forefront'], ['decoration', 'red'], ['direction'], ['direction', 'of', 'tree'], ['disease'], ['foot'], ['foot', 'two'], ['grass'], ['grass', 'green'], ['grass', 'overgrown'], ['grass', 'yellow'], ['head/forefront'], ['head/forefront', 'have', 'area/region'], ['horn'], ['horn', 'a'], ['horn', 'neat'], ['horn', 'on', 'head/forefront'], ['left'], ['left', 'of', 'portion'], ['nearest'], ['nearest', 'one'], ['nearest', 'show', 'age'], ['nearest', 'show', 'sign'], ['nearest', 'to', 'road'], ['neck'], ['pair'], ['pine'], ['pine', 'many'], ['pine', 'strong'], ['pine', 'to', 'head/forefront'], ['portion'], ['portion', 'of', 'road'], ['portion', 'visible'], ['portion', 'without', 'sidewalk'], ['road'], ['road', 'asphalt-covered'], ['second'], ['second', 'have', 'head/forefront'], ['second', 'have', 'neck'], ['second', 'show', 'collar'], ['second', 'show', 'decoration'], ['sidewalk'], ['sidewalk', 'abut', 'area/region'], ['sidewalk', 'abut to', 'left'], ['sign'], ['sign', 'of', 'disease'], ['size'], ['size', 'similar'], ['tree'], ['tree', 'numerous'], ['tree', 'pine'], ['tree', 'tall']]  
IPC:8262

Paragraph: "An older woman with gray hair and a blue zip up sweatshirt is holding a racket about to hit a tennis ball that is coming toward her. She is wearing a white visor and black pants with white sneakers. Another grey haired woman is standing behind her also in a darker blue sweater and black pants. On the court next to them a young man in a white shirt and blue pants is recovering from having just swung at a ball. Behind the courts is a chain link fence blocking them from a large brick building."
Triplet: [['ball'], ['ball', 'tennis'], ['building'], ['building', 'brick'], ['building', 'large'], ['court'], ['court', 'next to', 'court'], ['fence'], ['fence', 'behind', 'court'], ['fence', 'block', 'court'], ['fence', 'block from', 'building'], ['fence', 'chain'], ['fence', 'link'], ['hair'], ['hair', 'gray'], ['man'], ['man', 'in', 'pants'], ['man', 'in', 'shirt'], ['man', 'recover on', 'court'], ['man', 'young'], ['pants'], ['pants', 'black'], ['pants', 'blue'], ['racket'], ['shirt'], ['shirt', 'white'], ['sneaker'], ['sneaker', 'white'], ['sweater'], ['sweater', 'darker/blue'], ['visor'], ['visor', 'white'], ['woman'], ['woman', 'grey'], ['woman', 'haired'], ['woman', 'hold', 'racket'], ['woman', 'older'], ['woman', 'stand behind', 'woman'], ['woman', 'stand in', 'pants'], ['woman', 'stand in', 'sweater'], ['woman', 'with', 'hair'], ['woman', 'with', 'zip'], ['zip'], ['zip', 'blue']]  
IPC:8235

Triplet: [['card'], ['card', 'greeting'], ['card', 'on', 'table'], ['chair'], ['chair', 'green'], ['chair', 'on', 'wall'], ['corner'], ['corner', 'across from', 'couch'], ['corner', 'back'], ['corner', 'of', 'room'], ['couch'], ['couch', 'near', 'lamp'], ['dress'], ['dress', 'house'], ['dress', 'in front of', 'radio'], ['front'], ['lamp'], ['light'], ['light', 'sit in', 'corner'], ['magazine'], ['magazine', 'on', 'table'], ['mannequin'], ['phone'], ['phone', 'rotary'], ['plant'], ['plant', 'on', 'table'], ['player'], ['player', 'on', 'wall'], ['player', 'radio'], ['radio'], ['room'], ['style'], ['style', 'century'], ['style', 'mid'], ['table'], ['table', 'hold', 'phone'], ['table', 'hold next to', 'couch'], ['table', 'side'], ['tv'], ['tv', 'in', 'corner'], ['wall'], ['wall', 'other']] paragraph: A light sits in the back corner of a room that is decorated in mid century style. A couch is near the lamp, and a radio player on the other wall. There is a TV in the corner across from the couch, and a green chair on the wall it sits in front of. On the table there are magazines, greeting cards, and a plant. A mannequin is dressed in what appears to be a house dress in front of the radio. A side table next to the couch holds a rotary phone. IPC:3792
Triplet: [['bat'], ['bat', 'black'], ['bat', 'have', 'hand'], ['bat', 'in', 'hand'], ['catcher'], ['catcher', 'kneel on', 'ground/base'], ['field'], ['field', 'baseball'], ['front'], ['grass'], ['grass', 'green'], ['grass', 'on', 'field'], ['ground/base'], ['ground/base', 'in front of', 'catcher'], ['ground/base', 'in front of', 'ground/base'], ['ground/base', 'on', 'ground/base'], ['ground/base', 'white'], ['hand'], ['helmet'], ['helmet', 'blue'], ['helmet', 'red'], ['helmet', 'with', 'mask'], ['mask'], ['player'], ['player', 'baseball'], ['player', 'wear', 'helmet'], ['player', 'wear', 'uniform'], ['uniform'], ['uniform', 'gray'], ['uniform', 'red'], ['uniform', 'white']] paragraph: A baseball player is wearing a red and white uniform and a blue and red helmet. He is holding a black bat in his hands. A catcher is kneeling on the ground in front of him. He is wearing a red and gray uniform and a red helmet with a mask. A white base is on the ground in front of him. The baseball field is brown with green grass on it. IPC:15485
The sink is white and has a red and white toothbrush on it. There is a tube on the sink. The tube has a yellow label and the cap is attached. The tube has black writing on it.
Triplet: [['cap'], ['label'], ['label', 'yellow'], ['sink'], ['sink', 'have', 'toothbrush'], ['sink', 'white'], ['toothbrush'], ['toothbrush', 'on', 'sink'], ['toothbrush', 'red'], ['toothbrush', 'white'], ['tube'], ['tube', 'have', 'label'], ['tube', 'have', 'writing'], ['tube', 'on', 'sink'], ['writing'], ['writing', 'black'], ['writing', 'on', 'tube']] paragraph: The sink is white and has a red and white toothbrush on it. There is a tube on the sink. The tube has a yellow label and the cap is attached. The tube has black writing on it. IPC:5006

Triplet: [['bench'], ['bench', 'on', 'sidewalk'], ['bench', 'red'], ['building'], ['building', 'past'], ['building', 'sidewalk'], ['car'], ['color'], ['flower'], ['flower', 'hang above', 'sidewalk'], ['flower', 'potted'], ['jacket'], ['jacket', 'gray'], ['jeans'], ['man'], ['man', 'walk on', 'building'], ['man', 'walk towards', 'man'], ['sidewalk'], ['street'], ['street', 'near', 'sidewalk'], ['tree'], ['tree', 'green'], ['tree', 'large'], ['tree', 'stand on', 'sidewalk']] paragraph: A man is walking on a sidewalk past buildings. He is wearing a gray jacket and jeans. The man is walking towards another man that is sitting on a bench on the sidewalk. The bench is red in color. Potted flowers are hanging above the sidewalk. A large green tree is standing on the sidewalk. Cars are parked on the street near the sidewalk. IPC:12115


Tuples: [['baby'], ['baby', 'have', 'mouth'], ['baby', 'have', 'pacifier'], ['bed'], ['bed', 'in', 'pillow'], ['dresser'], ['dresser', 'brown'], ['dresser', 'small'], ['front'], ['front', 'of', 'bed'], ['headboard'], ['headboard', 'at', 'front'], ['headboard', 'brown'], ['headboard', 'tall'], ['man'], ['man', 'lie on', 'bed'], ['mouth'], ['pacifier'], ['pacifier', 'in', 'mouth'], ['part'], ['part', 'of', 'dresser'], ['pillow'], ['pillow', 'between'], ['pillow', 'two'], ['sheet'], ['sheet', 'brown'], ['sheet', 'on', 'bed'], ['shirt'], ['shirt', 'white'], ['wall'], ['wall', 'beside', 'bed'], ['wall', 'paint'], ['wall', 'white']] 
paragraph: "A man is lying on a bed in between two pillows. He is wearing a white shirt. The baby has a pacifier in his mouth. There are brown sheets on the bed. A tall brown headboard is at the front of the bed. There is a white painted wall beside the bed. Part of a small brown dresser can be seen beside the bed."
IPC:18886

Tuples: [['arm'], ['arm', 'right'], ['blue'], ['blue', 'at', 'bottom'], ['bottom'], ['camera'], ['hair'], ['hair', 'blonde'], ['hair', 'pull back in', 'ponytail'], ['ocean'], ['ponytail'], ['shirt'], ['shirt', 'grey'], ['shorts'], ['surfboard'], ['surfboard', 'in', 'arm'], ['surfboard', 'white'], ['water'], ['water', 'knee-deep'], ['wave'], ['wave', 'foamy'], ['woman'], ['woman', 'face away from', 'camera'], ['woman', 'have', 'arm'], ['woman', 'hold', 'surfboard']] 
paragraph: "A woman is facing away from the camera, looking out to the ocean. She is standing in knee-deep water and facing foamy waves. The woman is holding a surfboard in her right arm. The surfboard is mostly white, with some blue at the bottom. She has blonde hair pulled back in a ponytail. She is wearing a grey shirt and swim shorts." 
IPC:14232

Tuples: [['back'], ['helmet'], ['helmet', 'of', 'spandex'], ['number'], ['number', 'on', 'back'], ['people'], ['people', 'crouch down on', 'skateboard'], ['people', 'two'], ['road'], ['road', 'concrete'], ['skateboard'], ['skater'], ['skater', 'have', 'number'], ['skater', 'in', 'back'], ['spandex'], ['track'], ['uniform']] 
paragraph: "Two people are crouched down on skateboards. They are both wearing helmets and uniforms of spandex.  They are racing one another down a track on the concrete road. The skater in the back has a number on the back."
IPC:6093


paragraph: "This is a group of people possibly at a rally. Some of them have video and regular cameras. The man in the front is wearing a brown pin striped suit. Under the jacket he is wearing a white collar shirt with a purple striped tie; the stripes on the tie forms diamond patterns. His skin is brown and he has dark brown hair. He has a shadow of both a mustache and a beard. The man is also holding a water bottle and a small ticket in one of this hands."  
Triplet: [['beard'], ['bottle'], ['bottle', 'water'], ['camera'], ['camera', 'regular'], ['camera', 'video'], ['front'], ['group'], ['group', 'at', 'rally'], ['group', 'of', 'people'], ['hair'], ['hair', 'brown'], ['hair', 'dark'], ['hand'], ['hand', 'in'], ['jacket'], ['jacket', 'wear', 'shirt'], ['jacket', 'wear under', 'jacket'], ['jacket', 'wear with', 'tie'], ['man'], ['man', 'hold', 'bottle'], ['man', 'hold', 'ticket'], ['man', 'hold in', 'hand'], ['man', 'in', 'front'], ['man', 'wear', 'pin'], ['man', 'wear', 'suit'], ['mustache'], ['pattern'], ['pattern', 'diamond'], ['people'], ['pin'], ['pin', 'brown'], ['rally'], ['shadow'], ['shadow', 'of', 'beard'], ['shadow', 'of', 'mustache'], ['shirt'], ['shirt', 'collar'], ['shirt', 'white'], ['skin'], ['skin', 'brown'], ['skin', 'have', 'hair'], ['stripe'], ['stripe', 'form', 'pattern'], ['stripe', 'on', 'tie'], ['suit'], ['suit', 'striped'], ['ticket'], ['ticket', 'small'], ['tie'], ['tie', 'purple'], ['tie', 'striped']] 
IPC:12022

Triplet: [['background'], ['background', 'consist of', 'tree'], ['bear'], ['bear', 'have', 'expression'], ['bear', 'look into', 'camera'], ['bear', 'with', 'fur'], ['brown'], ['bushy'], ['camera'], ['day'], ['day', 'sunny'], ['expression'], ['expression', 'neutral'], ['fur'], ['fur', 'appear', 'bushy'], ['fur', 'brown'], ['nose'], ['nose', 'appear'], ['shades'], ['shades', 'different'], ['shades', 'of', 'brown'], ['tree']] paragraph: A bear with brown fur is looking straight into the camera.  The bear's expression is neutral.  Its fur appears bushy, and is in different shades of brown.  Its nose appears long.  The background consists of some trees.  It is a sunny day.  
IPC:5031


Triplet: [['cap'], ['label'], ['label', 'yellow'], ['sink'], ['sink', 'have', 'toothbrush'], ['sink', 'white'], ['toothbrush'], ['toothbrush', 'on', 'sink'], ['toothbrush', 'red'], ['toothbrush', 'white'], ['tube'], ['tube', 'have', 'label'], ['tube', 'have', 'writing'], ['tube', 'on', 'sink'], ['writing'], ['writing', 'black'], ['writing', 'on', 'tube']] paragraph: The sink is white and has a red and white toothbrush on it. There is a tube on the sink. The tube has a yellow label and the cap is attached. The tube has black writing on it. 
IPC:5006

todo : remove token "scene", ['daylight'], ['sunny', 'day'], ['image of'] ['in front of', 'camera'] ]['snow']

paragraph: "Two bicycles are parked near a fence. The fence is in front of a sign structure with a clock on top of it. The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign."
Triplet: [['bicycle'], ['debris'], ['fence'], ['two', 'bicycle'], ['building'], ['tall', 'building'], ['sign structure'], ['clock'], ['clock', 'on top of', 'sign'], ['clock', 'read' ],  ['fence', 'in front of', 'sign'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grow', 'grass'], ['grass', 'near', 'pole'], ['ground'], ['cement', 'ground'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'ground'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['sign', 'structure'], ['structure', 'with', 'clock']
# IPC:11621

Paragraph: "A beautiful scene of nature and some water. There are a couple of ducks and geese enjoying the beautiful day and atmosphere. There is a huge tree that has no leaves near the water. There are two birds near the water and one is seen inside. There is a park bench near a smaller tree that has a person sitting on it."
Triplet: [['atmosphere'], ['bench'], ['bench', 'near', 'tree'], ['bench', 'park'], ['bird'], ['bird', 'near', 'water'], ['bird', 'two'], ['couple'], ['couple', 'enjoy tmod', 'atmosphere'], ['couple', 'enjoy tmod', 'day'], ['couple', 'of', 'goose'], ['day'], ['day', 'beautiful'], ['duck'], ['duck', 'a'], ['goose'], ['leaf'], ['leaf', 'near', 'water'], ['nature'], ['person'], ['person', 'sit on', 'bench'], ['scene'], ['scene', 'beautiful'], ['scene', 'of', 'nature'], ['scene', 'of', 'water'], ['tree'], ['tree', 'huge'], ['tree', 'smaller'], ['water']] 
IPC:13555

Paragraph: "The guy holding the surfboard is also wearing a wetsuit to keep himself warm. There is a big wave in the distance. His surfboard has a string attached to it and the other side is attached to the man's ankle."
Tuples: [['ankle'], ['distance'], ['guy'], ['guy', 'hold', 'surfboard'], ['guy', 'warm'], ['guy', 'wear', 'wetsuit'], ['hand'], ['image'], ['image', 'black'], ['image', 'of', 'person'], ['image', 'white'], ['man'], ['man', 'have', 'ankle'], ['people'], ['people', 'in', 'water'], ['person'], ['person', 'stand by', 'water'], ['rock'], ['side'], ['side', 'other'], ['string'], ['string', 'attach to', 'surfboard'], ['surfboard'], ['surfboard', 'have', 'hand'], ['surfboard', 'have', 'string'], ['surfboard', 'in', 'hand'], ['surfboard', 'stand on', 'rock'], ['water'], ['water', 'in', 'distance'], ['water', 'wavy'], ['wave'], ['wave', 'big'], ['wave', 'in', 'distance'], ['wetsuit']] 
IPC:13922

Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door."
Triplet: [['door'], ['wooden', 'door'], ['dress'], ['colorful', 'dress'], ['hair'], ['dark', 'hair'], ['hair', 'long'], ['picture'], ['picture', 'hang on', 'wall'], ['remote'], ['remote', 'white'], ['wall'], ['woman'], ['woman', 'hold'], ['woman', 'wear', 'dress']] 
# IPC:2102

Paragraph: "A woman wearing a colorful dress is holding a white remote. She has dark long hair. She is standing in front of a wooden door. There is a picture hanging on the wall."
Triplet: [['door'], ['door', 'wooden'], ['dress'], ['dress', 'colorful'], ['front'], ['hair'], ['hair', 'dark'], ['hair', 'long'], ['picture'], ['picture', 'hang on', 'wall'], ['remote'], ['remote', 'white'], ['wall'], ['woman'], ['woman', 'hold'], ['woman', 'wear', 'dress']] 
# IPC:7874
# Paragraph: "room has many computers in it. The computers all sit by one desk. There is a black office chair next to the desk. Some headphones hang on one of the monitors. There are many wires hanging from the assorted computers. There is a phone by one of the computer. There are many computer towers as well. The walls are painted blue."
# Triplet: [['chair'], ['chair', 'black'], ['chair', 'next to', 'desk'], ['chair', 'office'], ['computer'], ['computer', 'assorted'], ['computer', 'in', 'room'], ['computer', 'many'], ['computer', 'sit by', 'desk'], ['desk'], ['monitor'], ['one'], ['phone/headphone'], ['phone/headphone', 'by', 'one'], ['phone/headphone', 'hang on', 'monitor'], ['phone/headphone', 'of', 'computer'], ['room'], ['room', 'have', 'computer'], ['tower'], ['tower', 'computer'], ['tower', 'many'], ['wall'], ['wire'], ['wire', 'hang from', 'computer'], ['wire', 'many']] 

paragraph: "Two bicycles are parked near a fence.  The fence is in front of a sign structure with a clock on top of it.  The clock reads 11:40.  There is graffiti on the sign and debris on the ground.  The ground is cement and there are patches of grass growing near the poles holding the sign.  Behind the fence are tall buildings and trees.  Electrical wires and poles are above the street and ground area."
Triplet: [['area'], ['area', 'ground'], ['area', 'street'], ['bicycle'], ['bicycle', 'two'], ['building'], ['building', 'tall'], ['cement'], ['clock'], ['clock', 'on top of', 'structure'], ['clock', 'read'], ['debris'], ['fence'], ['fence', 'in front of', 'structure'], ['front'], ['graffitus'], ['graffitus', 'on', 'debris'], ['graffitus', 'on', 'sign'], ['grass'], ['grass', 'grow'], ['grass', 'near', 'pole'], ['ground'], ['ground', 'cement'], ['patch'], ['patch', 'of', 'grass'], ['pole'], ['pole', 'above', 'area'], ['pole', 'hold', 'sign'], ['sign'], ['sign', 'on', 'ground'], ['structure'], ['structure', 'sign'], ['structure', 'with', 'clock'], ['top'], ['tree'], ['tree', 'tall'], ['wire'], ['wire', 'above', 'area'], ['wire', 'electrical']] 
# IPC:11621

Paragraph: "Someone is holding a knife and a fork in their hands. Someone is sitting at a wooden table getting ready to eat. There is a glass to the right of the plate on the table. There is a gold colored liquid in the glass. The plate is white. The food on the plate is small. There is a wooden tray of bread and meat with a brown sauce on it. The tree is in front of the plate."
Triplet: [['bread'], ['food'], ['food', 'on', 'plate'], ['food', 'small'], ['fork'], ['fork', 'in', 'hand'], ['front'], ['glass'], ['glass', 'to', 'right'], ['hand'], ['knife'], ['liquid'], ['liquid', 'color'], ['liquid', 'gold'], ['liquid', 'in', 'glass'], ['meat'], ['plate'], ['plate', 'on', 'table'], ['plate', 'white'], ['right'], ['right', 'of', 'plate'], ['sauce'], ['sauce', 'brown'], ['sauce', 'on', 'tray'], ['someone'], ['someone', 'have', 'hand'], ['someone', 'hold', 'fork'], ['someone', 'hold', 'knife'], ['someone', 'sit at', 'table'], ['table'], ['table', 'wooden'], ['tray'], ['tray', 'of', 'bread'], ['tray', 'of', 'meat'], ['tray', 'with', 'sauce'], ['tray', 'wooden'], ['tree'], ['tree', 'in front of', 'plate']] 
IPC:11449'''



Anderson not acurate

Paragraph: ""Both roofs are covered with snow.""
Tuples: [['roof'], ['snow']]