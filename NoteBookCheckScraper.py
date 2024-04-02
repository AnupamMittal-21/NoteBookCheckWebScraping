from telnetlib import EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def analyseDisplayInformation(displayAdditionalInfo):
    displayInfo = displayAdditionalInfo.split("\n")
    displayDetails = {}
    for info in displayInfo:
        if "Brightness" in info:
            displayDetails["Brightness Distribution"] = info.split("Distribution")[1].strip(" ")
        if "Center" in info:
            displayDetails["Center"] = info.split("Battery")[1].strip(" ")
        if "Contrast" in info:
            displayDetails["Contrast"] = info.split("Contrast")[1].strip(" ")
        if "Color" in info:
            displayDetails["Color Space"] = info.split("Color")[1].strip(" ")
        if "Greyscale" in info:
            displayDetails["Greyscale"] = info.split("Greyscale")[1].strip(" ")
        if "RGB" in info:
            displayDetails["RGB Balance"] = info.split("RGB")[1].strip(" ")
        if "Display" in info:
            displayDetails["Display"] = info.split("Display")[1].strip(" ")
        if "Gamma" in info:
            displayDetails["Gamma"] = info.split("Gamma")[1].strip(" ")

    return displayDetails


class NoteBookCheck(webdriver.Chrome):

    def __init__(self):
        super().__init__()
        # Properties.
        self.product_name = ""
        self.basic_details = {}
        self.chassis_details = {}
        self.features_details = {}
        self.display_details = {}
        self.hdd_details = {}
        self.mobile_data = {}
        self.dict_keys = ['Product_name',
                          'Processor', 'Graphics adapter', 'Memory', 'Display', 'Storage', 'Weight', 'Links', 'side_1',
                          'side_2', 'SD Card Reader_spec', 'SD Card Reader_value', 'Networking_spec',
                          'Networking_value',
                          'CPU Performance Rating_spec', 'CPU Performance Rating_value', 'Performance Rating_spec',
                          'Performance Rating_value', 'PCMark_10_Score_spec', 'PCMark_10_Score_value', 'Memory_spec',
                          'Memory_value', 'DPC_Latencies_spec', 'DPC_Latencies_value', 'Drive_Performance_spec',
                          'Drive_Performance_value', '3DMark_Performance_spec', '3DMark_Performance_value',
                          'Performance Rating - Percent_spec', 'Performance Rating - Percent_value',
                          'Brightness Distribution', 'Center', 'Contrast', 'Color Space', 'Greyscale', 'RGB Balance',
                          'Display', 'Gamma', 'Display_Display P3 Coverage', 'Display_sRGB Coverage',
                          'Display_AdobeRGB 1998 Coverage', 'Response Times_Response Time Grey 50% / Grey 80% *',
                          'Response Times_Response Time Black / White *', 'Response Times_PWM Frequency',
                          'Screen_Brightness middle', 'Screen_Brightness', 'Screen_Brightness Distribution',
                          'Screen_Black Level *', 'Screen_Contrast', 'Screen_Colorchecker dE 2000 *',
                          'Screen_Colorchecker dE 2000 max. *', 'Screen_Colorchecker dE 2000 calibrated *',
                          'Screen_Greyscale dE 2000 *', 'Screen_Gamma', 'Screen_CCT',
                          'Screen_Total Average (Program / Settings)', 'Sequential Read', 'Sequential Write', '4K Read',
                          '4K Write', '4K-64 Read', '4K-64 Write', 'Access Time Read', 'Access Time Write',
                          'Score Read',
                          'Score Write', 'Score Total']

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.quit()

    def getUrl(self, url):
        self.get(url)

    def scrapName(self):
        try:
            product_name = self.find_element(By.CSS_SELECTOR, "h1").text
            self.product_name = product_name.split("Review")[0]
            print(f"Product Name is {self.product_name}")
        except:
            print("No Product Name Found.")
            pass

        self.mobile_data['Product_name'] = self.product_name

    # Working Perfectly Fine...
    def scrapSpecs(self):
        print("Basic Details")
        self.implicitly_wait(2)
        try:
            element = WebDriverWait(self, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a.nbc_additional_specs_link"))
            )
            element.click()
            self.implicitly_wait(2)
            element.click()
            self.implicitly_wait(2)
        except:
            print("No additional button to click.")
        try:
            specs_elements = self.find_elements(By.CSS_SELECTOR, "div.specs_element")
            for specs_element in specs_elements:
                try:
                    specs = specs_element.find_element(By.CSS_SELECTOR, "div.specs")
                    specs_detail = specs_element.find_element(By.CSS_SELECTOR, "div.specs_details")
                    if specs.text != "":
                        self.basic_details[specs.text] = specs_detail.text
                except:
                    print("Some specs are void because additional specs are not available.")
                    pass

        except:
            print("No specs elements found.")
            pass

        # print(self.basic_details)

    # Working Perfectly Fine...
    def scrapChassis(self):
        print("Chassis Details")
        self.implicitly_wait(2)
        try:
            chassisInfoContainer = self.find_element(By.CSS_SELECTOR,
                                                     "div.csc-textpic.csc-textpic-center.csc-textpic-below")
            chassisInfoList = chassisInfoContainer.find_elements(By.CSS_SELECTOR,
                                                                 "div.csc-textpic-center-inner div.csc-textpic-imagerow figcaption")
            for i, chassisInfo in enumerate(chassisInfoList):
                self.chassis_details[f"side_{i + 1}"] = chassisInfo.text
        except:
            print("No chassis info found.")
        # print(self.chassis_details)

    # Working Perfectly Fine...
    def scrapSDCard(self):
        try:
            class_pattern = "r_compare_benchmark_"
            element = self.find_element(By.XPATH, f"//*[contains(@class, '{class_pattern}')]")
            try:
                headers = element.find_elements(By.CSS_SELECTOR, "td.settings_header")
                values = element.find_elements(By.CSS_SELECTOR, "tr.chart.referencespecs")

                for i, j in headers, values:
                    print("##############################################")
                    print(i.text, j.text)
                    print("##############################################")
            except:
                print("No Information of SD Card Found.")
        except:
            print("No SD Card Info Found.")

    # Working Perfectly Fine...
    def scrapDetailTables(self):
        try:
            elements = self.find_elements(By.CSS_SELECTOR, "table.r_compare_bars")
            for element in elements:
                try:
                    targetElement = element.find_element(By.CSS_SELECTOR, "td.prog_header")
                    headerName = targetElement.text
                    if headerName != "":
                        detailRows = element.find_elements(By.CSS_SELECTOR, "tr.chart.referencespecs")
                        for detailRow in detailRows:
                            headerSpec = detailRow.find_element(By.CSS_SELECTOR, "span.r_compare_bars_specs").text
                            headerValue = detailRow.find_element(By.CSS_SELECTOR, "td span.r_compare_bars_value").text
                            if "PCMark 10" in headerName:
                                self.features_details["PCMark_10_Score_spec"] = headerSpec
                                self.features_details["PCMark_10_Score_value"] = headerValue
                            elif "Memory" in headerName:
                                self.features_details["Memory_spec"] = headerSpec
                                self.features_details["Memory_value"] = headerValue
                            elif "DPC Latencies" in headerName:
                                self.features_details["DPC_Latencies_spec"] = headerSpec
                                self.features_details["DPC_Latencies_value"] = headerValue
                            elif "Drive Performance" in headerName:
                                self.features_details["Drive_Performance_spec"] = headerSpec
                                self.features_details["Drive_Performance_value"] = headerValue
                            elif "3DMark Performance" in headerName:
                                self.features_details["3DMark_Performance_spec"] = headerSpec
                                self.features_details["3DMark_Performance_value"] = headerValue
                            else:
                                self.features_details[headerName + "_spec"] = headerSpec
                                self.features_details[headerName + "_value"] = headerValue
                except:
                    print("No Detailed Info Found.")
        except:
            print("No Networking Table Found.")

        # print(self.features_details)

    # Working Perfectly Fine...
    def scrapDisplay(self):
        self.implicitly_wait(3)
        targetElementIndex = 1
        try:
            displayAdditionalInfo = self.find_element(By.CSS_SELECTOR, "div.auto_analysis").text
            self.display_details = analyseDisplayInformation(displayAdditionalInfo)
        except:
            print("No Display Info Found.")

        self.implicitly_wait(2)
        try:
            displayTable = self.find_element(By.CSS_SELECTOR, "table.contenttable.comparetable")
            displayTableHeaders = displayTable.find_elements(By.CSS_SELECTOR, "tbody>tr>th")
            for index, displayTableHeader in enumerate(displayTableHeaders):
                try:
                    headingText = displayTableHeader.find_element(By.CSS_SELECTOR, "a").text
                    spanText = displayTableHeader.find_element(By.CSS_SELECTOR, "span").text
                    if self.product_name in headingText:
                        targetElementIndex = index
                        break
                except:
                    print("No details in Header")
        except:
            print("unable to find Display Table")

        try:
            displayTable = self.find_element(By.CSS_SELECTOR, "table.contenttable.comparetable")
            displayTableRows = displayTable.find_elements(By.CSS_SELECTOR, "tbody>tr")
            propHeading = ""
            for displayTableRow in displayTableRows:
                try:
                    rowData = displayTableRow.find_element(By.CSS_SELECTOR, "td")
                    rowDataClassValue = rowData.get_attribute("class")
                    if "progname" in rowDataClassValue:
                        propHeading = rowData.text
                    else:
                        rowData = displayTableRow.find_elements(By.CSS_SELECTOR, "td")
                        propName = rowData[0].text
                        propValue = rowData[targetElementIndex].text
                        self.display_details[propHeading + "_" + propName] = propValue
                except:
                    print("No Display Table Data Found.")
        except:
            print("No Display Table Found.")
        # print(self.display_details)

    def scrapHdd(self):
        try:
            hddElements = self.find_elements(By.CSS_SELECTOR, "div.hdddata_container>div")
            for hddElement in hddElements:
                if hddElement.text != "":
                    if (":" in hddElement.text):
                        l1 = hddElement.text.split(":")
                        self.hdd_details[l1[0]] = l1[1].strip(" ")
        except:
            print("Np HDD data found.")

        # print(self.hdd_details)

    def collectData(self):
        print("Final Data.")
        for key in self.dict_keys:
            if key == "Product_name":
                self.mobile_data[key] = self.product_name
            elif key in self.basic_details.keys():
                self.mobile_data[key] = self.basic_details[key]
            elif key in self.chassis_details.keys():
                self.mobile_data[key] = self.chassis_details[key]
            elif key in self.features_details.keys():
                self.mobile_data[key] = self.features_details[key]
            elif key in self.display_details.keys():
                self.mobile_data[key] = self.display_details[key]
            elif key in self.hdd_details.keys():
                self.mobile_data[key] = self.hdd_details[key]
            else:
                self.mobile_data[key] = None

        # for i, j in self.mobile_data.items():
        #     print(i, j)
        print(self.product_name)
        print(self.mobile_data)
        return self.mobile_data
