'''
    Main del MCP
'''
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import requests

# Cargar variables de entorno
load_dotenv()

headers = {"Content-Type": "application/json"}

# Inicializar MCP
mcp = FastMCP('GestorPrestamos')


@mcp.tool()
def obtener_info_prueba_tecnica() -> dict:
    '''
        Obtiene información sobre la prueba técnica.
    '''
    return '''
            Esta prueba técnica ha sido desarrollada por Joaquin Borrego Fernandez junto a sus
            queridisimos alumnos de DAW 2024/26 en la fundación vedruna
            '''

@mcp.tool()
def login_as_manager() -> dict:
    '''
        Login as manager
    '''
    ############## VARIABLES DE ENTORNO ############## 
    loansmanagerpath = os.getenv("LOANSMANAGER_API")
    loginpath = os.getenv("LOGIN_ENDPOINT")
    user = os.getenv("MANAGER_USER")
    pw = os.getenv("MANAGER_PASS")

    auth_res = requests.post(f"{loansmanagerpath}{loginpath}",
        headers=headers, json={"username": user, "password": pw})
    auth_res.raise_for_status()
    response = auth_res.json()
    access_token = response.get("access_token")
    headers.update({"Authorization": f"Bearer {access_token}"})

    return response

@mcp.tool()
def get_pending_loanapplications(page: int, size: int) -> dict:
    '''
        Obtain all pending loan applications data from loansmanager api in json format using pagination
    '''

    ############## VARIABLES DE ENTORNO ############## 
    loansmanagerpath = os.getenv("LOANSMANAGER_API")

    pendingloanspath = os.getenv("PENDINGLOANAPPLICATION_ENDPOINT")

    pending_debts_res = requests.get(f"{loansmanagerpath}{pendingloanspath}status/PENDING?page={page}&size={size}", headers=headers)
    if pending_debts_res.status_code == 403:
        # HABRIA QUE REFRESCAR
        pending_debts_res.raise_for_status()
    return pending_debts_res.json()

@mcp.tool()
def get_debts_by_dni(dni: str, page: int, size: int) -> dict:
    """
        Obtain all pending debts data from defaulters_list-api in json format using pagination
    """

    ############## VARIABLES DE ENTORNO ############## 
    dnidebts_path = os.getenv("DEBTS_API") + os.getenv("DEBTS_BY_DNI_ENDPOINT")

    debts_list_res = requests.get(f"{dnidebts_path}{dni}?page={page}&size={size}", headers=headers)

    if debts_list_res.status_code == 403:
        # HABRIA QUE REFRESCAR
        debts_list_res.raise_for_status()
    return debts_list_res.json()

@mcp.tool()
def reject_loanapplication_by_uuid(uuid: str) -> dict:
    """
        Reject a loan application by uuid
    """
    ############## VARIABLES DE ENTORNO ############## 
    change_status_path = os.getenv("LOANSMANAGER_API") + os.getenv("PENDINGLOANAPPLICATION_ENDPOINT")

    return requests.patch(f"{change_status_path}{uuid}",
                               headers=headers, json={"status": "REJECTED"})

# @mcp.tool()
# def cancelar_solicitudes_prestamo_debts() -> str:
#     '''
#         Escanea préstamos pendientes en la api de Spring y verificar ASNEF en la api deFlask 
#         y tomamos una decisión en base a la información obtenida.
#     '''
#     ############## VARIABLES DE ENTORNO ############## 
#     loansmanagerpath = os.getenv("LOANSMANAGER_API")
#     loginpath = os.getenv("LOGIN_ENDPOINT")
#     user = os.getenv("MANAGER_USER")
#     pw = os.getenv("MANAGER_PASS")

#     pendingloanspath = os.getenv("PENDINGLOANAPPLICATION_ENDPOINT")

#     dnidebts_path = os.getenv("DEBTS_API") + os.getenv("DEBTS_BY_DNI_ENDPOINT")

#     change_status_path = os.getenv("LOANSMANAGER_API") + os.getenv("PENDINGLOANAPPLICATION_ENDPOINT")

#     ############## ############## 
#     headers = {"Content-Type": "application/json"}
    

#     auth_res = requests.post(f"{loansmanagerpath}{loginpath}",
#         headers=headers, json={"username": user, "password": pw})
#     auth_res.raise_for_status()
#     acces_token = auth_res.json().get("access_token")
#     #refresh_token = auth_res.json().get("refresh_token")
#     headers.update({"Authorization": f"Bearer {acces_token}"})

#     dni_dict = {}

#     pending_debts_res = requests.get(f"{loansmanagerpath}{pendingloanspath}status/PENDING", headers=headers)
#     if pending_debts_res.status_code == 403:
#         # HABRIA QUE REFRESCAR
#         pending_debts_res.raise_for_status()
#     total_pages = pending_debts_res.json().get("totalPages")

#     for loan in pending_debts_res.json().get("content"):
#         if loan["applicantDni"] not in dni_dict.keys():
#             dni_dict[loan["applicantDni"]] = [loan["uuid"]]
#         else:
#             dni_dict[loan["applicantDni"]].append(loan["uuid"])

#     for p in range(1,total_pages):
#         pending_debts_res = requests.get(f"{loansmanagerpath}{pendingloanspath}/satus/PENDING?page={p}", headers=headers)
#         pending_debts_res.raise_for_status()
#         for loan in pending_debts_res.json().get("content"):
#             if loan["applicantDni"] not in dni_dict.keys():
#                 dni_dict[loan["applicantDni"]] = [loan["uuid"]]
#             else:
#                 dni_dict[loan["applicantDni"]].append(loan["uuid"])

#     print("DNI_DICT", dni_dict)
#     for dni, applications_uuid in dni_dict.items():
#         print("DNI Y UUIDS", dni, applications_uuid)
#         debts_list_res = requests.get(f"{dnidebts_path}{dni}")
#         debts_list_res.raise_for_status()
#         debts_list = debts_list_res.json().get("content")
#         print("DEBTS_LIST", debts_list)
#         if debts_list:
#             print("AQUI ENTRA")
#             for uuid in applications_uuid:
#                 print("UUID", uuid)
                
#                 response = requests.patch(f"{change_status_path}{uuid}",
#                                headers=headers, json={"status": "REJECTED"})
#                 print("RESPONSE", response.json())

#     return f"Prestamos cancelados: {dni_dict}"

if __name__ == "__main__":
    mcp.run()