This is a snake game developed using pygame. The classic snake game had only one consumable, apple. I've added two more consumables; ice, and chili.
The ice and chili each have different effects. The ice, once consumed, will slow down the snake, and the chili will increase snake's speed.
The apple will also increase the snake's speed, but at a lower rate.
**Implementing NEAT:**
**Version 1.0.0:**
After many trials and errors, the snake finally understood to look for the apple. In this version, the initial topology of the population consists of 8 input nodes, 2 hidden nodes, and 3 output nodes. The inputs are as follows: whether the apple is above the snake, right of the snake, below the snake, or left of the snake, whether the snake is moving towards the apple, the Euclidean distance between the snake and the apple, the difference between the x coordinate of the snake’s head, and the difference between the y coordinate of the snake’s head. The values of the first five inputs are binary. The values of the next three inputs have been normalized to be between 0 and 1.
From the very first generation, some of genomes seem to realize to look for the apple. By the fourth generation, almost each genome in the population knew to look for the apple. But something that has become apparent is that the genomes have opted to not activate one of the outputs, which is turning anti-clockwise. So the outputs are whether continuing in straight ahead, turning clockwise, and turning anti-clockwise. The genomes have started to ignore having the ability to turn anti-clockwise. I think this may be the result of how I have defined the how the snake figures out where the apple is relative to its position. 
Ideas for improvement:
•	Adding two more inputs: x & y coordinates of the snake’s head.
•	Using RNNs instead of feed-forward NNs.
•	Figuring out a way add an input so the snake has some idea as to where the rest of his body parts are relative to its head.
•	Fixing how the snake figures out where the apple is relative to its position. 
Conclusion:
So I let the program run for 78 generations and the most number of apples eaten was 16, which was achieved in generation around 30, and it didn’t make any meaningful improvements passed that point on. Something to keep mind is that it reached 11 apples eaten by generation 7 or 6. Hence, this version of the implementation peaked really early on and it didn’t really make any noticeable improvements passed early generations.
**Version 1.1.0:**
In this version I fixed how the snake figures out where the apple is relative to its position. Previously, if the x coordinate of the apple was bigger than the x coordinate of the snake’s head, it would tell it that it’s to the right of it, and if it was smaller or equal, it would tell it that it’s to the left of it. The same thing applied for the y coordinate. So here the problem was when the x coordinates of the two were the same, the snake would think that the apple was to the left of it (for the y coordinates, the snake would think it’s below it). To fix this problem I added two new inputs to the initial topology. These two new inputs would tell the snake whether the apple was on the same line (had the same coordinates) or not. So in this version the structure of the initial population is the same as the previous version, the only difference is that two new inputs have been added.
One thing to keep in mind is that in this version, the snake still ignores its ability to turn anti-clockwise.
Ideas for improvement:
•	Adding two more inputs: x & y coordinates of the snake’s head.
•	Using RNNs instead of feed-forward NNs.
•	Figuring out a way add an input so the snake has some idea as to where the rest of his body parts are relative to its head.
Conclusion:
This version dramatically improved the performance of the model. In this version, it had surpassed the max score of the last version by generation 9, and it kept improving on the score incrementally. Also, the population on average performed significantly better.
The main thing seemed to be that it doesn’t learn to avoid colliding with its own body, which was predictable because none of the inputs help it to understand to avoid colliding with itself. Also, I don’t why the model keeps ignoring to turn anti-clockwise.
**Version 1.1.1:**
In this version, instead of having inputs tell the snake that the apple is on the same coordinates or not, I added the snake’s head coordinates as inputs. I did this just out of curiosity to see how this change affects the model’s performance.
Conclusion:
This change made the performance worse, and the snake seem to be more confused, as in many instances just right before colliding with the apple, it would change its direction.
**Version 1.2.0:**
This version is the combination of the last two versions, meaning that the model has 12 inputs (snake’s head coordinates and whether the apple has the same coordinates).
Conclusion:
Adding snake’s head coordinates didn’t seem to improve the performance of the model, and I’d even say that it made it slightly even worse. It peaked at generation 20 and didn’t make any improvements after that.
**Version 1.3.0:**
I have added 3 new input nodes which tell the snake whether by going straight, turning right, or left it will collide with its body. I did this as a means to help the snake learn not to collide with its body, as in the previous version, after a point the model’s performance did not improve and this was mainly caused by the snake not learning to avoid its own body.



