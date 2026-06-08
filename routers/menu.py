from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models.item import Item, Category
from schemas.item import ItemRequest, ItemUpdateRequest, ItemResponse, CategoryResponse, CreateCategoryRequest
from auth_utils import require_admin

router = APIRouter()


# ─── CATEGORY ENDPOINTS ───────────────────────────────────────────

@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    """Lấy danh sách danh mục"""
    return db.query(Category).all()


@router.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(
    payload: CreateCategoryRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """Tạo danh mục mới — chỉ admin"""
    category = Category(name=payload.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


# ─── ITEM ENDPOINTS ───────────────────────────────────────────────

@router.get("/", response_model=List[ItemResponse])
def get_menu(
    category_id: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Lấy danh sách món ăn, có thể filter theo category hoặc tìm kiếm"""
    query = db.query(Item).filter(Item.is_available == True)

    if category_id:
        query = query.filter(Item.category_id == category_id)

    if search:
        query = query.filter(Item.name.ilike(f"%{search}%"))

    return query.all()


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    """Lấy chi tiết 1 món"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy món ăn")
    return item


@router.post("/", response_model=ItemResponse, status_code=201)
def create_item(
    payload: ItemRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """Tạo món mới — chỉ admin"""
    category = db.query(Category).filter(Category.id == payload.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Danh mục không tồn tại")

    item = Item(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        category_id=payload.category_id,
        is_available=payload.is_available,
        image_url=None  # Tích hợp S3 tuần 3
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(
    item_id: int,
    payload: ItemUpdateRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """Cập nhật món — chỉ admin"""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Không tìm thấy món ăn")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


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