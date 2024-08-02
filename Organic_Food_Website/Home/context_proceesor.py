from django.urls import reverse


def link_reverse(request):
    log_reg = 'Login/Register'
    log_reg_link = reverse('signin')
    
    if request.user.is_authenticated:
        log_reg = request.user.username
        username= request.user.username
        log_reg_link = reverse('account', kwargs={'username': username})
    
    return {
        'log_reg': log_reg,
        'log_reg_link': log_reg_link,
       
    }