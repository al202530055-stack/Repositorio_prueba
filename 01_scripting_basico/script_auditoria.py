import requests
import json
from requests.auth import HTTPBasicAuth

# Deshabilitar advertencias de certificados SSL autofirmados
requests.packages.urllib3.disable_warnings()

# 1. Parámetros de la API RESTCONF
url = "https://devnetsandboxiosxec9k.cisco.com/restconf/data/ietf-interfaces:interfaces"

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

auth = HTTPBasicAuth("ca18ocho", "LR&uuL1$H8x*2o6")

try:
    # 2. Petición GET HTTP
    response = requests.get(
        url,
        headers=headers,
        auth=auth,
        verify=False,
        timeout=10
    )

    # 3. Validación del código de respuesta
    if response.status_code == 200:

        data = response.json()

        interfaces = data["ietf-interfaces:interfaces"]["interface"]

        # Lista para almacenar las interfaces
        inventario = []

        print(f"{'Nombre':<20} {'Tipo':<30} {'IP':<20}")
        print("-" * 70)

        # 4. Recorrer las interfaces
        for iface in interfaces:

            name = iface.get("name", "N/A")
            if_type = iface.get("type", "N/A")
            enabled = iface.get("enabled", False)

            # Obtener dirección IPv4
            ipv4 = iface.get("ietf-ip:ipv4", {})
            direcciones = ipv4.get("address", [])

            ip = direcciones[0].get("ip", "Sin IP") if direcciones else "Sin IP"

            # 5. Filtrar interfaces habilitadas con dirección IP
            if enabled and ip != "Sin IP":

                registro = {
                    "nombre": name,
                    "tipo": if_type,
                    "habilitada": enabled,
                    "direccion_ip": ip
                }

                inventario.append(registro)

                print(f"{name:<20} {if_type:<30} {ip:<20}")

        # 6. Guardar información en archivo JSON
        with open("inventario_interfaces.json", "w", encoding="utf-8") as archivo:

            json.dump(inventario, archivo, indent=4, ensure_ascii=False)

        print("\nInventario guardado correctamente.")

    else:
        print(f"Error HTTP {response.status_code}: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Error de conexión: {e}")

except (KeyError, ValueError, TypeError) as e:
    print(f"Error al procesar los datos: {e}")