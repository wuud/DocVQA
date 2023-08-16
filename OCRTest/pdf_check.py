# import os
# import pandas as pd
# import pdfplumber
# import PyPDF2
# from PIL import Image
# from paddleocr import PPStructure,PaddleOCR
# import fitz
#
# def load_ocr_model():
#     # 使用默认配置加载PaddleOCR模型
#     ocr = PaddleOCR(use_angle_cls=True, use_gpu=False,lang="ch")
#     return ocr
#
# OCR = load_ocr_model()
#
#
# def is_electronic_pdf(file_path):
#     # Check if the PDF is electronic or scanned image-based
#     with open(file_path, 'rb') as file:
#         pdf_reader = PyPDF2.PdfReader(file)
#         return not pdf_reader.is_encrypted  # If the PDF is not encrypted, it is likely electronic
#
#
# def extract_table_from_pdf(pdf_path, output_csv_path):
#     if is_electronic_pdf(pdf_path):
#         # Extract tables from electronic PDF using pdfplumber
#         with pdfplumber.open(pdf_path) as pdf:
#             all_tables = []
#             for page in pdf.pages:
#                 tables = page.extract_tables()
#                 all_tables.extend(tables)
#
#         # Save tables as CSV files
#         for i, table in enumerate(all_tables):
#             csv_path = output_csv_path.format(page=i + 1)
#             with open(csv_path, 'w') as f:
#                 for row in table:
#                     csv_row = ','.join(str(cell) for cell in row)
#                     f.write(csv_row + '\n')
#
#
#     # doc = fitz.open(filetype='pdf')
#     # # 判断是否为电子版PDF
#     # if is_electronic_pdf(pdf_path):
#     #     # 提取表格并保存为CSV
#     #     all_tables = []
#     #     for page_num in range(doc.page_count):
#     #         page = doc.load_page(page_num)
#     #         with pdfplumber.PDFPage(doc, page_num) as pdf_page:
#     #             tables = pdf_page.extract_tables()
#     #             all_tables.extend(tables)
#     #
#     #         for i, table in enumerate(all_tables):
#     #             csv_path = f"page_{page_num + 1}_table_{i + 1}.csv"
#     #             df = pd.DataFrame(table[1:], columns=table[0])
#     #             df.to_csv(csv_path, index=False)
#
#         print("Tables successfully extracted and saved as CSV.")
#     else:
#         # Convert scanned image-based PDF to image
#         images = []
#         with pdfplumber.open(pdf_path) as pdf:
#             for i, page in enumerate(pdf.pages):
#                 image = page.to_image()
#                 images.append(image)
#                 image_path = f"page_{i + 1}.png"
#                 image.save(image_path)
#
#
#         # OCR on images and save tables as CSV files
#         for i, image in enumerate(images):
#             # text = OCR(images)
#             image_path = f"page_{i + 1}.png"
#             text = OCR.image_to_string(Image.open(image_path))
#             print(text)
#             # Additional logic may be needed here to extract tabular data from OCR output
#             csv_path = output_csv_path.format(page=i + 1)
#             with open(csv_path, 'w') as f:
#                 f.write(text)
#                 print(f"Table from page {i + 1} successfully extracted and saved as CSV.")
#
#         # Cleanup intermediate image files
#         # for i in range(len(images)):
#         #     image_path = f"page_{i + 1}.png"
#         #     os.remove(image_path)
#
#
# if __name__ == "__main__":
#     pdf_file_path = "./data/01-13.pdf"
#     output_csv_path = "./imgs/table_page_{page}.csv"
#
#     extract_table_from_pdf(pdf_file_path, output_csv_path)


import pdfplumber


def is_electronic_pdf(file_path):
    # 使用pdfplumber检查PDF是否为电子版或扫描图像版
    with pdfplumber.open(file_path) as pdf:
        num_pages = len(pdf.pages)
        text_pages = 0
        for page in pdf.pages:
            # 提取页面文本并检查是否存在非空文本，如果存在，则视为电子版PDF
            if page.extract_text().strip():
                text_pages += 1

        # 假设大部分页面都含有文本，则判断为电子版PDF
        return text_pages >= num_pages // 2


# pdf_path = "D:\Desktop\DocVQA数据样例/都城伟业2022中期.pdf"
# is_electronic = is_electronic_pdf(pdf_path)
# if is_electronic:
#     print("这是电子版PDF。")
# else:
#     print("这是扫描图像版PDF。")

#扫描图像版的PDF可能会有一些空白页或没有有效文本的页码。
