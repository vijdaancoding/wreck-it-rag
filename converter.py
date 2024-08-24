from bs4 import BeautifulSoup

def html_to_json_table(table_html):
    soup = BeautifulSoup(table_html, 'html.parser')
    table_el = soup.find('table')

    if not table_el:
        return {'headers': [],
                'rows': []
                }

    columns = [th.text.strip() for th in table_el.find_all('th')]
    if not columns:
        columns = [td.text.strip() for td in table_el.find('tr').find_all('td')]

    tbody_el = table_el.find('tbody')
    if tbody_el:
        rows = tbody_el.find_all('tr')
    else:
        rows = table_el.find_all('tr')[1:]

    return_json = {
        'headers': columns,
        'rows': []
    }

    for row in rows:
        cells = row.find_all('td')
        row_data = {}
        for idx in range(len(columns)):
            if idx < len(cells):
                row_data[columns[idx]] = cells[idx].text.strip()
            else:
                row_data[columns[idx]] = ''
        return_json['rows'].append(row_data)

    return return_json