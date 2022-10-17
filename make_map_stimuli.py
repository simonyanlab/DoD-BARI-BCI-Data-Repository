#############################################################################
# Create "pandemic-style" visual stimuli characterized by a fantasy map
# background (created with https://azgaar.github.io/Fantasy-Map-Generator/)
# with two regions (1 and 2) and a number of colored circles (white to red)
# representing the severity of a disease. Background images are in .png format
# and need to be saved in the subfolder "backgrounds". The parameters for
# generating the backgrounds are as follows:
# - opacity: 0.5
# - displayed layers: rivers, states, borders
# - map size: 1920 x 1080
# - states number: 2
# - size variety: 10
# - growth rate: 2
#
# The severity of the disease in each region is computed as follows. We
# take the green channel of the color of each circle, we invert it
# (255 - number) so that a high number represents high severity, and then
# we sum all these numbers across the circles in the region.
#
# The difficulty of an image is given by the absolute difference in
# severity between the two regions.
#
# For each image, the script also generates the decision and confidence of
# a random agent, which improves over time (starting from random performance)
# and when correct (incorrect) samples its confidence from values 1-4 with
# probabilities 0.1 0.2 0.3 0.4 (0.4 0.3 0.2 0.1).#
#
# The script generates two images per stimulus: one with the empty background
# and the name of the regions (A and B), and one with the colored circles.
# A txt file containing the information of each stimulus (image number,
# background, number of circles in each region, severity in each region,
# ground truth, agent decision and confidence) is also created.
#
#
#   Command line (add -h for help on parameters):
#   python make_map_stimuli.py
#
#
# Author: Davide Valeriani, PhD
#         Mass Eye and Ear / Harvard Medical School
#         www.davidevaleriani.it
#
#############################################################################

import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np
import argparse
import os
import glob

np.random.seed(0)

parser = argparse.ArgumentParser(description='Make map stimuli script')
parser.add_argument('--num_circles_min', type=int, default=15,
                    help='Minimum number of circles in a stimulus')
parser.add_argument('--num_circles_max', type=int, default=40,
                    help='Maximum number of circles in a stimulus')
parser.add_argument('--circle_radius', type=int, default=10,
                    help='Radius of circles (in pixels)')
parser.add_argument('--num_backgrounds', type=int, default=40,
                    help='Number of different background images available (named map001.png, ..., map040.png)')
parser.add_argument('--num_blocks', type=int, default=7,
                    help='Number of blocks in the experiment, including practice (block 0)')
parser.add_argument('--num_images_per_block', type=int, default=30, choices=range(1, 41),
                    help='Number of visual stimuli (maps with dots) to generate for each block')
parser.add_argument('--min_difference_in_severity', type=int, default=100,
                    help='Minimum difference in severity')
parser.add_argument('--max_difference_in_severity', type=int, default=1000,
                    help='Maximum difference in severity')
args = parser.parse_args()

if not os.path.isdir("images/"):
    os.makedirs("images/")
if not os.path.isdir("practice_images/"):
    os.makedirs("practice_images/")
for f in glob.glob("images/stim*.png"):
    os.remove(f)
for f in glob.glob("practice_images/stim*.png"):
    os.remove(f)

