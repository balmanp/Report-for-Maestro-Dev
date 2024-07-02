import json
from datetime import datetime
import matplotlib.pyplot as plt

# Baca data JSON dari file
with open('flowtest.json') as f:
    data = json.load(f)

# Menghitung total test dan jumlah test yang berhasil, gagal, dan belum diuji
total_tests = 0
success_tests = 0
failure_tests = 0
untested_tests = 0
total_duration = 0
app_name = None

for entry in data:
    total_tests += 1
    if "launchAppCommand" in entry["command"]:
        app_name = entry["command"]["launchAppCommand"].get("appId", "Unknown App")
    if entry['metadata']['status'] == 'COMPLETED':
        success_tests += 1
        total_duration += entry['metadata']['duration']
    elif entry['metadata']['status'] == 'FAILED':
        failure_tests += 1
    else:
        untested_tests += 1

# Mengurutkan data berdasarkan timestamp
data.sort(key=lambda x: x['metadata']['timestamp'])

# Membuat details untuk setiap data
flow_details = ""
for i, entry in enumerate(data):
    command_type = list(entry['command'].keys())[0]
    details = entry['command'][command_type]
    status = entry['metadata']['status']
    timestamp = datetime.fromtimestamp(entry['metadata']['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')
    duration = entry['metadata']['duration']
    status_class = "completed" if status == "COMPLETED" else "failed" if status == "FAILED" else "untested"

    flow_details += f"""
    <div class="flow-item {status_class}" onclick="toggleDetails('details-{i}')">
        {'✅' if status == 'COMPLETED' else '❌' if status == 'FAILED' else '⬜'} {command_type} on "{details.get('selector', {}).get('textRegex', '')}"
        <div class="details" id="details-{i}" style="display:none;">
            <p><b>Step Detail</b></p>
            <p><b>Command:</b> {command_type}</p>
            <p><b>Details:</b> {json.dumps(details, indent=4)}</p>
            <p><b>Status:</b> {status}</p>
            <p><b>Timestamp:</b> {timestamp}</p>
            <p><b>Duration:</b> {duration} ms</p>
        </div>
    </div>
    """

# Menghitung persentase untuk setiap kategori
passed_percentage = success_tests / total_tests * 100 if total_tests > 0 else 0
failed_percentage = failure_tests / total_tests * 100 if total_tests > 0 else 0
untested_percentage = untested_tests / total_tests * 100 if total_tests > 0 else 0

# Bagian bar untuk untested, hanya ditambahkan jika untested_percentage > 0
untested_bar = ""
if untested_percentage > 0:
    untested_bar = f"""
    <div class="bar-segment untested" style="width: {untested_percentage}%">
        <span>{untested_percentage:.2f}%</span>
    </div>
    """

# Template HTML yang dimodifikasi
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Test Execution Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #f2f2f2;
            color: #333;
            margin: 0;
            padding: 0;
        }}
        .container {{
            width: 80%;
            margin: 20px auto;
            background-color: #fff;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 5px;
        }}
        .info-chart-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            margin-bottom: 20px;
        }}
        .flex-container {{
            display: flex;
            justify-content: space-between;
            width: 100%;
        }}
        .flex-container > div {{
            border: 1px solid #ddd;
            padding: 10px 20px;
            margin: 15px;
            display: flex;
            flex-direction: column;
            align-items: center;
            background-color: #d0e0e3;
            border-radius: 15px;
            flex: 1;
            text-align: center;
        }}
        .info-box p {{
            margin: 5px 0;
        }}
        .info-box .number {{
            font-size: 24px;
            font-weight: bold;
        }}
        .flow-column  {{
            width: auto;
            background-color: #fff;
            border: 1px solid #ddd;
            padding: 10px;
            border-radius: 5px;
        }}
        .flow-item {{
            cursor: pointer;
            padding: 10px;
            margin-bottom: 5px;
            background-color: #f9f9f9;
            border-left: 5px solid transparent;
            transition: background-color 0.3s;
        }}
        .flow-item:hover {{
            background-color: #e9ecef;
        }}
        .flow-item.completed {{
            border-left-color: #28a745; /* Green for completed */
        }}
        .flow-item.failed {{
            border-left-color: #dc3545; /* Red for failed */
        }}
        .flow-item.untested {{
            border-left-color: #ffc107; /* Yellow for untested */
        }}
        .details {{
            display: none;
            margin-left: 20px;
            border-left: 2px solid #ccc;
            padding-left: 10px;
            margin-top: 5px;
        }}
        .filters {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            width: 100%;
        }}
        .filter-btn {{
            padding: 8px 16px;
            margin-left: 5px;
            cursor: pointer;
            border: 1px solid #ddd;
            background-color: #f2f2f2;
            transition: background-color 0.3s;
            border-radius: 5px;
        }}
        .filter-btn:hover {{
            background-color: #ddd;
        }}
        .search-box {{
            flex: 1;
            display: flex;
            justify-content: flex-end;
        }}
        .search-input {{
            padding: 8px;
            width: 200px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        footer {{
            margin-top: 20px;
            text-align: center;
            font-size: 0.9em;
            color: #777;
        }}
        h1, h3 {{
            color: #333;
        }}
        .horizontal-bar {{
            width: auto;
            height: 20px;
            display: flex;
            border: 1px solid #ddd;
            margin: 15px 0;
            position: relative;
            border-radius: 5px;
        }}
        .bar-segment {{
            height: 100%;
            position: relative;
        }}
        .bar-segment.passed {{
            background-color: #28a745;
        }}
        .bar-segment.failed {{
            background-color: #dc3545;
        }}
        .bar-segment.untested {{
            background-color: #eeeeee;
        }}
        .bar-segment span {{
            position: absolute;
            left: 50%;
            transform: translateX(-50%);
            color: white;
            font-weight: bold;
        }}
    </style>
    <script>
        function toggleDetails(id) {{
            var x = document.getElementById(id);
            if (x.style.display === "none") {{
                x.style.display = "block";
            }} else {{
                x.style.display = "none";
            }}
        }}

        function filterFlow(status) {{
            var items = document.getElementsByClassName('flow-item');
            for (var i = 0; i < items.length; i++) {{
                if (status === 'all') {{
                    items[i].style.display = 'block';
                }} else if (items[i].classList.contains(status)) {{
                    items[i].style.display = 'block';
                }} else {{
                    items[i].style.display = 'none';
                }}
            }}
        }}

        function searchFlow() {{
            var input, filter, items, item, txtValue;
            input = document.getElementById('searchInput');
            filter = input.value.toLowerCase();
            items = document.getElementsByClassName('flow-item');
            for (var i = 0; i < items.length; i++) {{
                item = items[i];
                txtValue = item.textContent || item.innerText;
                if (txtValue.toLowerCase().indexOf(filter) > -1) {{
                    item.style.display = 'block';
                }} else {{
                    item.style.display = 'none';
                }}
            }}
        }}
    </script>
</head>
<body>
    <div class="container">
        <h1>Test Execution Report</h1>
        <h3>{app_name}</h3>
        <div class="info-chart-container">
            <div class="flex-container">
                <div class="info-box" >
                    <p class="number">{total_tests}</p>
                    <p><b>Test Cases</b></p>
                </div>
                <div class="info-box" style="background-color: #28a745; color: #ffffff;">
                    <p class="number">{success_tests}</p>
                    <p><b>Success</b></p>
                </div>
                <div class="info-box" style="background-color: #dc3545; color: #ffffff;">
                    <p class="number">{failure_tests}</p>
                    <p><b>Failed</b></p>
                </div>
                <div class="info-box" style="background-color: #eeeeee;">
                    <p class="number">{untested_tests}</p>
                    <p><b>Untested</b></p>
                </div>
            </div>
        </div>
        <div class="horizontal-bar">
            <div class="bar-segment passed" style="width: {passed_percentage}%">
                <span>{passed_percentage:.2f}%</span>
            </div>
            <div class="bar-segment failed" style="width: {failed_percentage}%">
                <span>{failed_percentage:.2f}%</span>
            </div>
            {untested_bar}
        </div>
        <h3><b>Total Duration: {total_duration} ms</b></h3>
        <div class="filters">
            <div>
                <button class="filter-btn" onclick="filterFlow('all')">All</button>
                <button class="filter-btn" onclick="filterFlow('completed')">Success</button>
                <button class="filter-btn" onclick="filterFlow('failed')">Failed</button>
                <button class="filter-btn" onclick="filterFlow('untested')">Untested</button>
            </div>
            <div class="search-box">
                <input type="text" id="searchInput" class="search-input" onkeyup="searchFlow()" placeholder="Search for steps...">
            </div>
        </div>
        <div class="flow-column">
            {flow_details}
        </div>
        <footer>
            <p>Generated on {generated_on}</p>
        </footer>
    </div>
</body>
</html>
"""

# Menyimpan HTML yang dihasilkan ke file dengan encoding utf-8
with open("report.html", "w", encoding='utf-8') as file:
    file.write(html_template.format(
        flow_details=flow_details,
        app_name=app_name if app_name else "Unknown",
        total_tests=total_tests,
        success_tests=success_tests,
        failure_tests=failure_tests,
        untested_tests=untested_tests,
        total_duration=total_duration,
        passed_percentage=passed_percentage,
        failed_percentage=failed_percentage,
        untested_bar=untested_bar,
        untested_percentage=untested_percentage,
        generated_on=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))

print("HTML report has been generated and saved as 'report.html'.")
