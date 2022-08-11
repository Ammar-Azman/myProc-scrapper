import pandas as pd
import time 
from bs4 import BeautifulSoup
import requests
from datetime import date

class Scrapper:
    # extract
    def html_scrap(self, page_number)->str:
            am_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36'}
            myPro_link = 'https://myprocurement.treasury.gov.my/iklan/tender/?pnum={}'.format(page_number)
            html_text = requests.get(myPro_link, headers=am_headers).text

            time.sleep(5)
            return html_text

    def extract_info(self, start:int, end_before:int)->pd.DataFrame:
            tender = []
            pautan = []
            tajuk_list = []
            kemen_list = []
            agensi_list = []
            kategori_list = []
            kod_list = []
            mula_list = []
            akhir_list = []

            all_info = {"No. Tender":tender, 
                "Pautan":pautan,
                "Tajuk": tajuk_list, 
                "Kementerian": kemen_list, 
                "Agensi": agensi_list,
                "Kategori":kategori_list,
                "Kod Bidang":kod_list,
                "Tarikh mula":mula_list,
                "Tarikh akhir":akhir_list}

            for page_num in range(start, end_before):
                html_text = self.html_scrap(page_num)
                soup = BeautifulSoup(html_text, 'lxml')
                card = soup.find_all('div', {'class':'mcs_resultRecord'})
                for item in card:
                    my_card = str(item)

                    # COMPONENT
                    no_tender = my_card[my_card.find('Tender')+7:]
                    no_tender = no_tender[:no_tender.find('</span')]

                    link_ = my_card[my_card.find('href')+6:]
                    link = link_[:link_.find('><')]

                    tajuk_ = my_card[my_card.find('<h4>')+4:]
                    tajuk = tajuk_[:tajuk_.find('</h4>')]

                    kementerian = my_card[my_card.find('Kementerian:')+23:]
                    kementerian = kementerian[:kementerian.find('>A')-22]

                    agensi = my_card[my_card.find('Agensi:')+18:]
                    agensi = agensi[:agensi.find('</div')]

                    kategori = my_card[my_card.find('Kategori Perolehan:')+30:]
                    kategori = kategori[:kategori.find('>Kod')-22]

                    kod_bidang = my_card[my_card.find('Kod Bidang')+22:]
                    kod_bidang = kod_bidang[:kod_bidang.find('class')-25]

                    tarikh_mula = my_card[my_card.find('Tarikh Pelawaan')+27:]
                    tarikh_mula = tarikh_mula[:tarikh_mula.find('Tarikh')-23]

                    tarikh_akhir = my_card[my_card.find('Tarikh Tutup')+54:my_card.find('exp')+20]
                    tarikh_akhir = tarikh_akhir[:tarikh_akhir.find('<')]

                    tender.append(no_tender)
                    pautan.append(link)
                    tajuk_list.append(tajuk)
                    kemen_list.append(kementerian)
                    kategori_list.append(kategori)
                    agensi_list.append(agensi)
                    kod_list.append(kod_bidang)
                    mula_list.append(tarikh_mula)
                    akhir_list.append(tarikh_akhir)

                    time.sleep(3)

            #return all_info

            df_main = pd.DataFrame(all_info)
            df_main['Tarikh Mula'] = pd.to_datetime(df_main['Tarikh mula'], format="%d/%m/%Y")
            df_main = df_main[df_main['Tarikh Mula'] == pd.to_datetime(date.today())]

            df_main = df_main[['No. Tender', 'Pautan', 'Tajuk', 'Kementerian', 'Agensi', 'Kategori',
                                'Kod Bidang', 'Tarikh mula','Tarikh akhir']]
            #df_main.to_csv('tender.csv')
            return df_main