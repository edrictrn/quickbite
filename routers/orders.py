from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.order import Order, OrderItem, OrderStatus
from models.item import Item
from schemas.order import CreateOrderRequest, OrderResponse, UpdateOrderStatusRequest
from auth_utils import get_current_user, require_admin

router = APIRouter()


@router.post("/", response_model=OrderResponse, status_code=201)
def create_order(
    payload: CreateOrderRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Tạo đơn hàng mới"""
    total = 0.0
    order_items = []

    for order_item in payload.items:
        item = db.query(Item).filter(Item.id == order_item.item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail=f"Món {order_item.item_id} không tồn tại")
        if not item.is_available:
            raise HTTPException(status_code=400, detail=f"Món '{item.name}' hiện không có sẵn")

        subtotal = item.price * order_item.quantity
        total += subtotal
        order_items.append(OrderItem(
            item_id=item.id,
            quantity=order_item.quantity,
            price=item.price
        ))

    order = Order(
        user_id=current_user.id,
        total=total,
        note=payload.note,
        items=order_items
    )
    db.add(order)
    db.commit()
    db.refresh(order)

    # TODO tuần 5: trigger Lambda gửi email xác nhận

    return order


@router.get("/my", response_model=List[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Lấy lịch sử đơn hàng của user hiện tại"""
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """Xem chi tiết đơn hàng"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Không có quyền xem đơn này")
    return order


@router.patch("/{order_id}/status")
def update_order_status(
    order_id: int,
    payload: UpdateOrderStatusRequest,
    db: Session = Depends(get_db),
    admin=Depends(require_admin)
):
    """Cập nhật trạng thái đơn hàng — chỉ admin"""
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn hàng")

    try:
        order.status = OrderStatus(payload.status)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Status không hợp lệ: {payload.status}")

    db.commit()
    db.refresh(order)
    return {"message": f"Cập nhật thành công", "order_id": order_id, "status": order.status}
