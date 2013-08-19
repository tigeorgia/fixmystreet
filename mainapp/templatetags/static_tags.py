# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.utils.translation import ugettext as _

register = template.Library()


@register.simple_tag
def _about_us_sidebar():
    text = _("""
    <h3>About Us </h3>

    FixMyStreet Georgia is run by Transparency International Georgia a Tbilisi-based NGO aiming to promote transparency
    and accountability. TI Georgia is part of the global Transparency International movement.
""")
    return text