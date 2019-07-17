import json

from django.db.models.fields import related


def model_to_dict(instance, fields, __raw_name=''):
    """
    获取model内容 并放回json
    :param instance:
    :param fields:
    :param __raw_name:
    :return:
    """
    if instance is None: return
    opts = instance._meta.get_fields(include_parents=True, include_hidden=False)
    resule = dict()

    for f in opts:
        filter_name = __raw_name + f.name
        if filter_name not in fields:
            continue
        if isinstance(f, related.ForeignKey) or isinstance(f, related.OneToOneField):
            resule[f.name] = model_to_dict(getattr(instance, f.name), fields, __raw_name=(__raw_name + f.name + '__'))
        elif isinstance(f, related.ManyToManyField):
            mtm_f = f.value_from_object(instance)
            resule[f.name] = [model_to_dict(mtm, fields, __raw_name=(__raw_name + f.name + '__')) for mtm in mtm_f]
        else:
            data = f.value_from_object(instance)
            if isinstance(data, str) and len(data) > 0 and \
                    ((data[0] == '{' and data[-1] == '}') or (data[0] == '[' and data[-1] == ']')):
                try:
                    data = json.loads(data)
                except:
                    pass
            resule[f.name] = data

    return resule
