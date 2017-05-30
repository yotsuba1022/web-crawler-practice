import requests
from bs4 import BeautifulSoup


EPA_TAQM_URL = 'http://taqm.epa.gov.tw/taqm/tw/HourlyData.aspx'


def generate_query_form_data(start_date, end_date):
    resp = requests.get(EPA_TAQM_URL)
    dom = BeautifulSoup(resp.text, 'html5lib')
    view_state = dom.find(id='__VIEWSTATE')['value']
    event_validation = dom.find(id='__EVENTVALIDATION')['value']
    viewstate_generator = dom.find(id='__VIEWSTATEGENERATOR')['value']
    # In all the ctlxx$[var_name], the xx will change dynamically,
    # need to check the value before craw the web.
    # TODO: Refactor it to collect the xx value dynamically.
    form_data = {
        '__VIEWSTATE': view_state,
        '__EVENTVALIDATION': event_validation,
        '__VIEWSTATEGENERATOR': viewstate_generator,
        'ctl09$lbSite': '56',
        'ctl09$lbParam': '4',
        'ctl09$txtDateS': start_date,
        'ctl09$txtDateE': end_date,
        'ctl09$btnQuery': '查詢即時值'
    }
    return form_data


def get_web_content(start_date, end_date):
    form_data = generate_query_form_data(start_date, end_date)
    if form_data:
        resp = requests.post(EPA_TAQM_URL, data=form_data)
        dom = BeautifulSoup(resp.text, 'html5lib')
        return dom
    else:
        return None


def main():
    start_date = '2017/05/20'
    end_date = '2017/05/22'
    dom = get_web_content(start_date, end_date)
    if dom:
        for table in dom.find_all('table', 'TABLE_G'):
            print([s for s in table.stripped_strings])


if __name__ == '__main__':
    main()
