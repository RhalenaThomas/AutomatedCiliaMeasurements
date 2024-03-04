import pandas as pd
from PIL import Image, ImageDraw
import argparse
from os.path import join, basename, splitext

# Makes paths for the output labeled images using the original filenames
def make_paths(im_path, output_path):
    filename = splitext(basename(im_path))[0]
    return join(output_path, filename + "_labelled.tiff")

# Makes lists of coordinates
def make_lists(im_num, grouped_cell):
    cell_df = (grouped_cell.get_group(im_num)).copy()
    cell_df.drop("ImageNumber", axis=1, inplace=True)
    cell_li = cell_df.values.tolist()
    return cell_li

# Labels image
def label_im(coordinate_list, im_path, output_path):
    img = Image.open(im_path)

    # Writes number onto image at center
    for i, val in enumerate(coordinate_list):
        x_coord = val[0]
        y_coord = val[1]
        d = ImageDraw.Draw(img)

        write_num = str(i + 1)
        d.text((x_coord, y_coord), write_num, fill=(255, 255, 255, 255))

    path = make_paths(im_path, output_path)
    img.save(path)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="Cellprofiler CSV path", required=True)
    parser.add_argument("-m", "--images", help="folder with images path", required=True)
    parser.add_argument("-o", "--output", help="output folder path", required=True)
    parser.add_argument("-n", "--num", help="number of images to label", required=False)

    return vars(parser.parse_args())

def main(**args):
    args = args or parse_args()

    CSV_PATH = args["input"]
    IM_DIR_PATH = args["images"]
    OUTPUT_IM_DIR_PATH = args["output"]

    # Columns we need to keep
    fields = ["ImageNumber", "Location_Center_X", "Location_Center_Y"]

    # Reads csv and groups by the im num
    cell_df = pd.read_csv(CSV_PATH, skipinitialspace=True, usecols=fields)
    grouped_cell = cell_df.groupby(["ImageNumber"])

    # Get number of images, either from the number inputted or from the total number of images
    images = args.get("num") or cell_df.ImageNumber.iat[-1]
    images = int(images)

    # Iterate through the images. Make list of cells, then label and save each image.
    for num in range(1, images + 1):
        cell_list = make_lists(num, grouped_cell)
        im_path = join(IM_DIR_PATH, f"prefix{num}.tiff")  # Adjust filename pattern as needed
        label_im(cell_list, im_path, OUTPUT_IM_DIR_PATH)

if __name__ == "__main__":
    main()
