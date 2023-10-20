# graylabel2color

A muitithread tool for transform the gray segmentation label into color label. The tool allows to determine the thread number to accelerate the image processing.

## label_color.txt

This TXT file contains the color dictiionary of gray label. There are 4 numbers in each row, label, color_R, color_G, color_B. These numbers will be detected by main.py

## run

To run this tool, just modify the run.sh like this:
```bash
python3 main.py --image_dir="<your_gray_label_dir>" --out_dir="<your_output_dir>" --threads=6
```
and input:
```bash
sh run.sh
```
