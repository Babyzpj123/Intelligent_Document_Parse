class DocumentParse_PDFPlumber:
    '''使用文档解析工具PDFPlumber对pdf文档进行解析
    '''
    def __init__(self):
        pass
    
    def remove_watermark_from_page(self,page):
        '''去pdf水印逻辑
        '''
        objects = page.objects

        # 新增空白页处理逻辑
        if not objects or 'char' not in objects or len(objects['char']) == 0:
            print("Empty page detected.")
            return page           

        new_chars = []
        try:
            #print("try-objects",len(objects['char']))
            for char in objects['char']:
                if not char['non_stroking_color'] or char['non_stroking_color'][0] == 0:
                    new_chars.append(char)

            page.objects['char'] = new_chars
            return page
        except Exception as e:
            print("except-objects：",objects)
            return page

    def extract_pages_text_table_content(self, page):
        '''解析pdf文档某页内容（包含文本、表格等解析）
        '''
        tables = page.extract_tables()                           # 解析该页的表格
        text = page.extract_text(x_tolerance=3, y_tolerance=10)  # 提取该页内容文本text，通过参数调整最优解析布局

        for table_idx, table in enumerate(tables):
            table_texts = []
            for row in table:
                row_text = " | ".join(cell if cell else '' for cell in row)
                table_texts.append(row_text)

            # Use a unique marker for table replacement
            table_marker = f"###$$$TABLE{table_idx}$$$###"
            text = text.replace(table_texts[0], table_marker, 1)  # Replace first row with marker

            # Replace marker with the full table content
            table_content = "\n".join(table_texts)
            text = text.replace(table_marker, table_content)

        return text

    ## 使用正则表达式替换两个或更多连续的换行符和空白字符为单个换行符
    def clean_newlines(self,text):
        cleaned_text = re.sub(r'\s*\n\s*', '\n', text)
        cleaned_text = re.sub(r'\s*\d+\s*$', '', cleaned_text)   # 剔除文末页码
        return cleaned_text
    
    def extract_content_by_pages(self,pdf_path):
        '''提取pdfpath文件的文本内容
            1. 去水印，剔除pdf每页水印
            2. 提取
        '''
        content_extracted = ""
        with pdfplumber.open(pdf_path) as pdf:
            # for page in pdf.pages[start_page:end_page]:
            for page in pdf.pages:
                page = self.remove_watermark_from_page(page)          # 先对每page去水印
                text = self.extract_pages_text_table_content(page)    # 提取每page的文本内容、表格文本内容
                text = self.clean_newlines(text)                      # 清洗每页文本内容
                content_extracted += text+'\n'
        return content_extracted
        
