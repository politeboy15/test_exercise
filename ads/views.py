from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from .forms import AdForm
from django.contrib import messages
# Create your views here.
def ad_detail(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    return render(request, 'ads/<int:ad_id>/detail.html', {'ad': ad})

def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect('ad_detail', ad_id=ad.id)
    else:
        form = AdForm()
    return render(request, 'ads/create_ad.html', {'form': form})


def trade_view(request, ad_id):
    if request.method == 'POST':
        user_choice = request.POST.get('choice')

        if user_choice == 'yes':
            if ad.user == user or ad.status != 'active' or user.ads.count() == 0:
                messages.error(request,
                    """You can not trade this ad. Because of the following:<br>
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

