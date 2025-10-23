"""
Seed marketing legends with their cognitive clones
"""
from models import ExpertCreate, ExpertType
from storage import MemStorage
from prompts.legends import LEGENDS_PROMPTS

async def seed_legends(storage: MemStorage):
    """Seed the 8 marketing legends as high-fidelity cognitive clones"""
    
    legends_data = [
        {
            "name": "Philip Kotler",
            "title": "O Pai do Marketing Moderno",
            "expertise": ["Estratégia de Marketing", "Segmentação", "4Ps", "Brand Positioning", "Marketing Internacional"],
            "system_prompt": LEGENDS_PROMPTS["philip_kotler"],
            "avatar": "/attached_assets/generated_images/Philip_Kotler_professional_portrait_bbb250dd.png",
            "prompt_key": "philip_kotler"
        },
        {
            "name": "David Ogilvy",
            "title": "O Pai da Publicidade",
            "expertise": ["Copywriting", "Brand Building", "Direct Response", "Creative Strategy", "Luxury Marketing"],
            "system_prompt": LEGENDS_PROMPTS["david_ogilvy"],
            "avatar": "/attached_assets/generated_images/David_Ogilvy_1960s_portrait_322198ff.png",
            "prompt_key": "david_ogilvy"
        },
        {
            "name": "Claude C. Hopkins",
            "title": "Pioneiro do Marketing Científico",
            "expertise": ["Scientific Advertising", "A/B Testing", "ROI Tracking", "Direct Response", "Teste e Mensuração"],
            "system_prompt": LEGENDS_PROMPTS["claude_hopkins"],
            "avatar": "/attached_assets/generated_images/Claude_Hopkins_vintage_portrait_b074ce60.png",
            "prompt_key": "claude_hopkins"
        },
        {
            "name": "John Wanamaker",
            "title": "Revolucionário do Varejo Moderno",
            "expertise": ["Retail Strategy", "Customer Trust", "Print Advertising", "Garantia de Devolução", "Mass Marketing"],
            "system_prompt": LEGENDS_PROMPTS["john_wanamaker"],
            "avatar": "/attached_assets/generated_images/John_Wanamaker_Victorian_portrait_9fe2f89b.png",
            "prompt_key": "john_wanamaker"
        },
        {
            "name": "Mary Wells Lawrence",
            "title": "Pioneira do Branding Emocional",
            "expertise": ["Branding Emocional", "Lifestyle Marketing", "Fashion Advertising", "I ♥ NY", "Creative Leadership"],
            "system_prompt": LEGENDS_PROMPTS["mary_wells_lawrence"],
            "avatar": "/attached_assets/generated_images/Mary_Wells_Lawrence_portrait_ee4b7088.png",
            "prompt_key": "mary_wells_lawrence"
        },
        {
            "name": "Seth Godin",
            "title": "Visionário do Permission Marketing",
            "expertise": ["Permission Marketing", "Purple Cow", "Tribes", "Storytelling Digital", "Nicho e Posicionamento"],
            "system_prompt": LEGENDS_PROMPTS["seth_godin"],
            "avatar": "/attached_assets/generated_images/Seth_Godin_modern_portrait_1b27fbc0.png",
            "prompt_key": "seth_godin"
        },
        {
            "name": "Gary Vaynerchuk",
            "title": "Rei do Marketing Digital e Hustle",
            "expertise": ["Social Media", "Personal Branding", "Day Trading Attention", "Content Creation", "Entrepreneurship"],
            "system_prompt": LEGENDS_PROMPTS["gary_vaynerchuk"],
            "avatar": "/attached_assets/generated_images/Gary_Vaynerchuk_entrepreneur_portrait_0501810f.png",
            "prompt_key": "gary_vaynerchuk"
        },
        {
            "name": "Leo Burnett",
            "title": "O Rei do Storytelling Publicitário",
            "expertise": ["Storytelling", "Archetypal Characters", "Inherent Drama", "Visual Branding", "Marlboro Man"],
            "system_prompt": LEGENDS_PROMPTS["leo_burnett"],
            "avatar": "/attached_assets/generated_images/Leo_Burnett_classic_portrait_e1f25f37.png",
            "prompt_key": "leo_burnett"
        },
    ]
    
    for legend in legends_data:
        expert_data = ExpertCreate(
            name=legend["name"],
            title=legend["title"],
            expertise=legend["expertise"],
            systemPrompt=legend["system_prompt"],
            avatar=legend["avatar"],
            expertType=ExpertType.HIGH_FIDELITY  # These are high-fidelity clones
        )
        await storage.create_expert(expert_data)
