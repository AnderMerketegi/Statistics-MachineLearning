from shiny import App, reactive, render, ui
import matplotlib.pyplot as plt
import numpy as np

app_ui = ui.page_fluid(
    ui.panel_title("Measuring Sensibility of Central Tendency Measures to Outliers"),
    ui.layout_sidebar(

        ui.panel_sidebar(
            ui.input_slider("n", "Sample size", 0, 10000, 1000, step=50),
            ui.input_slider("n_bins", "Number of bins", 0, 100, 40, step=10),
            ui.output_text_verbatim("measure_tendencies"),
            ui.input_checkbox("outliers", "Add outliers to distribution", False),
            ui.panel_conditional(
                "input.outliers",
                ui.input_slider("offset_outliers", "Select offset for outliers", 0, 50, 0, step=5)
            ),
            ui.panel_conditional(
                "input.outliers",
                ui.input_slider("n_outliers", "Select number of outlier values", 0, 10, 0, step=1)
            )
        ),

        ui.panel_main(
            ui.output_plot("plot", width = "70%", height = "800px")
        ),
    ),
)


def server(input, output, session):

    data = reactive.Value()
    original_data = reactive.Value()

    @reactive.Effect
    @reactive.event(input.n)
    def _():
        if input.n() == 0:
            distribution = np.exp(np.random.randn(1))
        else:
            distribution = np.exp(np.random.randn(input.n()))
        data.set(distribution)
        original_data.set(distribution)


    @reactive.Effect
    @reactive.event(input.n_outliers, input.offset_outliers, input.n)
    def _():
        d = original_data.get()
        if input.n_outliers() != 0 and input.offset_outliers() != 0:
            d = np.hstack((d, np.mean(d) * np.random.randn(input.n_outliers()) + input.offset_outliers() * np.std(d)))
        np.random.shuffle(d)
        data.set(d)


    @output
    @render.text
    def measure_tendencies():
        return f"Mean value: {round(np.mean(data()), 4)}\tMedian value: {round(np.median(data()), 4)}"

    @output
    @render.plot(alt="A histogram")
    def plot() -> object:

        # avoid 0 bins error
        if input.n_bins() == 0:
            nbins = 1
        else:
            nbins = input.n_bins()

        mean = np.mean(data())
        median = np.median(data())
        d = original_data.get()

        fig, ax = plt.subplots(3, 1)
        ax[0].hist(data(), bins=nbins)

        ax[1].plot(data(), '.', color="lightgray", label="Data")
        ax[1].plot([0, len(data.get())], [mean, mean], '--', color="deepskyblue", label="Mean")
        ax[1].plot([0, len(data.get())], [median, median], '-.', color="crimson", label="Median")
        ax[1].legend()

        y, x = np.histogram(data(), nbins)
        # calculate the centers of the bins
        x = (x[:-1] + x[1:]) / 2

        ax[2].plot(x, y, color="gray", label="Data (Histogram)")
        ax[2].plot([mean, mean], [0, max(y)], '--', color="deepskyblue", label="Mean")
        ax[2].plot([median, median], [0, max(y)], '-.', color="crimson", label="Median")
        if mean < np.max(d):
            ax[2].set_xlim(-1, int(np.max(d)))
        else:
            ax[2].set_xlim(-1, int(mean + mean/2))
        ax[2].legend()

        return fig

app = App(app_ui, server)