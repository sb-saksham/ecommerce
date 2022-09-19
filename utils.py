import random
import string
from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__          # it allows you to set 'Klass' to the actual class of any instance
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def unique_order_id(instance):
    """
    :param instance:The instance of class 
    :return: order id created
    """
    order_new_id = random_string_generator(8)
    Klass = instance.__class__  # it allows you to set 'Klass' to the actual class of any instance
    qs_exists = Klass.objects.filter(order_id=order_new_id).exists()
    if qs_exists:
        return unique_order_id(instance)
    return order_new_id


def unique_key(instance):
    """
    :param instance:The instance of class
    :return: key created
    """
    size = random.randint(25, 30)
    key = random_string_generator(size)
    Klass = instance.__class__  # it allows you to set 'Klass' to the actual class of any instance
    qs_exists = Klass.objects.filter(key=key).exists()
    if qs_exists:
        return unique_order_id(instance)
    return key

