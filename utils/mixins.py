"""
This file contains all the mixins for the project
"""

from copy import copy

from django.db import models
from django.forms import model_to_dict
from django.utils.functional import empty


class ModelDiffMixin(object):
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self._initial = self._dict

    @property
    def diff(self):
        """
        Returns a dictionary showing what has changed from initial to current
        state.

        Initial state is a snapshot of the model's fields when the model
        instance is first loaded from the database, and current state is
        the model's fields at the time ``diff`` is called.

        The dictionary is in the format ``{field_name: (initial, current)}``.
        The ``initial`` and ``current`` values are the initial value of a
        field and its current value.  The field will be excluded if its
        initial and current values are the same.

        If the model instance does not have a primary key, an empty
        dictionary is returned.
        """

        if not self.pk:
            return {}

        d1 = self._initial
        d2 = self._dict
        diffs = [
            (k, (d1.get(k, empty), d2.get(k, empty)))
            for k in set(d1.keys()).union(set(d2.keys()))
            if k not in d1 or k not in d2 or d1[k] != d2[k]
        ]
        return dict(diffs)

    @property
    def has_changed(self):
        """
        Checks if any fields in the model instance have changed.

        Returns:
            bool: True if there are any changes in the model fields compared to their initial state,
                False otherwise.
        """
        return bool(self.diff)

    @property
    def changed_fields(self):
        """
        Returns the names of the fields that have changed.

        This property retrieves the keys from the diff dictionary, representing
        the fields whose values have changed compared to their initial state.

        Returns:
            KeysView: A view of the keys in the diff dictionary, indicating
            the names of the changed fields.
        """
        return self.diff.keys()

    def refresh_from_db(self, using=None, fields=None):
        """
        Re-fetches the model instance from the database and updates the
        :py:attr:`_initial` snapshot.

        This is the same as calling the superclass' ``refresh_from_db``,
        but also updates the :py:attr:`_initial` snapshot.

        Args:
            using: The database alias to use for the refresh query.
            fields: A list of field names to update.
        """
        _fields = copy(fields)
        super().refresh_from_db(using=using, fields=fields)

        if _fields is None:
            self._initial = self._dict
        else:
            for field in _fields:
                self._initial[field] = getattr(self, field)

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.
        """
        return self.diff.get(field_name, None)

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self._initial = self._dict

    @property
    def _dict(self):
        deferred_fields = set(self.get_deferred_fields())
        fields = []

        for field in self._meta.fields:
            if (
                field.name in deferred_fields
                or isinstance(
                    field,
                    (
                        models.ForeignKey,
                        models.OneToOneField,
                    ),
                )
                and field.attname in deferred_fields
            ):
                continue

            fields.append(field.name)

        data = model_to_dict(
            self,
            fields=fields,
        )

        return data
