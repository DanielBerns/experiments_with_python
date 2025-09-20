import streamlit as st
import schemdraw
import schemdraw.elements as elm

st.set_page_config(layout="wide")

st.title("Simulador interactivo de circuitos eléctricos")

st.write(
    "Bienvenido al Simulador interactivo de circuitos eléctricos! "
    "Esta aplicacion permite construir y experimentar con un circuito eléctrico simple."
    "Podes ajustar los valores de los componentes y ver como se comporta el circuito en tiempo real."
    "El objetivo es aprender los fundamentos de circuitos eléctricos de manera interactiva."
)

st.header("Parámetros del circuito")

col1, col2 = st.columns(2)

with col1:
    voltage = st.slider("Voltaje (V)", min_value=0.0, max_value=24.0, value=12.0, step=0.1)
    r1 = st.slider("Resistor 1 (Ω)", min_value=1, max_value=1000, value=100)

with col2:
    r2 = st.slider("Resistor 2 (Ω)", min_value=1, max_value=1000, value=200)
    r3 = st.slider("Resistor Variable (Ω)", min_value=1, max_value=1000, value=300)

# To prevent division by zero if all resistances are 0
if (r1 + r2 + r3) > 0:
    total_resistance = r1 + r2 + r3
    total_current = voltage / total_resistance
else:
    total_resistance = 0
    total_current = 0


v1 = total_current * r1
v2 = total_current * r2
v3 = total_current * r3

p1 = v1 * total_current
p2 = v2 * total_current
p3 = v3 * total_current

st.header("Datos en tiempo real")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Corriente total", f"{total_current:.2f} A")

with col2:
    st.metric("Caída de tensión R1", f"{v1:.2f} V")
    st.metric("Caída de tensión R2", f"{v2:.2f} V")
    st.metric("Caída de tensión R3", f"{v3:.2f} V")

with col3:
    st.metric("Disipación de potencia R1", f"{p1:.2f} W")
    st.metric("Disipación de potencia R2", f"{p2:.2f} W")
    st.metric("Disipación de potencia R3", f"{p3:.2f} W")

with col4:
    with schemdraw.Drawing() as d:
        d.config(unit=2)
        d += elm.SourceV().label(f'{voltage}V')
        d += elm.Resistor().right().label(f'{r1}Ω').color('red' if p1 > 1 else 'black')
        d += elm.Resistor().down().label(f'{r2}Ω').color('red' if p2 > 1 else 'black')
        d += elm.Resistor().left().label(f'{r3}Ω').color('red' if p3 > 1 else 'black')
        d += elm.Line().up().to((0,0))

        # Get the SVG data from the drawing
        svg_data = d.get_imagedata('svg')

        # Decode the SVG bytes into a string before displaying
        st.image(svg_data.decode("utf-8"), caption="Circuito de corriente continua", use_container_width=True, width="stretch")
