
import streamlit as st
import random
from functools import lru_cache

# =====================================
# CONFIGURACIÓN
# =====================================

st.set_page_config(
    page_title="Tres en Raya",
    page_icon="🎮",
    layout="centered"
)

LINEAS = [
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6)
]

# =====================================
# FUNCIONES DEL JUEGO
# =====================================

def comprobar_ganador(tablero):

    for a, b, c in LINEAS:
        if (
            tablero[a] != ""
            and tablero[a] == tablero[b]
            and tablero[b] == tablero[c]
        ):
            return tablero[a]

    if all(casilla != "" for casilla in tablero):
        return "Empate"

    return None


def movimientos_disponibles(tablero):
    return [
        i for i, casilla in enumerate(tablero)
        if casilla == ""
    ]


def nueva_partida():

    st.session_state.tablero = [""] * 9
    st.session_state.turno = "X"
    st.session_state.resultado = None


def reiniciar_todo():

    nueva_partida()

    st.session_state.puntos = {
        "X": 0,
        "O": 0,
        "Empate": 0
    }


def registrar_resultado():

    resultado = comprobar_ganador(
        st.session_state.tablero
    )

    if resultado is not None:

        st.session_state.resultado = resultado
        st.session_state.puntos[resultado] += 1


# =====================================
# INTELIGENCIA ARTIFICIAL
# =====================================

def ia_facil(tablero):

    # Juega completamente al azar

    return random.choice(
        movimientos_disponibles(tablero)
    )


def ia_media(tablero):

    disponibles = movimientos_disponibles(tablero)

    # Primero intenta ganar
    for i in disponibles:

        copia = tablero.copy()
        copia[i] = "O"

        if comprobar_ganador(copia) == "O":
            return i

    # Después intenta bloquear al jugador
    for i in disponibles:

        copia = tablero.copy()
        copia[i] = "X"

        if comprobar_ganador(copia) == "X":
            return i

    # Si no hay amenaza, juega al azar
    return random.choice(disponibles)


@lru_cache(maxsize=None)
def minimax(estado, turno):

    tablero = list(estado)
    resultado = comprobar_ganador(tablero)

    jugadas = 9 - tablero.count("")

    if resultado == "O":
        return 10 - jugadas

    if resultado == "X":
        return jugadas - 10

    if resultado == "Empate":
        return 0

    puntuaciones = []

    for i in movimientos_disponibles(tablero):

        copia = tablero.copy()
        copia[i] = turno

        siguiente = "X" if turno == "O" else "O"

        valor = minimax(
            tuple(copia),
            siguiente
        )

        puntuaciones.append(valor)

    if turno == "O":
        return max(puntuaciones)

    return min(puntuaciones)


def ia_dificil(tablero):

    # Minimax: busca la mejor jugada posible

    orden = [4, 0, 2, 6, 8, 1, 3, 5, 7]

    mejor_jugada = None
    mejor_valor = float("-inf")

    for i in orden:

        if tablero[i] != "":
            continue

        copia = tablero.copy()
        copia[i] = "O"

        valor = minimax(
            tuple(copia),
            "X"
        )

        if valor > mejor_valor:

            mejor_valor = valor
            mejor_jugada = i

    return mejor_jugada


def movimiento_ia(dificultad):

    tablero = st.session_state.tablero

    if dificultad == "Fácil":
        posicion = ia_facil(tablero)

    elif dificultad == "Media":
        posicion = ia_media(tablero)

    else:
        posicion = ia_dificil(tablero)

    tablero[posicion] = "O"

    registrar_resultado()

    if st.session_state.resultado is None:
        st.session_state.turno = "X"


# =====================================
# REALIZAR JUGADA
# =====================================

def jugar(posicion, modo, dificultad):

    if st.session_state.resultado is not None:
        return

    tablero = st.session_state.tablero

    if tablero[posicion] != "":
        return

    turno = st.session_state.turno

    tablero[posicion] = turno

    registrar_resultado()

    if st.session_state.resultado is not None:
        return

    if modo == "Contra la IA":

        st.session_state.turno = "O"
        movimiento_ia(dificultad)

    else:

        if turno == "X":
            st.session_state.turno = "O"
        else:
            st.session_state.turno = "X"


# =====================================
# INICIALIZACIÓN
# =====================================

if "tablero" not in st.session_state:

    st.session_state.tablero = [""] * 9
    st.session_state.turno = "X"
    st.session_state.resultado = None

    st.session_state.puntos = {
        "X": 0,
        "O": 0,
        "Empate": 0
    }


# =====================================
# DISEÑO VISUAL
# =====================================

