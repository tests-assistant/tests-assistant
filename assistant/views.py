from datetime import datetime
from datetime import timedelta

from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_POST

from markdown import markdown
from taggit_machinetags.models import MachineTag as Tag

from .forms import EditTest
from .forms import EditRun
from .models import Test
from .models import Run
from .models import TestInstance


# Home view

def home(request):
    count = Test.objects.all().count()
    paginator = Paginator(Test.objects.all().order_by('title'), 30)
    num_page = int(request.GET.get('page', 1))
    if num_page > paginator.num_pages:
        return redirect('assistant-home')
    page = paginator.page(num_page)
    tags = Test.tags.all().order_by('name')
    ctx = dict(page=page, tests=page.object_list, tags=tags, count=count)
    return render(request, 'assistant/home.html', ctx)


# Test views
def test_detail(request, pk):
    test = get_object_or_404(Test, pk=pk)
    try:
        current = request.session.get('current', None)
        current = Run.objects.get(pk=current)
    except Run.DoesNotExist:
        request.session.pop('current', None)
    else:
        # add test to current run if POST
        if request.method == 'POST':
            if test not in current.tests.all():
                TestInstance(run=current, test=test).save()
            return redirect('run-detail', current.pk)
    ctx = dict(test=test, current=current)
    return render(request, 'assistant/test/detail.html', ctx)


def test_edit(request, pk):
    try:
        test_instance = Test.objects.get(pk=pk)
    except:
        test_instance = None

    if request.method == 'POST':
        form = EditTest(request.POST, instance=test_instance) if pk else EditTest(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.html = markdown(form.data['description'])
            test.save()
            test.tags.clear()
            tags = set(['test:%s' % e.lower() for e in form.data['tags'].split(',')])
            for tag in tags:
                test.tags.add(tag)
            return redirect('test-detail', test.pk)
    else:
        form = EditTest(instance=test_instance) if pk else EditTest()
    tags = Tag.objects.filter(namespace='test').order_by('name')
    ctx = dict(test=test_instance, form=form, tags=tags)
    return render(request, 'assistant/test/add.html', ctx)


def test_delete(request, pk):
    test = get_object_or_404(Test, pk=pk)
    if request.method == 'POST':
        test.delete()
        return redirect('assistant-home')
    ctx = dict(test=test)
    return render(request, 'assistant/test/delete.html', ctx)


def test_filter(request):
    pks = request.GET.get('tags', None)
    if not pks:
        return redirect('assistant-home')
    all_tags = Test.tags.all().order_by('name')
    pks = map(int, [e for e in pks.split(',') if e])
    tags = map(lambda x: Tag.objects.get(pk=x), pks)
    # manually match all tests tagged like that
    tests = Test.objects.all().order_by('title')
    for pk in pks:
        tests = tests.filter(tags__pk=pk)
    # fetch current if any and if it's POST and them to the run
    try:
        current = request.session.get('current', None)
        current = Run.objects.get(pk=current)
    except Run.DoesNotExist:
        if 'current' in request.session: request.session.pop('current')
    else:
        if request.method == 'POST':
            for test in tests:
                if test not in current.tests.all():
                    TestInstance(run=current, test=test).save()
            return redirect('run-detail', current.pk)

    count = tests.count()
    paginator = Paginator(tests, 30)
    num_page = int(request.GET.get('page', 1))
    if num_page > paginator.num_pages:
        return redirect('assistant-home')
    page = paginator.page(num_page)
    tests = page.object_list

    ctx = dict(tags=tags, all_tags=all_tags, tests=tests, page=page, count=count, current=current)
    return render(request, 'assistant/test/filter.html', ctx)


# Run views


def run_list(request):
    runs = Run.objects.all()
    count = Run.objects.all().count()
    paginator = Paginator(runs, 30)
    num_page = int(request.GET.get('page', 1))
    if num_page > paginator.num_pages:
        return redirect('run-list')
    page = paginator.page(num_page)
    ctx = dict(page=page, count=count)
    return render(request, 'assistant/run/list.html', ctx)


def run_edit(request, pk=None):
    if request.method == 'POST':
        form = EditRun(request.POST)
        if form.is_valid():
            run = form.save()
            run.tags.clear()
            tags = set(['run:%s' % e.lower() for e in form.data['tags'].split(',')])
            for tag in tags:
                run.tags.add(tag)
            # set it the current run
            request.session['current'] = run.pk
            return redirect('run-detail', run.pk)
    form = EditRun()
    tags = Tag.objects.filter(namespace='run').order_by('name')
    ctx = dict(form=form, tags=tags)
    return render(request, 'assistant/run/edit.html', ctx)


def run_detail(request, pk):
    run = get_object_or_404(Run, pk=pk)
    if request.method == 'POST':
        request.session['current'] = run.pk
        redirect('run-detail', run.pk)
    current = request.session.get('current', None)
    instances = TestInstance.objects.filter(run=run)
    count = instances.count()
    paginator = Paginator(instances, 30)
    num_page = int(request.GET.get('page', 1))
    if num_page > paginator.num_pages:
        return redirect('run-detail', run.pk)
    page = paginator.page(num_page)
    not_run_count = instances.filter(ended_at__isnull=True).count()
    # compute total time
    total_time = timedelta()
    for i in instances.filter(ended_at__isnull=False, started_at__isnull=False):
        total_time = i.ended_at - i.started_at + total_time
    ctx = dict(run=run, current=current, count=count, page=page, not_run_count=not_run_count, total_time=total_time)
    return render(request, 'assistant/run/detail.html', ctx)


def run_run(request, pk):
    run = get_object_or_404(Run, pk=pk)
    instances = TestInstance.objects.filter(run=run)
    count = instances.count()
    not_run = instances.filter(ended_at__isnull=True)
    not_run_count = not_run.count()
    done = count - not_run_count + 1
    if not_run_count:
        instance = not_run[0]
        if request.method == 'POST':
            flag = request.POST['success']
            instance.success = flag == 'ok'
            instance.comment = request.POST['comment']
            instance.html = markdown(request.POST['comment'])
            instance.ended_at = datetime.now()
            instance.save()
            return redirect('run-running', run.pk)
    else:
        return redirect('run-detail', run.pk)
    instance.started_at = datetime.now()
    instance.save()
    test = instance.test
    ctx = dict(run=run, instance=instance, count=count, done=done, test=test)
    return render(request, 'assistant/run/run.html', ctx)


def stats(request):
    instances = TestInstance.objects.all().order_by('run__version').distinct()

    xdata = [e[0] for e in instances.values_list('run__version')]
    ydata1 = [TestInstance.objects.all().filter(run__version=version, success=True).count() for version in xdata]

    ydata2 = [TestInstance.objects.all().filter(run__version=version, success=False).count() for version in xdata]
    ydata3 = [TestInstance.objects.all().filter(run__version=version).count() for version in xdata]

    xaxis = range(len(xdata))
    match = zip(xaxis, xdata)

    chartdata = {
        'x': xaxis,
        'name1': 'passed', 'y1': ydata1,
        'name2': 'failed', 'y2': ydata2,
        'name3': 'total', 'y3': ydata3,
    }
    charttype = "lineWithFocusChart"
    data = {
        'charttype': charttype,
        'chartdata': chartdata,
        'match': match
    }
    return render(request, 'assistant/stats.html', data)
