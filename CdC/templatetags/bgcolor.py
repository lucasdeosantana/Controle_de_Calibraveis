from django import template
from django.template.defaultfilters import stringfilter
from datetime import datetime, timedelta, date
register = template.Library()


@register.filter
@stringfilter
def colorBg(validityDateStr):
    validityDate=datetime.strptime(validityDateStr, "%Y-%m-%d").date()
    today=date.today()
    if(validityDate-timedelta(days=45)<today):
        if((validityDate.month - today.month)<=0):
            return "bg-danger"
        else:
            if (today.day>=20):
                return "bg-warning"
    else:
        return ""