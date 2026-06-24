from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.admin import auth, ingredients, cocktails, orders
from app.routers.public import cocktails as public_cocktails

app = FastAPI(title="hon_bar API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/admin", tags=["admin-auth"])
app.include_router(ingredients.router, prefix="/api/admin/ingredients", tags=["admin-ingredients"])
app.include_router(cocktails.router, prefix="/api/admin/cocktails", tags=["admin-cocktails"])
app.include_router(orders.router, prefix="/api/admin/orders", tags=["admin-orders"])
app.include_router(public_cocktails.router, prefix="/api/cocktails", tags=["public-cocktails"])


@app.get("/")
def root():
    return {"message": "hon_bar API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
