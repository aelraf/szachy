# -*- coding: utf-8 -*-
# https://pypi.org/project/pytest/

from flask.testing import Client
import pytest

from .models import Field


class TestsModelFields:
    def test_fields_init_only_cord(self):
        field = Field(2, 2)

        assert field.figure_code == 0
        assert field.is_empty
        assert field.field_name == 'B2'
        assert not field.is_black
