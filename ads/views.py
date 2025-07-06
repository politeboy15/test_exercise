from django.shortcuts import render, get_object_or_404, redirect
from .models import Ad
from .forms import AdForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# ✅ Детальный просмотр объявления
def ad_detail_view(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/detail.html', {'ad': ad})


# ✅ Создание объявления
@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_detail', ad_id=ad.id)  # ✅ редирект по имени URL
    else:
        form = AdForm()
    return render(request, 'ads/create_ad.html', {'form': form})  # ✅ правильный шаблон


# ✅ Предложение на обмен
@login_required
def trade_view(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    user = request.user

    if request.method == 'POST':
        user_choice = request.POST.get('choice')

        if user_choice == 'yes':
            if ad.user == user or ad.status != 'active' or not Ad.objects.filter(user=user).exists():
                messages.error(request,
                    """You cannot trade this ad. Because of the following:<br>
                    1) This is your ad<br>
                    2) Ad is not active<br>
                    3) You have no ads<br>
                    4) Ad is sold""")
                return redirect('home')
            else:
                return redirect('trade_page', ad_id=ad.id)

        elif user_choice == 'no':
            messages.info(request, "You chose not to trade.")
            return redirect('home')

    return redirect('home')


# ✅ Страница обмена
@login_required
def trade_page_view(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    user = request.user
    user_ads = Ad.objects.filter(user=user)

    if request.method == 'POST':
        selected_ad_id = request.POST.get('ad')
        selected_ad = get_object_or_404(Ad, id=selected_ad_id, user=user)

        messages.success(request, f"Вы предложили обмен: {selected_ad.title} на {ad.title}")
        return redirect('home')

    return render(request, 'ads/trade_page.html', {
        'ad': ad,
        'user_ads': user_ads
    })
