from pydantic import BaseModel
from typing import List, Optional
import os

class GeneratedReport(BaseModel):
    
    def save(self, path: str = None, filename: str = None) -> None:
        """
        Save the content of the model to a file.
        Args:
            path (str): The path where the file will be saved.
        Returns:
            None
        """
        filename = filename if filename else self.filename
        path = path if path else os.getcwd()
        with open(os.path.join(path, filename), "wb") as f:
            f.write(self.content)


class PDFReport(GeneratedReport):
    content: bytes
    filename: str


class DocxReport(GeneratedReport):
    content: bytes
    filename: str


class Event(BaseModel):
    id: int
    input: str


class Task(BaseModel):
    task_id: str
    event: Event
    created_at: str
    status: str
    created_by: int


class Paragraph(BaseModel):
    id: int
    title: str
    sentences: list[str]
    images: Optional[list[dict]] = None


class Section(BaseModel):
    id: int
    title: str
    paragraphs: List[Paragraph]
    sources: Optional[List[str]] = None
    tone: str
    style: str
    point_of_view: str


class Report(BaseModel):
    id: int
    task: Task
    title: str
    description: str
    sections: List[Section]


class RunTask(BaseModel):
    id: int
    agent_role: str
    description: str
    result: str
    name: str
    section_name: Optional[str] = None


class Run(BaseModel):
    id: int
    tasks: List[RunTask]
    result: str


class Report(BaseModel):
    id: Optional[int] = None
    report: Optional[Report] = None
    crew_run: Optional[Run] = None
    raw: Optional[list[str]] = None
