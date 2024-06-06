from django.shortcuts import render, redirect
from main import models
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from main.models import User
from main.func import staff_required
from django.db.models import Sum
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def paginator_page(List, num, request):
    paginator = Paginator(List, num)
    pages = request.GET.get('page')
    try:
        lists = paginator.page(pages)
    except PageNotAnInteger:
        lists = paginator.page(1)
    except EmptyPage:
        lists = paginator.page(paginator.num_pages)

    return lists


@staff_required
def index(request):
    products = models.Product.objects.all()
    categorys = models.Category.objects.all()
    datas = {}

    for category in categorys:
        total_quantity = models.Product.objects.filter(category=category).aggregate(total_quantity=Sum('quantity'))[
                             'total_quantity'] or 0
        datas[category] = total_quantity

    data = []
    for d in datas.values():
        data.append(d)

    context = {
        'products': products,
        'category': categorys,
        'datas': data,
    }

    return render(request, 'dashboard/index.html', context)


# ---------CATEGORY-------------

@staff_required
def category_list(request):
    queryset = models.Category.objects.all()

    context = {
        'queryset': queryset
    }
    return render(request, 'dashboard/category/list.html', context)


@staff_required
def category_create(request):
    if request.method == 'POST':
        models.Category.objects.create(
            name=request.POST['name']
        )
        return redirect('dashboard:category_list')
    return render(request, 'dashboard/category/create.html')


@staff_required
def category_update(request, id):
    queryset = models.Category.objects.get(id=id)
    queryset.name = request.POST['name']
    queryset.save()
    return redirect('dashboard:category_list')


@staff_required
def category_delete(request, id):
    queryset = models.Category.objects.get(id=id)
    queryset.delete()
    return redirect('dashboard:category_list')


# ---------PRODUCT----------------
@staff_required
def product_list(request):
    categorys = models.Category.objects.all()
    category_id = request.GET.get('category_id')
    if category_id and category_id != '0':
        queryset = models.Product.objects.filter(category__id=category_id)
        i = models.Category.objects.get(id=category_id)
    else:
        queryset = models.Product.objects.all()
        i = None
    context = {
        'queryset': paginator_page(queryset, 5, request),
        'categorys': categorys,
        'i': i
    }
    return render(request, 'dashboard/product/list.html', context)


@staff_required
def product_detail(request, code):
    queryset = models.Product.objects.get(code=code)
    images = models.ProductImg.objects.filter(product=queryset)
    reviews = models.Review.objects.filter(product=queryset)
    context = {
        'queryset': queryset,
        'images': images,
        'reviews': reviews
    }
    return render(request, 'dashboard/product/detail.html', context)


@staff_required
def product_create(request):
    categorys = models.Category.objects.all()
    context = {'categorys': categorys}
    if request.method == 'POST':
        delivery = True if request.POST.get('delivery') else False

        product = models.Product.objects.create(
            category_id=request.POST['category_id'],
            name=request.POST['name'],
            body=request.POST['body'],
            price=request.POST['price'],
            banner_img=request.FILES['banner_img'],
            quantity=request.POST['quantity'],
            delivery=delivery
        )
        if request.POST.get('discount_price'):
            discount_price = request.POST['discount_price']
            product.discount_price = Decimal(discount_price)
            product.save()
        images = request.FILES.getlist('images')
        for image in images:
            models.ProductImg.objects.create(
                product=product,
                img=image
            )

        videos = request.FILES.getlist('videos')
        for video in videos:
            models.ProductVideo.objects.create(
                product=product,
                video=video
            )

        return redirect('dashboard:product_list')
    return render(request, 'dashboard/product/create.html', context)


