import streamlit as st
import random
import time

# Configuración de la página
st.set_page_config(
    page_title="El Desafío del Número Secreto",
    page_icon="🎮",
    layout="centered"
)

# Estilos CSS personalizados para mejorar el aspecto dinámico
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        font-weight: bold;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar variables de estado de sesión
if 'secret_number' not in st_session_state:
    st.session_state.secret_number = random.randint(1, 100)
if 'attempts' not in st_session_state:
    st.session_state.attempts = 0
if 'max_attempts' not in st_session_state:
    st.session_state.max_attempts = 7
if 'game_over' not in st_session_state:
    st.session_state.game_over = False
if 'score' not in st_session_state:
    st.session_state.score = 0
if 'start_time' not in st_session_state:
    st.session_state.start_time = time.time()

def reset_game():
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.start_time = time.time()

# Encabezado
st.title("🎮 El Desafío del Número Secreto")
st.caption("¡Demuestra tu intuición y velocidad mental!")

# Menú lateral para ajustes
with st.sidebar:
    st.header("⚙️ Configuración")
    dificultad = st.selectbox("Selecciona la Dificultad:", ["Fácil (1-50, 10 intentos)", "Normal (1-100, 7 intentos)", "Difícil (1-200, 5 intentos)"])
    
    if st.button("🔄 Reiniciar Juego"):
        if "Fácil" in dificultad:
            st.session_state.secret_number = random.randint(1, 50)
            st.session_state.max_attempts = 10
        elif "Normal" in dificultad:
            st.session_state.secret_number = random.randint(1, 100)
            st.session_state.max_attempts = 7
        else:
            st.session_state.secret_number = random.randint(1, 200)
            st.session_state.max_attempts = 5
        st.session_state.attempts = 0
        st.session_state.game_over = False
        st.session_state.start_time = time.time()
        st.rerun()

    st.markdown("---")
    st.metric(label="🏆 Puntuación Acumulada", value=st.session_state.score)

# Panel de Estado del Juego
col1, col2, col3 = st.columns(3)
intentos_restantes = st.session_state.max_attempts - st.session_state.attempts

col1.metric("Intentos Usados", f"{st.session_state.attempts}/{st.session_state.max_attempts}")
col2.metric("Restantes", intentos_restantes)
col3.metric("Rango", "1 - 50" if "Fácil" in dificultad else ("1 - 100" if "Normal" in dificultad else "1 - 200"))

# Barra de progreso de intentos
progreso = st.session_state.attempts / st.session_state.max_attempts
st.progress(min(progreso, 1.0))

# Mecánica del Juego
if not st.session_state.game_over:
    rango_max = 50 if "Fácil" in dificultad else (100 if "Normal" in dificultad else 200)
    guess = st.number_input("Introduce tu número:", min_value=1, max_value=rango_max, step=1, key="input_guess")

    if st.button("🎯 Adivinar"):
        st.session_state.attempts += 1
        
        if guess == st.session_state.secret_number:
            tiempo_total = round(time.time() - st.session_state.start_time, 1)
            puntos_ganados = max(100 - (st.session_state.attempts * 10), 10)
            st.session_state.score += puntos_ganados
            st.session_state.game_over = True
            
            st.balloons()
            st.success(f"🎉 ¡Felicidades! Adivinaste el número **{st.session_state.secret_number}** en {st.session_state.attempts} intentos y {tiempo_total} segundos.")
            st.info(f"➕ Ganaste **{puntos_ganados} puntos**.")
        
        elif st.session_state.attempts >= st.session_state.max_attempts:
            st.session_state.game_over = True
            st.error(f"💥 ¡Juego terminado! Te quedaste sin intentos. El número era **{st.session_state.secret_number}**.")
            st.snow()
        
        else:
            if guess < st.session_state.secret_number:
                st.warning("📈 ¡El número secreto es **MAYOR**!")
            else:
                st.warning("📉 ¡El número secreto es **MENOR**!")

else:
    if st.button("🚀 Jugar de Nuevo"):
        reset_game()
        st.rerun()
