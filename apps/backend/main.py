from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.admin import auth, item_types, tags, items, cocktails, menu_items, orders
from app.routers.public import menu

app = FastAPI(title="hon_bar API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/admin", tags=["admin-auth"])
app.include_router(item_types.router, prefix="/api/admin/item-types", tags=["admin-item-types"])
app.include_router(tags.router, prefix="/api/admin/tags", tags=["admin-tags"])
app.include_router(items.router, prefix="/api/admin/items", tags=["admin-items"])
app.include_router(cocktails.router, prefix="/api/admin/cocktails", tags=["admin-cocktails"])
app.include_router(menu_items.router, prefix="/api/admin/menu-items", tags=["admin-menu-items"])
app.include_router(orders.router, prefix="/api/admin/orders", tags=["admin-orders"])
app.include_router(menu.router, prefix="/api", tags=["public"])


@app.get("/")
def root():
    return {"message": "hon_bar API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
