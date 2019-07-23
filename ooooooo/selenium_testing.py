from datetime import datetime
import csv
import time
import calendar
from datetime import timedelta
import logging
import os

from unipath import Path
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class XXXSelenium(object):

    def get_TodaysAgreements(self):
        today = datetime.today().date().strftime('%Y-%d-%m')
        self.get_AgreementsByDate(today)

    def get_AgreementsByDate(self, date):
        driver = self.start_Driver()
        districts = self.get_Districts(driver)
        self.set_Date(driver, date)
        for district in districts:
            self.select_District(driver, district)
            courts = self.get_Courts(driver)
            for court in courts:
                self.select_Court(driver, court)
                buscar = driver.find_element_by_id('buscar')
                driver.execute_script("var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", buscar)
                time.sleep(1)
                self.create_AgreementFile(driver, district, court)
        driver.quit()

    def create_AgreementFile(self, driver, district, court, page_elements=10):
        time.sleep(3)
        if 'gradeX' in driver.page_source:
            with open('{}, {}.csv'.format(district, court), 'w') as f:
                f.write('Tipo|Numero|Prom|Asunto|Resolucion|Destino|Fecha|Sintesis|Detalle|')

            while True:
                agreements = driver.find_elements(By.CLASS_NAME, 'gradeX')
                time.sleep(1)
                for element in agreements[0:page_elements-1]:
                    cells = element.find_elements_by_tag_name('td')
                    text = ""
                    for item in cells:
                        text = text + item.text + "|"
                    text = text + "\n"
                    with open('{}, {}.csv'.format(district, court), 'a') as f:
                        f.write(text)
                    print('------------------------------')
                html_source = driver.page_source
                if "paginate_button next disable" not in html_source and "paginate_button next" in html_source:
                    next_page_btn = driver.find_element_by_xpath('//*[@id="dataTables-example_next"]/a')
                else:
                    break
                if next_page_btn:
                    driver.execute_script("var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", next_page_btn)

    def select_Court(self, driver, court):
        time.sleep(1)
        if driver:
            if court:
                juzgado = Select(driver.find_element_by_id("juzgado"))
                ActionChains(driver).move_to_element(juzgado)
                juzgado.select_by_visible_text(court)
                time.sleep(1)

    def select_District(self, driver, district):
        time.sleep(1)
        if driver:
            if district:
                distrito = Select(driver.find_element_by_id("distrito"))
                ActionChains(driver).move_to_element(distrito)
                distrito.select_by_visible_text(district)
                time.sleep(1)

    def get_Courts(self, driver):
        time.sleep(1)
        juzgados_elem = driver.find_element_by_id("juzgado")
        options = juzgados_elem.find_elements_by_tag_name('option')
        courts = [elem.text for elem in options]
        courts.remove(courts[0])
        return courts

    def get_Districts(self, driver):
        time.sleep(1)
        distritos_elem = driver.find_element_by_id("distrito")
        options = distritos_elem.find_elements_by_tag_name('option')
        districts = [elem.text for elem in options]
        districts.remove(districts[0])
        return districts

    def set_Date(self, driver, date):
        time.sleep(1)
        fecha = driver.find_element_by_id('fecha')
        fecha.send_keys(date)

    def start_Driver(self):
        driver = webdriver.Chrome()
        driver.get('https://www.xxxxxxxxxxxxxxxx.com.mx/')
        driver.implicitly_wait(10)
        return driver


