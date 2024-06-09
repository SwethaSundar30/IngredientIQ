from paddleocr import PaddleOCR
def read_image(image_path):    
    ocr = PaddleOCR()
    #image_path = "images\lays.jpg"
    result = ocr.ocr(image_path)
    def text_to_list(filename):
      
      with open(filename, "r") as file:
        lines = [line.strip() for line in file.readlines()]

        lines = [line.rstrip(",") for line in lines]
        return lines
    filename = "DataValues.txt"
    ingredients_to_check = text_to_list(filename)
    extracted_ingredient_names = set()
    for line in result:
        line_text = ' '.join([word[1][0] for word in line])
        for ingredient in ingredients_to_check:
            if ingredient.strip().lower() in line_text.lower():
                extracted_ingredient_names.add(ingredient.strip())
    
    new_extracted_ingredient_names=set()
    for name in extracted_ingredient_names:
        new_extracted_ingredient_names.add(name.lower())
        
    return(new_extracted_ingredient_names)