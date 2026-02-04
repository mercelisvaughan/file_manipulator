from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from .utils import merge_pdfs, split_pdf, rotate_pdf, protect_pdf, extract_text_from_pdf
import zipfile
import io

def index(request):
    return render(request, 'index.html')

def upload_pdf(request):
    if request.method == 'POST':
        # 1. Get the uploaded files
        files = request.FILES.getlist('pdf_files')
        
        # 2. Get the selected action and extra data
        action = request.POST.get('action')
        
        if not files:
            return HttpResponse("No files selected.", status=400)

        # --- LOGIC MAPPING ---
        
        # CASE 1: MERGE (Takes the whole list of files)
        if action == 'merge':
            # We pass the whole list 'files'
            result_buffer = merge_pdfs(files)
            return FileResponse(
                result_buffer, 
                as_attachment=True, 
                filename="merged_document.pdf"
            )

        # CASE 2: SINGLE FILE ACTIONS (Split, Rotate, Protect)
        # Note: For simplicity, we process only the first file (files[0]).
        # If you want to process ALL uploaded files for rotation, 
        # we would need to loop through them and Zip the results.
        selected_file = files[0]

        if action == 'split':
            mode = request.POST.get('split_mode')
            page_range = request.POST.get('page_range')
            
            # Call the util function
            result = split_pdf(selected_file, mode, page_range)

            # Handle "Burst" mode (returns multiple files -> needs ZIP)
            if mode == 'burst' and isinstance(result, list):
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w") as zf:
                    for name, content in result:
                        zf.writestr(name, content.getvalue())
                zip_buffer.seek(0)
                return FileResponse(zip_buffer, as_attachment=True, filename="split_pages.zip")
            
            # Handle "Range" mode (returns one PDF)
            else:
                return FileResponse(result, as_attachment=True, filename="extracted_pages.pdf")

        elif action == 'rotate':
            angle = request.POST.get('rotation_angle')
            
            # Call the util function
            result_buffer = rotate_pdf(selected_file, angle)
            return FileResponse(
                result_buffer, 
                as_attachment=True, 
                filename="rotated_document.pdf"
            )

        elif action == 'protect':
            password = request.POST.get('password')
            
            # Call the util function
            result_buffer = protect_pdf(selected_file, password)
            return FileResponse(
                result_buffer, 
                as_attachment=True, 
                filename="protected_document.pdf"
            )
        
        elif action == 'scan':
            # Call the util function
            result_buffer = extract_text_from_pdf(selected_file)

            # Return as a .txt file download
            return FileResponse(
                result_buffer, 
                as_attachment=True, 
                filename="extracted_text.txt"
            )

    return render(request, 'upload.html')
