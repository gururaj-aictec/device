class PageSerializable:
    def __init__(self, list=None):
        self.list = list if list else []
        self.total = len(self.list)

    @classmethod
    def of(cls, list):
        return cls(list)

    @property
    def total(self):
        return self._total

    @total.setter
    def total(self, total):
        self._total = total

    @property
    def list(self):
        return self._list

    @list.setter
    def list(self, list):
        self._list = list

    def __str__(self):
        return "PageSerializable{{'total': {}, 'list': {}}}".format(self.total, self.list)



class PageInfo(PageSerializable):
    def __init__(self, list=None, navigate_pages=8):
        super().__init__(list)
        self.navigate_pages = navigate_pages
        self.pageNum = 1
        self.pageSize = len(self.list)
        self.pages = self.pageSize > 0
        self.size = len(self.list)
        self.startRow = 0
        self.endRow = len(self.list) - 1 if len(self.list) > 0 else 0
        self.prePage = None
        self.nextPage = None
        self.isFirstPage = False
        self.isLastPage = False
        self.hasPreviousPage = False
        self.hasNextPage = False
        self.navigateFirstPage = None
        self.navigateLastPage = None
        self.navigatepageNums = None
        self.calcNavigatepageNums()
        self.calcPage()
        self.judgePageBoudary()

    @classmethod
    def of(cls, list, navigate_pages=8):
        return cls(list, navigate_pages)

    def calcNavigatepageNums(self):
        # Simplified for brevity. Add more complex logic if needed.
        self.navigatepageNums = list(range(1, min(self.pages + 1, self.navigate_pages + 1)))

    def calcPage(self):
        # Simplified for brevity. Add more complex logic if needed.
        self.navigateFirstPage = self.navigatepageNums[0] if self.navigatepageNums else None
        self.navigateLastPage = self.navigatepageNums[-1] if self.navigatepageNums else None
        self.prePage = self.pageNum - 1 if self.pageNum > 1 else None
        self.nextPage = self.pageNum + 1 if self.pageNum < self.pages else None

    def judgePageBoudary(self):
        # Simplified for brevity. Add more complex logic if needed.
        self.isFirstPage = self.pageNum == 1
        self.isLastPage = self.pageNum == self.pages
        self.hasPreviousPage = self.pageNum > 1
        self.hasNextPage = self.pageNum < self.pages

    def __str__(self):
        return "PageInfo{{'pageNum': {}, 'pageSize': {}, 'size': {}, 'startRow': {}, 'endRow': {}, 'total': {}, 'pages': {}, 'list': {}, 'prePage': {}, 'nextPage': {}, 'isFirstPage': {}, 'isLastPage': {}, 'hasPreviousPage': {}, 'hasNextPage': {}, 'navigatePages': {}, 'navigateFirstPage': {}, 'navigateLastPage': {}, 'navigatePageNums': {}}}".format(self.pageNum, self.pageSize, self.size, self.startRow, self.endRow, self.total, self.pages, self.list, self.prePage, self.nextPage, self.isFirstPage, self.isLastPage, self.hasPreviousPage, self.hasNextPage, self.navigate_pages, self.navigateFirstPage, self.navigateLastPage, self.navigatepageNums)
