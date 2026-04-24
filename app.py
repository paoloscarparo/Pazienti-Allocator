import streamlit as st

# --- LOGICA CORE (Il tuo codice) ---
def assegna_camere(pazienti):
    camere = [
        {"nome": "Singola 1", "capacita": 1, "ospiti": []},
        {"nome": "Singola 2", "capacita": 1, "ospiti": []},
        {"nome": "Doppia 1",  "capacita": 2, "ospiti": []},
        {"nome": "Doppia 2",  "capacita": 2, "ospiti": []}
    ]

    def compatibili(paziente, ospiti_camera):
        for ospite in ospiti_camera:
            if paziente['sesso'] != ospite['sesso']:
                return False
            if paziente['placca'] != ospite['placca']:
                return False
        return True

    def risolvi(indice_paziente):
        if indice_paziente == len(pazienti):
            return True 
        paziente_corrente = pazienti[indice_paziente]
        for camera in camere:
            if len(camera["ospiti"]) < camera["capacita"]:
                if compatibili(paziente_corrente, camera["ospiti"]):
                    camera["ospiti"].append(paziente_corrente)
                    if risolvi(indice_paziente + 1):
                        return True
                    camera["ospiti"].pop()
        return False

    if risolvi(0):
        return camere
    return None

# --- INTERFACCIA STREAMLIT ---
st.set_page_config(page_title="Allocazione Camere", page_icon="🏥")
st.title("🏥 Gestione Allocazione Pazienti")
st.write("Aggiungi i pazienti e il sistema troverà la disposizione ottimale in base ai vincoli (Sesso e Placca).")

# Inizializzazione lista pazienti nella sessione
if 'lista_pazienti' not in st.session_state:
    st.session_state.lista_pazienti = []

# Sidebar per l'inserimento
with st.sidebar:
    st.header("Aggiungi Paziente")
    nome = st.text_input("Nome Paziente")
    sesso = st.selectbox("Sesso", ["M", "F"])
    placca = st.selectbox("Placca presente?", ["si", "no"])
    
    if st.button("Aggiungi alla lista"):
        if nome:
            st.session_state.lista_pazienti.append({"nome": nome, "sesso": sesso, "placca": placca})
            st.toast(f"{nome} aggiunto!")
        else:
            st.error("Inserisci un nome!")

    if st.button("Svuota lista"):
        st.session_state.lista_pazienti = []
        st.rerun()

# Visualizzazione tabella pazienti
st.subheader("Lista Pazienti Corrente")
if st.session_state.lista_pazienti:
    st.table(st.session_state.lista_pazienti)
    
    if st.button("Calcola Assegnazione Camere"):
        risultato = assegna_camere(st.session_state.lista_pazienti)
        
        if risultato:
            st.success("Disposizione trovata!")
            cols = st.columns(2)
            for i, cam in enumerate(risultato):
                with cols[i % 2]:
                    with st.container(border=True):
                        st.markdown(f"### {cam['nome']}")
                        st.caption(f"Capacità: {cam['capacita']}")
                        nomi_ospiti = [p["nome"] for p in cam["ospiti"]]
                        if nomi_ospiti:
                            for n in nomi_ospiti:
                                st.write(f"👤 {n}")
                        else:
                            st.write("*Vuota*")
        else:
            st.error("Impossibile trovare una disposizione che rispetti tutti i vincoli. Chiedere eventualmente posti letto in appoggio ad altri reparti")
else:
    st.info("La lista è vuota. Aggiungi pazienti dalla barra laterale.")
