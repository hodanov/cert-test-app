from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from frontend.models import TestResult
import subprocess, re, docker
from OpenSSL import crypto
from Crypto.Util import asn1

def index(request, num=1):
    try:
        if request.method == 'POST' and request.FILES['crt'] and request.FILES['incrt'] and request.FILES['key']:
            certificates = {
                'crt': request.FILES['crt'].read().decode().rstrip(),
                'incrt': request.FILES['incrt'].read().decode().rstrip(),
                'key': request.FILES['key'].read().decode().rstrip(),
            }
            test_result = certificates_test(request, certificates)
            if test_result:
                key = certificates['key']
                crt = certificates['crt'] + '\n' + certificates['incrt']
                upload_crts(crt, key)
                cn = get_cn(certificates)
                create_nginx_config(cn)
                restart_nginx_container()
            else:
                cn = "-"
            is_test_result = TestResult.objects.create(
                common_name=cn,
                filename_crt=request.FILES['crt'].name,
                filename_incrt=request.FILES['incrt'].name,
                filename_key=request.FILES['key'].name,
                is_test_result=test_result
            )
            is_test_result.save()
            return HttpResponseRedirect('/')
    except MultiValueDictKeyError:
        return HttpResponseRedirect('/')

    event_log = TestResult.objects.all().order_by('-tested_at')
    page = Paginator(event_log, 10)
    params = {
        'event_log': page.get_page(num)
    }
    return render(request, 'frontend/index.html', params)

def certificates_test(request, certificates):
    print('Start verify certificates..')
    # Get certificates data
    global crt_x509_object
    crt_x509_object = crypto.load_certificate(crypto.FILETYPE_PEM, certificates['crt'])
    incrt_x509_object = crypto.load_certificate(crypto.FILETYPE_PEM,certificates['incrt'])
    key_pkey_object = crypto.load_privatekey(crypto.FILETYPE_PEM,certificates['key'])

    # Get issuer and subject name
    crt_issuer = crt_x509_object.get_issuer().hash()
    incrt_subject_name = incrt_x509_object.subject_name_hash()

    # Verify CRT and INCRT
    print(f'crt_issuer_hash = {crt_issuer}')
    print(f'incrt_subject_name = {incrt_subject_name}')
    if crt_issuer == incrt_subject_name:
        print('CRT and INCRT are correct.')
        message_context = 'サーバ証明書と中間証明書の組み合わせは正常です。'
        messages.add_message(request, messages.SUCCESS, message_context)
        test_result1 = True
    else:
        print('CRT and INCRT are incorrect.')
        message_context = 'サーバー証明書と中間証明書が一致しませんでした。'
        messages.add_message(request, messages.ERROR, message_context)
        test_result1 = False

    # Get ASN1
    public_key_asn1 = crypto.dump_privatekey(crypto.FILETYPE_ASN1, crt_x509_object.get_pubkey())
    private_key_asn1 = crypto.dump_privatekey(crypto.FILETYPE_ASN1, key_pkey_object)

    # Decode DER
    public_key_der = asn1.DerSequence()
    public_key_der.decode(public_key_asn1)
    private_key_der = asn1.DerSequence()
    private_key_der.decode(private_key_asn1)

    # Get the modulus
    public_key_modulus = public_key_der[1]
    private_key_modulus = private_key_der[1]

    # Verify CRT and KEY
    print(f'public_key_modulus = {public_key_modulus}')
    print(f'private_key_modulus = {private_key_modulus}')
    if public_key_modulus == private_key_modulus:
        print('CRT and KEY are correct.')
        message_context = 'サーバ証明書とプライベートキーの組み合わせは正常です。'
        messages.add_message(request, messages.SUCCESS, message_context)
        test_result2 = True
    else:
        print('CRT and KEY are incorrect.')
        message_context = 'サーバ証明書とプライベートキーが一致しませんでした。'
        messages.add_message(request, messages.ERROR, message_context)
        test_result2 = False

    if test_result1 and test_result2:
        test_result = True
        return test_result
    else:
        test_result = False
        return test_result

def get_cn(certificates):
    print('Get CN...')
    cn = crt_x509_object.get_subject().CN

    print(f'CN = {cn}')
    print('Successful getting CN.')
    return cn

def upload_crts(crt, key):
    print('Upload files...')
    subprocess.check_call('echo \"%s\" > files/certificate.crt' % (crt), shell=True)
    subprocess.check_call('echo \"%s\" > files/certificate.key' % (key), shell=True)
    print('Successful uploading.')
    print('==============================')

def create_nginx_config(cn):
    print('Make a config of Nginx...')
    config = "server {\n"\
                "listen 443 ssl http2;\n"\
                "server_name " + cn + ";\n"\
                "root /usr/share/nginx/html;\n"\
                "ssl_certificate /etc/nginx/conf.d/certificate.crt;\n"\
                "ssl_certificate_key /etc/nginx/conf.d/certificate.key;\n"\
            "}"
    subprocess.check_call('echo \"%s\" > files/vhost.conf' % (config), shell=True)
    print('Successful making a config.')
    print('==============================')

def restart_nginx_container():
    print('Reboot the container of Nginx...')
    container = docker.from_env().containers.get('crt-test-app-nginx')
    container.restart()
    print('Successful rebooting the container.')
    print('==============================')
