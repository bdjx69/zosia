import time

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import io
from PIL import Image

NAME = "Zosia"  

PINK = "#ff5c8d"
BG = "#1d0c16"
GRID = "#4a2335"

st.set_page_config(page_title="Wszystkiego Najlepszego Misiaczku", page_icon="❤️")

def heart(t):
    x = 16 * np.sin(t) ** 3
    y = 13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t)
    return x, y


def bouncy(x, k):
    return np.cbrt(x**2) + 0.9 * np.sin(k * x) * np.sqrt(3 - x**2)

def new_axes(xlim, ylim):
    fig, ax = plt.subplots(figsize=(7, 5.5))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.grid(True, color=GRID, lw=0.8)
    ax.axhline(0, color="#a0607a", lw=1)
    ax.axvline(0, color="#a0607a", lw=1)
    ax.tick_params(colors="#c99bad")
    for side in ax.spines.values():
        side.set_visible(False)
    return fig, ax


def show(plot, fig):
    plot.pyplot(fig)
    plt.close(fig)

def fig_to_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=80, facecolor=BG)
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf).convert("RGB")


def to_gif(frames, ms=40):
    buf = io.BytesIO()
    frames[0].save(buf, format="GIF", save_all=True, append_images=frames[1:], duration=ms)
    return buf.getvalue()

@st.cache_data
def heart_gif():
    x, y = heart(np.linspace(0, 2 * np.pi, 600))
    frames = []
    for n in range(10, 601, 15):
        fig, ax = new_axes((-20, 20), (-19, 15))
        ax.plot(x[:n], y[:n], color=PINK, lw=3)
        ax.plot(x[n - 1], y[n - 1], "o", color=PINK, ms=10)
        frames.append(fig_to_image(fig))
    fig, ax = new_axes((-20, 20), (-19, 15))
    ax.fill(x, y, color=PINK, alpha=0.2)
    ax.plot(x, y, color=PINK, lw=3)
    frames.append(fig_to_image(fig))
    return to_gif(frames)


def page_heart():
    st.header("Urodzinowa funkcja")     
    st.latex(r"x(t)=16\sin^3 t,\quad y(t)=13\cos t-5\cos 2t-2\cos 3t-\cos 4t")
    st.write("Każdy punkt na niej jest dokładnie w miejscu na którym powinien być, troche jak ty w moich objęciach") 
    left, middle, right = st.columns([1, 4, 1])
    middle.image(heart_gif())


def page_bouncy():
    st.header("Funkcja która rozwija się z czasem")
    st.latex(r"f(x)=x^{2/3}+0.9\,\sin(kx)\,\sqrt{3-x^2}")
    st.write("Dla k = 0 jest ptaszkiem. Przewiń do przodu i zobaczysz jak się rozwinie (troche jak nasza miłość)")   # your text

    x = np.linspace(-np.sqrt(3), np.sqrt(3), 1500)
    ks = np.arange(0, 101)          # k = 0, 1, 2, ..., 100

    # one ready-made curve ("frame") for every k
    fig = go.Figure(
        data=[go.Scatter(x=x, y=bouncy(x, 0), mode="lines", line=dict(color=PINK, width=2))],
        frames=[go.Frame(data=[go.Scatter(x=x, y=bouncy(x, k))], name=str(k)) for k in ks],
    )

    instant = {"mode": "immediate", "frame": {"duration": 0, "redraw": False},
               "transition": {"duration": 0}}

    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG, font_color="#ffe8ef", height=600,
        showlegend=False, margin=dict(t=60),
        xaxis=dict(range=[-2.3, 2.3], gridcolor=GRID, zerolinecolor="#a0607a"),
        yaxis=dict(range=[-1.5, 2.6], gridcolor=GRID, zerolinecolor="#a0607a"),
        sliders=[dict(
            steps=[dict(label=str(k), method="animate", args=[[str(k)], instant]) for k in ks],
            currentvalue=dict(prefix="k = ", font=dict(size=18, color="#ffe8ef")),
            font=dict(size=1, color=BG),          # hides the 101 tiny tick labels
            bgcolor=GRID, activebgcolor=PINK, bordercolor=PINK,
        )],
        updatemenus=[dict(
            type="buttons", x=0, y=1.12, xanchor="left", showactive=False,
            buttons=[dict(label="▶ Play", method="animate",
                          args=[None, {"frame": {"duration": 40, "redraw": False},
                                       "transition": {"duration": 0}, "fromcurrent": True}])],
        )],
    )

    st.plotly_chart(fig, config={"displayModeBar": False})

@st.cache_data
def message_gif():
    ix = np.concatenate([np.linspace(-8, -6, 50), np.full(100, -7.0), np.linspace(-8, -6, 50)])
    iy = np.concatenate([np.full(50, 3.0), np.linspace(3, -3, 100), np.full(50, -3.0)])
    hx, hy = heart(np.linspace(0, 2 * np.pi, 400))
    hx, hy = 0.18 * hx, 0.18 * hy + 0.3
    ux = np.linspace(7 - np.sqrt(6), 7 + np.sqrt(6), 200)
    uy = (ux - 7) ** 2 - 3

    pieces = [(ix, iy), (hx, hy), (ux, uy)]
    frames = []
    for i, (px, py) in enumerate(pieces):
        for n in np.linspace(2, len(px), 15).astype(int):
            fig, ax = new_axes((-10.5, 10.5), (-5, 5))
            for qx, qy in pieces[:i]:
                ax.plot(qx, qy, color=PINK, lw=3)
            ax.plot(px[:n], py[:n], color=PINK, lw=3)
            frames.append(fig_to_image(fig))
    return to_gif(frames, ms=50)


def page_message():
    st.header("Ej zosia wiesz co...")
    st.latex(r"\mathrm{I}:\ x=-7,\ |y|\le 3")
    st.latex(r"\heartsuit:\ (x,y)=\left(0.18\,x(t),\ 0.18\,y(t)+0.3\right)")
    st.latex(r"\mathrm{U}:\ y=(x-7)^2-3,\ |y|\le 3")
    left, middle, right = st.columns([1, 4, 1])
    middle.image(message_gif())
    st.markdown("## I ❤️ U")

def page_final():
    st.header("Dowód (tort) urodzinowy")
    st.latex(r"\lim_{t\to\infty}\ \mathrm{love}(t)=\infty")

    x, y = heart(np.linspace(0, 2 * np.pi, 600))
    fig, ax = new_axes((-20, 20), (-19, 15))
    ax.fill(x, y, color=PINK, alpha=0.25)
    ax.plot(x, y, color=PINK, lw=3)
    ax.text(0, -1, NAME, ha="center", va="center", color="#ffe8ef", fontsize=26)
    st.pyplot(fig)
    plt.close(fig)

    st.write(f"Wszystkiego najlepszego, {NAME}. Kolejny rok twojego życia a ja nadal"
             "mam zaszczyt cie ragebaitowac, troche jak pochodna i")
    st.latex(r"\exp(x)")
    st.write(f"QED.")
    st.balloons()

pages = [page_heart, page_bouncy, page_message, page_final]

if "page" not in st.session_state:
    st.session_state.page = 0


def move(step):
    st.session_state.page += step


st.title(f"Nareszcie dorosła :D {NAME} ❤️")
left, middle, right = st.columns([1, 4, 1])
left.button("← Tył", on_click=move, args=(-1,), disabled=st.session_state.page == 0)
right.button("Przód →", on_click=move, args=(1,), disabled=st.session_state.page == len(pages) - 1)

pages[st.session_state.page]()