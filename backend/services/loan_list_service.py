# from sqlmodel import Session, select
# from backend.models.loan import Loan
#
#
# class LoanListService:
#     def __init__(self, db: Session):
#         self.db = db
#
#     def get_user_loans(self, user_id: int):
#         return self.db.exec(
#             select(Loan).where(Loan.user_id == user_id)
#         ).all()
#
#     def get_all_loans(self, status=None):
#         query = select(Loan)
#
#         if status:
#             query = query.where(Loan.status == status)
#
#         return self.db.exec(query).all()


# To jest plik-zaślepka, który pozwala uruchomić aplikację,
# dopóki moduł Loans nie zostanie w pełni zaimplementowany przez zespół.
class LoanListService:
    def __init__(self, db):
        self.db = db

    def get_user_loans(self, user_id):
        return []  # Zwracamy pustą listę, żeby aplikacja nie wywalała błędów