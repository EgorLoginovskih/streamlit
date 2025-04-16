import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import numpy as np

# Инициализация состояний сессии
if "df" not in st.session_state:
    st.session_state.df = None
if "dates_added" not in st.session_state:
    st.session_state.dates_added = False
if "analysis_total_tip" not in st.session_state:
    st.session_state.analysis_total_tip = False
if "sum_on_week" not in st.session_state:
    st.session_state.sum_on_week = False
if "graph1" not in st.session_state:
    st.session_state.graph1 = None
if "graph2" not in st.session_state:
    st.session_state.graph2 = None
if "graph3" not in st.session_state:
    st.session_state.graph3 = None


st.title("Работа с csv")

# Загрузка файла через сайдбар
with st.sidebar:
    st.write("Загрузите csv файл")
    fl = st.file_uploader("Раздел для загрузки файла", type="csv")
    
    if fl and st.session_state.df is None:
        st.session_state.df = pd.read_csv(fl)
        st.session_state.dates_added = False
        st.session_state.analysis_done = False
        st.rerun()


if st.session_state.df is None:
    st.info("Пожалуйста, загрузите CSV файл")
    st.stop()


st.write("Первые 5 строк данных:")
st.write(st.session_state.df.head())


if not st.session_state.dates_added:
    st.write("хмм...💬 Чего-то не хватает. Давай заполним новый столбец с датами")
    if st.button("Заполнить"):
        date = pd.date_range(start="2023-01-01", end="2023-01-31", freq="D")
        rr_d = np.random.choice(date, size=len(st.session_state.df), replace=True)
        st.session_state.df["date_time"] = pd.to_datetime(rr_d).date
        st.session_state.dates_added = True
        st.success("Столбец успешно добавлен!")
        st.rerun()
    st.stop()


if st.session_state.dates_added and not st.session_state.graph1:
    st.subheader("Проведем анализ чаевых по дате")
    
    tb = st.session_state.df.groupby("date_time", as_index=False)['tip'].sum()
        
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(data=tb, x="tip", y="date_time", hue="date_time", palette="viridis", ax=ax)
    ax.set_xlabel("Сумма чаевых")
    ax.set_ylabel("Дата")
    ax.set_title("Анализ чаевых по дате")
    plt.legend(loc="upper right",ncol=1,fontsize="x-small",bbox_to_anchor=(1.2,1))
    plt.xticks(rotation=45)
    plt.tight_layout()
        
    save = BytesIO()
    fig.savefig(save, format="png")
    save.seek(0)
    st.session_state.graph1 = save
        
    st.pyplot(fig)

if st.session_state.graph1:
    st.download_button(
        "Скачать график чаевых по дате",
        data=st.session_state.graph1,
        file_name="date_tip.png",
        mime="image/png"
    )



if st.session_state.dates_added and not st.session_state.analysis_total_tip:
    st.subheader("Интересно. А сумма счета как-то связана с кол-вом чаевых?")
    if st.button('Проверить'):
        ttlbl_and_tip = st.session_state.df.groupby("date_time", as_index=False)[["total_bill","tip"]].sum()
        ttlbl_and_tip = ttlbl_and_tip.round({"total_bill":2, "tip":2})

        fig1, ax1 = plt.subplots(figsize=(10, 6))
        sns.scatterplot(data=ttlbl_and_tip, x="total_bill", y="tip", hue="tip", palette="viridis", ax=ax1)
        ax1.set_xlabel("Сумма счета")
        ax1.set_ylabel("Чаевые")
        ax1.set_title("Взаимосвязь суммы счета и чаевых")# Кнопка скачивания второго графика
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        save1 = BytesIO()
        fig1.savefig(save1, format="png")
        save1.seek(0)
        st.session_state.graph2 = save1
        st.session_state.analysis_total_tip = True
            
        st.pyplot(fig1)


if st.session_state.graph2:
    st.download_button("Скачать график связи счета и чаевых", st.session_state.graph2,file_name="date1_tip.png",
        mime="image/png")
    st.write("Видно, что от суммы счета зависит колиечство оставленных чаевых")
    

if st.session_state.analysis_total_tip and not st.session_state.sum_on_week:
    st.header("Теперь давайте проверим сумму чеков на каждый из дней недели")
    if st.button('Результат'):
        df_week = st.session_state.df.copy()
        df_week['date_time'] = pd.to_datetime(df_week['date_time']) 
            
        days_translation = {'Monday': 'Понедельник','Tuesday': 'Вторник','Wednesday': 'Среда','Thursday': 'Четверг','Friday': 'Пятница',
                            'Saturday': 'Суббота','Sunday': 'Воскресенье'}
            
        df_week['day_of_week'] = df_week['date_time'].dt.day_name().map(days_translation)
        weekly_bills = df_week.groupby('day_of_week', as_index=True)['total_bill'].sum()
            
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        weekly_bills.plot(kind='bar', color="blue", ax=ax2)
            
        ax2.set_title("Сумма счетов по дням недели", fontsize=16)
        ax2.set_xlabel("День недели")
        ax2.set_ylabel("Сумма за день")
        plt.xticks(rotation=45)
        plt.tight_layout()

        save2 = BytesIO()
        fig2.savefig(save2, format="png", bbox_inches='tight', dpi=150)
        save2.seek(0)
        
        st.session_state.graph2 = save2
        st.session_state.sum_on_week = True
        st.pyplot(fig2)
        
        st.download_button("Скачать график по дням недели",data=save2,file_name="weekly_sum.png",mime="image/png")
