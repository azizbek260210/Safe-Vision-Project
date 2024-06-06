from django.shortcuts import render, redirect
from main import models
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django import template

register = template.Library()


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


@login_required(login_url='auth:sign-in')
def product_list(request):
    categorys = models.Category.objects.all()
    cart = models.Cart.objects.get_or_create(user=request.user, status=1)
    wishlist = models.WishList.objects.filter(user=request.user)

    category_code = request.GET.get('category_id')
    if category_code:
        filter_items = {}
        for key, value in request.GET.items():
            print(key, value)
            if value and not value == '0':
                if key == 'min_price':
                    key = 'price__gte'
                elif key == 'max_price':
                    key = 'price__lte'
                elif key == 'name':
                    key = 'name__icontains'

                filter_items[key] = value
        products = models.Product.objects.filter(**filter_items)
    elif request.GET.get('name'):
        products = models.Product.objects.filter(name__icontains=request.GET.get('name'))
    else:
        products = models.Product.objects.all()

    code = [item.product.code for item in wishlist]
    for product in products:
        value = product.code in code
        setattr(product, 'is_wishlisted', value)

    context = {
        'categorys': categorys,
        'products': paginator_page(products, 6, request),
        'cart': cart,
        'wishlist': wishlist,
        'range': range(5)

    }

    return render(request, 'front/products.html', context)


@login_required(login_url='auth:sign-in')
def category_list(request, id):
    categorys = models.Category.objects.all()
    catg = models.Category.objects.get(id=id)
    products = models.Product.objects.filter(category=catg)
    cart = models.Cart.objects.get_or_create(user=request.user, status=1)
    wishlist = models.WishList.objects.filter(user=request.user)

    code = [item.product.code for item in wishlist]
    for product in products:
        value = product.code in code
        setattr(product, 'is_wishlisted', value)
    context = {
        'categorys': categorys,
        'products': paginator_page(products, 8, request),
        'categor': catg,
        'cart': cart,
        'wishlist': wishlist,
        'range': range(5)

    }

    return render(request, 'front/shoplist.html', context)


@login_required(login_url='auth:sign-in')
def index(request):
    categorys = models.Category.objects.all()
    products = models.Product.objects.all()
    cart = models.Cart.objects.get_or_create(user=request.user, status=1)
    wishlist = models.WishList.objects.filter(user=request.user)
    testimonal = models.Review.objects.filter().order_by('-id')[1:6]

    wishlisted_codes = [item.product.code for item in wishlist]
    for product in products:
        v = product.code in wishlisted_codes
        setattr(product, 'is_wishlisted', v)

    newproduct = products.order_by('-id')[:4]
    for new in newproduct:
        v = new.code in wishlisted_codes
        setattr(new, 'is_wishlisted', v)

    context = {
        'categorys': categorys,
        'products': paginator_page(products, 8, request),
        'wishlist': wishlist,
        'cart': cart,
        'testimonal': testimonal,
        'newproducts': newproduct,
        'range':range(5)

    }

    return render(request, 'front/index.html', context)


def product_detail(request, code):
    categorys = models.Category.objects.all()
    product = models.Product.objects.get(code=code)
    images = models.ProductImg.objects.filter(product=product.id)
    reviews = models.Review.objects.filter(product=product.id)
    cart = models.Cart.objects.get_or_create(user=request.user, status=1)
    recproducts = models.Product.objects.filter(category=product.category).order_by('-id')[:4]
    wishlist = models.WishList.objects.filter(product=product, user=request.user)
    if wishlist:
        wishlist = wishlist[0]

    wishlists = models.WishList.objects.filter(user=request.user)
    wishlist_codes = [item.product.code for item in wishlists]
    for i in recproducts:
        v = i.code in wishlist_codes
        setattr(i, 'is_wishlisted', v)

    print(product.adv_mark)
    context = {
        'categorys': categorys,
        'product': product,
        'images': images,
        'reviews': reviews,
        'wishlist': wishlist,
        'cart': cart,
        'recproducts': recproducts,
        # 'videos': videos,

    }
    return render(request, 'front/shopdetail.html', context)


@login_required(login_url='auth:sign-in')
def cart_list(request):
    categorys = models.Category.objects.all()
    queryset = models.Cart.objects.filter(user=request.user, status=2)
    cart = models.Cart.objects.get_or_create(user=request.user, status=1)
    context = {
        'categorys': categorys,
        'queryset': queryset,
        'cart': cart,
    }
    return render(request, 'front/carts/list.html', context)


