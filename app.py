import streamlit as st

def optimizar_barras(piezas, largo=600):
    piezas.sort(reverse=True)
    barras = []
    for p in piezas:
        puesto = False
        for b in barras:
            if sum(b) + p <= largo:
                b.append(p); puesto = True; break
        if not puesto: barras.append([p])
    return barras

st.title("🛠️ Sistema Línea 25")
if 'pedido' not in st.session_state: st.session_state.pedido = []

with st.form("nueva"):
    ancho = st.number_input("Ancho (cm)")
    alto = st.number_input("Alto (cm)")
    div = st.selectbox("Divisiones",)
    if st.form_submit_button("➕ Agregar"):
        jamba, riel = alto, ancho - 1.5
        pierna, gancho = alto - 3.5, alto - 3.5
        if div == 2: zocalo, c_z, c_p = (ancho-16)/2, 4, 2
        elif div == 3: zocalo, c_z, c_p = (ancho-26.5)/3, 6, 4
        else: zocalo, c_z, c_p = (ancho-30)/4, 8, 6
        st.session_state.pedido.append({
            "medida": f"{ancho}x{alto}", "div": div,
            "piezas": {"JAMBA": [jamba]*2, "RIEL": [riel]*2, "PIERNA": [pierna]*c_p, "GANCHO": [gancho]*2, "ZOCALO": [zocalo]*c_z},
            "vidrio": f"{div} de {alto-15}x{zocalo+1.5:.1f}"
        })

if st.session_state.pedido:
    st.header("📋 Resumen")
    todos = {"JAMBA":[], "RIEL":[], "PIERNA":[], "GANCHO":[], "ZOCALO":[]}
    for v in st.session_state.pedido:
        for p, lista in v['piezas'].items(): todos[p].extend(lista)
    if st.button("🪚 OPTIMIZAR"):
        for p, piezas in todos.items():
            if piezas:
                st.subheader(f"🔹 {p}")
                for i, b in enumerate(optimizar_barras(piezas), 1):
                    st.write(f"Tira {i}: {b} (Sobra: {600-sum(b):.1f}cm)")
