import json
import scrapy


class spider(scrapy.Spider):
    name = 'caoThuoc3' 
    start_urls = [
                'https://www.thuocbietduoc.com.vn/nhom-thuoc-1-0/thuoc-gay-te-me.aspx',
                'https://www.thuocbietduoc.com.vn/nhom-thuoc-2-1/giam-dau-ha-sot-chong-viem.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-3-2/thuoc-chong-di-ung.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-4-3/thuoc-cap-cuu--giai-doc.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-5-4/thuoc-huong-tam-than.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-6-5/thuoc--tri-ky-sinh-trung-chong-nhiem-khuan.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-7-6/dieu-tri-dau-nua-dau.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-8-7/thuoc-chong-ung-thu.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-9-8/thuoc-duong-tiet-nieu.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-9-8/thuoc-duong-tiet-nieu.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-11-10/tac-dung-doi-voi-mau.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-12-11/mau-dung-dich-cao-phan-tu.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-13-12/thuoc-tim-mach.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-14-13/thuoc-tri-benh-da-lieu.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-15-14/thuoc-dung-chan-doan.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-16-15/thuoc-sat-khuan.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-17-16/thuoc-loi-tieu.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-18-17/thuoc-duong-tieu-hoa.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-19-18/hocmon-noi-tiet-to.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-20-19/huyet-thanh--globulin-mien-dich.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-21-20/thuoc-gian-co-va-tang-truong-luc-co.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-22-21/thuoc--mat-tai-mui-hong.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-23-22/thuoc-co-tac-dung-thuc-de.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-24-23/dd-tham-phan-phuc-mac.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-25-24/thuoc-ho-hap.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-26-25/dd-dieu-chinh-nuoc-dien-giai.aspx',
                  'https://www.thuocbietduoc.com.vn/nhom-thuoc-27-26/khoang-chat-va-vitamin.aspx',
                  ]
    
    def __init__(self):
        self.names = set()
        self.links = set()
        self.categories = {}
        # Create the output directory structure
        import os
        os.makedirs("caoThuoc/caoThuoc/save", exist_ok=True)
        with open("caoThuoc/caoThuoc/save/comments.json", "w", encoding="utf-8") as f:
            pass

    def parse(self, response):
        nhom_thuoc = response.css('span#Drugnews1_lblS_inf b::text').get()
        
        # Initialize category if not exists
        if nhom_thuoc not in self.categories:
            self.categories[nhom_thuoc] = []

        for products in response.css('h2'):
            name = products.css('a.textlink01_v::text').get()
            if not name:
                continue
            name = name.strip()
            link = response.urljoin(products.css('a.textlink01_v::attr(href)').get())

            if name in self.names or 'test' in name.lower():
                continue
            self.names.add(name)

            if link in self.links:
                continue
            self.links.add(link)

            yield response.follow(
                 link,
                 callback=self.parse_detail,
                 meta={'name': name, 'url': link, 'nhom_thuoc': nhom_thuoc}
                )
            
        current_page = int(response.meta.get('page', 1)) 
        viewstate = response.xpath('//input[@id="__VIEWSTATE"]/@value').get()
        
        next_page_link = response.xpath(f'//a[contains(@href, "setValue({current_page + 1},")]/@href').get()
        
        if next_page_link:
            yield scrapy.FormRequest(
                url=response.url,
                formdata={
                    '__VIEWSTATE': viewstate,
                    'page': str(current_page + 1),
                    'currentView': '1'
                },
                callback=self.parse,
                meta={'page': current_page + 1}
            )
            

    def parse_detail(self, response):
        name = response.meta['name']
        url = response.meta['url']
        nhom_thuoc = response.meta['nhom_thuoc']

        # Initialize variables with default values
        thanh_phan = []
        merged = []

        # Extract components from the page
        details = response.css('span.textdetaildrgI')
        if details:
            thanh_phan = details.css('a.texttplink::text').getall() + self.extract_components(response.css('span.textdetaildrgI::text').getall())
        
        # Process the components
        for item in thanh_phan:
            if item.startswith('(') or item.endswith(')'):
                if merged:
                    merged[-1] += " " + item
                else:
                    merged.append(item)

            elif len(thanh_phan) == 2 and item == "hydroclorid":
                if merged:
                    merged[-1] += " " + item
                else:
                    merged.append(item)
            else:
                merged.append(item)

                        
        # Extract other medicine information
        nhom_thuoc1 = response.css('a.textdetaillink::text').get()
        dang_bao_che = response.xpath('//span[@class="textdetailhead1"][contains(text(), "Dạng bào chế")]/following-sibling::span[@class="textdetaildrg"]/text()').get()
        SDK = response.xpath('//span[@class="textdetailhead1"][contains(text(), "SĐK:")]/following-sibling::span[@class="textdetaildrg"]/text()').get()
        dong_goi = response.xpath('//span[@class="textdetailhead1"][contains(text(), "Đóng gói:")]/following-sibling::span[@class="textdetaildrg"]/text()').get()
        nha_san_xuat = response.css('span.compst_link01_s1b::text').get()
        nha_dang_ki = response.css('span.compst_link01_s2b::text').get()

        # Extract detailed information sections
        chi_dinh = self.extract_content(response.xpath('//section[@id="chi-dinh"]'))

        lieu_luong_cach_dung_section = response.xpath('//section[@id="cach-dung"]')
        lieu_luong_cach_dung = None
        if lieu_luong_cach_dung_section:
            raw_text = lieu_luong_cach_dung_section.css('div.textdetaildrg1 div div::text').getall() 
            if not raw_text:
                raw_text = lieu_luong_cach_dung_section.css('div.textdetaildrg1 div::text').getall()
            if not raw_text: 
                raw_text = lieu_luong_cach_dung_section.css('div.textdetaildrg1::text').getall()
            lieu_luong_cach_dung = self.clean_text(raw_text)

        chong_chi_dinh = self.extract_content(response.xpath('//section[@id="chong-chi-dinh"]'))
        tac_dung_phu = self.extract_content(response.xpath('//section[@id="tac-dung-phu"]'))
        de_phong = self.extract_content(response.xpath('//section[@id="de-phong"]'))
        bao_quan = self.extract_content(response.xpath('//section[@id="bao-quan"]'))

        # Create medicine data
        data = {
            'nhom_thuoc': nhom_thuoc1,
            'ten_thuoc': name,
            'dang_bao_che': dang_bao_che or 'None',
            'dong_goi': dong_goi or 'None',
            'thanh_phan': self.clean_text(merged),
            'SDK': SDK,
            'nha_san_xuat': nha_san_xuat,
            'nha_dang_ki': nha_dang_ki,
            'chi_dinh': chi_dinh,
            'lieu_luong_va_cach_dung': lieu_luong_cach_dung,
            'chong_chi_dinh': chong_chi_dinh,
            'tac_dung_phu': tac_dung_phu,
            'de_phong': de_phong,
            'bao_quan': bao_quan,
        }
        
        # Add to categories
        if nhom_thuoc in self.categories:
            self.categories[nhom_thuoc].append(data)

    def closed(self, reason):
        """Called when spider finishes - create separate JSON file for each category"""
        import os
        import re
        
        # Create directory if it doesn't exist
        os.makedirs("/Users/vohaison/Documents/crawlData/caoThuoc/caoThuoc/save", exist_ok=True)
        
        for category_name, medicines in self.categories.items():
            # Clean category name for filename (remove special characters)
            safe_filename = re.sub(r'[^\w\s-]', '', category_name) if category_name else 'unknown'
            safe_filename = re.sub(r'[-\s]+', '_', safe_filename)
            filename = f"caoThuoc/caoThuoc/save/{safe_filename}.json"
            
            # Write medicines for this category as a flat list
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(medicines, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Saved {len(medicines)} medicines to {filename}")
        
        self.logger.info(f"Total categories saved: {len(self.categories)}")

    def extract_components(self, set):
        components = []
        component = None

        if not set:
            return []
        
        for i in set:
            lines = i.split(';')
            for line in lines:
                if not line.strip('.') or ':' in line:
                    continue
                cleaned_line = line.replace('…', '').replace('.', '')
                if len(cleaned_line) > 0 and cleaned_line[0].isdigit(): 
                    continue
                num_start = None
                for j, char in enumerate(cleaned_line):
                    if char.isdigit():
                        num_start = j
                        break
                if num_start is not None:
                    component = cleaned_line[:num_start].strip()
                    if component:
                        components.append(component)
        return components
    
    def clean_text(self, set):
        if not set:
            return None
        cleaned = [text.strip() for text in set if text.strip()]
        return "\n".join(cleaned) if cleaned else None
    
    def extract_content(self, section):
        if section:
            raw_text = section.css('div.textdetaildrg1 div div::text').getall() 
            if not raw_text:
                raw_text = section.css('div.textdetaildrg1 div::text').getall()
            if not raw_text: 
                raw_text = section.css('div.textdetaildrg1::text').getall()
            return self.clean_text(raw_text)
        return None
    