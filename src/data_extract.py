import configparser
import os

import pandas as pd


def process_directory(directory):
    # Store counts and their respective photon counts
    data = {}

    # Get subdirectories
    subdirectories = [
        os.path.join(directory, d)
        for d in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, d))
    ]

    for subdirectory in subdirectories:
        # Read .ini file
        ini_path = os.path.join(subdirectory, "config.ini")
        config = configparser.ConfigParser()
        config.read(ini_path)
        count = int(config["ion_cloud_1"]["count"])

        # Read .csv file
        csv_path = os.path.join(subdirectory, "ph_scattering.csv")
        df = pd.read_csv(csv_path)
        photon_counts = df["photon count"].iloc[:3].tolist()

        # Append data ensuring count and photon_counts stay connected
        if count not in data:
            data[count] = []
        data[count].extend(photon_counts)

    # Assuming 'count' ranges from 1 to 16 and repeats twice
    headers = [str(i) for i in range(1, 17)] * 2
    output_data = []

    # Prepare data rows
    for i in range(3):
        row = []
        for count in range(1, 17):
            row.append(data[count][i] if count in data and len(data[count]) > i else "")
        for count in range(1, 17):
            row.append(
                data[count][i + 3]
                if count in data and len(data[count]) > (i + 3)
                else ""
            )
        output_data.append(row)

    # Write to output csv
    output_df = pd.DataFrame(output_data, columns=headers)
    output_df.to_csv("output.csv", index=False)
    print("Output written to output.csv")


if __name__ == "__main__":
    directory = input("Enter the directory path: ")
    process_directory(directory)
