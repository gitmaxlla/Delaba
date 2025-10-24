from fastapi import APIRouter
from ..services import documents_service


v1_router = APIRouter(prefix="/documents", tags=["documents"])


@v1_router.get("/")
def get_all_documents_handles():
    documents_service.get_all_documents_handles()


@v1_router.put("/")
def add_document():
    documents_service.add_document()


@v1_router.get("/{id}")
def get_document(id):
    documents_service.get_document(id)


@v1_router.delete("/{id}")
def delete_document(id):
    documents_service.delete_document(id)


@v1_router.patch("/{id}/file")
def replace_documents_file(id):
    documents_service.replace_documents_file(id)


@v1_router.patch("/{id}/deadline")
def change_documents_deadline(id):
    documents_service.change_document_deadline(id)


@v1_router.patch("/{id}/heading")
def change_documents_heading(id):
    documents_service.change_document_heading(id)


@v1_router.patch("/{id}/body")
def change_documents_body(id):
    documents_service.change_document_body(id)
