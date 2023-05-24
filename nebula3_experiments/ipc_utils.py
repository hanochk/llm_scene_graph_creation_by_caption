import json
import os
import sys
import numpy as np


gradient_env_path_based = True
if gradient_env_path_based:
    result_path = "/notebooks/nebula3_playground/images"
    vgenome_images = '/media/vg_data/visualgenome/VG'
    vgenome_metadata = "/storage/vg_data/"
else:
    result_path = "/notebooks/nebula3_playground/images"
    vgenome_images = '/datasets/dataset/vgenome/images/VG_100K'
    vgenome_metadata = "/datasets/dataset/vgenome/metadata"

with open(os.path.join('/storage/ipc_data/paragraphs_v1.json'), "r") as f:
    images_data = json.load(f)
sample_ids = np.loadtxt(os.path.join(vgenome_metadata, "sample_ids_ipc_vgenome_ids.txt"))

ipc_data = json.load(open('/storage/ipc_data/paragraphs_v1.json','r'))
image_ids_related_to_ipc = [images_data[int(ix)]['image_id'] for ix in sample_ids]
# all_image_ids_related_to_ipc = [images_data[int(ix)]['image_id'] for ix in sample_ids]
def get_visual_genome_record_by_ipc_id(ipc_id):
    vg_ind_related_to_ipc = [ix for ix , x in enumerate(ipc_data) if x['image_id']==ipc_id][0]
    ipc = ipc_data[vg_ind_related_to_ipc]
    return ipc
    # ipc_triplets = spice_get_triplets(ipc['paragraph'])

