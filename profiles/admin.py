from django.contrib import admin
from .models import Profile, ProfileImage
from django.core.mail import send_mass_mail

<<<<<<< HEAD
=======
# # Register your models here.
# class OrderLineAdminInline(admin.TabularInline):
#     model = Profile, ProfileImage
    
# class OrderAdmin(admin.ModelAdmin):
#     inlines = (OrderLineAdminInline, )


>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
def verify(modeladmin, request, queryset):
    queryset.update(is_verified='APPROVED')

    emailtuple = ()
    for value in queryset:
<<<<<<< HEAD
        if isinstance(value, Profile):
            emailtuple += (('Your account has been approved', 'We have good news! Your account has been approved, you can now start dating!', 'worlds.best.dating.app@gmail.com', [value.user.email]),)
        else: 
            emailtuple += (('Your profile photo has been approved', 'Thank you for submitting your profile photos. The following image has been approved: "%s"> '% value.image.url, 'worlds.best.dating.app@gmail.com', [value.user.email]),)
                
    send_mass_mail(emailtuple)
        
def reject(modeladmin, request, queryset):
    emailtuple = ()
    
    for value in queryset:
        if isinstance(value, Profile):
            emailtuple = emailtuple + (('Your account has not been approved', 'Unfortunately your bio does not follow our community guidelines. Please update it by editing your profile.', 'worlds.best.dating.app@gmail.com', [value.user.email]),)
        else: 
            emailtuple = emailtuple + (('Your profile photo has been rejected', 'Thank you for submitting your profile photos. However, one of your profile photos do not follow our community guidelines and has been deleted', 'worlds.best.dating.app@gmail.com', [value.user.email]),)
     
    send_mass_mail(emailtuple)
    
    if isinstance(queryset.first(), Profile):
        queryset.update(is_verified='NOT APPROVED')
    else: 
        queryset.delete()
    
=======
        for query in queryset:
            if isinstance(query, Profile):
                emailtuple = emailtuple + (('Your account has been approved', 'yay!', 'matthewdenoronha@gmail.com', [value.user.email]),)
            else: 
                emailtuple = emailtuple + (('Your profile photo has been approved', 'The following image has been approved: "%s"> '% query.image.url, 'matthewdenoronha@gmail.com', [value.user.email]),)
                
    
             
    send_mass_mail(emailtuple)
    
        
def reject(modeladmin, request, queryset):
    queryset.update(is_verified='NOT APPROVED')
    emailtuple = ()
    
    for value in queryset:
        for query in queryset:
            if isinstance(query, Profile):
                emailtuple = emailtuple + (('Your account has not been approved', 'boo!', 'matthewdenoronha@gmail.com', [value.user.email]),)
            else: 
                emailtuple = emailtuple + (('Your profile photo has been rejected', 'The following image has been rejected: "%s"> '% query.image.url, 'matthewdenoronha@gmail.com', [value.user.email]),)
     
    send_mass_mail(emailtuple)
    
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
verify.short_description = "Mark selected as verified"
reject.short_description = "Mark selected as rejected"

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'is_verified')
    list_filter = ('is_verified', )
<<<<<<< HEAD
    readonly_fields = ('id',)
    actions = (verify, reject)
=======
    actions = (verify, reject)
    # list_display_links = ('id', 'title')
>>>>>>> 4efebe4 (Switch from C9 to AWS C9)
    list_per_page = 30
    
admin.site.register(Profile, ProfileAdmin)

class ProfileImageAdmin(admin.ModelAdmin):
    model = ProfileImage
    actions = (verify, reject)
    list_display = ('user', 'image', 'thumbnail', 'is_verified')

    def thumbnail(self, obj):
        return '<img src="{thumb}" width="150" />'.format(thumb=obj.image.url,)
        
    thumbnail.allow_tags = True
    thumbnail.short_description = 'Image'
    
admin.site.register(ProfileImage, ProfileImageAdmin)
