from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets.tables import NumberFormatter
from bokeh.models.widgets import TableColumn, DataTable

def kumulatif(df):

    def create_dataset(df):
        return ColumnDataSource(df)

    def create_style(plt):
        plt.title.text_font_size = "18pt"
        plt.title.align = "center"

        plt.xaxis.axis_label_text_font_size = "12pt"
        plt.xaxis.axis_label_text_font_style = "bold"
        plt.yaxis.axis_label_text_font_size = "12pt"
        plt.yaxis.axis_label_text_font_style = "bold"
        plt.xaxis.major_label_text_font_size = "12pt"
        plt.yaxis.major_label_text_font_size = "12pt"

        return plt

    def plot_terkonfirmasi(src):
        fig = figure(
            plot_width=1000,
            plot_height=400,
            title="Kasus Terkonfirmasi",
            x_axis_label="Tanggal",
            y_axis_label="Jumlah",
            x_axis_type="datetime"
        )

        hover = HoverTool(
            tooltips=[
                ("Tanggal", "@Date{%F}"), 
                ("Kasus Terkonfirmasi", "@TotalCases")],
            formatters={"@Date": "datetime"},
            mode="vline",
        )

        fig.circle(
            "Date",
            "TotalCases",
            source=src,
            size=4,
            color="blue",
        )

        fig.line("Date", "TotalCases", source=src, color="black")

        fig.add_tools(hover)

        fig = create_style(fig)

        return fig

    def plot_sembuh(src):
        fig = figure(
            plot_width=1000,
            plot_height=400,
            title="Kasus Sembuh",
            x_axis_label="Tanggal",
            y_axis_label="Jumlah",
            x_axis_type="datetime",
        )
        hover = HoverTool(
            tooltips=[
                ("Tanggal", "@Date{%F}"), 
                ("Kasus Sembuh", "@TotalRecovered")],
            formatters={"@Date": "datetime"},
            mode="vline",
        )

        fig.circle(
            "Date",
            "TotalRecovered",
            source=src,
            size=4,
            color="green",
        )

        fig.line("Date", "TotalRecovered", source=src, color="black")
        fig.add_tools(hover)
        fig = create_style(fig)

        return fig

    def plot_meninggal(src):
        fig = figure(
            plot_width=1000,
            plot_height=400,
            title="Terkonfirmasi Meninggal",
            x_axis_label="Tanggal",
            y_axis_label="Jumlah",
            x_axis_type="datetime",
        )

        hover = HoverTool(
            tooltips=[
                ("Tanggal", "@Date{%F}"), 
                ("Kasus Meninggal", "@TotalDeaths")],
            formatters={"@Date": "datetime"},
            mode="vline",
        )

        fig.circle(
            "Date",
            "TotalDeaths",
            source=src,
            size=4,
            color="red",
        )
        fig.line("Date", "TotalDeaths", source=src, color="gray")
        fig.add_tools(hover)
        fig = create_style(fig)

        return fig

    df_max = df.groupby('Location').max()
    df_min = df.groupby('Location').min()
    df_max['TotalCases_min'] = df_min['TotalCases']
    df_max['TotalRecovered_min'] = df_min['TotalRecovered']
    df_max['TotalDeaths_min'] = df_min['TotalDeaths']

    def top_terkonfirmasi(src):
        columns = [
            TableColumn(field="Location", title="Provinsi"),
            TableColumn(field="TotalCases", title="Kasus Baru Tertinggi Kumulatif", formatter=NumberFormatter(text_align='center')),
            TableColumn(field="TotalCases_min", title="Kasus Baru Terendah Kumulatif", formatter=NumberFormatter(text_align='center')),
        ]
        top_new = DataTable(source=src, name="Terkonfirmasi Tertinggi (Kumulatif)", columns=columns, width=800, height=380)

        return top_new

    def top_sembuh(src):
        columns = [
            TableColumn(field="Location", title="Provinsi"),
            TableColumn(field="TotalRecovered", title="Kasus Sembuh Tertinggi Kumulatif", formatter=NumberFormatter(text_align='center')),
            TableColumn(field="TotalRecovered_min", title="Kasus Sembuh Terendah Kumulatif", formatter=NumberFormatter(text_align='center'))
        ]
        top_new = DataTable(source=src, name="Terkonfirmasi Tertinggi (Kumulatif)", columns=columns, width=800, height=380)

        return top_new

    def top_meninggal(src):
        columns = [
            TableColumn(field="Location", title="Provinsi"),
            TableColumn(field="TotalDeaths", title="Kasus Meninggal Tertinggi Kumulatif", formatter=NumberFormatter(text_align='center')),
            TableColumn(field="TotalDeaths_min", title="Kasus Meninggal Terendah Kumulatif", formatter=NumberFormatter(text_align='center'))
        ]
        top_new = DataTable(source=src, name="Terkonfirmasi Tertinggi (Kumulatif)", columns=columns, width=800, height=380)

        return top_new
    
    def update(attr, old, new):
        location = menu.value
        df1 = df[df["Location"] == location]
        new_src = create_dataset(df1)
        src.data.update(new_src.data)
        return location

    option = list(df["Location"].value_counts().index)
    option.sort()

    menu = Select(options=option, value=option[0], title="Location")

    menu.on_change("value", update)

    controls = column(menu)

    location = menu.value

    df1 = df[df["Location"] == location]
    src = create_dataset(df1)
    src_max = create_dataset(df_max)
    plot_k = plot_terkonfirmasi(src)
    plot_s = plot_sembuh(src)
    plot_m = plot_meninggal(src)
    table_terkonfirmasi = top_terkonfirmasi(src_max)
    table_sembuh = top_sembuh(src_max)
    table_meninggal = top_meninggal(src_max)

    layout1 = row([controls])
    layout2 = row([plot_k, table_terkonfirmasi])
    layout3 = row([plot_s, table_sembuh])
    layout4 = row([plot_m, table_meninggal])
    layout = column(layout1, layout2, layout3, layout4)

    tab = Panel(child=layout, title="Kasus Kumulatif")

    return tab