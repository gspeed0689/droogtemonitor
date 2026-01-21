import streamlit as st
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
# import scipy.fft as fft
from datetime import datetime, timedelta

# st.code(np.std([2, 4, 4, 4, 5,5,7,9]))

st.set_page_config(layout="wide", page_icon="🌦️")

st.title("Interactief Droogte Monitor")

yearly_data_path = "./data/int_nl.dat"
# data_2025_path = "interactief-droogtemonitor/data/rdev_tijdreeks.txt"

yearly_df = pd.read_csv(yearly_data_path, 
                        skiprows=11, 
                        sep="\t", 
                        names=["date", "mm_deficit"],
                        usecols=[0,1])
# d2025_df = pd.read_csv(data_2025_path)

yearly_df["datetime"] = [datetime.strptime(str(x), "%Y%m%d").date() for x in yearly_df["date"]]
yearly_df["year"] = [datetime.strftime(x, "%Y") for x in yearly_df["datetime"]]
yearly_df["doy"] = [datetime.strftime(x, "%d-%m") for x in yearly_df["datetime"]]
# ffftrange = np.arange(256)
# ffft = fft.fft(yearly_df["mm_deficit"])
# fffts = fft.fftshift(ffft)
# ffftfreq = fft.fftfreq(ffftrange.shape[-1])
# st.code(ffftfreq)
# st.code(fffts.real)

# fft_plot = go.Figure()
# fft_plot.add_trace(go.Scatter(x=ffftrange,
#                               y=fffts.real))
# st.plotly_chart(fft_plot)

unique_doy = list(yearly_df["doy"].unique())

def decadel(decade_0, decade_1, df):
    d0 = int(decade_0)
    d1 = int(decade_1)
    years = [str(x) for x in range(d0, d1+1)]
    mm_deficit_decade_doy = []
    for year in years:
        tdf = df[df["year"]==year]
        mm_deficit_decade_doy.append(tdf["mm_deficit"])
    mm_deficit_decade_doy = np.array(mm_deficit_decade_doy)
    dec_max = mm_deficit_decade_doy.max()
    dec_min = mm_deficit_decade_doy.min()
    dec_med = np.median(mm_deficit_decade_doy)
    dec_95 = np.percentile(mm_deficit_decade_doy, 95)
    dec_5 = np.percentile(mm_deficit_decade_doy, 5)
    dec_mean = np.std(mm_deficit_decade_doy)
    dec_std = np.std(mm_deficit_decade_doy, mean=dec_mean)
    
    # st.code(dec_std)
    return (round(float(dec_max), 3), 
            round(float(dec_min),  3), 
            round(float(dec_med), 3), 
            round(float(dec_95), 3), 
            round(float(dec_5), 3),
            round(float(dec_std), 3),
            round(float(dec_mean), 3),)

decdf = pd.DataFrame(columns=["doy", 
                              "decade",
                              "min", 
                              "max",
                              "5%",
                              "95%",
                              "median",
                              "stddev",
                              "mean",
                              ])
decdict = {}
for day in unique_doy:
    temp_df = yearly_df[yearly_df["doy"]==day]
    # temp_stats = np.percentile(temp_df["mm_deficit"], 95)
    # st.code(temp_stats)
    yearly_df.loc[max(yearly_df.index) + 1] = {"date": "max",
                                               "mm_deficit": temp_df["mm_deficit"].max(),
                                               "doy": day,
                                               "year": "max"}
    yearly_df.loc[max(yearly_df.index) + 1] = {"date": "5%",
                                               "mm_deficit": np.percentile(temp_df["mm_deficit"], 95),
                                               "doy": day,
                                               "year": "5%"}
    yearly_df.loc[max(yearly_df.index) + 1] = {"date": "median",
                                               "mm_deficit": np.median(temp_df["mm_deficit"]),
                                               "doy": day,
                                               "year": "median"}
    # yearly_df.loc[max(yearly_df.index) + 1] = {"date": "mean",
    #                                            "mm_deficit": np.mean(temp_df["mm_deficit"]),
    #                                            "doy": day,
    #                                            "year": "mean"}
    
    for dstart in range(1906, 2017, 10):
        dmax, dmin, dmed, d95, d5, dstd, dmean = decadel(dstart, dstart+9, temp_df)
        try:
            decdf.loc[max(decdf.index) + 1] = (day, dstart, dmin, dmax, d5, d95, dmed, dstd, dmean)
        except ValueError:
            decdf.loc[0] = (day, dstart, dmin, dmax, d5, d95, dmed, dstd, dmean)

decdf["σ+1"] = decdf["mean"] + decdf["stddev"]/2
decdf["σ-1"] = decdf["mean"] - decdf["stddev"]/2
decdf["σ+2"] = decdf["mean"] + decdf["stddev"]
decdf["σ-2"] = decdf["mean"] - decdf["stddev"]
decdf[["σ-1", "σ-2"]] = decdf[["σ-1", "σ-2"]].clip(lower=0)
# st.dataframe(yearly_df)

