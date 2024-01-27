import streamlit as st
from func import read_data_string, first_fit, plot_data_bars
import matplotlib.pyplot as plt
import io
from datetime import datetime

st.title('Cut List Generator')
tab1, tab2 = st.tabs(["Settings", "Cutting List"])


def entryButtonCall():
    data = f"""Material Length = {materialSize}
Material Price = {materialPrice}
{materialLengths}"""

    data_first_fit = first_fit(read_data_string(data))

    lst = []
    for item in data_first_fit:
        lst.append(item.data)
    for itr, item in enumerate(data_first_fit):
        lst[itr].append(item.waste())

    fig = plot_data_bars(lst, materialPrice)
    tab2.pyplot(fig)

    fn = f'{datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p")}.png'
    img = io.BytesIO()
    plt.savefig(img, format='png')

    btn = tab2.download_button(
        label="Download image",
        data=img,
        file_name=fn,
        mime="image/png"
    )


defaultText = """2 x 2"""

materialSize = tab1.text_input("Material Size (m)", value=3)
materialPrice = tab1.text_input("Material Price (per/length)", value=9.99)
materialLengths = tab1.text_area("Lengths", value=defaultText)
entryButton = tab1.button(label="Calculate", on_click=entryButtonCall)
