
import os
import argparse
from automated_cilia_measurements.pixels_to_measurement import (
    main as pixels_to_measurement,
)
from automated_cilia_measurements.center2center import main as center2center
from automated_cilia_measurements.clustering import main as clustering
from automated_cilia_measurements.make_relations_df import main as make_relations_df
from automated_cilia_measurements.label_cprof_im import main as label_cprof_im
from automated_cilia_measurements.data_table import main as data_table
from automated_cilia_measurements.label_c2c import main as label_c2c
from automated_cilia_measurements.label_valid_cilia import main as organelle_labeler
from automated_cilia_measurements.check_accuracy import main as check_accuracy
from automated_cilia_measurements.cluster_as_one import main as cluster_as_one
from automated_cilia_measurements.summary_measurements import main as summary_measurements

def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-ic",
        "--input_csvs",
        help="input csvs from cellprofiler",
        required=True,
    )

    parser.add_argument(
        "-ii",
        "--input_images",
        help="input images from cellprofiler",
        required=True,
    )

    parser.add_argument(
        "-o",
        "--output",
        help="output folder",
        required=True,
    )

    parser.add_argument(
        "-f",
        "--factor",
        help="conversion factor. enter number if you want to convert pixels to micrometer",
        required=False,
    )

    parser.add_argument(
        "-cu",
        "--cluster_as_one",
        help="cluster with all images combined rather than per-image. NOTE: this may crash if not using a computer with sufficient processing capability",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "-hr",
        "--heirarchical",
        help="make dendrograms",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "-x",
        "--xmeans",
        help="perform xmeans clustering",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "-p",
        "--pca",
        help="perform dimensionality reduction",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "-u", "--umap", help="perform UMAP", required=False, action="store_true"
    )

    parser.add_argument(
        "-ce",
        "--cellprofiler_labeling",
        help="label cellprofiler images",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "-nce",
        "--num_cellprofiler_images",
        help="number of images to label for cellprofiler image labeling, if specific number of im wanted",
        required=False,
    )

    parser.add_argument(
        "-cce",
        "--centriole_cellprofiler_images",
        help="label centriole images for cellprofiler image labeling",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "-dt",
        "--data_table",
        help="make a data table",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "-cc",
        "--label_c2c",
        help="label c2c images",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "-ncc",
        "--num_c2c_images",
        help="number of images to label for c2c image labeling, if specific number of im wanted",
        required=False,
    )

    parser.add_argument(
        "-nl",
        "--nuclei_label",
        help="label nuclei images",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "-nnl",
        "--num_nuclei_images",
        help="number of images to label for nuclei image labeling, if specific number of im wanted",
        required=False,
    )

    parser.add_argument(
        "-cl",
        "--cilia_label",
        help="label cilia images",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "-ncl",
        "--num_cilia_images",
        help="number of images to label for cilia image labeling, if specific number of im wanted",
        required=False,
    )

    parser.add_argument(
        "-cel",
        "--cent_label",
        help="label centriole images",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "-ncel",
        "--num_cent_images",
        help="number of images to label for centriole image labeling, if specific number of im wanted",
        required=False,
    )

    parser.add_argument(
        "-ac",
        "--true_results_for_accuracy_checker",
        help="true results of cilia path, if accuracy checker wanted",
        required=False,
    )

    parser.add_argument(
        "-mi",
        "--measurements_per_im",
        help="whether measurements per image should be included",
        required=False,
        action="store_true",
    )
    parser.add_argument(
        "-sc",
        "--scatters",
        help="whether scatterplots should be included",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "-hs",
        "--hist",
        help="whether histograms should be included",
        required=False,
        action="store_true",
    )

    parser.add_argument(
        "-b", 
        "--bins", 
        help="enter something here if you want to use custom bins for histograms", 
        required=False, 
        action="store_true",
    )
    
    return vars(parser.parse_args())


