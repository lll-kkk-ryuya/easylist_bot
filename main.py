from PDFTextExtractor import PDFTextExtractor

import os
import re

def main():
    # PDFファイルのパス
    pdf_path = '学部別pdf/文学部2,3,4.pdf'

    # PDFTextExtractorのインスタンスを作成
    pdf_extractor = PDFTextExtractor(pdf_path)

    # 抽出するページ範囲（目次のページ範囲）
    start_page = 3  # 例: 目次が始まるページ番号
    end_page = 4   # 例: 目次が終わるページ番号
    
    page_offset = 4
    # タイトルとテキストを抽出
    titles_and_texts_list = pdf_extractor.extract_title(start_page, end_page ,page_offset)

    # 結果を出力し、ファイルに保存
    for title, text in titles_and_texts_list:
        print(f"タイトル: {title}\n{text}\n")

        # ファイル名の作成（使用不可の文字を除去）
        filename = re.sub(r'[\\/*?:"<>|]', '', title) + '.txt'

        # テキストファイルとして保存
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(text)

if __name__ == '__main__':
    main()
