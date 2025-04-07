import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
import hashlib
import heapq

from solution import Solution

BLOCK_SHAPES = [ #[x,y,blockID,offsetX,offsetY,rz]
            [2,1,41],
            [3,1,42],
            [4,1,43],
            [2,2,47],
            [8,1,44],
            [4,2,46],
            [16,1,45],
            [4,4,48],
            [8,8,49],
            [6,16,50],
]

class ShapeOptimizer:
    def __init__(self):
        self.existing_hashes = set()
        self.existing_solutions = []
        self.best_efficiency = float('inf')
        self.best_solution = None
        self.depth_coeff = 4
    
    def Plot_Matrix(self, arr):
        # colours_float = {key: [float(val) for val in value] for key, value in self.colour_dict.items()}
        # cmap = ListedColormap(colours_float.values())
        plt.imshow(arr)
        plt.gca().invert_yaxis()
        plt.show()
        
    def hash_array(self, array):
        array_bytes = array.tobytes()
        return hashlib.sha256(array_bytes).hexdigest()
    
    def get_fitting_blocks(self, shape_coords):
        fitting_blocks = []
        crop = self.crop_shape(shape_coords)
        for block in BLOCK_SHAPES:
            block_height = block[0]
            block_width = block[1]

            if block_width <= (crop[3] - crop[2] + 1) and block_height <= (crop[1] - crop[0] + 1):
                fitting_blocks.insert(0,[block[1], block[0], block[2], 0])
            elif block_width <= (crop[1] - crop[0] + 1) and block_height <= (crop[3] - crop[2] + 1):
                fitting_blocks.insert(0,[block[1], block[0], block[2], 0])
        return fitting_blocks
    
    def crop_shape(self, shape_coords):
        min_x = min([coord[1] for coord in shape_coords])
        max_x = max([coord[1] for coord in shape_coords])
        min_y = min([coord[0] for coord in shape_coords])
        max_y = max([coord[0] for coord in shape_coords])

        return [min_x, max_x, min_y, max_y]
    
    def display_results(self, permutations):
        print('Best efficiency: ', self.best_efficiency)
        print('Solutions: ', len(permutations))
        for sol in permutations:
            # self.Plot_Matrix(sol.arr)
            efficiency = sol.assess_efficiency()
            if efficiency == self.best_efficiency:
                print('Best solution: ')
                # self.Plot_Matrix(sol.arr)
        print('BEST SOL')
        self.Plot_Matrix(self.best_solution.arr)
    
    def optimize_shape(self, shape, arr, color):
        shape_arr = np.zeros_like(arr)
        shape_coords = shape
        for row, col in shape_coords:
            shape_arr[row, col] = color
            
        base_solution = Solution(shape_arr, shape_coords, [], color, 0, None)
        self.existing_solutions.append(base_solution)
        
        permutations = self.search_handler(base_solution, color)
        print('HERE', permutations)
        self.display_results(permutations)

    def get_sorted_permutations(self, permutations, sort_by, block=None):
        if sort_by == 'eff':
            sorted_permutations = sorted(permutations, key=lambda solution: solution.assess_efficiency())
        elif sort_by == 'pot':
            if block:
                sorted_permutations = sorted(permutations, key=lambda solution: solution.assess_potential_efficiency(block))
            else:
                return None
        elif sort_by == 'per':
            sorted_permutations = sorted(permutations, key=lambda solution: solution.get_perimeter())
        return sorted_permutations
            
    def search_handler(self, base_solution, color):
        blocks = self.get_fitting_blocks(base_solution.shape_coords)
        
        max_depth = 3
        trim = 10
        block_count = len(blocks)
        
        permutations = [base_solution]

        if block_count < max_depth:
            for block in blocks:
                new_permutations = []
                sorted_permutations = self.get_sorted_permutations(permutations, sort_by='eff')
                for permutation in sorted_permutations:
                    new_permutations.extend(self.find_block_permutations(block, color, permutation))
                permutations.extend(new_permutations)

        else:
            for block in blocks:
                new_permutations = []
                sorted_pot_permutations = self.get_sorted_permutations(permutations, sort_by='pot', block=block)
                trimmed_permutations = self.get_sorted_permutations(sorted_pot_permutations[:trim], sort_by='per')
                for permutation in trimmed_permutations:
                    new_permutations.extend(self.find_block_permutations(block, color, permutation))
                permutations.extend(new_permutations)
        return permutations 
    
    def find_block_permutations(self, block, color, root):
        permutations = [root]
        finding_solutions = True
        while finding_solutions:
            for solution in permutations:
                new_permutations = self.iterate_over_shape(solution, block, color, root)
                if len(new_permutations) == 0:
                    finding_solutions = False
                else:
                    permutations.extend(new_permutations)
                    
        if root in permutations:
            permutations.remove(root)
        return permutations

    def iterate_over_shape(self, solution, block, color, root):
        arr = solution.arr
        
        potential_efficiency = solution.assess_potential_efficiency(block)
        if potential_efficiency > self.best_efficiency:
            return []
        
        if block[0] != block[1]:
            rotated_block = [block[1], block[0], block[2], 90]
            blocks = [block, rotated_block]
        else:
            blocks = [block]
        
        new_solutions = []
        for block in blocks:
            block_height = block[0]
            block_width = block[1]
            block_id = block[2]
            for row, col in solution.shape_coords:
                if arr[row, col] == color:
                    pos_arr = arr.copy()
                    pos_arr[row: row + block_height, col: col + block_width] = block_id
                    # self.Plot_Matrix(pos_arr)
                    
                    if self.can_place_block(solution, row, col, block, color):
                        if self.is_new_shape(pos_arr):
                            coords = list(solution.shape_coords)
                            block_list = list(solution.block_list)
                            new_solution = Solution(pos_arr, coords, block_list, color, root)
                            new_solution.place_block((row, col), block)
                            new_solutions.append(new_solution)
                            self.existing_solutions.append(new_solution)
                            
                            arr_hash = self.hash_array(pos_arr)
                            self.existing_hashes.add(arr_hash)
                            
                            self.check_efficiency(new_solution)
        return new_solutions
    
    def check_efficiency(self, solution):
        efficiency = solution.assess_efficiency()
        if efficiency < self.best_efficiency:
            self.best_efficiency = efficiency
            self.best_solution = solution
            
    def can_place_block(self, solution, row, col, block, color):
        block_height = block[0]
        block_width = block[1]
        arr = solution.arr
        
        if np.all(arr[row: row + block_height, col: col + block_width] == color):
            return True
        return False

    def is_new_shape(self, array):
        hashes = set()
        base_hash = self.hash_array(array)
        if base_hash in self.existing_hashes:
            return False

        for i in range(4):
            rotated = np.rot90(array, k=i)
            h_reflect = np.fliplr(rotated)
            v_reflect = np.flipud(rotated)
            for arr in [rotated, h_reflect, v_reflect]:
                hashes.add(self.hash_array(arr))

        if any(arr_hash in self.existing_hashes for arr_hash in hashes):
            return False
        return True
    
    def preview_placement(self, arr, row, col, block_height, block_width, block_id):
        if row == 2 and col == 1:
            print('\nhere\n')
            self.Plot_Matrix(arr)
            print('Previewing placement: ')
            tmp_arr = arr.copy()
            tmp_arr[row:row+block_height, col:col+block_width] = block_id
            print('with placement:')
            self.Plot_Matrix(tmp_arr)
            # print('without placement:')
            # self.Plot_Matrix(arr)
            

                
        

                    
        



                        