for block in range(args.num_blocks):
    if block == 0:
        eprime_file = open("PracticeTrials.txt", "w")
        trial_type = "PracticeTrial"
        agent_accuracy = 0.5  # Random agent during practice
        output_folder = "practice_images/"
    else:
        eprime_file = open("Block%dTrials.txt" % block, "w")
        trial_type = "TrialProcedure"
        agent_accuracy = np.clip(0.5+block*0.4/(args.num_blocks-1), 0.0, 1.0)  # The agent gets better over time
        output_folder = "images/"
    if block == 0:
        f = open("practice_stimuli.txt", "w")
    elif block == 1:
        f.close()
        f = open("stimuli.txt", "w")
    eprime_file.write("Weight\tNested\tProcedure\tCorrectAnswer\tPreImageFile\tImageFile\tDifficulty\tConfidenceValue\tAgentDecision\tAgentConfidence\tFinalResponseValue\tCellNumber\tCellLabel\n")
    image_number = 0
    bg_available = list(range(1, args.num_backgrounds+1))
    ground_truths = ["1"]*(args.num_images_per_block//2)+["2"]*(args.num_images_per_block//2)
    np.random.shuffle(bg_available)
    np.random.shuffle(ground_truths)
    while image_number < args.num_images_per_block:
        fig, ax = plt.subplots(1, figsize=(1920/96, 1080/96), dpi=96, num=1)
        background = bg_available[image_number]
        num_circles = np.random.randint(args.num_circles_min, args.num_circles_max+1)
        img = plt.imread("backgrounds/map%03d.png" % background)
        h, l, _ = img.shape
        has_circle = np.zeros((l, h), dtype=bool)
        # Add the text for the regions
        written_A = False
        written_B = False
        while not written_A or not written_B:
            x = np.random.randint(0, l-200)
            y = np.random.randint(200, h)
            # Check that there is land on the background map
            if np.any(img[max(y-100, 0):y, x:min(x+100, l), 1] < 0.8):
                continue
            # Check which region is it
            if np.all(img[max(y-100, 0):y, x:min(x+100, l), 1] > 0.85) and np.all(img[max(y-100, 0):y, x:min(x+100, l), 1] < 0.92) and not written_A:
                written_A = True
                has_circle[x:x+100, y-100:y] = True
                plt.text(x, y, "1", fontsize=50)
            elif np.all(img[max(y-100, 0):y, x:min(x+100, l), 1] > 0.92) and not written_B:
                written_B = True
                has_circle[x:x+100, y-100:y] = True
                plt.text(x, y, "2", fontsize=50)
        plt.axis('off')
        plt.subplots_adjust(0,0,1,1,0,0)
        plt.imshow(img)
        plt.savefig("%sstim_%d_%03d_empty.png" % (output_folder, block, image_number+1))
        num_circles_region_A = 0
        num_circles_region_B = 0
        severity_A = 0
        severity_B = 0
        timeout_attempts = 200
        for c in range(num_circles):
            # Generate coordinates of the center of the circle
            while timeout_attempts:
                x = np.random.randint(args.circle_radius, l-args.circle_radius)
                y = np.random.randint(args.circle_radius, h-args.circle_radius)
                # Check that there is land on the background map
                if np.any(img[y-args.circle_radius:y+args.circle_radius, x-args.circle_radius:x+args.circle_radius, 1] < 0.8):
                    timeout_attempts -= 1
                    continue
                # Check that there is not already another circle
                if has_circle[x-args.circle_radius:x+args.circle_radius, y-args.circle_radius:y+args.circle_radius].any():
                    timeout_attempts -= 1
                    continue
                has_circle[x-args.circle_radius:x+args.circle_radius, y-args.circle_radius:y+args.circle_radius] = True
                # Add the circle
                gb_intensity = ''.join([np.random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']) for j in range(2)])
                color = "#FF%s%s" % (gb_intensity, gb_intensity)
                circ = Circle((x, y), args.circle_radius, facecolor=color, linewidth=0.5, edgecolor="k")
                ax.add_patch(circ)
                # Save whether the circle was added to region A or B, and its color
                if 0.85 < img[y, x, 1] < 0.92:
                    # Greenish
                    num_circles_region_A += 1
                    # The higher the green component, the lighter the severity
                    severity_A += 255-int(color[3:5], 16)
                elif img[y, x, 1] > 0.92:
                    # Yellowish
                    num_circles_region_B += 1
                    severity_B += 255-int(color[3:5], 16)
                break
        # Check that we have placed all circles
        if timeout_attempts == 0:
            continue
        # Check the severity is within bounds
        if abs(severity_A-severity_B) < args.min_difference_in_severity or abs(severity_A-severity_B) > args.max_difference_in_severity:
            continue
        # Check that the ground truth corresponds to the one assigned to the trial
        ground_truth = "1" if severity_A > severity_B else "2"
        if ground_truth != ground_truths[image_number]:
            continue
        print(block, image_number, ground_truth)
        image_number += 1
        plt.savefig("%sstim_%d_%03d.png" % (output_folder, block, image_number))
        # Building a random (but good) agent
        agent_decision = np.random.choice(["1", "2"], p=[agent_accuracy, 1-agent_accuracy] if ground_truth == "1" else [1-agent_accuracy, agent_accuracy])
        agent_confidence = np.random.choice([1, 2, 3, 4], p=[0.1, 0.2, 0.3, 0.4] if agent_decision == ground_truth else [0.4, 0.3, 0.2, 0.1])
        f.write("%d %d %d %d %d %d %d %s %s %d\n" % (block, image_number, background, num_circles_region_A, num_circles_region_B, severity_A, severity_B, ground_truth, agent_decision, agent_confidence))
        eprime_file.write("1\t\t%s\t%s\tstim_%d_%03d_empty.png\tstim_%d_%03d.png\t%d\t?\t%s\t%d\t?\t1\tmyCell\n" % (trial_type, ground_truth, block, image_number, block, image_number, abs(severity_A-severity_B), agent_decision, agent_confidence))
        plt.clf()
        plt.close()
    eprime_file.close()
f.close()
