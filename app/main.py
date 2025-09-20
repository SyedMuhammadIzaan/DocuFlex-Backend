from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import StreamingResponse
import io
import pandas as pd
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

router = APIRouter(prefix="/convert", tags=["File Converter"])

@router.post("/")
async def convert_file(file: UploadFile, target_format: str = Form(...)):
    # Read file content into memory
    content = await file.read()
    input_stream = io.BytesIO(content)
    output_stream = io.BytesIO()

    name, ext = file.filename.rsplit(".", 1)

    # Example conversions
    if ext == "txt" and target_format == "pdf":
        c = canvas.Canvas(output_stream, pagesize=letter)
        text = content.decode("utf-8").splitlines()

        width, height = letter
        x, y = 50, height - 50   # start position (top margin)

        for line in text:
            if y < 50:  # if space is less than bottom margin
                c.showPage()  # create new page
                y = height - 50  # reset y for new page
            c.drawString(x, y, line.strip())
            y -= 15  # move down for next line

        c.save()

    elif ext == "csv" and target_format == "xlsx":
        df = pd.read_csv(input_stream)
        df.to_excel(output_stream, index=False)
        
    elif ext in ["jpg", "jpeg", "png","webp"] and target_format in ["png", "jpg","webp"]:
        img = Image.open(input_stream)
        img.save(output_stream, format=target_format.upper())

    else:
        return {"error": "Unsupported conversion"}

    # Reset stream position before sending
    output_stream.seek(0)

    return StreamingResponse(
        output_stream,
        media_type="application/octet-stream",
        headers={"Content-Disposition": f"attachment; filename={name}.{target_format}"}
    )