@staff_required
def product_update(request, code):
    product = models.Product.objects.get(code=code)
    categorys = models.Category.objects.all()
    images = models.ProductImg.objects.filter(product=product)
    videos = models.ProductVideo.objects.filter(product=product)
    context = {
        'product': product,
        'categorys': categorys,
        'images': images,
        'videos': videos

    }
    if request.method == 'POST':
        delivery = True if request.POST.get('delivery') else False
        product.category.id = request.POST['category_id']
        product.name = request.POST['name']
        product.body = request.POST['body']
        price = request.POST.get('price')
        product.price = Decimal(price)
        if request.POST.get('discount_price'):
            discount_price = request.POST['discount_price']
            product.discount_price = Decimal(discount_price)

        if request.FILES.get('banner_id'):
            product.banner_img = request.FILES['banner_img']
        product.delivery = delivery
        product.save()

        imagess = request.FILES.getlist('images')
        for image in imagess:
            models.ProductImg.objects.create(
                product=product,
                img=image
            )

        videos = request.FILES.getlist('videos')
        for video in videos:
            models.ProductVideo.objects.create(
                product=product,
                video=video
            )

        return redirect('dashboard:product_list')
    return render(request, 'dashboard/product/update.html', context)


@staff_required
def product_delete(request, code):
    product = models.Product.objects.get(code=code)
    product.delete()
    return redirect('dashboard:product_list')


def image_delete(request, id):
    image = models.ProductImg.objects.get(id=id)
    # product = models.Product.objects.get(id=image.product)
    # print(product.id)
    image.delete()

    return redirect('dashboard:product_update', image.product.id)


def video_delete(request, id):
    video = models.ProductVideo.objects.get(id=id)
    video.delete()

    return redirect('dashboard:product_update', video.product.id)


# ---------Enter product----------------

def enter_product_create(request):
    context = {'product': models.Product.objects.all()}
    if request.method == 'POST':
        product = models.Product.objects.get(code=request.POST.get('code'))
        quantity = request.POST.get('quantity')
        quantity = int(quantity)
        # product = request.POST.get('product')
        models.EnterProduct.objects.create(
            product=product,
            quantity=quantity,
        )
    return render(request, 'dashboard/enterproduct/create.html', context)


@staff_required
def enter_product_update(request, code):
    context = {
        'queryset': models.EnterProduct.objects.get(code=code),
        'products': models.Product.objects.all()
    }

    if request.method == 'POST':
        product = request.POST.get('product_id')
        quantity = request.POST.get('quantity')
        quantity = int(quantity)
        a = models.EnterProduct.objects.get(code=code)
        a.product_id = product
        a.quantity = quantity
        a.save()
        return redirect('dashboard:enter_product_list')
    return render(request, 'dashboard/enterproduct/update.html', context)


@staff_required
def enter_product_list(request):
    queryset = models.EnterProduct.objects.all()
    context = {
        'queryset': queryset
    }
    return render(request, 'dashboard/enterproduct/list.html', context)


# def enter_product_detail(request, code):
#     queryset = models.EnterProduct.objects.get(code=code)
#     context = {
#         'queryset': queryset
#     }
#     return render(request, 'dashboard/enterproduct/detail.html', context)

@staff_required
def enter_product_history(request, code):
    kirim = models.EnterProduct.objects.filter(product__code=code)
    chiqim = models.Cart.objects.filter(user=request.user, is_active=False)
    kirim.union(chiqim)
    sorted(kirim, key=lambda k: k.date, reverse=True)
    context = {
        'queryset': kirim
    }

    return render(request, 'dashboard/enterproduct/detail.html', context)


# ---------Settings----------------
@login_required(login_url='auth:sign-in')
def profile_update(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST['username']
        user.email = request.POST['email']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        if request.FILES.get('avatar'):
            user.avatar = request.FILES['avatar']
        user.save()
        return redirect('front:index')
    return render(request, 'dashboard/setting.html', )


@login_required(login_url='auth:sign-in')
def edit_password(request):
    user = request.user
    password = request.POST.get('password')
    password_new = request.POST.get('password_new')
    password_conf = request.POST.get('password_conf')
    if user.check_password(password) and password_new == password_conf:
        user.set_password(password_new)
        user.save()
        return redirect('front:index')
