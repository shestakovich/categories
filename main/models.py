from django.db import models


class Category(models.Model):
    parent = models.ForeignKey('Category', on_delete=models.SET_NULL, related_name='children', verbose_name='parent',
                               blank=True, null=True)
    name = models.CharField('name', max_length=512, unique=True)

    def get_siblings(self):
        return self.parent.children.exclude(pk=self.pk) if self.parent is not None else []

    def get_parents(self):
        parents = Category.objects.raw('''
with tree as
(
   select id, parent_id, main_category.name
   from main_category
   where id = %s
   union all
   select main_category.id, main_category.parent_id, main_category.name
   from main_category
   join tree on main_category.id = tree.parent_id
    AND tree.parent_id not NULL
)
select * from tree;
''', [self.id])
        parents = list(parents)[1:]

#         obj = self
#         parents = []
#         while obj.parent is not None:
#             obj = obj.parent
#             parents.append(obj)
        return parents

    def __str__(self):
        return self.name
