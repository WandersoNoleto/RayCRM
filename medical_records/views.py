from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

@csrf_exempt
def create_pdf(request):
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body)
            file_name = data.get('file_name', 'documento')
            file_content = data.get('file_content', '')

            buffer = BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)
            width, height = letter
            p.drawString(72, height - 72, file_content)
            p.save()
            buffer.seek(0)
            
            response = JsonResponse({'success': True})
            response['Content-Disposition'] = f'attachment; filename={file_name}.pdf'
            response.write(buffer.getvalue())
            return response

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

