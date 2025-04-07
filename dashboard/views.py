from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.utils.timezone import localtime, now
from django.contrib import messages
from core.models import TblFormDataNew, FeatureToggle, FetchLog
import csv
import io
from datetime import datetime

# ===== Dashboard View =====
def dashboard_view(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', '')
    paginate_by = request.GET.get('paginate_by', '25')

    # Default to local server, or use Heroku if specified
    server_type = 'heroku' if request.GET.get('server_type') == 'heroku' else 'local'

    if paginate_by == 'All':
        paginate_by = None
    else:
        paginate_by = int(paginate_by)

    subscribers = TblFormDataNew.objects.all()

    if query:
        subscribers = subscribers.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )

    if sort == 'email':
        subscribers = subscribers.order_by('email')
    elif sort == 'name':
        subscribers = subscribers.order_by('first_name', 'last_name')

    total_count = subscribers.count()

    if paginate_by:
        page = int(request.GET.get('page', 1))
        start = (page - 1) * paginate_by
        end = start + paginate_by
        paginated = subscribers[start:end]
    else:
        page = 1
        paginated = subscribers

    return render(request, 'dashboard/index.html', {
        'subscribers': paginated,
        'query': query,
        'sort': sort,
        'page': page,
        'paginate_by': request.GET.get('paginate_by', '25'),
        'total_count': total_count,
        'server_type': server_type  # Pass server type to template
    })

# ===== CSV Import with Encoding Fallback =====
def import_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        file = request.FILES['csv_file']
        try:
            decoded = file.read().decode('utf-8')
        except UnicodeDecodeError:
            file.seek(0)
            decoded = file.read().decode('latin-1')

        io_string = io.StringIO(decoded)
        reader = csv.DictReader(io_string)
        added, skipped = 0, 0

        for row in reader:
            email = (
                row.get('Subscriber', '') or
                row.get('email', '')
            ).strip().lower()

            raw_date = row.get('Subscribed', '').strip()
            try:
                sub_date = datetime.strptime(raw_date, "%Y-%m-%d %H:%M:%S")
            except Exception:
                sub_date = now()

            if email and not TblFormDataNew.objects.filter(email=email).exists():
                TblFormDataNew.objects.create(
                    email=email,
                    first_name=row.get('first_name', '').strip(),
                    last_name=row.get('last_name', '').strip(),
                    subscriber_group=row.get('subscriber_group', '').strip() or 'Imported',
                    shares=int(row.get('shares', 0)),
                    credits=int(row.get('credits', 0)),
                    total_submissions=int(row.get('total_submissions', 0)),
                    decoding_requests=int(row.get('decoding_requests', 0)),
                    subscription_date=sub_date
                )
                added += 1
            else:
                skipped += 1

        messages.success(request, f"Imported {added} subscribers. Skipped {skipped} duplicates.")
    return redirect('dashboard:dashboard_home')

# ===== Clear Table =====
def clear_table(request):
    if request.method == 'POST':
        TblFormDataNew.objects.all().delete()
        messages.success(request, "All subscribers deleted.")
    return redirect('dashboard:dashboard_home')

# ===== Export CSV =====
def export_csv(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', '')
    subscribers = TblFormDataNew.objects.all()

    if query:
        subscribers = subscribers.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )

    if sort == 'email':
        subscribers = subscribers.order_by('email')
    elif sort == 'name':
        subscribers = subscribers.order_by('first_name', 'last_name')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="subscribers.csv"'
    writer = csv.writer(response)
    writer.writerow(['Email', 'First Name', 'Last Name', 'Subscription Date'])

    for sub in subscribers:
        writer.writerow([
            sub.email,
            sub.first_name or '',
            sub.last_name or '',
            localtime(sub.subscription_date).strftime("%Y-%m-%d %H:%M:%S") if sub.subscription_date else ''
        ])
    return response

# ===== Fetch Log View =====
def fetch_log_view(request):
    logs = FetchLog.objects.order_by('-timestamp')[:50]
    return render(request, 'dashboard/fetch_logs.html', {'logs': logs})

# ===== Subscriber Detail View =====
def subscriber_detail(request, pk):
    subscriber = get_object_or_404(TblFormDataNew, pk=pk)
    return render(request, 'dashboard/subscriber_detail.html', {'subscriber': subscriber})

# ===== Edit Subscriber View =====
def edit_subscriber(request, pk):
    subscriber = get_object_or_404(TblFormDataNew, pk=pk)
    if request.method == 'POST':
        subscriber.first_name = request.POST.get('first_name')
        subscriber.last_name = request.POST.get('last_name')
        subscriber.email = request.POST.get('email')
        subscriber.subscriber_group = request.POST.get('subscriber_group')
        subscriber.shares = int(request.POST.get('shares', 0))
        subscriber.credits = int(request.POST.get('credits', 0))
        subscriber.total_submissions = int(request.POST.get('total_submissions', 0))
        subscriber.decoding_requests = int(request.POST.get('decoding_requests', 0))
        subscriber.subscription_date = request.POST.get('subscription_date')

        # Save the updated subscriber object
        subscriber.save()
        messages.success(request, f"Subscriber {subscriber.email} updated successfully.")
        return redirect('dashboard:dashboard_home')
    return render(request, 'dashboard/edit_subscriber.html', {'subscriber': subscriber})

# ===== Delete Subscriber View =====
def delete_subscriber(request, pk):
    subscriber = get_object_or_404(TblFormDataNew, pk=pk)
    if request.method == 'POST':
        subscriber.delete()
        return redirect('dashboard:dashboard_home')
    return render(request, 'dashboard/confirm_delete.html', {'subscriber': subscriber})

# ===== Toggle Scheduler View =====
def toggle_scheduler(request):
    toggle, created = FeatureToggle.objects.get_or_create(name='scheduler_enabled')
    toggle.enabled = not toggle.enabled
    toggle.save()
    return redirect('dashboard:dashboard_home')