@login_required(login_url='auth:sign-in')
def active_cart(request):
    queryset, _ = models.Cart.objects.get_or_create(user=request.user, status=1)
    return redirect('front:cart', queryset.code)


@login_required(login_url='auth:sign-in')
def cart_detail(request, code):
    categorys = models.Category.objects.all()
    cart = models.Cart.objects.get(code=code)
    queryset = models.CartProduct.objects.filter(cart=cart)

    context = {
        'cart': cart,
        'queryset': queryset,
        'categorys': categorys,
    }

    return render(request, 'front/carts/detail.html', context)


def nima(request, id):
    if request.method == 'POST':
        count = int(request.POST['count'])
        cart_product = models.CartProduct.objects.get(id=id)
        cart_product.count = count
        cart_product.save()
        return redirect('front:cart', cart_product.cart.code)


@login_required(login_url='auth:sign-in')
def cart_product_delete(request, id):
    cart_product = models.CartProduct.objects.get(id=id)
    cart_product.delete()
    return redirect('front:cart', cart_product.cart.code)


@login_required(login_url='auth:sign-in')
def add_cart_product(request, code):
    product = models.Product.objects.get(code=code)
    cart, _ = models.Cart.objects.get_or_create(user=request.user, status=1)
    count = 1
    if models.CartProduct.objects.filter(product=product, cart=cart).count():
        c = models.CartProduct.objects.get(product=product, cart=cart)
        c.count += 1
        c.save()
    else:
        p = models.CartProduct.objects.create(
            product=product,
            cart=cart,
            count=count,
        )

    return redirect('front:cart', cart.code)


@login_required(login_url='auth:sign-in')
def product_order(request):
    cart = models.Cart.objects.get(user=request.user, status=1)
    cart_product = models.CartProduct.objects.filter(cart=cart)
    for item in cart_product:
        item.product.quantity -= item.count
        item.product.save()

    cart.status = 2
    cart.save()

    return redirect('front:order_list')


@login_required(login_url='auth:sign-in')
def order_list(request):
    categorys = models.Category.objects.all()
    queryset = models.Cart.objects.filter(user=request.user, status__in=[2, 3, 4]).order_by('-date')
    context = {
        'queryset': queryset,
        'categorys': categorys,
    }

    return render(request, 'front/order/list.html', context)


@login_required(login_url='auth:sign-in')
def order_confirm(request, code):
    cart = models.Cart.objects.get(code=code, user=request.user)
    cart.status = 4
    cart.save()
    return redirect('front:order_list')


@login_required(login_url='auth:sign-in')
def order_rejection(request, code):
    cart = models.Cart.objects.get(code=code, user=request.user)
    cart.status = 3
    cart.save()
    return redirect('front:order_list')


@login_required(login_url='auth:sign-in')
def order_review(request, code):
    cart = models.Cart.objects.get(code=code, user=request.user)
    products = models.CartProduct.objects.filter(cart=cart)
    if request.method == 'POST':
        for product in products:
            review = models.Review.objects.create(
                product=product.product,
                user=request.user,
                mark=int(request.POST.get('mark')),
                text=request.POST.get('message')
            )

    return redirect('front:order_list')


# ---------WISHLIST---------
@login_required(login_url='auth:sign-in')
def wishlist(request):
    categorys = models.Category.objects.all()
    queryset = models.WishList.objects.filter(user=request.user)

    context = {
        'categorys': categorys,
        'queryset': queryset,
    }

    return render(request, 'front/wishlist.html', context)


@login_required(login_url='auth:sign-in')
def wishlist_delete(request, code):
    wishlist = models.WishList.objects.get(product__code=code, user=request.user)
    if wishlist:
        wishlist.delete()
    else:
        pass
    # return redirect('front:wishlist')
    return redirect(request.META.get('HTTP_REFERER', 'front:wishlis'))


@login_required(login_url='auth:sign-in')
def wishlist_add(request, code):
    product = models.Product.objects.get(code=code)
    models.WishList.objects.create(product=product, user=request.user)
    # return redirect('front:wishlist')
    return redirect(request.META.get('HTTP_REFERER', 'front:wishlis'))
