# -*- coding: utf-8 -*-
class InvalidPage(Exception):
    pass


class PageNotAnInteger(InvalidPage):
    pass


class EmptyPage(InvalidPage):
    pass


class MyPaginator(object):
    def __init__(self, object_list, per_page):
        self.object_list = object_list
        self.per_page = int(per_page)   # 多少个一分
        self.num_pages = None   # 能拆多少个
        self.num = None
        self.number = None
        self.page_list = None

    def validate_number(self, number):
        """
        Validates the given 1-based page number.
        """
        try:
            number = int(number)
        except (TypeError, ValueError):
            raise PageNotAnInteger('That page number is not an integer')
        if number < 1:
            raise EmptyPage('That page number is less than 1')
        if number > self.get_num_pages():
            if number == 1:
                pass
            else:
                raise EmptyPage('That page contains no results')
        return number

    def get_num_pages(self):
        # 可以分成多少页
        self.num = len(self.object_list)
        num_pages = self.num / self.per_page
        if self.num % self.per_page > 0:
            self.num_pages = num_pages + 1
        else:
            self.num_pages = num_pages
        return self.num_pages

    def page(self, number):
        """得到第number页"""
        self.number = self.validate_number(number)
        # 分页查询列表
        bottom = (self.number - 1) * self.per_page
        up = bottom + self.per_page
        self.page_list = self.object_list[bottom: up] # 已拆分的列表
        if self.num_pages < 5:
            # 如果能拆的页面小于5
            self.page_range = range(1, self.num_pages+1)
        else:
            if self.number >3:
                self.page_range = range(self.number-2, min(self.number+3, self.num_pages+1))
            else:
                self.page_range = range(1, 6)


# if __name__ == '__main__':
#     x = MyPaginator([11,2,3,4,5,6,7,8,9,10,11,12,13,14,15], 2)
#     page = 4
#     x.page(page)
#     print x.num_pages
#     print "第%s页的列表%s"% (page,x.page_list)
#     print "分页按钮%s"%x.page_range