from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderItem
from cart_Checkout.models import Cart, CartItem
from Account_Dashboard.models import ShippingAddress, BillingAddress
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT, TA_CENTER, TA_LEFT
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from django.http import HttpResponse


# Create your views here.

@csrf_exempt
def order_create(request):
    cart = get_object_or_404(Cart, user = request.user)
    cartitem = CartItem.objects.filter(cart = cart)
    order = Order.objects.create(
        user = request.user,
        shipping_address = get_object_or_404(ShippingAddress, user= request.user),
        billing_address = get_object_or_404(BillingAddress, user= request.user),
        total_price = cart.get_total_price(),
    )
    for item in cartitem:
        if item.quantity:
            price = item.product.new_price * item.quantity
        orderitem, Created = OrderItem.objects.get_or_create(
            order = order,
            product = item.product,
            price = price,
            quantity = item.quantity
        )
        item.delete()
        
        
    return redirect('home')





def generate_invoice_pdf(request, order_id):
    order = Order.objects.get(id=order_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="invoice_{order_id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4, rightMargin=20*mm, leftMargin=20*mm, topMargin=20*mm, bottomMargin=20*mm)
    elements = []

    styles = getSampleStyleSheet()

    # Add Company Logo
    logo_path = 'path/to/logo.png'  # Replace with actual logo path
    try:
        logo = utils.ImageReader(logo_path)
        image = Image(logo, width=50*mm, height=20*mm)
        elements.append(image)
    except Exception as e:
        elements.append(Paragraph("Company Logo", styles['Title']))

    # Spacer after logo
    elements.append(Spacer(1, 12))

    # Custom Title Style
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    # Custom Info Style
    info_style = ParagraphStyle(
        'Info',
        parent=styles['Normal'],
        fontSize=12,
        leading=15,
        spaceAfter=10,
    )

    # Title with Advanced Style
    title = Paragraph(f'Invoice for Order #{order.id}', title_style)
    elements.append(title)

    # Customer Information with Advanced Style
    customer_info = Paragraph(
        f'Customer: {order.user.first_name}<br/>Email: {order.user.email}', 
        info_style
    )
    elements.append(customer_info)

    # Add a line divider
    elements.append(Spacer(1, 12))
    elements.append(Paragraph('<hr width="100%" size="1" />', styles['Normal']))
    elements.append(Spacer(1, 12))

    # Table Header Style
    table_header_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ])

    # Table Body Style with Alternating Row Colors
    table_body_style = TableStyle([
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
        ('BACKGROUND', (0, 1), (-1, 1), colors.lightgrey),
    ])

    # Table Data
    table_data = [['Product', 'Quantity', 'Price', 'Total']]
    for item in OrderItem.objects.filter(order=order):
        product_name = item.product.name[:20] + '...' if len(item.product.name) > 20 else item.product.name
        table_data.append([
            product_name, 
            item.quantity, 
            f'${item.product.new_price}', 
            f'${item.quantity * item.product.new_price}'
        ])

    table = Table(table_data, colWidths=[100*mm, 30*mm, 30*mm, 40*mm])
    table.setStyle(table_header_style)
    table.setStyle(table_body_style)

    elements.append(table)

    # Add another line divider
    elements.append(Spacer(1, 12))
    elements.append(Paragraph('<hr width="100%" size="1" />', styles['Normal']))
    elements.append(Spacer(1, 12))

    # Total price
    total_price = sum(item.get_total_price() for item in OrderItem.objects.filter(order=order))
    total_style = ParagraphStyle(
        'Total',
        parent=styles['Heading3'],
        alignment=TA_RIGHT,
        fontSize=14,
        spaceAfter=20,
    )
    elements.append(Paragraph(f'Total: ${total_price}', total_style))

    # Add footer with advanced styling
    footer_style = ParagraphStyle(
        'Footer',
        parent=styles['Normal'],
        fontSize=10,
        alignment=TA_CENTER,
    )
    elements.append(Spacer(1, 30))
    elements.append(Paragraph('Thank you for your business!', footer_style))

    # Watermark
    def add_watermark(canvas, doc):
        canvas.saveState()
        canvas.setFont('Helvetica', 50)
        canvas.setStrokeColorRGB(0.9, 0.9, 0.9)
        canvas.setFillColorRGB(0.9, 0.9, 0.9)
        canvas.drawCentredString(A4[0] / 2, A4[1] / 2, 'PAID')
        canvas.restoreState()

    doc.build(elements, onFirstPage=add_watermark, onLaterPages=add_watermark)
    return response



