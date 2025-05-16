import pytesseract
from PIL import Image
import cv2
import numpy as np
import re

# Create facture instance

def sort_contours_reading_order(contours, tolerance=10):
    bounding_boxes = [cv2.boundingRect(c) for c in contours]
    contours_with_boxes = sorted(zip(contours, bounding_boxes), key=lambda b: b[1][1])

    sorted_contours = []
    current_line = []
    last_y = -2 * tolerance

    for contour, (x, y, w, h) in contours_with_boxes:
        if abs(y - last_y) > tolerance:
            if current_line:
                current_line.sort(key=lambda b: b[1][0])
                sorted_contours.extend([c for c, _ in current_line])
            current_line = [(contour, (x, y, w, h))]
            last_y = y
        else:
            current_line.append((contour, (x, y, w, h)))

    if current_line:
        current_line.sort(key=lambda b: b[1][0])
        sorted_contours.extend([c for c, _ in current_line])

    return sorted_contours


def extract_values_from_list(text_list):
    results = []
    
    # 1. Invoice Number (num_facture)
    invoice_match = re.search(r'Invoice\s+no[:\s]*(\d+)', text_list[0], re.IGNORECASE)
    results.append(invoice_match.group(1) if invoice_match else '')
    
    # 2. Invoice Date (date_facture)
    results.append(text_list[1].strip())
    
    # 3-4. Seller Info (vendeur_nom, vendeur_adresse)
    seller_lines = text_list[2].split('\n')
    results.append(seller_lines[0].strip() if seller_lines else '')
    results.append(' '.join(seller_lines[1:]).strip() if len(seller_lines) > 1 else '')
    
    # 5. Seller Tax ID (vendeur_id_fiscal)
    tax_id_seller = re.search(r'Tax\s*Id:\s*(\d{3}-\d{2}-\d{4})', text_list[4], re.IGNORECASE)
    results.append(tax_id_seller.group(1) if tax_id_seller else '')
      # 9. IBAN (iban)
    iban = re.search(r'IBAN\s*:\s*(.+)', text_list[4], re.IGNORECASE)
    results.append(iban.group(1).strip() if iban else '')
    
    # 6-7. Client Info (client_nom, client_adresse)
    client_lines = text_list[3].split('\n')
    results.append(client_lines[0].strip() if client_lines else '')
    results.append(' '.join(client_lines[1:]).strip() if len(client_lines) > 1 else '')
    
    # 8. Client Tax ID (client_id_fiscal)
    tax_id_client = re.search(r'Tax\s*Id\s*:\s*(.+)', text_list[5], re.IGNORECASE)
    results.append(tax_id_client.group(1).strip() if tax_id_client else '')
    results.append(text_list[-1].strip())
    results.append(text_list[-2].replace('$', '').replace(' ', '').strip())  
    results.append(text_list[-3].replace('$', '').replace(' ', '').strip())  
    results.append(text_list[-4].replace('$', '').replace(' ', '').strip())  

    return results


def extract_produits_from_list(flat_list):
    produits = []
    for i in range(0, len(flat_list), 7):
        bloc = flat_list[i:i+7]
        if len(bloc) == 7:
            produits.append({
                "description": bloc[0].replace('\n', ' ').strip(),
                "quantite": bloc[1].strip(),
                "unite": bloc[2].strip(),
                "prix_unitaire": bloc[3].strip(),
                "valeur_nette": bloc[4].strip(),
                "TVA": bloc[5].strip(),
                "valeur_brute": bloc[6].strip()
            })
    return produits


def extraire_facture_de_liste(flat_list):
    if len(flat_list) < 12:
        return {}

    return {
        "numero_facture": flat_list[0].strip(),
        "date_emission": flat_list[1].strip(),
        "nom_vendeur": flat_list[2].strip(),
        "adresse_vendeur": flat_list[3].strip(),
        "identifiant_fiscal_vendeur": flat_list[4].strip(),
        "iban_vendeur": flat_list[5].strip(),
        "nom_client": flat_list[6].strip(),
        "adresse_client": flat_list[7].strip(),
        "identifiant_fiscal_client": flat_list[8].strip(),
        "taux_tva": flat_list[9].strip(),
        "valeur_nette": flat_list[10].strip(),
        "valeur_brute": flat_list[11].strip()
    }


def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    dilated = cv2.dilate(thresh, kernel, iterations=3)
    return gray, dilated


def extract_facture_data(image):
    gray, dilated = preprocess_image(image)
    contours = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    sorted_cnts = sort_contours_reading_order(contours)

    indices = [0, 2, 5, 6, 7, 8, -1, -2, -3, -8]
    selected_cnts = [sorted_cnts[i] for i in indices]
    results = []

    for c in selected_cnts:
        x, y, w, h = cv2.boundingRect(c)
        roi = gray[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, config='--psm 6').strip()
        results.append(text)
    
    tmp = extract_values_from_list(results)
    return extraire_facture_de_liste(tmp)


def extract_produits_data(image):
    gray, dilated = preprocess_image(image)
    contours = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if len(contours) == 2 else contours[1]
    sorted_cnts = sort_contours_reading_order(contours)

    produit_contours = sorted_cnts[18:-13]
    produit_contours = [produit_contours[i] for i in range(len(produit_contours)) if i % 8 != 0]

    resultss = []
    for c in produit_contours:
        x, y, w, h = cv2.boundingRect(c)
        roi = gray[y:y+h, x:x+w]
        text = pytesseract.image_to_string(roi, config='--psm 6').strip()
        resultss.append(text)

    return extract_produits_from_list(resultss)

