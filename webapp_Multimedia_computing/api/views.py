from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
import os
from api.models import Document
from .Huffman.HuffmanCompress import huffman_compress_main_process
from .Huffman.HuffmanDecompress import huffman_decompress_main_process
from .forms import DocumentForm
from .LZW.lzw_compression import LZW
from .Arithmetic.arithmetic import *


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
        saving_path = '/' + filepath_parts[1] + '/' +filepath_parts[2]
        saving_path = '/' + filepath_parts[1] + '/' +filepath_parts[2] + '/compress_' + request.POST['algorithm'] + '_' + filepath_parts[3][:-4]  + '.ahihi'

        # Paths
        origin_file_path = os.path.join(module_dir, filepath_parts[3])

        compressed_file_path = os.path.join(module_dir,'compress_'+ request.POST['algorithm'] + '_' + filepath_parts[3][:-4]) + '.ahihi'


        # Paths
        origin_file_path = os.path.join(module_dir, filepath_parts[3])

        # select algorithm
        i = 0
        try:
            if request.POST['algorithm'] == 'Huffman':
                #
                # huffman_compress_main_process(uploaded_file_url, saving_path)
                #
                # generate file name
                i = 1
                compression_ratio = huffman_compress_main_process(origin_file_path, compressed_file_path)
            elif request.POST['algorithm'] == 'LZW':
                i = 2
                # generate file name

                # run LZW on origin file and save to compressed file path
                lzw_compress = LZW()
                compression_ratio = lzw_compress.lzw_compression(origin_file_path, compressed_file_path)
            elif request.POST['algorithm'] == 'Arithmetic':
                i = 3
                compression_ratio = arithmetic_compression(origin_file_path, compressed_file_path)

            # module_dir = os.path.dirname(__file__)
            return render(request, 'simple_view_compression.html', {
                'uploaded_file_url': uploaded_file_url,
                'download_path': saving_path,
                'compression_ratio': compression_ratio
            })
        except:
            if i== 1:
                return render(request, 'exceptions.html', {})
            return render(request, 'exceptions.html', {'internal_unicode_error': 1})

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

        try:
            # select algorithm
            if request.POST['algorithm'] == 'Huffman':
                #
                # huffman_compress_main_process(uploaded_file_url, saving_path)
                #
                # generate file name
                huffman_decompress_main_process(origin_file_path, compressed_file_path)
            elif request.POST['algorithm'] == 'LZW':
                # generate file name

                # run LZW on origin file and save to compressed file path
                lzw_compress = LZW()
                lzw_compress.lzw_decompression(origin_file_path, compressed_file_path)
            elif request.POST['algorithm'] == 'Arithmetic':
                arithmetic_decompression(origin_file_path, compressed_file_path)
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


