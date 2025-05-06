import requests
from services.data_utils import extract_field

def add_to_excel_backup(token, data):
    access_token = token
    file_path = "TRACKING/KAI_WA_TRACKING.xlsx"
    table_name = "Table1"  # pastikan kamu tahu nama table-nya

    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{file_path}:/workbook/tables/{table_name}/rows/add"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("✅ Data berhasil ditambahkan.")
    else:
        print("❌ Gagal:", response.status_code, response.text)

def add_to_excel(token, data):
    access_token = token
    file_path = "TRACKING/KAI_WA_TRACKING.xlsx"
    table_name = "Table1"

    url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{file_path}:/workbook/tables/{table_name}/rows/add"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    values = []
    for row in data:
        if "[Automation]" in row["message"]:
            print("Automation Detected not sending to xlsx")
        elif "NOC KAI" in row["message"]:
            print("Message from noc not sending to xlsx")
        else:
            case_id = extract_field("Case ID", row["message"])
            values.append([
                row.get("timestamp", ""),
                case_id,
                row.get("message", "")  # hilangkan newline jika ada
            ])

            payload = {"values": values}
            
            response = requests.post(url, headers=headers, json=payload)

            if response.status_code == 201:
                print("✅ Data berhasil ditambahkan.")
            else:
                print("❌ Gagal:", response.status_code, response.text)

def read_excel(token):
    sheet_name = 'caseIdList'
    file_path = "TRACKING/KAI_WA_TRACKING.xlsx"
    graph_url = f'https://graph.microsoft.com/v1.0/me/drive/sharedWithMe:/{file_path}:/workbook/worksheets/{sheet_name}/usedRange(valuesOnly=true)'

    # Kirim request
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(graph_url, headers=headers)

    # Tampilkan hasil
    if response.status_code == 200:
        data = response.json()
        for row in data['values']:
            print(row)
    else:
        print(f"Gagal mengambil data: {response.status_code}\n{response.text}")