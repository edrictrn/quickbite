from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.item import Item, Category
from auth_utils import get_current_user, require_admin

router = APIRouter()


@router.get("/")
def get_menu(db: Session = Depends(get_db)):
    """Lấy toàn bộ món ăn đang available"""
    items = db.query(Item).filter(Item.is_available == True).all()
    return items


@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết 1 món"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy món ăn")
    return item


@router.post("/", status_code=201)
def create_item(
    # TODO (Người B/C): Thêm schema ItemRequest
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """Tạo món mới — chỉ admin"""
    # TODO: implement sau khi có S3 upload (tuần 3)
    pass


@router.patch("/{item_id}")
def update_item(
    item_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """Cập nhật món — chỉ admin"""
    # TODO: implement tuần 2
    pass


@router.delete("/{item_id}", status_code=204)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """Xoá món — chỉ admin"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy món ăn")
    db.delete(item)
    db.commit()
