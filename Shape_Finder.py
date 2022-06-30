from cgi import test
import numpy as np
from matplotlib import pyplot as plt
import itertools, operator

def plot_matrix(matrix, vertices = None):
    if vertices != None:
        plt.scatter(*zip(*vertices))
    plt.imshow(matrix)
    plt.show()

def find_shapes(opt_mat):
    shape_list = []
    opt_mat_rows = np.size(opt_mat,0)
    opt_mat_cols = np.size(opt_mat,1)
    for ind_col in range(opt_mat_cols):
        for ind_row in range(opt_mat_rows):
            if opt_mat[ind_row,ind_col] == 1:
                shape_list.append((produce_shape(opt_mat, np.zeros((opt_mat_rows, opt_mat_cols)),(ind_row,ind_col))))
    return shape_list

def produce_shape(opt_mat, shape_mat, position): 
    adjacent_tiles = [(position[0]+1, position[1]),(position[0]-1, position[1]),(position[0], position[1]+1),(position[0], position[1]-1)]
    shape_mat[position] = 1
    opt_mat[position] = 2
    for checkable_tile in [tile for tile in adjacent_tiles if opt_mat[tile] == 1]:
        produce_shape(opt_mat, shape_mat, checkable_tile)
    return shape_mat

def crop_shape(shape):
    row_lst = [np.any(row) for row in shape]
    col_lst = [np.any(col) for col in shape.T]

    ind_rowa = row_lst.index(True)-1
    ind_rowb = len(row_lst) - row_lst[::-1].index(True)+1
    ind_cola = col_lst.index(True)-1
    ind_colb = len(col_lst) - col_lst[::-1].index(True)+1

    shape = shape[ind_rowa:ind_rowb,ind_cola:ind_colb]

    return shape, [ind_cola,ind_colb,ind_rowa,ind_rowb]

def shape_to_vertices(shape, origin):
    shape_b = shape[0:-1,0:-1]
    vertices = []
    print(origin)
    for ind_col in range(np.size(shape_b,1)):
        for ind_row in range(np.size(shape_b,0)):
            sub_mat = shape[ind_row:ind_row+2,ind_col:ind_col+2]
            sub_mat_count = np.count_nonzero(sub_mat)
            if sub_mat_count == 0 or sub_mat_count == 4:
                pass
            elif sub_mat_count == 1 or sub_mat_count == 3:
                vertices.append((ind_col+0.5-origin[0],ind_row+0.5-origin[2]))
            elif np.count_nonzero(sub_mat-sub_mat.T) == 0:
                vertices.append((ind_col+0.5+origin[0],ind_row+0.5+origin[2]))
    plot_matrix(shape,vertices)

if __name__ == "__main__":
    test_matrix = np.random.randint(2, size=(4,4))
    test_matrix = np.pad(test_matrix, pad_width = 1, mode='constant', constant_values=0)
    plot_matrix(test_matrix)
    shape_list = find_shapes(test_matrix)
    for shape in shape_list:
        cropped_shape, position = crop_shape(shape)
        shape_vertices = shape_to_vertices(cropped_shape, position)
    print('done')
