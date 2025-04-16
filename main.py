import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf
from io import BytesIO

st.title("Котировка компании Apple")

with st.expander("Выберете цвет для построения графиков в боковой панели",expanded=True):
    color= st.sidebar.color_picker("Pick a color",value="#1663C9",key="main_color")
    but= st.sidebar.button("Я выбрал(-а) цвет")

if not but:
    st.info("Выберете цвет и нажмите на кнопку в боковой панели")
    st.stop()


with st.spinner("Загрузка данных"):
    ticketsymbol='AAPL'
    ticketData= yf.Ticker(ticketsymbol)
    ticketdf=ticketData.history(period="1d",start="2015-4-15",end="2024-4-15")


def create_graph(data, y, title,color):
    fig, ax=plt.subplots(figsize=(14,8))
    ax.plot(data.index,data,color=color)
    ax.set_title(title, fontfamily="sans-serif",fontsize=15)
    ax.set_xlabel("Date",fontsize=11)
    ax.set_ylabel(y,fontsize=11)
    ax.grid(True)
    save= BytesIO()
    fig.savefig(save,format="png")
    save.seek(0)
    plt.close(fig)
    return save


st.write("Closing Price")
st.line_chart(ticketdf.Close,color=color)
close_plot= create_graph(ticketdf.Close, "Цена в $", "Заключительная Цена", color)
st.download_button(label="Скачать график Close Price", data=close_plot,
                file_name="apple_close_price.png",mime="image/png")

st.write("Volume Price")
st.line_chart(ticketdf.Volume,color=color)
volume_plot= create_graph(ticketdf.Volume, "Цена в $", "Объем продаж", color)
st.download_button(label="Скачать график Volume Price", data=volume_plot,
                file_name="apple_volume_price.png",mime="image/png")



# upload_file=st.file_uploader("Загрузка Dataframe", type="csv")

# if upload_file is not None:
#     df=pd.read_csv(upload_file)
#     st.write(df.head(5))
# else:
#     st.stop()

# count_nan=df.isna().sum()
# st.write(count_nan)