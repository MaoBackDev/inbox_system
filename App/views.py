from datetime import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.cache import cache_control  # Destruye la sesisón después de hacer logout
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator  # Paginación
from django.db.models import Q   # Codiciones en los filtros (OR)
from django.core.mail import EmailMessage  # Envío correos
from django.contrib.auth import logout  # Auto logout

from .models import Customer
from .forms import CustomerForm, EmailForm


# ====================== FRONTEND VIEWS ================================
def home_view(request):
    return render(request, 'home.html', {})

# FUNCTION TO SEND A MESSAGE
def send_message_view(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, 'Mensaje enviado !')
            return HttpResponseRedirect('/')
    else:
        form = CustomerForm()
        return render(request, 'home.html', {'form': form})


# ====================== BACKEND VIEWS ================================
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def inbox_view(request):
    customer_list = []
    if 'q' in request.GET:
        q = request.GET['q']
        customer_list = Customer.objects.filter(
            Q(name__icontains=q) | Q(phone__icontains=q) |
            Q(email__icontains=q) | Q(subject__icontains=q) |
            Q(status__icontains=q) | Q(message__icontains=q) 
        ).order_by('-created_at')
    else:
        customer_list = Customer.objects.all().order_by('-created_at')

    # Pagination
    paginator = Paginator(customer_list, 6)
    page = request.GET.get('page')
    all_customers = paginator.get_page(page)

    date_current = datetime.now().date()
    print(date_current)
    context = {
        'customers': all_customers,
        'total': Customer.objects.all().count(),
        'read': Customer.objects.filter(status='Read'),
        'pending': Customer.objects.filter(status='Pending'),
        'today': Customer.objects.filter(created_at__gt=date_current)
    }

    return render(request, 'inbox.html', context)


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_message_view(request, id):
    customer = Customer.objects.get(id=id)
    customer.delete()
    messages.success(request, 'Registro Eliminado !')
    return HttpResponseRedirect('/inbox')


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def customer_detail_view(request, id):
    customer = Customer.objects.get(id=id)

    if customer is not None:
        return render(request, 'customer.html', {'customer': customer})


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def mark_message(request):
    if request.method == 'POST':
        customer = Customer.objects.get(id=request.POST.get('id'))
        print(customer)
        if customer is not None:
            customer.status = request.POST.get('status')
            customer.save()
            messages.success(request, 'Mensaje marcado como leído !')
            return HttpResponseRedirect('/inbox')



# RESPONSE A MESSAGE AND SEND EMAIL VIEW
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        company = 'Reply Consultoring'

        # lines add to resolve the change status message
        customer_id = request.POST.get('customer_id')  #
        customer_status = request.POST.get('status')
        customer = Customer.objects.get(id=customer_id)

        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            cc = form.cleaned_data['cc']
            files = request.FILES.getlist('attach')

            mail = EmailMessage(subject, message, company, [email], [cc])

            for file in files:
                mail.attach(file.name, file.read(), file.content_type)
            mail.send()

            # lines add to resolve the change status message
            if customer_status == 'Pending':
                customer.status = 'Read'
                customer.save()

            messages.success(request, 'Respuesta Enviada correctamente!')
            return HttpResponseRedirect('/inbox')
    else:
        form = EmailForm()
        return render(request, {'form', form})


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def auto_logout_user(request):
    logout(request)
    request.user = None
    messages.info(request, '.')  # el mensaje se pasa en el front. se pone . porque el argumento no puede ser vacío
    return HttpResponseRedirect('/')


# =================================  ERROR PAGES ===============================
def error_500(request):
    return render(request, '500.html')


def error_404(request, exception):
    return render(request, '404.html')