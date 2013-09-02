from markdown import markdown

from django.shortcuts import render
from django.shortcuts import redirect
from django.core.paginator import Paginator

from taggit.models import Tag

from .forms import EditTest
from .models import Test


def home(request):
    count = Test.objects.all().count()
    paginator = Paginator(Test.objects.all(), 30)
    num_page = int(request.GET.get('page', 1))
    if num_page > paginator.num_pages:
        return redirect('/')
    page = paginator.page(num_page)
    tags = Test.tags.all()
    ctx = dict(page=page, tests=page.object_list, tags=tags, count=count)
    return render(request, 'assistant/home.html', ctx)


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
    ctx = dict(test=test)
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


def test_filter(request):
    pks = request.GET.get('tags', None)
    if not pks:
        return redirect('/')
    all_tags = Test.tags.all()
    pks = map(int, [e for e in pks.split(',') if e])
    tags = map(lambda x: Tag.objects.get(pk=x), pks)
    # manually match all tests tagged like that
    tests = Test.objects.all()
    for pk in pks:
        tests = tests.filter(tags__pk=pk)
    count = tests.count()
    paginator = Paginator(tests, 30)
    num_page = int(request.GET.get('page', 1))
    if num_page > paginator.num_pages:
        return redirect('/')
    page = paginator.page(num_page)
    tests = page.object_list
    ctx = dict(tags=tags, all_tags=all_tags, tests=tests, page=page, count=count)
    return render(request, 'assistant/test/filter.html', ctx)
