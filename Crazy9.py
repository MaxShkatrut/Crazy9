import os
import math
import time
import numpy as np
import itertools
import configparser
from PIL import Image

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.pyplot import figure

# Puzzles Type
puz = "Houses"
config = configparser.ConfigParser()
config.read(puz + '/Cards/Cards.ini')
num_of_cards = len(config.sections())

# Create Tiles
sides = []
colors = []
num_colors = []
tiles = np.zeros([num_of_cards, 3, 3])
for i in range(num_of_cards):
        for j in range(4):
                temp = config['Card_' + str(i+1)]['loc' + str(j+1)]
                temp = temp.split(' ')

                temp_side = temp[1]
                if temp_side not in sides:
                        sides.append(temp_side)
                temp_color = temp[0]
                if temp_color not in colors:
                        colors.append(temp_color)
                        num_colors.append(len(colors))

                if j==0:
                        for c, color in enumerate(colors):
                                if temp_color==color:
                                        tiles[i][0][1] = num_colors[c]
                                        if temp_side==sides[0]:
                                                tiles[i][0][1] = -1 * tiles[i][0][1]
                                        break;
                elif j==1:
                        for c, color in enumerate(colors):
                                if temp_color==color:
                                        tiles[i][1][0] = num_colors[c]
                                        if temp_side==sides[0]:
                                                tiles[i][1][0] = -1 * tiles[i][1][0]
                                        break;
                elif j==2:
                        for c, color in enumerate(colors):
                                if temp_color==color:
                                        tiles[i][1][2] = num_colors[c]
                                        if temp_side==sides[0]:
                                                tiles[i][1][2] = -1 * tiles[i][1][2]
                                        break;
                elif j==3:
                        for c, color in enumerate(colors):
                                if temp_color==color:
                                        tiles[i][2][1] = num_colors[c]
                                        if temp_side==sides[0]:
                                                tiles[i][2][1] = -1 * tiles[i][2][1]
                                        break;

# Rotate {tile} 90 degrees {rotations} times
def turn_tile(tile, rotations):
	new_tile = np.zeros([tile.shape[0], tile.shape[1]])
	for r in range(rotations):
		new_tile[0][1] = tile[1][0]
		new_tile[1][0] = tile[2][1]
		new_tile[1][2] = tile[0][1]
		new_tile[2][1] = tile[1][2]
		tile[:][:] = new_tile[:][:]
	return tile

# Find identical Cards
double_cards = []
for i in range(tiles.shape[0]-1):
	for j in range(i+1, tiles.shape[0]):
		rot = 0
		tile_to_check = np.array(tiles[i])
		while rot<4:
			if ((tile_to_check[0][1]==tiles[j][0][1]) and
			    (tile_to_check[1][0]==tiles[j][1][0]) and
			    (tile_to_check[1][2]==tiles[j][1][2]) and
			    (tile_to_check[2][1]==tiles[j][2][1])):
				double_cards.append(np.array([i+1, j+1]))

			rot = rot + 1
			turn_tile(tile_to_check, rot)

# Check if the combination is legal
def is_legal(tiles, position, tile, turn, sol_tiles, sol_turns):
	# Positions = | 0 | 1 | 2 |
	#             | 3 | 4 | 5 |
	#             | 6 | 7 | 8 |
	if position==0:
		return True

	elif position==1:
		tile1 = turn_tile(np.array(tiles[tile]), turn)
		tile0 = turn_tile(np.array(tiles[sol_tiles[0]-1]), sol_turns[0])
		if tile1[1][0]+tile0[1][2]==0:
			return True

	elif position==2:
		tile2 = turn_tile(np.array(tiles[tile]), turn)
		tile1 = turn_tile(np.array(tiles[sol_tiles[1]-1]), sol_turns[1])
		if tile2[1][0]+tile1[1][2]==0:
			return True

	elif position==3:
		tile3 = turn_tile(np.array(tiles[tile]), turn)
		tile0 = turn_tile(np.array(tiles[sol_tiles[0]-1]), sol_turns[0])
		if tile3[0][1]+tile0[2][1]==0:
			return True

	elif position==4:
		tile4 = turn_tile(np.array(tiles[tile]), turn)
		tile1 = turn_tile(np.array(tiles[sol_tiles[1]-1]), sol_turns[1])
		tile3 = turn_tile(np.array(tiles[sol_tiles[3]-1]), sol_turns[3])
		if tile4[0][1]+tile1[2][1]==0 and tile4[1][0]+tile3[1][2]==0:
			return True

	elif position==5:
		tile5 = turn_tile(np.array(tiles[tile]), turn)
		tile2 = turn_tile(np.array(tiles[sol_tiles[2]-1]), sol_turns[2])
		tile4 = turn_tile(np.array(tiles[sol_tiles[4]-1]), sol_turns[4])
		if tile5[0][1]+tile2[2][1]==0 and tile5[1][0]+tile4[1][2]==0:
			return True

	elif position==6:
		tile6 = turn_tile(np.array(tiles[tile]), turn)
		tile3 = turn_tile(np.array(tiles[sol_tiles[3]-1]), sol_turns[3])
		if tile6[0][1]+tile3[2][1]==0:
			return True

	elif position==7:
		tile7 = turn_tile(np.array(tiles[tile]), turn)
		tile4 = turn_tile(np.array(tiles[sol_tiles[4]-1]), sol_turns[4])
		tile6 = turn_tile(np.array(tiles[sol_tiles[6]-1]), sol_turns[6])
		if tile7[0][1]+tile4[2][1]==0 and tile7[1][0]+tile6[1][2]==0:
			return True

	elif position==8:
		tile8 = turn_tile(np.array(tiles[tile]), turn)
		tile5 = turn_tile(np.array(tiles[sol_tiles[5]-1]), sol_turns[5])
		tile7 = turn_tile(np.array(tiles[sol_tiles[7]-1]), sol_turns[7])
		if tile8[0][1]+tile5[2][1]==0 and tile8[1][0]+tile7[1][2]==0:
			return True

	return False