st.markdown("""
<style>

.stApp {
    background: linear-gradient(
        135deg,
        #0f172a,
        #1e293b
    );
}

h1, h2, h3 {
    text-align: center;
    color: white !important;
}

div[data-testid="stMetric"] {
    background: #273449;
    padding: 12px;
    border-radius: 12px;
    text-align: center;
    border: 1px solid #475569;
}

div[data-testid="stMetric"] label {
    color: #cbd5e1;
}

div[data-testid="stMetric"] div {
    color: white;
}

div.stButton > button {
    border-radius: 12px;
    font-weight: bold;
}

div.stButton > button[kind="secondary"] {
    background: #e2e8f0;
    color: #0f172a;
    border: 2px solid #64748b;
}

</style>
""", unsafe_allow_html=True)


# =====================================
# TÍTULO PRINCIPAL
# =====================================

st.title("🎮 TRES EN RAYA")

st.markdown(
    "<h3>❌ VS ⭕</h3>",
    unsafe_allow_html=True
)

st.write(
    "Juega con un amigo o desafía "
    "a la inteligencia artificial."
)

st.divider()


# =====================================
# OPCIONES DEL JUEGO
# =====================================

col1, col2 = st.columns(2)

with col1:

    modo = st.selectbox(
        "Modo de juego",
        [
            "Contra la IA",
            "Dos jugadores"
        ]
    )

with col2:

    if modo == "Contra la IA":

        dificultad = st.selectbox(
            "Dificultad",
            [
                "Fácil",
                "Media",
                "Difícil"
            ],
            index=1
        )

    else:

        dificultad = "No aplica"
        st.info("Modo multijugador")


# Reiniciar cuando cambie la configuración

configuracion = (modo, dificultad)

if st.session_state.get("configuracion") != configuracion:

    reiniciar_todo()
    st.session_state.configuracion = configuracion


# =====================================
# MARCADOR
# =====================================

st.subheader("🏆 Marcador")

col1, col2, col3 = st.columns(3)

if modo == "Contra la IA":
    nombre_x = "Tú ❌"
    nombre_o = "IA ⭕"
else:
    nombre_x = "Jugador 1 ❌"
    nombre_o = "Jugador 2 ⭕"

with col1:
    st.metric(
        nombre_x,
        st.session_state.puntos["X"]
    )

with col2:
    st.metric(
        nombre_o,
        st.session_state.puntos["O"]
    )

with col3:
    st.metric(
        "Empates 🤝",
        st.session_state.puntos["Empate"]
    )

st.divider()


# =====================================
# INFORMACIÓN DEL TURNO
# =====================================

resultado = st.session_state.resultado

if resultado is None:

    if st.session_state.turno == "X":

        if modo == "Contra la IA":
            st.info("🎯 Tu turno: ❌")
        else:
            st.info("🎯 Turno del jugador 1: ❌")

    else:
        st.info("🎯 Turno del jugador 2: ⭕")

elif resultado == "Empate":

    st.warning("🤝 ¡EMPATE!")

elif resultado == "X":

    if modo == "Contra la IA":
        st.success("🏆 ¡GANASTE CONTRA LA IA!")
    else:
        st.success("🏆 ¡GANÓ EL JUGADOR 1!")

else:

    if modo == "Contra la IA":
        st.error("🤖 ¡LA IA HA GANADO!")
    else:
        st.success("🏆 ¡GANÓ EL JUGADOR 2!")


# =====================================
# TABLERO DE TRES EN RAYA
# =====================================

st.subheader("Tablero")

for fila in range(3):

    columnas = st.columns(
        [1, 1, 1],
        gap="small"
    )

    for columna in range(3):

        posicion = fila * 3 + columna

        valor = st.session_state.tablero[posicion]

        if valor == "X":
            texto = "❌"
        elif valor == "O":
            texto = "⭕"
        else:
            texto = "➕"

        with columnas[columna]:

            if st.button(
                texto,
                key=f"casilla_{posicion}",
                use_container_width=True,
                disabled=(
                    valor != ""
                    or st.session_state.resultado is not None
                )
            ):

                jugar(
                    posicion,
                    modo,
                    dificultad
                )

                st.rerun()


# =====================================
# BOTONES DE CONTROL
# =====================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🔄 Nueva partida",
        use_container_width=True,
        type="primary"
    ):

        nueva_partida()
        st.rerun()


with col2:

    if st.button(
        "🗑️ Reiniciar marcador",
        use_container_width=True
    ):

        reiniciar_todo()
        st.rerun()


# =====================================
# DESCRIPCIÓN DE DIFICULTADES
# =====================================

if modo == "Contra la IA":

    with st.expander("🤖 ¿Cómo funciona la dificultad?"):

        st.write(
            "🟢 **Fácil:** la computadora "
            "realiza movimientos aleatorios."
        )

        st.write(
            "🟡 **Media:** intenta ganar y "
            "bloquea tus movimientos peligrosos."
        )

        st.write(
            "🔴 **Difícil:** utiliza el algoritmo "
            "Minimax para encontrar las mejores "
            "jugadas. Es imposible ganarle "
            "si juega correctamente."
        )


# =====================================
# PIE DE PÁGINA
# =====================================

st.divider()

st.caption(
    "Tres en Raya | Desarrollado con Python y Streamlit"
)
