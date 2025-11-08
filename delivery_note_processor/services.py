# /home/MiguelAeTxio/CampuStudiOnline/delivery_note_processor/services.py
import logging
import os
import json
from pathlib import Path
from .models import DeliveryNote, Vehicle
from django.utils import timezone
from django.conf import settings
from django.db import transaction

# Importaciones para las APIs de Google
from google.cloud import vision
import google.generativeai as genai
from PIL import Image
from google.api_core import exceptions as google_exceptions

# --- Excepción Personalizada para un Control de Errores Robusto ---
class AIServiceError(Exception):
    """Excepción base para errores en los servicios de IA."""
    pass

logger = logging.getLogger(__name__)

# --- Constante para la nueva variable de entorno ---
DELIVERY_NOTE_GEMINI_API_KEY = os.environ.get("DELIVERY_NOTE_GEMINI_API_KEY")

# --- Funciones de Llamada a APIs (Refactorizadas para Robustez) ---

def _extract_text_with_vision_api(image_path: str) -> str:
    """Extrae texto usando Google Cloud Vision y lanza AIServiceError en caso de fallo."""
    try:
        logger.info(f"Vision API: Iniciando OCR para la imagen: {image_path}")
        client = vision.ImageAnnotatorClient()
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)
        
        if response.error.message:
            raise AIServiceError(f"Vision API devolvió un error: {response.error.message}")
            
        full_text = response.full_text_annotation.text
        logger.info("Vision API: Texto extraído con éxito.")
        return full_text if full_text else ""
        
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Error de Permiso en Vision API: {e}", exc_info=True)
        raise AIServiceError("Error de Permiso en Vision API. ¿Está la API 'Cloud Vision API' habilitada?") from e
    except Exception as e:
        logger.error(f"Error crítico en _extract_text_with_vision_api: {e}", exc_info=True)
        raise AIServiceError(f"Error inesperado en Vision API: {e}") from e

