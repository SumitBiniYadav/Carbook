from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from datetime import datetime
from django.conf import settings
import os

def generate_invoice_pdf(booking):
    template_path = 'invoice_template.html'  
    context = {
        'booking': booking,
        'car': booking.car,  # Fetch car details
        'date': datetime.now().strftime('%d-%m-%Y'),
        'image_url': os.path.join(settings.MEDIA_URL, booking.car.cimage.name)  # Car image
    }

    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename=invoice_{booking.id}.pdf'

    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(html.encode("UTF-8")), dest=result)
    
    if not pdf.err:
        response.write(result.getvalue())
        return response
    return None
