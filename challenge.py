import os
import re
from time import sleep
from datetime import timedelta
from RPA.Browser.Selenium import Selenium
from RPA.Excel.Files import Files
from RPA.PDF import PDF


class Challenge:

    def __init__(self, url, agency_to_scrap, dirname):
        self.dirname = dirname
        self.create_default_directory(dirname)
        self.agencies = []
        self.headers = []
        self.investment_data = {
            "uii": [], "bureau": [], "company": [], "final_year": [], "agency_type": [], "rating": [],
            "no_of_project": [], "pdf_match_title": ["PDF Match Title"], "pdf_match_uii": ["PDF Match UII"]
        }
        self.browser = Selenium()
        self.files = Files()
        self.downloader = Selenium()
        self.downloader.set_download_directory(os.path.join(os.getcwd(), f"{self.dirname}"))
        self.browser.open_available_browser(url)
        self.pdf = PDF()
        self.perform_scraping(agency_to_scrap)

    def create_default_directory(self, dirname):
        if not os.path.exists(dirname):
            os.mkdir(dirname)

    def scrap_agencies(self):
        self.browser.wait_until_page_contains_element('//*[@id="node-23"]/div/div/div/div/div/div/div/a')
        self.browser.find_element('//*[@id="node-23"]/div/div/div/div/div/div/div/a').click()
        sleep(3)
        self.agencies = self.browser.find_elements(
            '//div[@id="agency-tiles-widget"]//div[@class="col-sm-4 text-center noUnderline"]')
        companies = ['companies', ]
        investments = ['investments', ]
        for item in self.agencies:
            agency_data = item.text.split('\n')
            companies.append(agency_data[0])
            investments.append(agency_data[2])
        entries = {"companies": companies, "investments": investments}
        wb = self.files.create_workbook(f"{self.dirname}/Agencies.xlsx")
        wb.append_worksheet("Sheet", entries)
        wb.save()

    def get_table_headers(self):
        while True:
            try:
                find_table_header = self.browser.find_element(
                    '//table[@class="datasource-table usa-table-borderless dataTable no-footer"]'
                ).find_element_by_tag_name(
                    "thead").find_elements_by_tag_name("tr")[1].find_elements_by_tag_name("th")
                if find_table_header:
                    break
            except:
                sleep(1)
        for head in find_table_header:
            self.headers.append(head.text)

    def match_text(self, page_text, text_to_find):
        if text_to_find in page_text:
            return True
        return False

    def match_pdf(self, uii, name):
        all_text = self.pdf.get_text_from_pdf(f"{self.dirname}/{uii}.pdf")
        section_a = re.split(r'Bureau:|Section B', all_text[1])[1]
        name_match = self.match_text(section_a, name)
        uii_match = self.match_text(section_a, uii)
        return name_match, uii_match

    def scrap_single_agency(self, agency_to_open):
        agency = self.agencies[agency_to_open]
        url = self.browser.find_element(agency).find_element_by_tag_name("a").get_attribute("href")
        self.browser.go_to(url)
        self.browser.wait_until_page_contains_element('//*[@id="investments-table-object_info"]',
                                                      timeout=timedelta(seconds=50))
        raw_total = self.browser.find_element('//*[@id="investments-table-object_info"]')
        total_entries = raw_total.text.split(" ")[-2]
        self.browser.wait_until_page_contains_element('//*[@id="investments-table-object_length"]/label/select')
        self.browser.find_element('//*[@id="investments-table-object_length"]/label/select').click()
        self.browser.find_element('//*[@id="investments-table-object_length"]/label/select/option[4]').click()
        self.browser.wait_until_page_contains_element(
            f'//*[@id="investments-table-object"]/tbody/tr[{total_entries}]/td[1]', timeout=timedelta(seconds=20))
        self.get_table_headers()
        self.investment_data["uii"].append(self.headers[0])
        self.investment_data["bureau"].append(self.headers[1])
        self.investment_data["company"].append(self.headers[2])
        self.investment_data["final_year"].append(self.headers[3])
        self.investment_data["agency_type"].append(self.headers[4])
        self.investment_data["rating"].append(self.headers[5])
        self.investment_data["no_of_project"].append(self.headers[6])

        for i in range(1, int(total_entries) + 1):
            item = self.browser.find_element(f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[1]')
            self.investment_data["uii"].append(item.text)
            self.investment_data["bureau"].append(self.browser.find_element(
                f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[2]').text)
            self.investment_data["company"].append(self.browser.find_element(
                f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[3]').text)
            self.investment_data["final_year"].append(self.browser.find_element(
                f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[4]').text)
            self.investment_data["agency_type"].append(self.browser.find_element(
                f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[5]').text)
            self.investment_data["rating"].append(self.browser.find_element(
                f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[6]').text)
            self.investment_data["no_of_project"].append(self.browser.find_element(
                f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[7]').text)
            try:
                link = self.browser.find_element(
                    f'//*[@id="investments-table-object"]/tbody/tr[{i}]/td[1]').find_element_by_tag_name(
                    "a").get_attribute("href")
            except:
                link = ''
            match = "--"
            uii_match = "--"
            if link:
                self.downloader.open_available_browser(link)
                self.downloader.wait_until_page_contains_element('//div[@id="business-case-pdf"]')
                self.downloader.find_element('//div[@id="business-case-pdf"]').click()
                while True:
                    if os.path.exists(f"{self.dirname}/{self.investment_data['uii'][i]}.pdf"):
                        break
                    else:
                        sleep(1)
                self.downloader.close_browser()
                (name_match, uii_matched) = self.match_pdf(self.investment_data['uii'][i], self.investment_data['company'][i])
                if name_match:
                    match = f"{self.investment_data['uii'][i]}.pdf"
                if uii_matched:
                    uii_match = f"{self.investment_data['uii'][i]}.pdf"
            self.investment_data['pdf_match_title'].append(match)
            self.investment_data['pdf_match_uii'].append(uii_match)

    def write_investment_file(self):
        work_book = self.files.create_workbook(f"{self.dirname}/Investment.xlsx")
        work_book.append_worksheet("Sheet", self.investment_data)
        work_book.save()

    def perform_scraping(self, agency_to_scrap):
        self.scrap_agencies()
        self.scrap_single_agency(agency_to_scrap)
        self.write_investment_file()


if __name__ == "__main__":
    obj = Challenge("https://itdashboard.gov/", 9, "output")
