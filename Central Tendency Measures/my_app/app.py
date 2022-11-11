"""
    In this file a Shiny app will be created in order to see how Mean and Median Measuring values behave
    when adding outliers to the data. There will be several interactive parameters in the application:
    - Sample size
    - Number of bins
    - If outlier selection checkbox is selected:
        * Outlier offset: add big or small outlier values
        * Number of outliers
"""

# import packages
from shiny import App, reactive, render, ui
import matplotlib.pyplot as plt
import numpy as np


# design Shiny application
app_ui = ui.page_fluid(
    ui.panel_title("Measuring Sensitivity of Central Tendency Measures to Outliers"),
    ui.layout_sidebar(
        # left side panel - parameters
        ui.panel_sidebar(
            ui.input_slider("n", "Sample size", 0, 10000, 1000, step=50),
            ui.input_slider("n_bins", "Number of bins", 0, 100, 40, step=10),
            # show mean and median values
            ui.output_text_verbatim("measure_tendencies"),
            ui.input_checkbox("outliers", "Add outliers to distribution", False),
            ui.panel_conditional(
                "input.outliers",
                ui.input_slider("offset_outliers", "Select offset for outliers (big/small outliers)", 0, 50, 0, step=5)
            ),
            ui.panel_conditional(
                "input.outliers",
                ui.input_slider("n_outliers", "Select amount of outlier values", 0, 10, 0, step=1)
            )
        ),
        # right side panel - plot
        ui.panel_main(
            ui.output_plot("plot", width = "60%", height = "855px")
        ),
    ),
)


# define functions and use cases for application
def server(input, output, session):

    # define reactive values - original data will be saved
    data = reactive.Value()
    original_data = reactive.Value()

    # create new sample when n (sample_size) is changed (log distribution)
    @reactive.Effect
    @reactive.event(input.n)
    def _():
        # avoid error when sample_size 0 is selected - use 1 instead
        if input.n() == 0:
            distribution = np.exp(np.random.randn(1))
        else:
            distribution = np.exp(np.random.randn(input.n()))
        data.set(distribution)
        original_data.set(distribution)


    # reactive event to create corresponding outlier values and append to original data
    @reactive.Effect
    @reactive.event(input.n_outliers, input.offset_outliers, input.n)
    def _():
        # load original sample
        d = original_data.get()
        # do not do anything when offset or n_outliers are 0
        if input.n_outliers() != 0 and input.offset_outliers() != 0:
            d = np.hstack((d, np.mean(d) * np.random.randn(input.n_outliers()) + input.offset_outliers() * np.std(d)))
        np.random.shuffle(d)
        # set to current data
        data.set(d)


    # show sample mean and median
    @output
    @render.text
    def measure_tendencies():
        return f"Mean value: {round(np.mean(data()), 4)}\tMedian value: {round(np.median(data()), 4)}"

    # create plots
    @output
    @render.plot(alt="A histogram")
    def plot() -> object:

        # avoid 0 bins error
        if input.n_bins() == 0:
            nbins = 1
        else:
            nbins = input.n_bins()

        # get mean and median values
        mean = np.mean(data())
        median = np.median(data())
        d = original_data.get()
        # create histogram
        fig, ax = plt.subplots(3, 1)
        ax[0].hist(data(), bins=nbins)
        ax[0].set_title("Log distribution histogram", fontsize="8")
        ax[0].set_xlabel("Value")
        ax[0].set_ylabel("Counts")
        # create plot to show datapoints, mean and median
        ax[1].plot(data(), '.', color="lightgray", label="Data")
        ax[1].plot([0, len(data.get())], [mean, mean], '--', color="deepskyblue", label="Mean")
        ax[1].plot([0, len(data.get())], [median, median], '-.', color="crimson", label="Median")
        ax[1].legend()
        ax[1].set_title("Log distribution datapoints", fontsize="8")
        ax[1].set_xlabel("N")
        ax[1].set_ylabel("Value")
        # get histogram values
        y, x = np.histogram(data(), nbins)
        # calculate the centers of the bins
        x = (x[:-1] + x[1:]) / 2
        # create plot with histogram shape, mean and median
        ax[2].plot(x, y, color="gray", label="Data (Histogram)")
        ax[2].plot([mean, mean], [0, max(y)], '--', color="deepskyblue", label="Mean")
        ax[2].plot([median, median], [0, max(y)], '-.', color="crimson", label="Median")
        # avoid changing axes if not necessary - help mean change visualization
        if mean < np.max(d):
            ax[2].set_xlim(-1, int(np.max(d)))
        else:
            ax[2].set_xlim(-1, int(mean + mean/2))
        ax[2].legend()
        ax[2].set_title("Log distribution histogram, mean and median", fontsize="8")
        ax[2].set_xlabel("Value")
        ax[2].set_ylabel("Counts")

        plt.subplots_adjust(hspace=0.4)

        return fig

app = App(app_ui, server)