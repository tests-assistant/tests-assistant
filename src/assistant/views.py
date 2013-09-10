from datetime import datetime
from datetime import timedelta

from markdown import markdown

from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator

from taggit.models import Tag
from chartit import DataPool, Chart

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
        return redirect('/')
    page = paginator.page(num_page)
    tags = Test.tags.all().order_by('name')
    ctx = dict(page=page, tests=page.object_list, tags=tags, count=count)
    return render(request, 'assistant/home.html', ctx)


# Test views

def test_add(request):
    if request.method == 'POST':
        form = EditTest(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            test = Test(
                title=data['title'],
                description=data['description'],
                html=markdown(data['description'])
            )
            test.save()
            for tag in map(lambda x: x.lower(), data['tags'].split()):
                test.tags.add(tag)
            return redirect('/test/detail/%s' % test.id)
    form = EditTest()
    ctx = dict(form=form)
    return render(request, 'assistant/test/add.html', ctx)


def test_detail(request, pk):
    test = Test.objects.get(pk=pk)
    current = request.session.get('current', None)
    if current:
        current = Run.objects.get(pk=current)
        # add test to current run if POST 
        if request.method == 'POST':
            if test not in current.tests.all():
                TestInstance(run=current, test=test).save()
            return redirect('/run/detail/%s' % current.pk)
    ctx = dict(test=test, current=current)
    return render(request, 'assistant/test/detail.html', ctx)


def test_edit(request, pk):
    test = Test.objects.get(pk=pk)
    if request.method == 'POST':
        form = EditTest(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            test.title = data['title']
            test.description = data['description']
            test.html = markdown(data['description'])
            test.save()
            test.tags.clear()
            for tag in map(lambda x: x.lower(), data['tags'].split()):
                test.tags.add(tag)
            return redirect('/test/detail/%s' % test.pk)
    form = EditTest()
    ctx = dict(test=test, form=form)
    return render(request, 'assistant/test/add.html', ctx)


def test_delete(request, pk):
    test = Test.objects.get(pk=pk)
    if request.method == 'POST':
        test.delete()
        return redirect('/')
    ctx = dict(test=test)
    return render(request, 'assistant/test/delete.html', ctx)


def test_filter(request):
    pks = request.GET.get('tags', None)
    if not pks:
        return redirect('/')
    all_tags = Test.tags.all().order_by('name')
    pks = map(int, [e for e in pks.split(',') if e])
    tags = map(lambda x: Tag.objects.get(pk=x), pks)
    # manually match all tests tagged like that
    tests = Test.objects.all().order_by('title')
    for pk in pks:
        tests = tests.filter(tags__pk=pk)
    # fetch current if any and if it's POST and them to the run
    current = request.session.get('current', None)
    if current:
        current = Run.objects.get(pk=current)
        if request.method == 'POST':
            for test in tests:
                if test not in current.tests.all():
                    TestInstance(run=current, test=test).save()
            return redirect('/run/detail/%s' % current.pk)

    count = tests.count()
    paginator = Paginator(tests, 30)
    num_page = int(request.GET.get('page', 1))
    if num_page > paginator.num_pages:
        return redirect('/')
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
        return redirect('/run/list')
    page = paginator.page(num_page)
    ctx = dict(page=page, count=count)
    return render(request, 'assistant/run/list.html', ctx)


def run_add(request):
    if request.method == 'POST':
        form = EditRun(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            run = Run(
                title=data['title'],
                version=data['version'].lower(),
            )
            run.save()
            request.session['current'] = run.pk
            return redirect('/run/detail/%s' % run.pk)
    form = EditRun()
    ctx = dict(form=form)
    return render(request, 'assistant/run/edit.html', ctx)


def run_detail(request, pk):
    run = Run.objects.get(pk=pk)
    if request.method == 'POST':
        request.session['current'] = run.pk
        redirect('/run/detail/%s' % run.pk)
    current = request.session.get('current', None)
    instances = TestInstance.objects.filter(run=run)
    count = instances.count()
    paginator = Paginator(instances, 30)
    num_page = int(request.GET.get('page', 1))
    if num_page > paginator.num_pages:
        return redirect('/run/detail/%s' % run.pk)
    page = paginator.page(num_page)    
    not_run_count = instances.filter(ended_at__isnull=True).count()
    # compute total time
    total_time = timedelta()
    for i in instances.filter(ended_at__isnull=False, started_at__isnull=False):
        total_time = i.ended_at - i.started_at + total_time
    ctx = dict(run=run, current=current, count=count, page=page, not_run_count=not_run_count, total_time=total_time)
    return render(request, 'assistant/run/detail.html', ctx)


def run_run(request, pk):
    run = Run.objects.get(pk=pk)
    instances = TestInstance.objects.filter(run=run)
    count = instances.count()
    not_run = instances.filter(ended_at__isnull=True)
    not_run_count = not_run.count()
    done = count - not_run_count + 1
    if not_run_count:
        instance = not_run[0]
        if request.method == 'POST':
            flag = request.POST['flag']
            instance.success = flag == 'ok'
            instance.ended_at = datetime.now()
            instance.save()
            return redirect('/run/detail/%s/running' % run.pk)
    else:
        return redirect('/run/detail/%s' % run.pk)
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

    print xdata, ydata1, ydata2, ydata3
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