# yearly_plot = px.line(
#                     #   yearly_df[yearly_df["year"]=="2025"], 
#                       yearly_df,
#                       x="doy", 
#                       y="mm_deficit",
#                       color="year", 
#                       height=800,)

yearly_plot = go.Figure()
y2025 = yearly_df[yearly_df["year"]=="2025"]
yearly_plot.add_trace(go.Scatter(x=unique_doy,
                                 y=y2025["mm_deficit"],
                                 line=dict(color="white", width=5),
                                 name="2025"))
y2018 = yearly_df[yearly_df["year"]=="2018"]
yearly_plot.add_trace(go.Scatter(x=unique_doy,
                                 y=y2018["mm_deficit"],
                                 line=dict(color="gray", width=3),
                                 name="2018"))
y1976 = yearly_df[yearly_df["year"]=="1976"]
yearly_plot.add_trace(go.Scatter(x=unique_doy,
                                 y=y1976["mm_deficit"],
                                 line=dict(color="red", width=3),
                                 name="1976 Record Yard"))
ymax = yearly_df[yearly_df["year"]=="max"]
yearly_plot.add_trace(go.Scatter(x=unique_doy,
                                 y=ymax["mm_deficit"],
                                 line=dict(color="orange", width=3, dash="dash"),
                                 name="Maximum"))
y5pct = yearly_df[yearly_df["year"]=="5%"]
yearly_plot.add_trace(go.Scatter(x=unique_doy,
                                 y=y5pct["mm_deficit"],
                                 line=dict(color="limegreen", width=3, dash="dash"),
                                 name="5% Droogste Jaren"))
ymedian = yearly_df[yearly_df["year"]=="median"]
yearly_plot.add_trace(go.Scatter(x=unique_doy,
                                 y=ymedian["mm_deficit"],
                                 line=dict(color="blue", width=3, dash="dash"),
                                 name="Mediaan"))
# ymean = yearly_df[yearly_df["year"]=="mean"]
# yearly_plot.add_trace(go.Scatter(x=unique_doy,
#                                  y=ymedian["mm_deficit"],
#                                  line=dict(color="darkblue", width=3, dash="dash"),
#                                  name="Mean"))

yearly_plot.update_layout(xaxis={"type":"category", 
                                 "title":"Dag v/d Jaar (1 April t/m 30 September)"},
                          yaxis={"title": "Neerslagtekort (mm)"},
                          height=800,
                          title="Neerslagtekort Nederland 2025",
                        #   subtitle="Landelijk gemiddelde over 13 stations",
                          )

# yearly_plot.add_scatter(x=yearly_df["doy"],
#                         y=yearly_df[yearly_df["year"]=="1976"],
#                         mode="lines")

st.plotly_chart(yearly_plot)

# yearly_box = px.box(yearly_df, 
#                     x="doy", 
#                     y="mm_deficit",
#                     height=800)
# yearly_box.update_layout(xaxis={"type":"category"})
# st.plotly_chart(yearly_box)

# decdf = pd.DataFrame(decdict)
# st.dataframe(decdf)

decadel_plot = go.Figure()

dec1906df = decdf[decdf["decade"]==1906]
decadel_plot.add_trace(go.Scatter(x=unique_doy,
                                  y=dec1906df["mean"],
                                  name="Mean 1906-1915"))
# decadel_plot.add_trace(go.Scatter(x=unique_doy+unique_doy[::-1],
#                                   y=list(dec1906df["max"])+list(dec1906df["min"])[::-1],
#                                   fill="toself",
#                                   name="1906-1915"))

dec1916df = decdf[decdf["decade"]==1916]
decadel_plot.add_trace(go.Scatter(x=unique_doy,
                                  y=dec1916df["mean"],
                                  name="Mean 1916-1925"))
# decadel_plot.add_trace(go.Scatter(x=unique_doy+unique_doy[::-1],
#                                   y=list(dec1916df["max"])+list(dec1916df["min"])[::-1],
#                                   fill="toself",
#                                   name="1916-1925"))

dec1926df = decdf[decdf["decade"]==1926]
decadel_plot.add_trace(go.Scatter(x=unique_doy,
                                  y=dec1926df["mean"],
                                  name="Mean 1926-1935"))
# decadel_plot.add_trace(go.Scatter(x=unique_doy+unique_doy[::-1],
#                                   y=list(dec1926df["max"])+list(dec1926df["min"])[::-1],
#                                   fill="toself",
#                                   name="1926-1935"))

dec1936df = decdf[decdf["decade"]==1936]
decadel_plot.add_trace(go.Scatter(x=unique_doy,
                                  y=dec1936df["mean"],
                                  name="Mean 1936-1945"))
# decadel_plot.add_trace(go.Scatter(x=unique_doy+unique_doy[::-1],
#                                   y=list(dec1936df["max"])+list(dec1936df["min"])[::-1],
#                                   fill="toself",
#                                   name="1936-1945"))