def main(**args):
    
    args = args or parse_args()
    
    dir_out = args["output"]

    if not os.path.exists(dir_out):
        os.makedirs(dir_out)

    csvs_in = args["input_csvs"]
    
    images_in = args["input_images"]

    if args.get("factor"):
        csvs_in = pixels_to_measurement(
            measurements=csvs_in, factor=args["factor"], output=dir_out
        )

    c2c_output_path = center2center(
        measurements=csvs_in, output=dir_out
    )

    make_relations_df(
        measurements=csvs_in, c2c=c2c_output_path, output=dir_out
    )
    

    if (
        args.get("xmeans")
        or args.get("pca_features")
        or args.get("heirarchical")
        or args.get("umap")
    ):
        cluster_output = os.path.join(dir_out, "clustering_output")

        if not os.path.exists(cluster_output):
            os.mkdir(cluster_output)
        if not args.get("cluster_as_one"):
            clustering(
                measurements=csvs_in,
                c2c=os.path.join(c2c_output_path, "c2c_output.csv"),
                xmeans=args.get("xmeans"),
                pca_features=args.get("pca_features"),
                heirarchical=args.get("heirarchical"),
                umap=args.get("umap"),
                output=cluster_output,
            )
        else:
            cluster_as_one(
                measurements=csvs_in,
                c2c=os.path.join(c2c_output_path, "c2c_output.csv"),
                xmeans=args.get("xmeans"),
                pca_features=args.get("pca_features"),
                heirarchical=args.get("heirarchical"),
                umap=args.get("umap"),
                output=cluster_output,
            )
    if (
        args.get("measurements_per_im")
        or args.get("scatters")
        or args.get("hist")
    ):
        summary_measure_output = os.path.join(dir_out, "summary_measures_output")

        if not os.path.exists(summary_measure_output):
            os.mkdir(summary_measure_output)
        if not args.get("cluster_as_one"):
            summary_measurements(
                measurements=csvs_in,
                c2c_results=os.path.join(c2c_output_path),
                measurements_per_im=args.get("measurements_per_im"),
                scatters=args.get("scatters"),
                hist=args.get("hist"),
                output=summary_measure_output,
            )

    if args.get("cellprofiler_labeling"):
        cprof_vis_output = os.path.join(dir_out, "cprof_vis_output")

        if not os.path.exists(cprof_vis_output):
            os.mkdir(cprof_vis_output)

        label_cprof_im(
            input=csvs_in,
            images=images_in,
            output=cprof_vis_output,
            num=args.get("num_cellprofiler_images"),
            centriole=args.get("centriole_cellprofiler_images"),
        )

    if args.get("data_table"):
        data_tbl_output = os.path.join(dir_out, "data_tbl")

        if not os.path.exists(data_tbl_output):
            os.mkdir(data_tbl_output)

        data_table(input=csvs_in, c2c=c2c_output_path, output=data_tbl_output)

    if args.get("label_c2c"):
        c2c_vis_output = os.path.join(dir_out, "c2c_vis_output")

        if not os.path.exists(c2c_vis_output):
            os.mkdir(c2c_vis_output)

        label_c2c(
            input=csvs_in,
            images=images_in,
            c2c=c2c_output_path,
            num=args.get("num_c2c_images"),
            output=c2c_vis_output,
        )

    if args.get("nuclei_label"):
        channel_lbl = os.path.join(dir_out, "channel_NucleusOverlay_vis_output")
        if not os.path.exists(channel_lbl):
            os.mkdir(channel_lbl)

        organelle_labeler(
            measurements=csvs_in,
            output=channel_lbl,
            images=images_in,
            num=args.get("num_nuclei_images"),
            channel="01",
        )

    if args.get("cilia_label"):
        channel_lbl = os.path.join(dir_out, "channel_CiliaOverlay_vis_output")
        if not os.path.exists(channel_lbl):
            os.mkdir(channel_lbl)

        organelle_labeler(
            measurements=csvs_in,
            output=channel_lbl,
            images=images_in,
            num=args.get("num_cilia_images"),
            channel="02",
            c2c=c2c_output_path,
        )

    if args.get("cent_label"):
        channel_lbl = os.path.join(dir_out, "channel_CentrioleOverlay_vis_output")
        if not os.path.exists(channel_lbl):
            os.mkdir(channel_lbl)

        organelle_labeler(
            measurements=csvs_in,
            output=channel_lbl,
            images=images_in,
            num=args.get("num_cent_images"),
            channel="03",
            c2c=c2c_output_path,
        )

    if args.get("true_results_for_accuracy_checker"):
        accuracy_path = os.path.join(dir_out, "check_accuracy")
        if not os.path.exists(accuracy_path):
            os.mkdir(accuracy_path)

        check_accuracy(
            true=args["true_results_for_accuracy_checker"],
            output=accuracy_path,
            c2c=os.path.join(c2c_output_path, "new_cilia.csv"),
        )


if __name__ == "__main__":
    main()

