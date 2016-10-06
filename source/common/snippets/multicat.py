# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms import widgets
from django.utils import six


class PartitionSelectMultiple(widgets.MultiWidget):
    
    def __init__(self, partition_function, attrs=None, empty_label=''):
        self.partition_function = partition_function
        self.empty_label = empty_label
        super(PartitionSelectMultiple, self).__init__([], attrs=attrs)

    def render(self, name, value, attrs=None):
        self.widgets = []
        self.partitions = {}
        pre_partitions = self.partition_function([x[0] for x in self.choices])
        for i, choice in enumerate(self.choices):
            val, partitioner = pre_partitions[i]
            self.partitions.setdefault(partitioner, [])
            self.partitions[partitioner].append(choice)
        for partitioner, pairs in six.iteritems(self.partitions):
            choices = [('', self.empty_label.format(partitioner))]
            for item in pairs:
                choices.append(item)
            self.widgets.append(widgets.Select(choices=choices))
        # NOTE: Hack to make 'decompress' method be called since
        #       decompress is not called if value is a list
        new_value = {'items': value}
        return super(PartitionSelectMultiple, self).render(name, new_value, attrs)
    
    def format_output(self, rendered_widgets):
        output = '<table class="partition-table">'
        labels = self.partitions.keys()
        for i, widget in enumerate(rendered_widgets):
            output += '''
                <tr>
                    <td class="partitioner">%s</td>
                    <td class="choices">%s</td>
                </tr>
            ''' % (labels[i], widget)
        output += '</table>'
        return output

    def decompress(self, value):
        value = value['items']
        count = len(self.partitions.keys())
        if not value:
            return [] * count
        final_list = []
        for partitioner, pairs in six.iteritems(self.partitions):
            found = False
            for val in [x[0] for x in pairs]:
                if val in value:
                    found = True
                    break
            if found:
                final_list.append(six.text_type(val))
            else:
                final_list.append('')
        return final_list

    def value_from_datadict(self, data, files, name):
        items = []
        template = '%s_' % name
        for label, value in six.iteritems(data):
            if label.startswith(template) and value:
                items.append(value)
        return items