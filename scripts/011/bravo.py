import streamlit as st
import schemdraw
import schemdraw.elements as elm

st.set_page_config(layout="wide")

st.title("Interactive Circuit Simulator Game")

st.write(
    "Welcome to the Interactive Circuit Simulator Game! "
    "This application allows you to build and experiment with a simple "
    "electrical circuit. You can adjust the values of the components and "
    "see how the circuit behaves in real-time. The goal is to learn about "
    "the fundamentals of electrical circuits in a fun and interactive way."
)

st.header("Circuit Parameters")

col1, col2 = st.columns(2)

with col1:
    voltage = st.slider("Voltage (V)", min_value=0.0, max_value=24.0, value=12.0, step=0.1)
    r1 = st.slider("Resistor 1 (Ω)", min_value=1, max_value=1000, value=100)

with col2:
    r2 = st.slider("Resistor 2 (Ω)", min_value=1, max_value=1000, value=200)
    r3 = st.slider("Variable Resistor (Ω)", min_value=1, max_value=1000, value=300)

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

st.header("Real-Time Data")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Current", f"{total_current:.2f} A")

with col2:
    st.metric("Voltage Drop R1", f"{v1:.2f} V")
    st.metric("Voltage Drop R2", f"{v2:.2f} V")
    st.metric("Voltage Drop R3", f"{v3:.2f} V")

with col3:
    st.metric("Power Dissipation R1", f"{p1:.2f} W")
    st.metric("Power Dissipation R2", f"{p2:.2f} W")
    st.metric("Power Dissipation R3", f"{p3:.2f} W")

with col4:
    with schemdraw.Drawing() as d:
        d.config(unit=2)
        d += elm.SourceV().label(f'{voltage}V')
        d += elm.Resistor().right().label(f'{r1}Ω').color('red' if p1 > 1 else 'black')
        d += elm.Resistor().down().label(f'{r2}Ω').color('red' if p2 > 1 else 'black')
        d += elm.Resistor().left().label(f'{r3}Ω').color('red' if p3 > 1 else 'black')
        d += elm.Line().up().to((0,0))

        # st.pyplot(d.draw(show=False))

        # Get the SVG data from the drawing
        svg_data = d.get_imagedata('svg')

        # Display the SVG image in Streamlit
        st.image(svg_data, caption="Simple DC Circuit", use_column_width=True)
