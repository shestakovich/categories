from rest_framework import serializers
from rest_framework.fields import Field, JSONField

from main.models import Category


class SubCategoryDetail(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
        )


class CategoryDetailSerializer(serializers.ModelSerializer):
    siblings = SubCategoryDetail(many=True, source='get_siblings', read_only=True)
    children = SubCategoryDetail(many=True)
    parents = SubCategoryDetail(many=True, source='get_parents', read_only=True)

    # def create(self, validated_data):
    #     print(validated_data)

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'parents',
            'children',
            'siblings',
        )


class ChildrenField(JSONField):

    def to_internal_value(self, data):
        data = super().to_internal_value(data)
        for child in data:
            category = CategoryCreateSerializer(data=child)
            category.is_valid(raise_exception=True)
        return data


class CategoryCreateSerializer(serializers.ModelSerializer):
    children = ChildrenField(required=False)

    def create(self, validated_data, parent=None):
        print(validated_data)
        children = validated_data.pop('children', [])
        category = Category.objects.create(**validated_data, parent=parent)
        for child in children:
            self.create(child, parent=category)

        return category

    class Meta:
        model = Category
        fields = (
            'name',
            'children',
        )