def _parse_text_with_gemini(text: str) -> dict:
    """Usa Gemini para analizar el texto y lanza AIServiceError en caso de fallo."""
    if not text:
        return {}
    if not DELIVERY_NOTE_GEMINI_API_KEY:
        raise AIServiceError("La variable de entorno DELIVERY_NOTE_GEMINI_API_KEY no está configurada.")
        
    try:
        logger.info("Gemini Parse: Mecanizando el albarán.")
        genai.configure(api_key=DELIVERY_NOTE_GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash') # <-- MODELO CORRECTO Y ACTUAL
        prompt = f"""
        Analiza el texto de un albarán y extrae la información clave en formato JSON.
        Texto:
        ---
        {text}
        ---
        Formato JSON estricto (si un campo no se encuentra, usa `null`):
        {{
            "company_name": "Nombre", "company_cif": "CIF", "company_address": "Dirección",
            "line_items": [{{"description": "Desc", "quantity": 1, "unit_price": 1.0, "total_price": 1.0}}],
            "subtotal": 1.0, "vat_amount": 1.0, "total_amount": 1.0
        }}
        """
        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        parsed_data = json.loads(cleaned_response)
        logger.info("Gemini Parse: Datos del albarán mecanizados con éxito.")
        return parsed_data
    except json.JSONDecodeError as e:
        logger.error(f"Error de parseo JSON en la respuesta de Gemini: {e}", exc_info=True)
        raise AIServiceError("Fallo al decodificar la respuesta JSON de Gemini.") from e
    except Exception as e:
        logger.error(f"Error crítico en _parse_text_with_gemini: {e}", exc_info=True)
        raise AIServiceError(f"Error inesperado en Gemini (Parse): {e}") from e

def _find_vehicle_code_with_gemini(image_path: str) -> str | None:
    """Usa Gemini Pro Vision para encontrar el código y lanza AIServiceError en caso de fallo."""
    if not DELIVERY_NOTE_GEMINI_API_KEY:
        raise AIServiceError("La variable de entorno DELIVERY_NOTE_GEMINI_API_KEY no está configurada.")

    try:
        logger.info(f"Gemini Find Code: Analizando imagen {image_path}.")
        genai.configure(api_key=DELIVERY_NOTE_GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        image_file = Image.open(image_path)
        
        prompt = """
        Tu tarea es encontrar un código de vehículo en la imagen.
        El código SIEMPRE sigue el formato Letra-Número-Número.
        
        Ejemplos de códigos válidos: A01, M15, T04, F88.
        Ejemplos de texto que NO son códigos válidos: M01.04 (es un artículo), 1234 (es una matrícula), REF-99 (es una referencia).

        Examina la imagen cuidadosamente, busca el código que coincida con el formato Letra-Número-Número.
        Responde ÚNICAMENTE con el código encontrado. Si no encuentras ningún código que cumpla el formato, responde con la palabra 'None'.
        """
        
        response = model.generate_content([prompt, image_file])
        result_text = response.text.strip()
        
        # Validación extra en Python para asegurar el formato antes de devolver
        if result_text and result_text != 'None' and len(result_text) == 3 and result_text[0].isalpha() and result_text[1:].isdigit():
            logger.info(f"Gemini Find Code: Código de vehículo encontrado y validado: {result_text}")
            return result_text
        else:
            logger.warning(f"Gemini Find Code: No se encontró un código válido o la respuesta no pasó la validación. Respuesta: '{result_text}'")
            # Si la IA devuelve algo que no es 'None' pero no cumple el formato, lo registramos pero devolvemos None para evitar errores.
            return result_text if result_text != 'None' else None

    except Exception as e:
        logger.error(f"Error crítico en _find_vehicle_code_with_gemini: {e}", exc_info=True)
        raise AIServiceError(f"Error inesperado en Gemini (Find Code): {e}") from e

def _find_vehicle_in_db(vehicle_code: str) -> Vehicle | None:
    """Busca un vehículo en la BBDD por su código."""
    if not vehicle_code:
        return None
    try:
        vehicle = Vehicle.objects.get(code__iexact=vehicle_code)
        logger.info(f"BBDD: Vehículo {vehicle_code} encontrado: {vehicle}")
        return vehicle
    except Vehicle.DoesNotExist:
        logger.warning(f"BBDD: No se encontró ningún vehículo con el código: {vehicle_code}")
        return None

# --- Función Orquestadora Principal (Refactorizada) ---

def process_delivery_note_image(delivery_note_id: int):
    """Orquesta el proceso completo con manejo de errores robusto."""
    note = None
    try:
        note = DeliveryNote.objects.get(id=delivery_note_id)
        logger.info(f"PROCESO INICIADO para albarán ID: {note.id}")

        full_text = _extract_text_with_vision_api(note.original_image.path)
        structured_data = _parse_text_with_gemini(full_text)
        vehicle_code = _find_vehicle_code_with_gemini(note.original_image.path)
        
        # Guardamos el código extraído inmediatamente para tener trazabilidad
        note.extracted_vehicle_code = vehicle_code
        
        vehicle = _find_vehicle_in_db(vehicle_code)

        # Actualización final basada en si el vehículo fue encontrado
        note.processed_data = {
            'structured_info': structured_data,
            'raw_text': full_text,
        }
        note.vehicle = vehicle
        note.processed_at = timezone.now()

        if vehicle:
            note.status = 'completed'
            logger.info(f"PROCESO COMPLETADO con éxito para albarán ID: {note.id}. Vehículo {vehicle_code} asignado.")
        else:
            note.status = 'needs_review'
            logger.warning(f"PROCESO FINALIZADO CON REVISIÓN PENDIENTE para albarán ID: {note.id}. Código '{vehicle_code}' no encontrado en BBDD.")
        
        note.save()

    except AIServiceError as e:
        # Errores controlados de las APIs
        logger.error(f"Error de servicio de IA procesando albarán ID {delivery_note_id}: {e}", exc_info=True)
        if note:
            note.status = 'error'
            note.processed_data = {'error_message': f"AIServiceError: {e}"}
            note.processed_at = timezone.now()
            note.save()
            
    except Exception as e:
        # Errores inesperados (ej: BBDD, etc.)
        logger.error(f"Error inesperado procesando albarán ID {delivery_note_id}: {e}", exc_info=True)
        if note:
            note.status = 'error'
            note.processed_data = {'error_message': f"UnexpectedError: {e}"}
            note.processed_at = timezone.now()
            note.save()