# The backtracking recursive function that checks the combinations
def check_card_combination(tiles, position, sol_tiles, sol_turns, solutions, rotations):
	if position > 8:
		solutions.append(np.array(sol_tiles))
		rotations.append(np.array(sol_turns))
		return True

	res = False
	for tile in range(tiles.shape[0]):
		if tile+1 in sol_tiles:
			continue;
		for turn in range(4):
			if is_legal(tiles, position, tile, turn, sol_tiles, sol_turns):
				sol_tiles[position] = tile+1
				sol_turns[position] = turn

				res = check_card_combination(tiles, position+1, sol_tiles, sol_turns, solutions, rotations) or res

				sol_tiles[position] = 0
				sol_turns[position] = 0

	return res

# Main code
start_time = time.time()
sol_tiles = [0] * num_of_cards
sol_turns = [0] * num_of_cards
solutions_rep = []
rotations_rep = []
check_card_combination(tiles, 0, sol_tiles, sol_turns, solutions_rep, rotations_rep)

num_of_sols_rep = len(solutions_rep)
print('Total number of corrected combinations that was found: %d' % num_of_sols_rep)
print('Running time: %.5f seconds' % (time.time() - start_time))

# Check repeated solutions
# Rotate solution 90 degrees {rotations} times
def turn_sol(sol, rotations):
	new_sol = np.zeros(sol.shape[0])
	for r in range(rotations):
		new_sol[0:3] = [sol[6], sol[3], sol[0]]
		new_sol[3:6] = [sol[7], sol[4], sol[1]]
		new_sol[6:9] = [sol[8], sol[5], sol[2]]
		sol[:] = new_sol[:]
	return sol

def turn_rot(rot, rotations):
	new_rot = np.zeros(rot.shape[0])
	for r in range(rotations):
		new_rot[0:3] = [rot[6]+1, rot[3]+1, rot[0]+1]
		new_rot[3:6] = [rot[7]+1, rot[4]+1, rot[1]+1]
		new_rot[6:9] = [rot[8]+1, rot[5]+1, rot[2]+1]
		for i in range(new_rot.shape[0]):
			if new_rot[i]==4:
				new_rot[i] = 0
		rot[:] = new_rot[:]
	return rot

# Check repeated rotated solutions
solutions = list(solutions_rep)
rotations = list(rotations_rep)
for s1 in range(num_of_sols_rep-1):
	for s2 in range(s1+1, num_of_sols_rep):
		rot = 1
		sol_to_check = turn_sol(np.array(solutions_rep[s1]), rot)
		rot_to_check = turn_rot(np.array(rotations_rep[s1]), rot)
		while rot<4:
			if (sol_to_check==solutions_rep[s2]).all() and (rot_to_check==rotations_rep[s2]).all():
				solutions[s2] = np.zeros(sol_to_check.shape[0], dtype=int)
				rotations[s2] = np.zeros(rot_to_check.shape[0], dtype=int)
				break;
			else:
				rot = rot + 1
				sol_to_check = turn_sol(np.array(solutions_rep[s1]), rot)
				rot_to_check = turn_rot(np.array(rotations_rep[s1]), rot)

while (solutions[-1]==0).all():
	del solutions[-1]
	del rotations[-1]

num_of_sols = len(solutions)
print('Number of corrected combinations after elimation of rotated solutions: %d' % num_of_sols)

