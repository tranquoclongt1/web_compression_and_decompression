from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
import os
from api.models import Document
from .Huffman.HuffmanCompress import huffman_compress_main_process
from .Huffman.HuffmanDecompress import huffman_decompress_main_process
from .forms import DocumentForm


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def home(request):
    documents = Document.objects.all()
    return render(request, 'home.html', {'documents': documents})


def compression(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        # todo: server need to receive file name with spaces and unicode characters
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        # file path on server
        module_dir = os.path.dirname(__file__)
        module_dir = os.path.join(module_dir, 'media')
        filepath_parts =  uploaded_file_url.split('/')
        saving_path = '/' + filepath_parts[1] + '/' +filepath_parts[2] + '/compress_' + filepath_parts[3] + '.ahihi'

        # Paths
        origin_file_path = os.path.join(module_dir, filepath_parts[3])

        compressed_file_path = os.path.join(module_dir,'compress_'+ filepath_parts[3]) + '.ahihi'
        #
        # huffman_compress_main_process(uploaded_file_url, saving_path)
        try:
            huffman_compress_main_process(origin_file_path, compressed_file_path)
        except:
            return render(request, 'exceptions.html', {})
        # module_dir = os.path.dirname(__file__)
        return render(request, 'simple_view_compression.html', {
            'uploaded_file_url': uploaded_file_url,
            'download_path': saving_path
        })
    return render(request, 'simple_view_compression.html')

def decompression(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']

        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        # file path on server
        module_dir = os.path.dirname(__file__)
        module_dir = os.path.join(module_dir, 'media')
        filepath_parts =  uploaded_file_url.split('/')
        saving_path = '/' + filepath_parts[1] + '/' +filepath_parts[2] + '/decompress_' + filepath_parts[3] + '.txt'
        # saving_path.replace('%20',' ')

        # Paths
        origin_file_path = os.path.join(module_dir, filepath_parts[3])
        compressed_file_path = os.path.join(module_dir,'decompress_'+ filepath_parts[3]) + '.txt'
        #
        # huffman_compress_main_process(uploaded_file_url, saving_path)
        try:
            huffman_decompress_main_process(origin_file_path, compressed_file_path)

        except:
            return render(request, 'exceptions.html', {})
        # module_dir = os.path.dirname(__file__)
        return render(request, 'simple_view_decompression.html', {
            'uploaded_file_url': uploaded_file_url,
            'download_path': saving_path
        })
    return render(request, 'simple_view_decompression.html')

# Upgrading later
def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DocumentForm()
    return render(request, 'simple_application_view.html', {
        'form': form
    })


