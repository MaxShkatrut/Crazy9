# Crazy9

Solver for Crazy9 puzzle, or as it calls at his original German name: Legespiel.

The Rules of this puzzle are simple, the player needs to place all nine small squares in larger 3x3 square in a manner that all images fit together.

The idea for the solver came to me after purchasing HEYE's Crazy9 Ketner Owls puzzle. At the back of the box it was written that the puzzle has "two different solutions (at least...)". After founding one of them, I was triggered to find the second one and discover what HEYE's creators meant by saying that this puzzle has "at least" two solutions.

<p align="center">
  <img src="./Ketner Owls/Ketner Owls.jpg" alt=".." title="Crazy9 Ketner Owls puzzle." />
</p>

At first, I wrote straight forward solver that checks all possible combinations with all possible card's orientations and saves only the correct one. In total, the algorithm needed to check 9!=362,880 combinations with 4^9=262,144 orientations in each combination, which means that in total there are 9!*4^9=95,126,814,720 combinations. Even if it will take 1 second for the code to check each combination with all its orientation it will take for the code more than 4 days to finish the task. And this is exactly what happened. This code ran for 4 days and presented all 16 possible solutions, but since the puzzle have two identical cards, this number of solutions should be divided by 2 and because the total list of solutions includes in it also rotated solutions, so this number also should be divided by 4. This is how I found the 2 only solutions that this puzzle has.

Of course, this code is very inefficient since after eliminating specific combination by only examining first two cards, all other similar combinations should also be eliminated. It looked like a classic backtracking problem and in the end, this is what I did. I rewrote the code to solve this puzzle with backtracking recursive function. The improved code run for less than 2 seconds and presented me the same 16 solutions that inefficient code found, but much faster. In other words, it was a success!

The inefficient code Crazy9.py also uploaded to this repository, but you are welcome to ignore it.

The efficient program consists of two codes: Crazy9_BT.py and Crazy9_Results.py. The first one finds all solutions that the puzzle has and the second one creates images of these solutions.

In order to execute the first code, the user needs to create a folder with the puzzle that he desires to solve and change the name of the puzzle in the correct place:
```[bash]
puz = "Ketner Owls"
```

Inside the puzzle folder, the user needs to have a folder that calls "Cards". The folder will have the scans of all 9 cards and "Cards.ini" file in which the user needs to import the figures that the cards have, for example:
```[bash]
[Card_1]
loc1 = Blue Head
loc2 = Purple Tail
loc3 = Green Head
loc4 = Pink Tail
```
where numbering of the locations defined in next manner:
<p>
  <img src="./Locations.png" alt=".." title="Locations." />
</p>

The code is ready to run.

There are two outputs that the code can show.
- First output:
```[bash]
Total number of corrected combinations that was found: 16
Running time: 1.878 seconds
```
- Second output:
```[bash]
Saved data file already exist. Please create backup before running this code again.
```
The first one means that the code successfully executed. It presents the running-time and a total number of possible solutions with the given cards. In addition to that, the code creates "Saved Data.txt" file inside puzzles folder, where is saves the corrected combinations with cards orientations.
The second output I created in case that the user already has a "Saved Data.txt" file, so the code prevented from overwriting of this file.

After that, if user wants to see all the possible results, he should execute the Crazy9_Results.py. For this, the user must have the scans of the cards in Cards folder, named "Card 01.png", "Card 02.png", "Card 03.png", etc., accordingly to the order and the orientation that was typed in the input file "Cards.ini".

This code will create folder "Solutions" inside puzzles folder and will save all possible solutions that the puzzle has as a PNG image.

In addition to HEYE's Crazy9 Ketner Owls puzzle, I found another two puzzles online to test the codes, "Houses" and "Vin, Vino, Wein, Wine!". Their cards and solutions also included in this repository. Accordingly to HEYE's website, https://heye-puzzle.de/en/?s=crazy9, they have another three puzzles: Burgerman Doddles, Mordillo Cows and Wachtmeister Cats. Hopefully I will purchase them and will be able to present their solutions too.

### Notes:
Two minor additions that can be added to the code:
- Check if there are similar cards and removed identical solutions.
- Remove the rotated solutions.

Probably I will spend some time in a near future and add this two last features, but until then, we will continue to get multiplied solutions.