# Check double carded repeated solutions
if double_cards!=[]:
	solutions_temp = np.array(solutions)
	for d in range(len(double_cards)):
		for i in range(num_of_sols-1):
			for j in range(solutions_temp[0].shape[0]):
				if solutions_temp[i][j]==double_cards[d][0]:
					solutions_temp[i][j] = double_cards[d][1]
				elif solutions_temp[i][j]==double_cards[d][1]:
					solutions_temp[i][j] = double_cards[d][0]

			for s in range(i+1, num_of_sols):
				if (solutions_temp[i]==solutions[s]).all():
					solutions[s] = np.zeros(sol_to_check.shape[0], dtype=int)

			solutions_temp = np.array(solutions)

	index = 0
	while index<len(solutions):
		if (solutions[index]==0).all():
			del solutions[index]
			del rotations[index]
		else:
			index = index + 1

	num_of_sols = len(solutions)
	print('Number of corrected combinations after elimation double carded solutions: %d' % num_of_sols)

# Preparing the cards
for i in range(num_of_cards):
        img = np.array(Image.open(puz + '/Cards/Card 0{}.png'.format(i+1)))

        if i==0:
                cards = np.zeros([num_of_cards, 4, img.shape[0], img.shape[1], img.shape[2]])

        for j in range(4):
                cards[i][j][:][:][:] = np.rot90(img, 3*j)
cards = cards.astype(int)

# Create the solutions
if not os.path.exists(puz + '/Solutions (Repeated)'):
        os.makedirs(puz + '/Solutions (Repeated)')

for s in range(num_of_sols_rep):
        img1 = cards[solutions_rep[s][0]-1][rotations_rep[s][0]][:][:][:]
        img2 = cards[solutions_rep[s][1]-1][rotations_rep[s][1]][:][:][:]
        img3 = cards[solutions_rep[s][2]-1][rotations_rep[s][2]][:][:][:]
        img4 = cards[solutions_rep[s][3]-1][rotations_rep[s][3]][:][:][:]
        img5 = cards[solutions_rep[s][4]-1][rotations_rep[s][4]][:][:][:]
        img6 = cards[solutions_rep[s][5]-1][rotations_rep[s][5]][:][:][:]
        img7 = cards[solutions_rep[s][6]-1][rotations_rep[s][6]][:][:][:]
        img8 = cards[solutions_rep[s][7]-1][rotations_rep[s][7]][:][:][:]
        img9 = cards[solutions_rep[s][8]-1][rotations_rep[s][8]][:][:][:]

        f, ((ax1, ax2, ax3),
	    (ax4, ax5, ax6),
	    (ax7, ax8, ax9)) = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(8, 8))

        ax1.imshow(img1); ax1.axis('off')
        ax2.imshow(img2); ax2.axis('off')
        ax3.imshow(img3); ax3.axis('off')
        ax4.imshow(img4); ax4.axis('off')
        ax5.imshow(img5); ax5.axis('off')
        ax6.imshow(img6); ax6.axis('off')
        ax7.imshow(img7); ax7.axis('off')
        ax8.imshow(img8); ax8.axis('off')
        ax9.imshow(img9); ax9.axis('off')

        f.subplots_adjust(hspace=0.01, wspace=0.01)

        if s+1<10:
                plt.savefig(puz + '/Solutions (Repeated)/Solution_0{}.png'.format(s+1))
        else:
                plt.savefig(puz + '/Solutions (Repeated)/Solution_{}.png'.format(s+1))

        plt.close(f)

for s in range(num_of_sols):
        img1 = cards[solutions[s][0]-1][rotations[s][0]][:][:][:]
        img2 = cards[solutions[s][1]-1][rotations[s][1]][:][:][:]
        img3 = cards[solutions[s][2]-1][rotations[s][2]][:][:][:]
        img4 = cards[solutions[s][3]-1][rotations[s][3]][:][:][:]
        img5 = cards[solutions[s][4]-1][rotations[s][4]][:][:][:]
        img6 = cards[solutions[s][5]-1][rotations[s][5]][:][:][:]
        img7 = cards[solutions[s][6]-1][rotations[s][6]][:][:][:]
        img8 = cards[solutions[s][7]-1][rotations[s][7]][:][:][:]
        img9 = cards[solutions[s][8]-1][rotations[s][8]][:][:][:]

        f, ((ax1, ax2, ax3),
	    (ax4, ax5, ax6),
	    (ax7, ax8, ax9)) = plt.subplots(3, 3, sharex=True, sharey=True, figsize=(8, 8))

        ax1.imshow(img1); ax1.axis('off')
        ax2.imshow(img2); ax2.axis('off')
        ax3.imshow(img3); ax3.axis('off')
        ax4.imshow(img4); ax4.axis('off')
        ax5.imshow(img5); ax5.axis('off')
        ax6.imshow(img6); ax6.axis('off')
        ax7.imshow(img7); ax7.axis('off')
        ax8.imshow(img8); ax8.axis('off')
        ax9.imshow(img9); ax9.axis('off')

        f.subplots_adjust(hspace=0.01, wspace=0.01)

        if s+1<10:
                plt.savefig(puz + '/Solution_0{}.png'.format(s+1))
        else:
                plt.savefig(puz + '/Solution_{}.png'.format(s+1))

        plt.close(f)
