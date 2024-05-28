import os  # file paths
import cv2  # image operations
from ultralytics import YOLO  # YOLO
import pytesseract  # OCR
import re 

def clean_extracted_text(text, label):
    if label == 'TOTAL':
        # Cleaning totals
        # Remove except digits, decimal points
        cleaned_text = re.sub(r'[^\d.]', '', text)
        # multiple decimal points, non-numeric 
        if cleaned_text.count('.') > 1:
            # Remove decimal except the first one
            parts = cleaned_text.split('.')
            cleaned_text = parts[0] + '.' + ''.join(parts[1:])
        # Remove non-numeric characters 
        cleaned_text = re.sub(r'\.$', '', cleaned_text)
        return cleaned_text
    elif label == 'INVOICE_NUMBER':
        # Remove characters 
        return text.replace("'", "").strip()
    elif label == 'NAME_CLIENT':
        # Remove quotes 
        return re.sub(r'^\W+|\W+$', '', text.replace('"', ''))
    else:
        return text

def extract_correct_total(extracted_texts):
    total_key = next((key for key in extracted_texts if 'total' in key.lower()), None)
    if total_key:
        total_amount = extracted_texts[total_key]
        cleaned_total = clean_extracted_text(total_amount, 'TOTAL')
        try:
            num = float(cleaned_total)
            # Check if the number is improbably high for an invoice total
            if num > 10000:  
                cleaned_total = f"{cleaned_total[:-3]}.{cleaned_total[-2:]}"
                num = float(cleaned_total)  
            return num
        except ValueError:
            return None 
    return None


def process_image(image_path, threshold=0.5):
    # Define paths for saving the processed image and the extracted text
    image_out_path = '{}_out.jpg'.format(image_path)
    text_out_path = '{}_extracted_text.txt'.format(image_path)

    # Load an image 
    image = cv2.imread(image_path)
    #image = preprocess_image(image)

    model_dir = os.path.join(os.getcwd(), 'Kods', 'Models', 'BEST')
    model_path = os.path.join(model_dir, 'best.pt')
    
    class_colors = {
        'INVOICE NUMBER': (255, 0, 0),  # Blue idk
        'TOTAL': (0, 255, 0),           # Green 
        'INVOICE DATE': (0, 0, 255),    # Red 
        'DUE_DATE': (255, 255, 0),      # Light blue idk
        'NAME_CLIENT':(255, 0, 255),    # Purple
    }

    # Load the YOLO 
    model = YOLO(model_path)

    # Process the image with the model
    results = model(image)[0]
    extracted_texts = {}  

    # Iterate over each detected object
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result  
        if score > threshold:  
            # label name for detected class
            label = results.names[int(class_id)].upper()
            # Round 
            label_text = f"{label}"
            # Default to black 
            color = class_colors.get(label, (0, 0, 0))  
            # Draw a rectangle 
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
            # Put the label text 
            cv2.putText(image, label_text, (int(x1), int(y1 - 10)), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)

            # Crop the detected region from the image
            cropped_image = image[int(y1):int(y2), int(x1):int(x2)]

            custom_config = r'--oem 3 --psm 6'
            # Use pytesseract to extract text from the cropped image
            text = pytesseract.image_to_string(cropped_image, config=custom_config, lang='lav')
            # Clean the extracted text
            clean_text = clean_extracted_text(text.strip(), label)
            # Store the extracted text along with its bounding box in the dictionary
            extracted_texts[label_text] = (clean_text, (int(x1), int(y1), int(x2), int(y2)))

    cv2.imwrite(image_out_path, image)

    with open(text_out_path, 'w') as file:
        for key, value in extracted_texts.items():
            file.write(f"{key}: {value}\n")

    return extracted_texts, image_out_path
