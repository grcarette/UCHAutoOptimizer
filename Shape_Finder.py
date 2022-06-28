import numpy as np
from matplotlib import pyplot as plt
from anytree import Node, RenderTree, NodeMixin, LevelOrderIter

def produce_shape(opt_mat, shape_mat, position): 
    if opt_mat[position] != 0:
        iterable_size = (tuple([index -1 for index in np.shape(opt_mat)])) #np.shape produces shape of matrix starting from 1, change to start from 0
        adjacent_tiles = [(position[0]+1, position[1]),(position[0]-1, position[1]),(position[0], position[1]+1),(position[0], position[1]-1)]
        shape_mat[position] = 1
        opt_mat[position] = 0
        for checkable_tile in [tile for tile in adjacent_tiles if all(0 <= tile[x] <= iterable_size[x] for x in range(len(iterable_size)))]:
            produce_shape(opt_mat, shape_mat, checkable_tile)
    return shape_mat

def find_shapes(opt_mat):
    shape_list = []
    opt_mat_rows = np.size(opt_mat,0)
    opt_mat_cols = np.size(opt_mat,1)
    shape_mat = np.zeros((opt_mat_rows, opt_mat_cols))
    while not np.array_equiv(opt_mat, np.zeros((opt_mat_rows,opt_mat_cols))):
        for ind_col in range(opt_mat_cols):
            for ind_row in range(opt_mat_rows):
                if opt_mat[ind_row,ind_col] != 0:
                    shape_list.append(produce_shape(opt_mat, shape_mat, (ind_row,ind_col)))
                    shape_mat = np.zeros((opt_mat_rows, opt_mat_cols))
    return shape_list

if __name__ == "__main__":
    test_matrix = np.random.randint(2, size=(16,16))
    shape_list = find_shapes(test_matrix)
    
