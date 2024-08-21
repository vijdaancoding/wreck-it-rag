from bs4 import BeautifulSoup

def html_to_json_table(table_html, expecting_header_row=True):
    soup = BeautifulSoup(table_html, 'html.parser')
    table_el = soup.find('table')

    if not table_el:
        return {'headers': [],
                'rows': []
                }

    columns = [th.text.strip() for th in table_el.find_all('th')]
    rows = table_el.find('tbody').find_all('tr')

    if not columns and expecting_header_row:
        columns = [td.text.strip() for td in rows[0].find_all('td')]
        rows = rows[1:]

    return_json = {
        'headers': columns,
        'rows': []
    }

    for row in rows:
        cells = row.find_all('td')
        row_data = {columns[idx]: cells[idx].text.strip() for idx in range(len(columns))}
        return_json['rows'].append(row_data)

    if not expecting_header_row and not return_json['headers']:
        if return_json['rows'] and not any(return_json['rows'][0].values()):
            return html_to_json_table(table_html, expecting_header_row=True)

    return return_json