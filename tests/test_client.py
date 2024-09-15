from evrim import Evrim
from evrim import models
import os
import pytest
import requests
import vcr


url = os.getenv("EVRIM_URL")
username = os.getenv("EVRIM_USERNAME")
password = os.getenv("EVRIM_PASSWORD")
expired_token = os.getenv("EVRIM_TOKEN")
report_id = os.getenv("EVRIM_REPORT_ID")
run_id = os.getenv("EVRIM_RUN_ID")


@vcr.use_cassette(filter_headers=["Authorization", "x-moesif-transaction-id"])
def test_evrim_from_username_password() -> None:
    evrim = Evrim(url=url, username=username, password=password)
    assert evrim is not None
    assert evrim.url == url
    assert evrim.username == username
    assert evrim._password == password
    assert evrim.session.headers["Authorization"] is not None


@vcr.use_cassette(filter_headers=["Authorization", "x-moesif-transaction-id"])
def test_evrim_from_expired__token() -> None:
    with pytest.raises(requests.HTTPError):
        Evrim.from_token(url=url, access_token=expired_token)


@vcr.use_cassette(filter_headers=["Authorization", "x-moesif-transaction-id"])
def test_get_report(evrim_client: Evrim) -> None:
    report = evrim_client.get_report(1)
    assert report is not None
    assert isinstance(report, models.Report)


@vcr.use_cassette(filter_headers=["Authorization", "x-moesif-transaction-id"])
def test_get_report_not_found(evrim_client: Evrim) -> None:
    with pytest.raises(requests.HTTPError):
        evrim_client.get_report(9999)


@vcr.use_cassette(filter_headers=["Authorization", "x-moesif-transaction-id"])
def test_generate_pdf_report(evrim_client: Evrim) -> None:
    pdf = evrim_client.generate_pdf(report_id)
    assert pdf is not None
    assert isinstance(pdf, models.PDFReport)


@vcr.use_cassette(filter_headers=["Authorization", "x-moesif-transaction-id"])
def test_generate_docx_report(evrim_client: Evrim) -> None:
    docx = evrim_client.generate_docx(report_id)
    assert docx is not None
    assert isinstance(docx, models.DocxReport)


@vcr.use_cassette(filter_headers=["Authorization", "x-moesif-transaction-id"])
def test_save_report_no_input(evrim_client: Evrim) -> None:
    pdf = evrim_client.generate_pdf(report_id)
    pdf.save()
    default_path = os.path.join(os.getcwd(), pdf.filename)
    assert os.path.exists(default_path)
    os.remove(default_path)


@vcr.use_cassette(filter_headers=["Authorization", "x-moesif-transaction-id"])
def test_get_run(evrim_client: Evrim) -> None:
    run = evrim_client.get_run(run_id)
    assert run is not None
    assert isinstance(run, models.Run)


@vcr.use_cassette(filter_headers=["Authorization", "x-moesif-transaction-id"])
def test_get_runs(evrim_client: Evrim) -> None:
    runs = evrim_client.get_runs()
    assert runs is not None
    assert isinstance(runs, list)
    assert all(isinstance(run, models.Run) for run in runs)


@vcr.use_cassette(filter_headers=["Authorization", "x-moesif-transaction-id"])
def test_get_run_not_found(evrim_client: Evrim) -> None:
    with pytest.raises(requests.HTTPError):
        evrim_client.get_run(9999)
