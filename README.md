# Bad Apple in logisim

Video demo: https://youtu.be/Uxlg-xcYgaY

I overheard someone in my Digital Electronics class joking about playing the Bad Apple music video in Logisim and I thought it might be a fun project.

The Bad Apple music video is commonly put on weird displays as a challange (similar to loading Doom onto weird things) due to it being only two colors: black and white.

This animation runs off of a sum of products circuit for each pixel which takes in the current frame in binary and has a minterm for each frame it should be lit. It is all generated in the very messy python script `logism_bad_apple.py` which was thrown together in a night. It will take about 10 minutes to run as it is very poorly optimized. The `.circ` file may take a while to get loaded into logism, I would recomend using logism-evolution instead for a speed increase. The Python program does not connect the counter to the final grid, but this can be done simply with two extra wires.

Bad Apple music video credits: https://www.youtube.com/watch?v=FtutLA63Cp8

Here is a much better implementation of Bad Apple in logisim I found after coding mine: https://www.youtube.com/watch?v=DpyAgNdl6oA
