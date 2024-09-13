"""
Client code for the Evrim API
"""
import requests
from requests.sessions import Session
from evrim import models


class Evrim:
    """
    Simple to use client for the Evrim API
    """

    def __init__(self, url, username: str = None, password: str = None) -> None:
        """
        Initializes a new instance of the `Client` class.
        Args:
            url (str): The URL of the client.
            username (str): The username for authentication.
            password (str): The password for authentication.
        """
        
        self.url = url
        self.username = username
        self._password = password
        self.session = Session()
        if self.username and self._password:
            self.set_token()
        self.refresh = None

    @classmethod
    def from_token(cls, url: str, token: str, validate: bool = True) -> "Evrim":
        """
        Initializes a new instance of the `Client` class from a token.
        Args:
            url (str): The URL of the client.
            token (str): The token for authentication.
        Returns:
            Evrim: A new instance of the `Client` class.
        """
        client = cls(url)
        if validate:
            client.validate_token(token)
        client.session.headers.update({"Authorization": f"Bearer {token}"})
        return client

    def set_token(self) -> bool:
        """
        Sets the authentication token for the session.
        Returns:
            bool: True if the token was successfully set, False otherwise.
        Raises:
            ValueError: If the username or password is not set.
            requests.HTTPError: If the request to the server fails.
        """
        if self.username is None or self._password is None:
            raise ValueError("Username and password must be set to set the token.")
        response = requests.post(
            f"{self.url}/token/",
            json={"username": self.username, "password": self._password}
        )
        response.raise_for_status()
        if response.ok:
            # set headers for the session
            self.session.headers.update({
                "Authorization": f"Bearer {response.json()['access']}"
            })
            # set refresh token
            self.refresh = response.json()["refresh"]
            return True

    def refresh_token(self) -> bool:
        """
        Refreshes the access token using the refresh token.
        Returns:
            bool: True if the token was successfully refreshed, False otherwise.
        Raises:
            requests.HTTPError: If the request to the server fails.
        """
        if self.refresh is None:
            raise ValueError("Refresh token is not set.")
        response = requests.post(
            f"{self.url}/token/refresh/",
            json={"refresh": self.refresh}
        )
        response.raise_for_status()
        if response.ok:
            self.session.headers.update({
                "Authorization": f"Bearer {response.json()['access']}"
            })
            return True

    def validate_token(self, token: str) -> dict:
        """
        Validates the token by sending a POST request to the server.
        Returns:
            A dictionary containing the response from the server.
        Raises:
            requests.HTTPError: If the request to the server fails.
        """
        # code implementation here
        
        response = requests.post(
            f"{self.url}/token/verify/",
            json={"token": token}  # split on Bearer and get the token
        )
        response.raise_for_status()
        if response.ok:
            return response.json()


    def generate_pdf(self, report_id: int) -> models.PDFReport:
        """
        Generates a PDF report for the given report ID.
        Parameters:
            report_id (int): The ID of the report to generate the PDF for.
        Returns:
            models.PDFReport: The generated PDF report.
        Raises:
            requests.HTTPError: If there is an error in the HTTP request.
        """
        
        response = self.session.get(
            f"{self.url}/generate/{report_id}/pdf/",
        )
        response.raise_for_status()
        if response.ok:
            return models.PDFReport(
                content=response.content,
                filename=response.headers["Content-Disposition"].split("=")[1].strip('"'),
            )

    def generate_docx(self, report_id: int) -> models.DocxReport:
        """
        Generates a DocxReport for the given report ID.
        Args:
            report_id (int): The ID of the report.
        Returns:
            models.DocxReport: The generated DocxReport object.
        Raises:
            requests.HTTPError: If the request to the server fails.
        """
        response = self.session.get(
            f"{self.url}/generate/{report_id}/docx/",
        )
        response.raise_for_status()
        if response.ok:
            return models.DocxReport(
                content=response.content,
                filename=response.headers["Content-Disposition"].split("=")[1].strip('"'),
            )

    def submit_research(
        self,
        url: str,
        title: str,
        description: str,
        style: str,
        tone: str,
        point_of_view: str,
    ) -> models.Task:
        """
        Submits a research request to the server.
        Args:
            url (str): The URL of the research.
            title (str): The title of the research.
            description (str): The description of the research.
            style (str): The style of the research.
            tone (str): The tone of the research.
            point_of_view (str): The point of view of the research.
        Returns:
            models.Research: The submitted research object.
        Raises:
            requests.HTTPError: If the request to the server fails.
        """
        response = self.session.post(
            f"{self.url}/marketing/research/",
            json={
                "url": url,
                "title": title,
                "description": description,
                "style": style,
                "tone": tone,
                "point_of_view": point_of_view,
            },
        )
        response.raise_for_status()
        if response.ok:
            return models.Task(**response.json())

    def get_reports(self) -> list[models.Report]:
        """
        Retrieves a list of reports from the server.
        Returns:
            list[models.Report]: A list of Report objects representing the reports.
        Raises:
            requests.HTTPError: If the request to the server fails.
        """
        
        response = self.session.get(f"{self.url}/reports/")
        response.raise_for_status()
        if response.ok:
            return [models.Report(**report) for report in response.json()]

    def get_report(self, report_id: int) -> models.Report:
        """
        Retrieves a report from the server.
        Args:
            report_id (int): The ID of the report to retrieve.
        Returns:
            models.Report: The retrieved report object.
        Raises:
            requests.HTTPError: If the request to the server fails.
        """
        
        response = self.session.get(f"{self.url}/reports/{report_id}/")
        response.raise_for_status()
        if response.ok:
            return models.Report(**response.json())

    def get_runs(self) -> list[models.Run]:
        """
        Retrieves a list of runs from the server.
        Returns:
            list[models.Run]: A list of Run objects representing the runs.
        Raises:
            requests.HTTPError: If the request to the server fails.
        """
        
        response = self.session.get(f"{self.url}/runs")
        response.raise_for_status()
        if response.ok:
            return [models.Run(**run) for run in response.json()]

    def get_run(self, run_id: int) -> models.Run:
        """
        Retrieves a run from the server.
        Args:
            run_id (int): The ID of the run to retrieve.
        Returns:
            models.Run: The retrieved run object.
        Raises:
            requests.HTTPError: If the request to the server fails.
        """
        
        response = self.session.get(f"{self.url}/runs/{run_id}/")
        response.raise_for_status()
        if response.ok:
            return models.Run(**response.json())


    def get_tasks(self) -> list[models.Task]:
        """
        Retrieves a list of tasks from the server.
        Returns:
            list[models.Task]: A list of Task objects representing the tasks retrieved from the server.
        Raises:
            requests.HTTPError: If the request to the server fails.
        """
        
        response = self.session.get(f"{self.url}/tasks/")
        response.raise_for_status()
        if response.ok:
            return [models.Task(**task) for task in response.json()]

    def get_task(self, task_id: int) -> models.Task:
        """
        Retrieves a task from the server.
        Args:
            task_id (int): The ID of the task to retrieve.
        Returns:
            models.Task: The retrieved task object.
        Raises:
            requests.HTTPError: If the request to the server fails.
        """
        response = self.session.get(f"{self.url}/tasks/{task_id}/")
        response.raise_for_status()
        if response.ok:
            return models.Task(**response.json())

    def get_paragraph(self, paragraph_id: int) -> models.Paragraph:
        """
        Retrieves a paragraph from the server.
        Args:
            paragraph_id (int): The ID of the paragraph to retrieve.
        Returns:
            models.Paragraph: The retrieved paragraph object.
        Raises:
            requests.HTTPError: If the request to the server fails.
        """
        response = self.session.get(f"{self.url}/paragraphs/{paragraph_id}/")
        response.raise_for_status()
        if response.ok:
            return models.Paragraph(**response.json())

    def get_paragraphs(self) -> list[models.Paragraph]:
        """
        Retrieves a list of paragraphs from the server.
        Returns:
            list[models.Paragraph]: A list of Paragraph objects representing the paragraphs retrieved from the server.
        Raises:
            requests.HTTPError: If the request to the server fails.
        """
        response = self.session.get(f"{self.url}/paragraphs/")
        response.raise_for_status()
        if response.ok:
            return [models.Paragraph(**paragraph) for paragraph in response.json()]

    def get_section(self, section_id: int) -> models.Section:
        """
        Retrieves a section from the server.
        Args:
            section_id (int): The ID of the section to retrieve.
        Returns:
            models.Section: The retrieved section object.
        Raises:
            requests.HTTPError: If the request to the server fails.
        """
        response = self.session.get(f"{self.url}/sections/{section_id}/")
        response.raise_for_status()
        if response.ok:
            return models.Section(**response.json())

    def get_sections(self) -> list[models.Section]:
        """
        Retrieves a list of sections from the server.
        Returns:
            list[models.Section]: A list of Section objects representing the sections retrieved from the server.
        Raises:
            requests.HTTPError: If the request to the server fails.
        """
        response = self.session.get(f"{self.url}/sections/")
        response.raise_for_status()
        if response.ok:
            return [models.Section(**section) for section in response.json()]