class XXXXXXXXXSelenium(object):

    def get_Travel(self):
        driver = self.start_Driver()
        if self.check_StatusPage(driver):
            origins = self.get_Origins(driver)
            start_date, end_date = self.get_DateRange()
            today = datetime.today().date() + timedelta(days=1)
            mark = today

            self.select_Origin(driver)
            self.select_Destination(driver)
            self.select_Date(driver)
            self.select_Find(driver)
            filename = self.create_File(driver)
            for n in range(len(origins)):
                self.select_EditButton(driver)
                self.select_OriginField(driver)
                self.select_Origin(driver, n + 1)
                destinations = self.get_Destinations(driver)
                for i in range(len(destinations)):
                    self.select_DestinationField(driver)
                    self.select_Destination(driver, i + 1)
                    not_found = 0
                    for dt in range(60):
                        date = today + timedelta(days=dt)
                        if today.month != mark.month and dt == 0:
                            for n in range(mark.month - today.month):
                                self.select_BackMonth(driver)
                        if today.month != date.month and date.day == 1:
                            self.select_NextMonth(driver)
                        month = self.get_CalendarMonth(driver, date)
                        self.set_DayCalendar(driver, month, date)
                        self.select_Find(driver)
                        mark = date
                        extracted = self.extraxt_Info(driver, date, filename)
                        if not extracted:
                            not_found += 1
                            print('not_found', not_found)
                            if not_found >= 10:
                                print('break')
                                break
                        else:
                            not_found = 0
        else:
            print('XXXXXXXXX Selenium Task: Could Not Connect')
            # logging.error('XXXXXXXXX Selenium Task: Could Not Connect')
            driver.quit()

    def create_File(self, driver):
        filename = 'Travels, {}.csv'.format(datetime.today().date().strftime('%d-%m-%Y'))
        with open(filename, 'w') as f:
            f.write('Origen,Destino,Fecha Salida, Hora Salida, Precio Base,Precio Promocion Internet,Tipo de Servicio,Id Sitio,Fecha de Procesamiento,Hora de Procesamiento,\n')
        return filename

    def extraxt_Info(self, driver, date, filename):
        travels = driver.find_elements_by_xpath('//*[@id="table-container"]/div/div')
        if travels:
            try:
                for travel in travels:
                    travel_origin = travel.find_element_by_xpath('.//div/div[2]/div/div[1]/div[2]/div[1]/strong').text
                    travel_destination = travel.find_element_by_xpath('.//div/div[2]/div/div[1]/div[2]/div[2]/strong').text
                    travel_date = date.strftime('%d/%m/%Y')
                    travel_time = travel.find_element_by_xpath('.//div/div[1]').text.split('\n')[1]

                    if travel.find_element_by_xpath('.//div/div[2]/div/div[2]/div[1]/span').text != ' ':
                        travel_base_price = travel.find_element_by_xpath('.//div/div[2]/div/div[2]/div[1]/span').text.translate({ord('$'):None})
                        travel_promo_price = travel.find_element_by_xpath('.//div/div[2]/div/div[2]/div[1]/div/span').text.translate({ord('$'):None})
                    else:
                        travel_promo_price = '0'
                        travel_base_price = travel.find_element_by_xpath('.//div/div[2]/div/div[2]/div[1]/div/span').text.translate({ord('$'):None})

                    service_type = travel.find_element_by_xpath('.//div/div[2]/div/div[1]/div[1]/div/img').get_attribute('title')
                    id_sitio = '????????????????????'
                    date_process = datetime.now().date().strftime('%d/%m/%Y')
                    time_process = datetime.now().time().strftime('%H:%M')

                    with open(filename, 'a') as f:
                        text = '\"{}\",\"{}\",{},{},{}.00,{}.00,{},{},{},{},\n'.format(
                            travel_origin, travel_destination, travel_date,
                            travel_time, travel_base_price, travel_promo_price,
                            service_type, id_sitio, date_process, time_process
                        )
                        f.write(text)
                        print(text)
                return True
            except:
                pass
        else:
            return False

    def select_Calendar(self, driver):
        selector = driver.find_element_by_xpath('//*[@id="search-bar"]/div[4]/button')
        driver.execute_script("var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", selector)

    def select_BackMonth(self, driver):
        selector = driver.find_element_by_xpath('//*[@id="datepicker"]/div/div[3]/calendar[1]/div/div/div[3]/div/div[1]/button')
        driver.execute_script("var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", selector)

    def select_NextMonth(self, driver):
        selector = driver.find_element_by_xpath('//*[@id="datepicker"]/div/div[3]/calendar[1]/div/div/div[3]/div/div[3]/button')
        driver.execute_script("var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", selector)

    def set_DayCalendar(self, driver, month, date):
        driver.execute_script(
            "var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", month[date.day-1]
        )

    def get_CalendarMonth(self, driver, date):
        days_calendar = self.get_DaysInCalendar(driver)
        month_info = calendar.monthrange(date.year, date.month)
        index_start = [1, 2, 3, 4, 5, 6, 0][month_info[0]]
        month = days_calendar[index_start:index_start + month_info[1]]
        return month

    def get_DaysInCalendar(self, driver):
        days_calendar = []
        days_calendar.extend(
            driver.find_elements_by_xpath(
                '//*[@id="datepicker"]/div/div[3]/calendar[1]/div/div/div[5]/div/div')
        )
        days_calendar.extend(
            driver.find_elements_by_xpath(
                '//*[@id="datepicker"]/div/div[3]/calendar[1]/div/div/div[6]/div/div')
        )
        days_calendar.extend(
            driver.find_elements_by_xpath(
                '//*[@id="datepicker"]/div/div[3]/calendar[1]/div/div/div[7]/div/div')
        )
        days_calendar.extend(
            driver.find_elements_by_xpath(
                '//*[@id="datepicker"]/div/div[3]/calendar[1]/div/div/div[8]/div/div')
        )
        days_calendar.extend(
            driver.find_elements_by_xpath(
                '//*[@id="datepicker"]/div/div[3]/calendar[1]/div/div/div[9]/div/div')
        )
        try:
            driver.implicitly_wait(1)
            days_calendar.extend(
                driver.find_elements_by_xpath(
                    '//*[@id="datepicker"]/div/div[3]/calendar[1]/div/div/div[10]/div/div')
            )
        except:
            pass
        return days_calendar

    def get_DateRange(self):
        start_date = datetime.today().date()
        end_date = start_date + timedelta(days=60)
        return start_date, end_date

    def select_DestinationField(self, driver):
        selector = driver.find_element_by_xpath('//*[@id="search-bar"]/div[2]/button')
        driver.execute_script("var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", selector)
        time.sleep(1)

    def select_OriginField(self, driver):
        selector = driver.find_element_by_xpath('//*[@id="search-bar"]/div[1]/button[2]')
        driver.execute_script("var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", selector)
        time.sleep(1)

    def select_EditButton(self, driver):
        selector = driver.find_element_by_xpath('//*[@id="primary-container"]/div[1]/header/nav/div[2]/div[1]/div[2]/div[2]/button')
        driver.execute_script("var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", selector)
        time.sleep(1)

    def select_Find(self, driver):
        selector = driver.find_element_by_xpath('//*[@id="search-bar"]/div[5]/button')
        driver.execute_script("var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", selector)
        time.sleep(1)

    def select_Date(self, driver):
        selector = driver.find_element_by_xpath('//*[@id="datepicker"]/div/div[3]/calendar[1]/div/div/div[10]/button')
        driver.execute_script("var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", selector)
        time.sleep(1)

    def select_Destination(self, driver, origin=1):
        selector = driver.find_element_by_xpath('//*[@id="search-bar"]/div[2]/div/div[1]/div[2]/div/ul/li[{}]/strong/span'.format(origin))
        driver.execute_script("var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", selector)
        time.sleep(1)

    def select_Origin(self, driver, origin=1):
        selector = driver.find_element_by_xpath('//*[@id="search-bar"]/div[1]/div/div[1]/div[2]/div/ul/li[{}]/strong/span'.format(origin))
        driver.execute_script("var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", selector)
        time.sleep(1)

    def get_Destinations(self, driver):
        container_list = driver.find_element_by_xpath('//*[@id="search-bar"]/div[2]/div/div[1]/div[2]/div/ul')
        options = container_list.find_elements_by_xpath('.//li/strong/span')
        destionations = [elem.text for elem in options]
        return destionations

    def get_Origins(self, driver):
        container_list = driver.find_element_by_xpath('//*[@id="search-bar"]/div[1]/div/div[1]/div[2]/div/ul')
        options = container_list.find_elements_by_xpath('.//li/strong/span')
        origins = [elem.text for elem in options]
        return origins

    def check_StatusPage(self, driver):
        not_resolved = 0
        print('check status')
        url = driver.current_url
        while True:
            driver.get(url)
            print(not_resolved, url)
            html_source = driver.page_source
            errors = [
                'ERR_NAME_NOT_RESOLVED',
                'ERR_CONNECTION_REFUSED',
                'ERR_CONNECTION_TIMED_OUT'
            ]
            if errors[0] in html_source:
                not_resolved += 1
            elif errors[1] in html_source:
                not_resolved += 1
            elif errors[2] in html_source:
                not_resolved += 1
            else:
                break

            if not_resolved >= 5:
                return False
        return True

    def start_Driver(self):
        BASE_DIR = Path(__file__).ancestor(1)
        relative_path = os.path.join(
            BASE_DIR,
            'chromedriver'
        )
        abs_path = os.path.abspath(relative_path)
        driver = webdriver.Chrome(executable_path=abs_path)
        driver.get('https://www.xxxxxxxxxxxxxxxxxx.com.mx')
        print('start_driver')
        driver.implicitly_wait(30)
        return driver


