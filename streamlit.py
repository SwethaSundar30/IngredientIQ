import streamlit as st
import PyPDF2
def extract_text_from_pdf(uploaded_file):
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        num_pages = len(pdf_reader.pages)

        if num_pages > 3:
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                text += page_text

            return text
        else:
            return "This PDF does not exceed 30 pages."
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    st.title("PDF Text Extractor")
    st.write("Upload a PDF file to extract text.")

    uploaded_file = st.file_uploader("Upload PDF", type="pdf")

    if uploaded_file is not None:
        extracted_text = extract_text_from_pdf(uploaded_file)
        if extracted_text:
            st.subheader("Extracted Text:")
            st.write(extracted_text)
        else:
            st.write("Text extraction failed.")

if __name__ == "__main__":
    main()
