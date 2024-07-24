from fastapi import Depends

from repository.demo import DemoRepo


class DemoService:
    def __init__(
        self,
        demo_repo: DemoRepo = Depends(DemoRepo),
    ):
        self._demo_repo = demo_repo

    def demo(self):
        print("DemoService")
        return self._demo_repo.demo()
