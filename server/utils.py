from drf_stripe import models
from django.conf import settings
from django.db.models import QuerySet
from drf_stripe.stripe_api.api import stripe_api
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_list_or_404, get_object_or_404


def all_query(model, *args, **kwargs):
    if isinstance(model, QuerySet):
        return model.all()
    return model.objects.all()


def filter_query(model, *args, **kwargs):
    if isinstance(model, QuerySet):
        return model.filter(*args, **kwargs)
    return model.objects.filter(*args, **kwargs)


def one_query(model, *args, **kwargs):
    if isinstance(model, QuerySet):
        return model.get(*args, **kwargs)
    return model.objects.get(*args, **kwargs)


def update_create_query(model, *args, **kwargs):
    if isinstance(model, QuerySet):
        return model.update_or_create(*args, **kwargs)
    return model.objects.update_or_create(*args, **kwargs)


def get_create_query(model, *args, **kwargs):
    if isinstance(model, QuerySet):
        return model.get_or_create(*args, **kwargs)
    return model.objects.get_or_create(*args, **kwargs)


def prefetch_query(model, *args, **kwargs):
    if isinstance(model, QuerySet):
        return model.prefetch_related(*args, **kwargs)
    return model.objects.prefetch_related(*args, **kwargs)


def select_query(model, *args, **kwargs):
    if isinstance(model, QuerySet):
        return model.select_related(*args, **kwargs)
    return model.objects.select_related(*args, **kwargs)


def join_args(*args, **kwargs):
    chain = kwargs.get("chain", "/")
    replace = kwargs.get("replace", "-")
    return chain.join(args).replace(" ", replace).lower()


def get_model(model, *args, **kwargs):
    return ContentType.objects.get_for_model(model)


def get_or_create_stripe_user(user):
    try:
        print("attempt getting stripe user")
        return models.StripeUser.objects.get(user=user)
    except models.StripeUser.DoesNotExist:
        print("user not found, attempt creating")
        stripe_user = stripe_api.Customer.create(
            email=user.email,
            name=user.get_full_name(),
            phone=user.profile.phone_number if hasattr(user, "profile") else "",
        )
        return models.StripeUser.objects.create(user=user, customer_id=stripe_user.id)
    except Exception as e:
        print(e, "user creation failed")
        raise ValidationError({"detail": str(e)})


def email_user(user, title, template_name, context={}):
    print('sending mail to user', render_to_string(template_name, context))
    if not settings.DEBUG:
        try:
            user.email_user(
                title, "", html_message=render_to_string(template_name, context)
            )
            print('success')
        except Exception as e:
            print(e, 'send email failed')
            raise ValidationError(str(e))


query_one = get_object_or_404

chain_path = join_args
