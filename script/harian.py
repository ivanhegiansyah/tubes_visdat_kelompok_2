from bokeh.models import ColumnDataSource, Select
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.models import HoverTool, ColumnDataSource, Panel
from bokeh.models.widgets.tables import NumberFormatter
from bokeh.models.widgets import TableColumn, DataTable

def harian(df):

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
            x_axis_type="datetime",
        )
        hover = HoverTool(
            tooltips=[
                ("Tanggal", "@Date{%F}"),
                ("Kasus Terkonfirmasi", "@NewCases"),
            ],
            formatters={"@Date": "datetime"},
            mode="vline",
        )
        fig.circle(
            "Date",
            "NewCases",
            source=src,
            size=4,
            color="blue",
        )

        fig.line("Date", "NewCases", source=src, color="black")

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
                ("Kasus Sembuh", "@NewRecovered"),
            ],
            formatters={"@Date": "datetime"},
            mode="vline",
        )

        fig.circle(
            "Date",
            "NewRecovered",
            source=src,
            size=4,
            color="green",
        )

        fig.line("Date", "NewRecovered", source=src, color="black")
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
                ("Kasus Meninggal", "@NewDeaths"),
            ],
            formatters={"@Date": "datetime"},
            mode="vline",
        )

        fig.circle(
            "Date",
            "NewDeaths",
            source=src,
            size=4,
            color="red",
        )
        fig.line("Date", "NewDeaths", source=src, color="black")
        fig.add_tools(hover)
        fig = create_style(fig)

        return fig
    
    df_max = df.groupby('Location').max()
    df_min = df.groupby('Location').min()
    df_max['NewCases_min'] = df_min['NewCases']
    df_max['NewRecovered_min'] = df_min['NewRecovered']
    df_max['NewDeaths_min'] = df_min['NewDeaths']

    def top_terkonfirmasi(src):
        columns = [
            TableColumn(field="Location", title="Provinsi"),
            TableColumn(field="NewCases", title="Kasus Baru Tertinggi Harian", formatter=NumberFormatter(text_align='center')),
            TableColumn(field="NewCases_min", title="Kasus Baru Terendah Harian", formatter=NumberFormatter(text_align='center')),
        ]
        top_new = DataTable(source=src, name="Terkonfirmasi Tertinggi (Harian)", columns=columns, width=800, height=380)

        return top_new

    def top_sembuh(src):
        columns = [
            TableColumn(field="Location", title="Provinsi"),
            TableColumn(field="NewRecovered", title="Kasus Sembuh Tertinggi Harian", formatter=NumberFormatter(text_align='center')),
            TableColumn(field="NewRecovered_min", title="Kasus Sembuh Terendah Harian", formatter=NumberFormatter(text_align='center'))
        ]
        top_new = DataTable(source=src, name="Terkonfirmasi Tertinggi (Harian)", columns=columns, width=800, height=380)

        return top_new

    def top_meninggal(src):
        columns = [
            TableColumn(field="Location", title="Provinsi"),
            TableColumn(field="NewDeaths", title="Kasus Meninggal Tertinggi Harian", formatter=NumberFormatter(text_align='center')),
            TableColumn(field="NewDeaths_min", title="Kasus Meninggal Terendah Harian", formatter=NumberFormatter(text_align='center'))
        ]
        top_new = DataTable(source=src, name="Terkonfirmasi Tertinggi (Harian)", columns=columns, width=800, height=380)

        return top_new
    
    def update(attr, old, new):
        location = menu.value
        df1 = df[df["Location"] == location]
        new_src = create_dataset(df1)
        src.data.update(new_src.data)
        return location

    option = list(df["Location"].value_counts().index)
    option.sort()

    menu = Select(options=option, value="Aceh", title="Location")

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
    
    tab = Panel(child=layout, title="Kasus Harian")

    return tab
