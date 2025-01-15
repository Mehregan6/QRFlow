from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO
from PIL import Image, ImageDraw, ImageColor
import logging

# Set up Flask app
app = Flask(__name__)

# Set up logging configuration
logging.basicConfig(
    filename='log.log',  # Log file name
    level=logging.INFO,  # Log level (INFO for basic logs)
    format='%(asctime)s - %(message)s',  # Log format with timestamp
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        # Get data from form
        data = request.form['data']
        color = request.form.get('color', '#000000')  # QR code color
        bg_color = request.form.get('bg_color', '#FFFFFF')  # Background color
        size = int(request.form.get('size', 300))  # Size of the QR code
        format = request.form.get('format', 'png')  # Output format (e.g., PNG)
        gradient = request.form.get('gradient', 'none')  # Gradient option

        # Create the QR code object
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        # Generate the QR code image separately
        img_qr = qr.make_image(fill_color=color, back_color=bg_color).convert('RGB')

        # If gradient is enabled
        if gradient != 'none':
            # Create a gradient from the start color to the background color
            start_color = ImageColor.getrgb(color)
            end_color = ImageColor.getrgb(bg_color)

            # Create a new image with the same size as the QR code
            img = Image.new('RGB', (size, size))
            draw = ImageDraw.Draw(img)

            # Apply gradient from top to bottom
            for i in range(size):
                r = start_color[0] + (end_color[0] - start_color[0]) * i // size
                g = start_color[1] + (end_color[1] - start_color[1]) * i // size
                b = start_color[2] + (end_color[2] - start_color[2]) * i // size
                draw.line((0, i, size, i), fill=(r, g, b))

            # Paste the QR code onto the gradient image
            img.paste(img_qr, (0, 0), img_qr)  # Place the QR code on top of the gradient

        else:
            # If gradient is disabled, just use the QR code image
            img = img_qr

        # Save the image to memory
        buffer = BytesIO()
        img.save(buffer, format=format.upper())
        buffer.seek(0)

        # Log the QR code creation details
        logging.info(f"QR Code generated with data: {data}, Color: {color}, Background: {bg_color}, Size: {size}, Format: {format}")

        # Return the generated image file
        return send_file(buffer, mimetype=f'image/{format}')

    except Exception as e:
        # Log any errors
        logging.error(f"Error generating QR Code: {str(e)}")
        return str(e), 500

if __name__ == '__main__':
    app.run(debug=True)
