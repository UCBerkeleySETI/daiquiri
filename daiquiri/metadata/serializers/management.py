from rest_framework import serializers

from ..models import Database, Table, Column, Function


class ColumnSerializer(serializers.ModelSerializer):

    class Meta:
        model = Column
        fields = ('id', 'name')


class TableSerializer(serializers.ModelSerializer):

    columns = ColumnSerializer(many=True, read_only=True)

    class Meta:
        model = Table
        fields = ('id', 'name', 'columns')


class DatabaseSerializer(serializers.ModelSerializer):

    tables = TableSerializer(many=True, read_only=True)

    class Meta:
        model = Database
        fields = ('id', 'name', 'tables')


class FunctionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Function
        fields = ('id', 'name')
