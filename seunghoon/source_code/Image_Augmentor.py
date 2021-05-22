import Augmentor
import os

dir_list = os.listdir("../dataset/Tomato_P04_jpg/")
base_dir = "../dataset/Tomato_P04_jpg/"

p = Augmentor.Pipeline("../dataset/Tomato_P04_jpg")

p.rotate(probability=0.8, max_left_rotation=10, max_right_rotation=10)
p.zoom(probability=0.5, min_factor=0.8, max_factor=1.2)
p.flip_left_right(probability=0.5)
p.flip_top_bottom(probability=0.5)
p.random_distortion(probability=0.9, grid_width=5, grid_height=5, magnitude=8)
p.skew(probability=0.7, magnitude=0.6)
# p.shear(probability=0.9, max_shear_left=15, max_shear_right=15)

p.sample(224)

p.process()


