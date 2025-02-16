import json
import re


def transform_table_to_json(table, websocket_response, base_ws):
    result = {
        base_ws["Columns View"]: [],
        base_ws["Sort By"]: None,
        base_ws["Condition"]: {},
        base_ws["Lines per page"]: None,
        base_ws["Row Height"]: None,
        base_ws["Highlight By"]: {},
        "module": "SO",
    }

    for i, row in enumerate(table):
        col_name = row.get("Columns View")
        if col_name not in websocket_response:
            continue

        column_info = websocket_response[col_name]
        result["columns"].append({"index": column_info["index"], "sort": i})

        if row.get("Sort By"):
            result["order_by"] = {
                "direction": row["Sort By"],
                "index": column_info["index"],
            }

        conditions = row.get("Condition", "")
        if conditions:
            condition_list = []
            for cond in conditions.split(","):
                parts = cond.split("=")
                if len(parts) == 2:
                    condition_type, value = parts[0], parts[1]
                    condition_list.append({"type": condition_type, "value": value})
            result["conditions_data"][column_info["filter"]] = condition_list

        highlights = row.get('Highlight By', '')
        color_list = []
        pattern = re.compile(r'(\w+)=(\w+)=((?:rgba\([^)]*\))?)')
        matches = pattern.findall(highlights)
        for match in matches:
            condition_type, value, color = match
            color_list.append({'type': condition_type, 'value': value, 'color': color})
        result[base_ws["Highlight By"]][column_info['filter']] = color_list

        if row.get("Lines per page"):
            result["page_size"] = int(row["Lines per page"])
        if row.get("Row Height"):
            result["row_height"] = int(row["Row Height"])

    if result["order_by"] is None and result["columns"]:
        result["order_by"] = {
            "direction": "asc",
            "index": result["columns"][0]["index"],
        }

    return json.dumps(result, indent=4)


table = [
    {
        "Columns View": "SO Number",
        "Sort By": "",
        "Highlight By": "equals=S110=rgba(172,86,86,1),equals=S111",
        "Condition": "equals=S110,equals=S111",
        "Row Height": "60",
        "Lines per page": "25",
    },
    {
        "Columns View": "Client PO",
        "Sort By": "",
        "Highlight By": "equals=P110,equals=P111",
        "Condition": "equals=P110",
        "Row Height": "",
        "Lines per page": "",
    },
    {
        "Columns View": "Terms of Sale",
        "Sort By": "asc",
        "Highlight By": "equals=S110=rgba(172,86,86,1)",
        "Condition": "",
        "Row Height": "",
        "Lines per page": "",
    },
]

websocket_response = {
    "Client PO": {"index": "so_list_client_po", "filter": "client_po"},
    "SO Number": {"index": "so_list_so_number", "filter": "so_no"},
    "Terms of Sale": {"index": "so_list_terms_of_sale", "filter": "term_sale"},
}

base_ws = {
    "Columns View": "columns",
    "Sort By": "order_by",
    "Condition": "conditions_data",
    "Lines per page": "page_size",
    "Row Height": "row_height",
    "Highlight By": "color_conditions",
}

result = {
    "columns": [
        {"index": "so_list_so_number", "sort": 0},
        {"index": "so_list_client_po", "sort": 1},
        {"index": "so_list_terms_of_sale", "sort": 2},
    ],
    "order_by": {"direction": "asc", "index": "so_list_terms_of_sale"},
    "conditions_data": {
        "so_no": [
            {"type": "equals", "value": "S110"},
            {"type": "equals", "value": "S111"},
        ],
        "client_po": [{"type": "equals", "value": "P110"}],
    },
    "page_size": "25",
    "row_height": "60",
    "color_conditions": {
        "so_no": [{"type": "equals", "value": "S110", "color": "rgba(172,86,86,1)"}],
        "client_po": [
            {"type": "equals", "value": "S110", "color": ""},
            {"type": "equals", "value": "S111", "color": ""},
        ],
        "term_sale": [],
    },
    "module": "SO",
}

json_result = transform_table_to_json(table, websocket_response, base_ws)
print(json_result)
