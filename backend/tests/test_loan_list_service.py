from backend.services.loan_list_service import LoanListService


def test_service_exists(db):
    service = LoanListService(db)
    assert service is not None


def test_get_user_loans_returns_list(db, user):
    service = LoanListService(db)

    result = service.get_user_loans(user.id)

    assert isinstance(result, list)


def test_get_all_loans_returns_list(db):
    service = LoanListService(db)

    result = service.get_all_loans()

    assert isinstance(result, list)


def test_get_all_loans_with_status_filter(db):
    service = LoanListService(db)

    result = service.get_all_loans(status="APPROVED")

    assert isinstance(result, list)