dec1946df = decdf[decdf["decade"]==1946]
decadel_plot.add_trace(go.Scatter(x=unique_doy,
                                  y=dec1946df["mean"],
                                  name="Mean 1946-1955"))
# decadel_plot.add_trace(go.Scatter(x=unique_doy+unique_doy[::-1],
#                                   y=list(dec1946df["max"])+list(dec1946df["min"])[::-1],
#                                   fill="toself",
#                                   name="1946-1955"))

dec1956df = decdf[decdf["decade"]==1956]
decadel_plot.add_trace(go.Scatter(x=unique_doy,
                                  y=dec1956df["mean"],
                                  name="Mean 1956-1965"))
# decadel_plot.add_trace(go.Scatter(x=unique_doy+unique_doy[::-1],
#                                   y=list(dec1956df["max"])+list(dec1956df["min"])[::-1],
#                                   fill="toself",
#                                   name="1956-1965"))

dec1966df = decdf[decdf["decade"]==1966]
# decadel_plot.add_trace(go.Scatter(x=unique_doy+unique_doy[::-1],
#                                   y=list(dec1966df["max"])+list(dec1966df["min"])[::-1],
#                                   fill="toself",
#                                   name="1966-1975"))
decadel_plot.add_trace(go.Scatter(x=unique_doy,
                                  y=dec1966df["mean"],
                                  name="Mean 1966-1975"))

dec1976df = decdf[decdf["decade"] == 1976]
# decadel_plot.add_trace(go.Scatter(x=unique_doy+unique_doy[::-1],
#                                   y=list(dec1976df["max"])+list(dec1976df["min"])[::-1],
#                                   fill="toself", 
#                                   name="1976-1985"))
# decadel_plot.add_trace(go.Scatter(x=unique_doy+unique_doy[::-1],
#                                   y=list(dec1976df["σ+1"])+list(dec1976df["σ-1"])[::-1],
#                                   fill="toself",
#                                   name="1976-1985 +/- 1σ"))
decadel_plot.add_trace(go.Scatter(x=unique_doy,
                                  y=dec1976df["mean"],
                                  name="Mean 1976-1985"))
# decadel_plot.add_trace(go.Scatter(x=unique_doy,
#                                   y=dec1976df["max"]))
# decadel_plot.add_trace(go.Scatter(x=unique_doy,
#                                   y=dec1976df["min"]))

dec1986df = decdf[decdf["decade"] == 1986]
decadel_plot.add_trace(go.Scatter(x=unique_doy,
                                  y=dec1986df["mean"],
                                  name="Mean 1986-1995"))
# decadel_plot.add_trace(go.Scatter(x=unique_doy+unique_doy[::-1],
#                                   y=list(dec1986df["max"])+list(dec1986df["min"])[::-1],
#                                   fill="toself", 
#                                   name="1986-1995"))

dec1996df = decdf[decdf["decade"]==1996]
decadel_plot.add_trace(go.Scatter(x=unique_doy,
                                  y=dec1996df["mean"],
                                  name="Mean 1996-2005"))
# decadel_plot.add_trace(go.Scatter(x=unique_doy+unique_doy[::-1],
#                                   y=list(dec1996df["max"])+list(dec1996df["min"])[::-1],
#                                   fill="toself",
#                                   name="1996-2005"))

dec2006df = decdf[decdf["decade"] == 2006]
decadel_plot.add_trace(go.Scatter(x=unique_doy,
                                  y=dec2006df["mean"],
                                  name="Mean 2006-2015"))
# decadel_plot.add_trace(go.Scatter(x=unique_doy+unique_doy[::-1],
#                                   y=list(dec2006df["max"])+list(dec2006df["min"])[::-1],
#                                   fill="toself", 
#                                   name="2006-2015"))

dec2016df = decdf[decdf["decade"] == 2016]
decadel_plot.add_trace(go.Scatter(x=unique_doy,
                                  y=dec2016df["mean"],
                                  name="Mean 2016-2025"))
# decadel_plot.add_trace(go.Scatter(x=unique_doy+unique_doy[::-1],
#                                   y=list(dec2016df["max"])+list(dec2016df["min"])[::-1],
#                                   fill="toself", 
#                                   name="2016-2025"))

# for dstart in range(1906, 2017, 10):
#     temp_df = decdf[decdf["decade"] == dstart]
#     decadel_plot.add_trace(go.Scatter(x=unique_doy+unique_doy[::-1],
#                                       y=decdf["min"]+decdf["max"][::-1],
#                                       fill="toself"))

decadel_plot.update_layout(xaxis={"type":"category", 
                                 "title":"Dag v/d Jaar (1 April t/m 30 September)"},
                                 yaxis={"title": "Neerslagtekort (mm)"},
                                 height=800,
                                 title="Gemiddelde Neerslagtekort bij Decade Nederland 1906-2025",)
st.plotly_chart(decadel_plot)

# st.dataframe(decdf)

# st.code(yearly_df["year"].unique())

