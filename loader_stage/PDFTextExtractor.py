import PyPDF2
import re

class PDFTextExtractor:
    def __init__(self, filepath):
        self.filepath = filepath

    def extract_text(self):
        #全てのpdfファイル内の読み込み
        # PDFファイルをバイナリモードで開く
        with open(self.filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)  # 修正: PdfFileReaderからPdfReaderに変更
            num_pages = len(reader.pages)  # 修正: numPagesからlen(reader.pages)に変更

            # 全ページのテキストを保持するリスト
            all_pages_text = []

            # 各ページからテキストを抽出
            for page_num in range(num_pages):
                page = reader.pages[page_num]  # 修正: getPageからreader.pages[page_num]に変更
                text = page.extract_text()  # 修正: extractTextからextract_textに変更
                all_pages_text.append((page_num + 1, text))

            return all_pages_text
        
    def extract_pages(self, start_page, end_page):
        # 指定されたページ範囲のテキストを抽出
        with open(self.filepath, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            extracted_text = []

            # 開始ページと終了ページを考慮して抽出
            for page_num in range(start_page - 1, end_page):
                page = reader.pages[page_num]
                text = page.extract_text()
                extracted_text.append((page_num + 1, text))

            return extracted_text
        # 使用例
        #pdf_extractor = PDFTextExtractor('path/to/your/document.pdf')
        #start_page = 5  # 開始ページ番号
        #end_page = 10   # 終了ページ番号
        #pages_text = pdf_extractor.extract_pages(start_page, end_page)
        
    def extract_title(self, start_page, end_page, page_offset):
        # 目次ページからテキストを抽出
        pages_text = self.extract_pages(start_page, end_page)
        toc_text = ' '.join([text for _, text in pages_text])

        # 正規表現パターン
        pattern = r'(\d+)[^\S\r\n]+([^\.]+)\.{2,}\s*(\d+)'

        # リスト形式で情報を抽出
        extracted_info = re.findall(pattern, toc_text)

        # 結果を辞書に格納
        titles_to_pages = {entry[1].strip(): entry[2] for entry in extracted_info}

        extracted_texts = {}
        for i, (title, page) in enumerate(titles_to_pages.items()):
            start_page = int(page) + page_offset
            end_page = int(list(titles_to_pages.values())[i + 1]) + page_offset - 1 if i + 1 < len(titles_to_pages) else None
            text = self.extract_pages(start_page, end_page if end_page else start_page + 1)
            extracted_texts[title] = ' '.join([t for _, t in text])

        # 辞書からタイトルとテキストのペアをリストに格納
        titles_and_texts_list = [(title, text) for title, text in extracted_texts.items()]

        return titles_and_texts_list
