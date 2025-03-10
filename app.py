import streamlit as st
import pandas as pd
import re

pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'

def consultar(dir_ip):
    filtros = ['Dirección IP', 'Tipo de servicio por el cual se solicita la reserva', '# Servicio']
    df = pd.read_csv( st.secrets["DB_FILE"])
    df_ip = df.loc[df["Dirección IP"] == dir_ip]
    df_final = df_ip.filter(items=filtros)
    return df_final

def main():
    st.title("Consultar IP reservada")
    direccion_ip=st.text_input('Ingrese la dirección IP a consultar')
    if direccion_ip:
        match = re.match(pattern, direccion_ip)
        if match:
            ip_result = consultar(direccion_ip)
            if ip_result.empty:
                st.info(f'La dirección IP: {direccion_ip} no está reservada.', icon="ℹ️")
            else:
                st.success(f'La dirección IP: {direccion_ip} tiene una reserva activa.', icon="✅" )
                st.dataframe(ip_result)
        else:
            st.error(f'{direccion_ip} no es una dirección IP válida', icon="🚨")





if __name__ == '__main__':
    main()