class XXXXXXXXXXSelenium:

    def test(self):
        driver = self.start_Driver()
        self.select_Login(driver)
        window2 = driver.window_handles[1]
        driver.switch_to_window(window2)
        self.set_ClientCode(driver)
        self.select_Login(driver)
        self.set_ClientNIP(driver)
        self.select_NIPContinue(driver)
        time.sleep(60)

    def set_ClientCode(self, driver, code="XXXXXXXXXXXXXXXXX"):
        code_field = driver.find_element_by_id("login.claveCliente")
        code_field.send_keys(code)
        time.sleep(1)

    def set_ClientNIP(self, driver, code="XXXXXXXXXXXXXXXXX"):
        code_field = driver.find_element_by_id("stu.nip")
        code_field.send_keys(code)

    def select_NIPContinue(self, driver):
        selector = driver.find_element_by_xpath('//*[@id="login.Continuar"]')
        driver.execute_script("var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", selector)
        time.sleep(1)

    def start_Driver(self):
        driver = webdriver.Chrome()
        driver.get('https://www.xxxxxxxxxxxxxxxxxx.com.mx/')
        driver.implicitly_wait(20)
        return driver

    def select_Login(self, driver):
        selector = driver.find_element_by_xpath('//*[@id="splg.btnEntrar"]')
        driver.execute_script("var evt = document.createEvent('MouseEvents');" + "evt.initMouseEvent('click',true, true, window, 0, 0, 0, 0, 0, false, false, false, false, 0,null);" + "arguments[0].dispatchEvent(evt);", selector)
        time.sleep(1)