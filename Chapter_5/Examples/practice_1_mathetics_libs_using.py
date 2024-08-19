import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
from mpl_toolkits.mplot3d import Axes3D

pd.options.display.max_rows = 10
pd.options.display.max_columns = 10
pd.options.display.float_format = "{:.1f}".format

california_housing_dataframe = pd.read_csv(
    "https://download.mlcc.google.cn/mledu-datasets/california_housing_train.csv", sep=",")
california_housing_dataframe = california_housing_dataframe.reindex(
    np.random.permutation(california_housing_dataframe.index)
)


def preprocess_features(data):
    """
    Preprocess the input features from the data.

    Args:
        data (pd.DataFrame): The input data containing various features.

    Returns:
        pd.DataFrame: A DataFrame containing the selected and processed features.
    """
    selected_features = data[
        ["latitude",
         "longitude",
         "housing_median_age",
         "total_rooms",
         "total_bedrooms",
         "population",
         "households",
         "median_income"]
    ]
    processed_features = selected_features.copy()
    processed_features["rooms_per_person"] = (
            data["total_rooms"] / data["population"]
    )
    return processed_features


def preprocess_targets(data, need_normalize):
    """
    Preprocess the target values from the data.

    Args:
        data (pd.DataFrame): The input data containing the target values.
        need_normalize: Whether to normalize the output median_house_value

    Returns:
        pd.DataFrame: A DataFrame containing the processed target values.
    """
    output_targets = pd.DataFrame()
    output_targets['median_house_value_is_high'] = (
        (data['median_house_value'] > 265000).astype(float)
    )
    output_targets["median_house_value"] = (
            data["median_house_value"] / 1000.0
    )
    if need_normalize:
        output_targets["median_house_value"] /= output_targets["median_house_value"].max()
    return output_targets


def ploting_2d_histogram(examples, targets):
    """
    Plot a 2D histogram of the examples and targets.

    Args:
        examples (pd.DataFrame): The input features to plot.
        targets (pd.DataFrame): The target values to plot.

    Returns:
        None
    """
    # Create a new figure with a specified size
    plt.figure(figsize=(13.00, 9.00))

    # Add a 2D subplot to the figure
    plt.subplot(1, 1, 1)

    # Set the title and labels for the 2D plot
    plt.title("California Housing Validation Data")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.autoscale(False)
    plt.ylim([32, 43])
    plt.xlim([-126, -112])

    # Create a 2D scatter plot
    plt.scatter(
        examples["longitude"],
        examples["latitude"],
        cmap="coolwarm",
        c=targets
    )

    # Display the plot
    plt.show()


def ploting_3d_histogram(examples, targets, z_label):
    """
    Plot a 3D histogram of the examples and targets.

    Args:
        examples (pd.DataFrame): The input features to plot.
        targets (pd.DataFrame): The target values to plot.
        z_label (string): The Z-Label descriptions

    Returns:
        None
    """
    # Create a new figure with a specified size
    fig = plt.figure(figsize=(13.00, 9.00))

    # Add a 3D subplot to the figure
    ax = fig.add_subplot(111, projection='3d')

    # Set the title and labels for the 3D plot
    ax.set_title("California Housing 3D Data")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel(z_label)

    # Create a 3D scatter plot
    scatter = ax.scatter(
        examples["longitude"],
        examples["latitude"],
        targets,
        c=targets,
        cmap="coolwarm"
    )

    # Add a color bar which maps values to colors
    cbar = fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
    cbar.set_label('Color State')

    # <3D special>: Set initial view angle
    ax.view_init(elev=30, azim=30)

    # Display the plot
    plt.show()


total_examples = preprocess_features(california_housing_dataframe.head(17000))
total_targets = preprocess_targets(california_housing_dataframe.head(17000), True)
print("total::\n")
print(total_examples.describe())
print(total_targets.describe())

ploting_2d_histogram(total_examples, total_targets["median_house_value"])
ploting_3d_histogram(total_examples, total_targets["median_house_value"], "Median House Value (in $1000's)")
ploting_3d_histogram(total_examples, total_examples["rooms_per_person"], "Rooms/Person")
