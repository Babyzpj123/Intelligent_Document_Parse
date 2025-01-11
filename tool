  def download_pdf_document(pdf_url, download_path='./tmp/'):
      '''func:根据文档链接,下载到本地/tmp/
         input: PDF文档超链（wget或点击链接也可下载）
         output: 下载到本地的pdf路径
      '''
      if not os.path.exists(download_path):
          os.makedirs(download_path)

      # 下载PDF文件
      pdf_filename = os.path.join(download_path, pdf_url.split('/')[-1])
      response = requests.get(pdf_url)

      if response.status_code == 200:
          with open(pdf_filename, 'wb') as pdf_file:
              pdf_file.write(response.content)
          print(f"PDF file has been downloaded to {pdf_filename}")
      else:
          print(f"Failed to download file from {pdf_url}")
          return None

      return pdf_filename
