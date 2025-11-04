from fastapi import APIRouter, HTTPException, File, UploadFile, Depends, Request
from typing import List, Optional
from slowapi import Limiter
from slowapi.util import get_remote_address

from python_backend.models import Expert, ExpertCreate, CategoryInfo, AutoCloneRequest
from python_backend.storage import storage

router = APIRouter(
    tags=["Experts"],
)

limiter = Limiter(key_func=get_remote_address)

# TODO: Move this to a shared location if used by other routers
CATEGORY_METADATA = {
    "marketing": { "name": "Marketing Tradicional", "description": "Estratégias clássicas, brand building e publicidade.", "icon": "Megaphone", "color": "violet" },
    "positioning": { "name": "Posicionamento Estratégico", "description": "Ocupar uma posição única na mente do consumidor.", "icon": "Target", "color": "blue" },
    "creative": { "name": "Criatividade Publicitária", "description": "A arte e a ciência de campanhas que marcam.", "icon": "Lightbulb", "color": "amber" },
    "direct_response": { "name": "Direct Response", "description": "Copy que converte e funis de vendas.", "icon": "Mail", "color": "red" },
    "content": { "name": "Content Marketing", "description": "Storytelling, permission marketing e conteúdo que engaja.", "icon": "FileText", "color": "indigo" },
    "seo": { "name": "SEO & Marketing Digital", "description": "Otimização para buscas e marketing orientado a dados.", "icon": "Search", "color": "cyan" },
    "social": { "name": "Social Media Marketing", "description": "Personal branding e redes sociais.", "icon": "Users", "color": "pink" },
    "growth": { "name": "Growth Hacking", "description": "Sistemas de crescimento e product-market fit.", "icon": "TrendingUp", "color": "emerald" },
    "viral": { "name": "Marketing Viral", "description": "Conteúdo contagiante e word-of-mouth.", "icon": "Share2", "color": "orange" },
    "product": { "name": "Psicologia do Produto", "description": "Formação de hábitos e design comportamental.", "icon": "Brain", "color": "purple" }
}

@router.get("/api/experts", response_model=List[Expert])
async def get_experts(category: Optional[str] = None):
    try:
        experts = await storage.get_experts()
        print(f"[Experts Router] get_experts called. Found {len(experts)} experts. Category filter: {category}")
        
        if len(experts) == 0:
            print("[Experts Router] ⚠️  WARNING: No experts found! Check if seeding completed successfully.")
            return []
        
        if category:
            experts = [e for e in experts if e.category.value == category]
            print(f"[Experts Router] After category filter: {len(experts)} experts")
        
        return experts
    except Exception as e:
        print(f"[Experts Router] ERROR: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Erro ao buscar experts: {str(e)}")

@router.get("/api/categories", response_model=List[CategoryInfo])
async def get_categories():
    experts = await storage.get_experts()
    category_counts = {}
    for expert in experts:
        cat = expert.category
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    categories = []
    for cat_type, metadata in CATEGORY_METADATA.items():
        count = category_counts.get(cat_type, 0)
        if count > 0:
            categories.append(CategoryInfo(
                id=cat_type,
                name=metadata["name"],
                description=metadata["description"],
                icon=metadata["icon"],
                color=metadata["color"],
                expertCount=count
            ))
    
    categories.sort(key=lambda x: (-x.expertCount, x.name))
    return categories

@router.get("/api/experts/{expert_id}", response_model=Expert)
async def get_expert(expert_id: str):
    expert = await storage.get_expert(expert_id)
    if not expert:
        raise HTTPException(status_code=404, detail="Expert not found")
    return expert

@router.post("/api/experts", response_model=Expert, status_code=201)
@limiter.limit("10/day")
async def create_expert(request: Request, data: ExpertCreate):
    try:
        # 🆕 GERAR CLASSE PYTHON AUTOMATICAMENTE
        from python_backend.clone_generator import clone_generator
        
        try:
            # Salvar como classe Python
            file_path, class_name = clone_generator.save_clone_to_file(data)
            print(f"[CreateExpert] ✅ Classe Python gerada: {file_path}")
            
            # Registrar no CloneRegistry
            success = clone_generator.register_clone(data.name, class_name, file_path)
            if success:
                print(f"[CreateExpert] ✅ Clone registrado no CloneRegistry: {data.name}")
            else:
                print(f"[CreateExpert] ⚠️ Falha ao registrar no CloneRegistry (não crítico)")
        except Exception as gen_error:
            print(f"[CreateExpert] ⚠️ Erro ao gerar classe Python (não crítico): {gen_error}")
            # Continua com salvamento no banco mesmo se geração de Python falhar
        
        # Salvar no banco de dados (comportamento original)
        expert = await storage.create_expert(data)
        
        return expert
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create expert: {str(e)}")

# Note: /api/experts/auto-clone is implemented in main.py due to its complexity
# It uses both Perplexity and Claude APIs with extensive prompt engineering

# Placeholder for avatar upload
@router.post("/api/experts/{expert_id}/avatar", status_code=501)
async def upload_expert_avatar_placeholder():
    return {"message": "Endpoint de upload de avatar ainda não foi movido para o roteador."}

@router.get("/api/experts/debug")
async def debug_experts():
    """Endpoint de diagnóstico para verificar experts"""
    experts = await storage.get_experts()
    return {
        "count": len(experts),
        "experts": [{"id": e.id, "name": e.name, "title": e.title} for e in experts[:5]],  # Primeiros 5
        "storage_type": type(storage).__name__
    }
