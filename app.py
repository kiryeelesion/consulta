import streamlit as st
import pandas as pd
import re
import ipaddress

pattern = r'^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$'

def consultar(dir_ip):
    filtros = ['Dirección IP', 'Tipo de servicio por el cual se solicita la reserva', '# Servicio']
    df = pd.read_csv(st.secrets["DB_FILE"])
    df_ip = df.loc[df["Dirección IP"] == dir_ip]
    df_final = df_ip.filter(items=filtros)
    return df_final

def ip_en_scope(ip):
    """Verifica si la IP está dentro de alguna de las redes definidas en st.secrets."""
    try:
        ip_obj = ipaddress.ip_address(ip)
        # Leemos la lista de redes desde los secrets de Streamlit
        scope_list = st.secrets["SCOPE_LIST"]
        return any(ip_obj in ipaddress.ip_network(red) for red in scope_list)
    except ValueError:
        return False
    except KeyError:
        st.error("Error de configuración: 'SCOPE_LIST' no está definido en los secrets.", icon="🛠️")
        return False

def main():
    st.title("Consultar IP reservada")
    direccion_ip = st.text_input('Ingrese la dirección IP a consultar')
    
    if direccion_ip:
        match = re.match(pattern, direccion_ip)
        if match:
            if not ip_en_scope(direccion_ip):
                st.error(f'No es posible realizar la reserva de la dirección IP: {direccion_ip}, no pertenece al alcance.', icon="🚨")
            else:
                ip_result = consultar(direccion_ip)
                if ip_result.empty:
                    st.info(f'La dirección IP: {direccion_ip} no está reservada.', icon="ℹ️")
                else:
                    st.success(f'La dirección IP: {direccion_ip} tiene una reserva activa.', icon="✅")
                    st.dataframe(ip_result)
        else:
            st.error(f'{direccion_ip} no es una dirección IP válida', icon="🚨")

if __name__ == '__main__':
    main()
